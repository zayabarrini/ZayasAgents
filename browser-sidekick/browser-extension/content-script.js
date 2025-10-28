// browser-extension/content-script.js
class BrowserSidekick {
    constructor() {
        this.isActive = false;
        this.overlay = null;
        this.currentSession = null;
        this.init();
    }

    init() {
        this.createOverlay();
        this.injectStyles();
        this.setupMessageListeners();
    }

    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.id = 'sidekick-overlay';
        this.overlay.innerHTML = `
            <div class="sidekick-container">
                <div class="sidekick-header">
                    <h3>AI Sidekick</h3>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="sidekick-chat">
                    <div class="messages-container"></div>
                    <div class="input-container">
                        <input type="text" placeholder="Ask your sidekick..." class="chat-input">
                        <button class="send-btn">Send</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(this.overlay);
        
        // Add event listeners
        this.overlay.querySelector('.close-btn').addEventListener('click', () => this.hide());
        this.overlay.querySelector('.send-btn').addEventListener('click', () => this.sendMessage());
        this.overlay.querySelector('.chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    injectStyles() {
        const styles = `
            #sidekick-overlay {
                position: fixed;
                top: 20px;
                right: 20px;
                width: 400px;
                height: 500px;
                background: white;
                border: 1px solid #ccc;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                z-index: 10000;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                display: none;
            }
            
            .sidekick-container {
                height: 100%;
                display: flex;
                flex-direction: column;
            }
            
            .sidekick-header {
                padding: 15px;
                background: #007bff;
                color: white;
                border-radius: 10px 10px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .sidekick-header h3 {
                margin: 0;
                font-size: 16px;
            }
            
            .close-btn {
                background: none;
                border: none;
                color: white;
                font-size: 20px;
                cursor: pointer;
            }
            
            .sidekick-chat {
                flex: 1;
                display: flex;
                flex-direction: column;
            }
            
            .messages-container {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
            }
            
            .message {
                margin-bottom: 10px;
                padding: 8px 12px;
                border-radius: 8px;
                max-width: 80%;
            }
            
            .user-message {
                background: #007bff;
                color: white;
                margin-left: auto;
            }
            
            .ai-message {
                background: #f1f3f4;
                color: #333;
            }
            
            .input-container {
                padding: 15px;
                border-top: 1px solid #eee;
                display: flex;
                gap: 10px;
            }
            
            .chat-input {
                flex: 1;
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                outline: none;
            }
            
            .send-btn {
                background: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
            }
            
            .sidekick-floating-btn {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 50px;
                height: 50px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 50%;
                font-size: 20px;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                z-index: 9999;
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }

    show() {
        this.overlay.style.display = 'block';
        this.isActive = true;
        this.capturePageContext();
    }

    hide() {
        this.overlay.style.display = 'none';
        this.isActive = false;
    }

    capturePageContext() {
        const pageContext = {
            url: window.location.href,
            title: document.title,
            content: document.body.innerText.substring(0, 2000),
            selectedText: window.getSelection().toString(),
            timestamp: new Date().toISOString()
        };
        
        this.currentPageContext = pageContext;
        return pageContext;
    }

    async sendMessage() {
        const input = this.overlay.querySelector('.chat-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        this.addMessage(message, 'user');
        input.value = '';
        
        try {
            const response = await this.sendToAgent(message);
            this.addMessage(response, 'ai');
        } catch (error) {
            this.addMessage('Sorry, I encountered an error. Please try again.', 'ai');
            console.error('Error sending message to agent:', error);
        }
    }

    addMessage(text, sender) {
        const messagesContainer = this.overlay.querySelector('.messages-container');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async sendToAgent(message) {
        const context = this.capturePageContext();
        
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                context: context,
                session_id: this.currentSession
            })
        });
        
        const data = await response.json();
        return data.response;
    }

    setupMessageListeners() {
        // Listen for keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                this.show();
            }
        });

        // Create floating activation button
        const floatingBtn = document.createElement('button');
        floatingBtn.className = 'sidekick-floating-btn';
        floatingBtn.innerHTML = '🤖';
        floatingBtn.title = 'Open AI Sidekick (Ctrl+K)';
        floatingBtn.addEventListener('click', () => this.show());
        document.body.appendChild(floatingBtn);
    }
}

// Initialize the sidekick when the page loads
let sidekick;
document.addEventListener('DOMContentLoaded', () => {
    sidekick = new BrowserSidekick();
});
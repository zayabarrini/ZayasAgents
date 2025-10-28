// scripts/app.js
class CareerDigitalTwin {
    constructor() {
        this.profileData = null;
        this.chatHistory = [];
        this.initializeApp();
    }

    async initializeApp() {
        await this.loadProfileData();
        this.setupEventListeners();
        this.renderProfile();
    }

    async loadProfileData() {
        try {
            // In a real application, this would be an API call
            const response = await fetch('/api/profile');
            this.profileData = await response.json();
        } catch (error) {
            console.error('Error loading profile data:', error);
            // Fallback to sample data
            this.profileData = await this.getSampleProfile();
        }
    }

    async getSampleProfile() {
        const response = await fetch('/data/sample_profile.json');
        return await response.json();
    }

    setupEventListeners() {
        const sendButton = document.getElementById('send-btn');
        const userInput = document.getElementById('user-input');
        const analyzeButton = document.getElementById('analyze-match');

        sendButton.addEventListener('click', () => this.handleUserMessage());
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleUserMessage();
        });

        analyzeButton.addEventListener('click', () => this.analyzeJobMatch());
    }

    renderProfile() {
        if (!this.profileData) return;

        const profile = this.profileData;
        
        // Basic profile info
        document.getElementById('profile-name').textContent = profile.name;
        document.getElementById('profile-title').textContent = profile.title;
        document.getElementById('about-me').textContent = profile.about;
        
        // Profile image
        const profileImg = document.getElementById('profile-image');
        profileImg.src = profile.image_url || 'https://via.placeholder.com/120';
        profileImg.alt = `${profile.name} profile picture`;

        // Skills
        this.renderSkills(profile.skills);
        
        // Experience
        this.renderExperience(profile.experience);
        
        // Education
        this.renderEducation(profile.education);
    }

    renderSkills(skills) {
        const skillsContainer = document.getElementById('skills-list');
        skillsContainer.innerHTML = skills.map(skill => 
            `<span class="skill-tag">${skill}</span>`
        ).join('');
    }

    renderExperience(experience) {
        const experienceContainer = document.getElementById('experience-list');
        experienceContainer.innerHTML = experience.map(exp => `
            <div class="experience-item">
                <h5>${exp.position} at ${exp.company}</h5>
                <p class="date">${exp.start_date} - ${exp.end_date || 'Present'}</p>
                <p>${exp.description}</p>
                ${exp.achievements ? `<ul>${exp.achievements.map(achievement => 
                    `<li>${achievement}</li>`
                ).join('')}</ul>` : ''}
            </div>
        `).join('');
    }

    renderEducation(education) {
        const educationContainer = document.getElementById('education-list');
        educationContainer.innerHTML = education.map(edu => `
            <div class="education-item">
                <h5>${edu.degree}</h5>
                <p class="institution">${edu.institution}</p>
                <p class="date">${edu.year}</p>
                ${edu.gpa ? `<p>GPA: ${edu.gpa}</p>` : ''}
            </div>
        `).join('');
    }

    async handleUserMessage() {
        const userInput = document.getElementById('user-input');
        const message = userInput.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessageToChat(message, 'user');
        userInput.value = '';

        // Get response from AI agent
        try {
            const response = await this.getAIResponse(message);
            this.addMessageToChat(response, 'bot');
        } catch (error) {
            console.error('Error getting AI response:', error);
            this.addMessageToChat('Sorry, I encountered an error while processing your question.', 'bot');
        }
    }

    async getAIResponse(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                chat_history: this.chatHistory
            })
        });

        const data = await response.json();
        this.chatHistory.push({ role: 'user', content: message });
        this.chatHistory.push({ role: 'assistant', content: data.response });
        
        return data.response;
    }

    addMessageToChat(message, sender) {
        const chatMessages = document.getElementById('chat-messages');
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}-message`;
        messageElement.textContent = message;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async analyzeJobMatch() {
        const jobDescription = document.getElementById('job-description').value.trim();
        
        if (!jobDescription) {
            alert('Please enter a job description to analyze.');
            return;
        }

        try {
            const response = await fetch('/api/analyze-match', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    job_description: jobDescription
                })
            });

            const matchData = await response.json();
            this.displayMatchResults(matchData);
        } catch (error) {
            console.error('Error analyzing job match:', error);
            alert('Error analyzing job match. Please try again.');
        }
    }

    displayMatchResults(matchData) {
        const resultsContainer = document.getElementById('match-results');
        
        resultsContainer.innerHTML = `
            <div class="match-score">
                Match Score: ${matchData.overall_match}%
            </div>
            <div class="match-breakdown">
                ${Object.entries(matchData.breakdown).map(([category, score]) => `
                    <div class="match-category">
                        <strong>${this.formatCategoryName(category)}:</strong> ${score}%
                    </div>
                `).join('')}
            </div>
            ${matchData.recommendations ? `
                <div class="recommendations">
                    <h4>Recommendations:</h4>
                    <ul>
                        ${matchData.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        `;
    }

    formatCategoryName(category) {
        return category.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CareerDigitalTwin();
});
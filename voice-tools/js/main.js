class AudioTranslateApp {
    constructor() {
        this.managers = {};
        this.init();
    }

    init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupApp());
        } else {
            this.setupApp();
        }
    }

    setupApp() {
        this.loadPageContent();
        this.initializeManagers();
        this.setupGlobalEventListeners();
        this.setupTabNavigation();
    }

    loadPageContent() {
        this.loadFeatures();
        this.loadTabContents();
        this.loadFooterContent();
    }

    loadFeatures() {
        const featuresContainer = document.getElementById('features-container');
        if (!featuresContainer) return;

        const features = [
            {
                icon: '📝',
                title: 'Automatic Transcription',
                description: 'Convert speech to text with high accuracy using advanced speech recognition algorithms.'
            },
            {
                icon: '🌐',
                title: 'Multi-Language Translation',
                description: 'Translate your audio content into dozens of languages while preserving voice characteristics.'
            },
            {
                icon: '🎚️',
                title: 'Subtitle Generation',
                description: 'Create perfectly timed subtitles with speaker identification and formatting options.'
            },
            {
                icon: '🔊',
                title: 'Voice Preservation',
                description: 'Maintain the original speaker\'s voice characteristics in translated audio outputs.'
            },
            {
                icon: '📁',
                title: 'Multiple Export Formats',
                description: 'Download transcripts as SRT, VTT, TXT, or translated audio as MP3, WAV, and more.'
            },
            {
                icon: '🔒',
                title: 'Secure Processing',
                description: 'Your audio files are processed securely and deleted after conversion for privacy.'
            }
        ];

        featuresContainer.innerHTML = features.map(feature => `
            <div class="feature-card">
                <div class="feature-icon">${feature.icon}</div>
                <h3>${feature.title}</h3>
                <p>${feature.description}</p>
            </div>
        `).join('');
    }

    loadTabContents() {
        const tabContents = document.getElementById('tab-contents');
        if (!tabContents) return;

        tabContents.innerHTML = `
            <div id="transcription" class="tab-content active">
                ${this.getTranscriptionTabHTML()}
            </div>
            <div id="translation" class="tab-content">
                ${this.getTranslationTabHTML()}
            </div>
            <div id="batch" class="tab-content">
                ${this.getBatchTabHTML()}
            </div>
        `;
    }

    getTranscriptionTabHTML() {
        return `
            <div class="form-group">
                <h3>Upload Audio for Transcription</h3>
                <p>Upload an audio file to automatically generate subtitles and transcript.</p>
                
                <div class="upload-area" id="transcription-upload-area">
                    <div class="upload-icon">📁</div>
                    <h3>Drag & Drop Audio File Here</h3>
                    <p>or click to browse files</p>
                    <p><small>Supported formats: MP3, WAV, M4A, OGG (Max 100MB)</small></p>
                    <input type="file" id="transcription-file" accept="audio/*" style="display: none;">
                </div>
                
                <div id="transcription-file-info" style="margin-top: 1rem;"></div>
            </div>
            
            <div class="form-group">
                <label for="transcription-language">Source Language:</label>
                <select id="transcription-language">
                    <option value="auto">Auto-detect</option>
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                    <option value="it">Italian</option>
                    <option value="pt">Portuguese</option>
                    <option value="ru">Russian</option>
                    <option value="ja">Japanese</option>
                    <option value="zh">Chinese</option>
                    <option value="ar">Arabic</option>
                    <option value="hi">Hindi</option>
                </select>
            </div>
            
            <button id="transcribe-btn" class="btn" disabled>Transcribe Audio</button>
            
            <div class="progress-container" id="transcription-progress">
                <div class="progress-bar">
                    <div class="progress" id="transcription-progress-bar"></div>
                </div>
                <div class="progress-text">
                    <span id="transcription-status">Processing...</span>
                    <span id="transcription-percentage">0%</span>
                </div>
            </div>
            
            <div class="results-container" id="transcription-results">
                <div class="result-tabs">
                    <div class="result-tab active" data-result-tab="transcript">Transcript</div>
                    <div class="result-tab" data-result-tab="subtitles">Subtitles</div>
                </div>
                
                <div id="transcript" class="result-content active">
                    <h3>Generated Transcript</h3>
                    <div class="transcript-container" id="transcript-text"></div>
                    
                    <div class="download-options">
                        <div class="download-btn" data-format="txt">
                            <i>📄</i> Download as TXT
                        </div>
                        <div class="download-btn" data-format="docx">
                            <i>📄</i> Download as DOCX
                        </div>
                    </div>
                </div>
                
                <div id="subtitles" class="result-content">
                    <h3>Generated Subtitles</h3>
                    <div class="transcript-container" id="subtitles-text"></div>
                    
                    <div class="download-options">
                        <div class="download-btn" data-format="srt">
                            <i>📄</i> Download as SRT
                        </div>
                        <div class="download-btn" data-format="vtt">
                            <i>📄</i> Download as VTT
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getTranslationTabHTML() {
        return `
            <div class="form-group">
                <h3>Upload Audio for Translation</h3>
                <p>Upload an audio file to translate it to multiple languages.</p>
                
                <div class="upload-area" id="translation-upload-area">
                    <div class="upload-icon">📁</div>
                    <h3>Drag & Drop Audio File Here</h3>
                    <p>or click to browse files</p>
                    <p><small>Supported formats: MP3, WAV, M4A, OGG (Max 100MB)</small></p>
                    <input type="file" id="translation-file" accept="audio/*" style="display: none;">
                </div>
                
                <div id="translation-file-info" style="margin-top: 1rem;"></div>
            </div>
            
            <div class="form-group">
                <label for="source-language">Source Language:</label>
                <select id="source-language">
                    <option value="auto">Auto-detect</option>
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                    <option value="it">Italian</option>
                    <option value="pt">Portuguese</option>
                    <option value="ru">Russian</option>
                    <option value="ja">Japanese</option>
                    <option value="zh">Chinese</option>
                    <option value="ar">Arabic</option>
                    <option value="hi">Hindi</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Target Languages:</label>
                <div class="language-grid">
                    <div class="language-option" data-lang="de">
                        <div class="language-flag">🇩🇪</div>
                        <div>German</div>
                    </div>
                    <div class="language-option" data-lang="fr">
                        <div class="language-flag">🇫🇷</div>
                        <div>French</div>
                    </div>
                    <div class="language-option" data-lang="ru">
                        <div class="language-flag">🇷🇺</div>
                        <div>Russian</div>
                    </div>
                    <div class="language-option" data-lang="zh">
                        <div class="language-flag">🇨🇳</div>
                        <div>Chinese</div>
                    </div>
                    <div class="language-option" data-lang="ja">
                        <div class="language-flag">🇯🇵</div>
                        <div>Japanese</div>
                    </div>
                    <div class="language-option" data-lang="hi">
                        <div class="language-flag">🇮🇳</div>
                        <div>Hindi</div>
                    </div>
                    <div class="language-option" data-lang="ar">
                        <div class="language-flag">🇸🇦</div>
                        <div>Arabic</div>
                    </div>
                    <div class="language-option" data-lang="it">
                        <div class="language-flag">🇮🇹</div>
                        <div>Italian</div>
                    </div>
                </div>
            </div>
            
            <button id="translate-btn" class="btn btn-accent" disabled>Translate Audio</button>
            
            <div class="progress-container" id="translation-progress">
                <div class="progress-bar">
                    <div class="progress" id="translation-progress-bar"></div>
                </div>
                <div class="progress-text">
                    <span id="translation-status">Processing...</span>
                    <span id="translation-percentage">0%</span>
                </div>
            </div>
            
            <div class="results-container" id="translation-results">
                <h3>Translation Results</h3>
                <div id="translation-outputs"></div>
            </div>
        `;
    }

    getBatchTabHTML() {
        return `
            <h3>Batch Processing</h3>
            <p>Upload multiple audio files for transcription and translation in one go.</p>
            
            <div class="upload-area" id="batch-upload-area">
                <div class="upload-icon">📁</div>
                <h3>Drag & Drop Multiple Audio Files Here</h3>
                <p>or click to browse files</p>
                <p><small>Supported formats: MP3, WAV, M4A, OGG (Max 10 files, 500MB total)</small></p>
                <input type="file" id="batch-files" accept="audio/*" multiple style="display: none;">
            </div>
            
            <div id="batch-file-list" style="margin-top: 1rem;"></div>
            
            <div class="form-group">
                <label for="batch-operation">Operation:</label>
                <select id="batch-operation">
                    <option value="transcribe">Transcribe only</option>
                    <option value="translate">Translate only</option>
                    <option value="both">Transcribe and Translate</option>
                </select>
            </div>
            
            <button id="process-batch-btn" class="btn btn-secondary" disabled>Process Files</button>
            
            <div class="progress-container" id="batch-progress">
                <div class="progress-bar">
                    <div class="progress" id="batch-progress-bar"></div>
                </div>
                <div class="progress-text">
                    <span id="batch-status">Processing...</span>
                    <span id="batch-percentage">0%</span>
                </div>
            </div>
            
            <div class="results-container" id="batch-results">
                <h3>Batch Processing Results</h3>
                <div id="batch-outputs"></div>
            </div>
        `;
    }

    loadFooterContent() {
        const footerContent = document.getElementById('footer-content');
        if (!footerContent) return;

        footerContent.innerHTML = `
            <div class="footer-section">
                <h3>AudioTranslate Pro</h3>
                <p>Advanced AI audio transcription and translation technology for content creators, businesses, and developers.</p>
            </div>
            <div class="footer-section">
                <h3>Quick Links</h3>
                <ul class="footer-links">
                    <li><a href="#features">Features</a></li>
                    <li><a href="#app">Try It</a></li>
                    <li><a href="#pricing">Pricing</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>Legal</h3>
                <ul class="footer-links">
                    <li><a href="#">Privacy Policy</a></li>
                    <li><a href="#">Terms of Service</a></li>
                    <li><a href="#">Cookie Policy</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>Contact Us</h3>
                <ul class="footer-links">
                    <li>Email: info@audiotranslate.pro</li>
                    <li>Phone: +1 (555) 123-4567</li>
                    <li>Address: 123 AI Street, Tech City</li>
                </ul>
            </div>
        `;
    }

    initializeManagers() {
        // Reinitialize file upload manager after loading tab contents
        setTimeout(() => {
            window.fileUploadManager = new FileUploadManager();
        }, 100);

        // Initialize other managers
        this.managers.transcription = new TranscriptionManager();
        this.managers.translation = new TranslationManager();
        this.managers.batch = new BatchProcessingManager();
    }

    setupGlobalEventListeners() {
        // Smooth scrolling for navigation links
        document.addEventListener('click', (e) => {
            if (e.target.matches('a[href^="#"]')) {
                e.preventDefault();
                const target = document.querySelector(e.target.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });

        // Global error handler
        window.addEventListener('error', (e) => {
            console.error('Global error:', e.error);
            AudioTranslateUtils.showNotification('An unexpected error occurred.', 'error');
        });
    }

    setupTabNavigation() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('.tab')) {
                const tab = e.target.closest('.tab');
                
                // Remove active class from all tabs and contents
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked tab and corresponding content
                tab.classList.add('active');
                const tabId = tab.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
            }
        });
    }
}

// Initialize the application
const audioTranslateApp = new AudioTranslateApp();
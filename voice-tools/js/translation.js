class TranslationManager {
    constructor() {
        this.selectedLanguages = new Set();
        this.isProcessing = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupLanguageSelection();
    }

    bindEvents() {
        // Translation button
        const translateBtn = document.getElementById('translate-btn');
        if (translateBtn) {
            translateBtn.addEventListener('click', () => this.startTranslation());
        }

        // Download buttons for translations
        document.addEventListener('click', (e) => {
            if (e.target.closest('.download-btn') && e.target.closest('.audio-player')) {
                const button = e.target.closest('.download-btn');
                const format = button.getAttribute('data-format');
                const language = button.closest('.audio-player').dataset.language;
                this.handleTranslationDownload(language, format);
            }
        });
    }

    setupLanguageSelection() {
        const languageOptions = document.querySelectorAll('.language-option');
        
        languageOptions.forEach(option => {
            option.addEventListener('click', () => {
                const lang = option.getAttribute('data-lang');
                
                if (this.selectedLanguages.has(lang)) {
                    this.selectedLanguages.delete(lang);
                    option.classList.remove('selected');
                } else {
                    this.selectedLanguages.add(lang);
                    option.classList.add('selected');
                }

                this.updateTranslateButton();
            });
        });
    }

    updateTranslateButton() {
        const translateBtn = document.getElementById('translate-btn');
        if (translateBtn) {
            translateBtn.disabled = this.selectedLanguages.size === 0;
        }
    }

    async startTranslation() {
        if (this.isProcessing) return;

        const fileInput = document.getElementById('translation-file');
        if (!fileInput.files.length) {
            AudioTranslateUtils.showNotification('Please select an audio file first.', 'error');
            return;
        }

        if (this.selectedLanguages.size === 0) {
            AudioTranslateUtils.showNotification('Please select at least one target language.', 'error');
            return;
        }

        this.isProcessing = true;
        const translateBtn = document.getElementById('translate-btn');
        translateBtn.disabled = true;
        translateBtn.textContent = 'Translating...';

        const progressContainer = document.getElementById('translation-progress');
        const progressBar = document.getElementById('translation-progress-bar');
        const progressPercentage = document.getElementById('translation-percentage');

        progressContainer.style.display = 'block';

        try {
            // Simulate API call to translation service
            await this.simulateTranslationProcess(progressBar, progressPercentage);
            
            // Show results
            this.showTranslationResults();
            AudioTranslateUtils.showNotification('Translation completed successfully!', 'success');
            
        } catch (error) {
            AudioTranslateUtils.showNotification('Translation failed. Please try again.', 'error');
            console.error('Translation error:', error);
        } finally {
            this.isProcessing = false;
            translateBtn.disabled = false;
            translateBtn.textContent = 'Translate Audio';
        }
    }

    simulateTranslationProcess(progressBar, progressPercentage) {
        return new Promise((resolve) => {
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 10;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                    resolve();
                }
                
                progressBar.style.width = `${progress}%`;
                progressPercentage.textContent = `${Math.round(progress)}%`;
            }, 300);
        });
    }

    showTranslationResults() {
        const resultsContainer = document.getElementById('translation-results');
        resultsContainer.style.display = 'block';

        const translationOutputs = document.getElementById('translation-outputs');
        translationOutputs.innerHTML = '';

        this.selectedLanguages.forEach(lang => {
            const languageData = this.getLanguageData(lang);
            translationOutputs.innerHTML += this.createTranslationOutput(languageData);
        });
    }

    getLanguageData(langCode) {
        const languages = {
            'de': { name: 'German', flag: '🇩🇪' },
            'fr': { name: 'French', flag: '🇫🇷' },
            'ru': { name: 'Russian', flag: '🇷🇺' },
            'zh': { name: 'Chinese', flag: '🇨🇳' },
            'ja': { name: 'Japanese', flag: '🇯🇵' },
            'hi': { name: 'Hindi', flag: '🇮🇳' },
            'ar': { name: 'Arabic', flag: '🇸🇦' },
            'it': { name: 'Italian', flag: '🇮🇹' }
        };

        return languages[langCode] || { name: 'Unknown', flag: '🌐' };
    }

    createTranslationOutput(languageData) {
        return `
            <div class="audio-player" data-language="${languageData.name.toLowerCase()}">
                <h4>${languageData.flag} ${languageData.name} Translation</h4>
                <p>Translated audio ready for download. The voice characteristics have been preserved in the translation.</p>
                <audio controls style="width: 100%; margin: 1rem 0;">
                    <source src="#" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                <div class="download-options">
                    <div class="download-btn" data-format="mp3">
                        <i>📥</i> Download MP3
                    </div>
                    <div class="download-btn" data-format="wav">
                        <i>📥</i> Download WAV
                    </div>
                    <div class="download-btn" data-format="srt">
                        <i>📄</i> Download Subtitles
                    </div>
                </div>
            </div>
        `;
    }

    handleTranslationDownload(language, format) {
        // In a real application, this would download the actual translated file
        const filename = `translation_${language}.${format}`;
        AudioTranslateUtils.showNotification(`Downloading ${filename}...`, 'info');
        
        // Simulate download
        setTimeout(() => {
            AudioTranslateUtils.showNotification(`${filename} downloaded successfully!`, 'success');
        }, 1000);
    }

    getSelectedLanguages() {
        return Array.from(this.selectedLanguages);
    }

    clearSelection() {
        this.selectedLanguages.clear();
        document.querySelectorAll('.language-option').forEach(option => {
            option.classList.remove('selected');
        });
        this.updateTranslateButton();
    }
}
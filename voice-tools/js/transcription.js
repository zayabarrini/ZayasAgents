class TranscriptionManager {
    constructor() {
        this.currentAudio = null;
        this.isProcessing = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupAudioPlayer();
    }

    bindEvents() {
        // Transcription button
        const transcribeBtn = document.getElementById('transcribe-btn');
        if (transcribeBtn) {
            transcribeBtn.addEventListener('click', () => this.startTranscription());
        }

        // Download buttons
        document.addEventListener('click', (e) => {
            if (e.target.closest('.download-btn')) {
                const button = e.target.closest('.download-btn');
                const format = button.getAttribute('data-format');
                this.handleDownload(format);
            }
        });

        // Result tabs
        document.addEventListener('click', (e) => {
            if (e.target.closest('.result-tab')) {
                const tab = e.target.closest('.result-tab');
                this.switchResultTab(tab);
            }
        });
    }

    setupAudioPlayer() {
        // This would be connected to actual audio elements in a real implementation
        const audioElement = document.createElement('audio');
        audioElement.id = 'transcription-audio';
        audioElement.style.display = 'none';
        document.body.appendChild(audioElement);
    }

    async startTranscription() {
        if (this.isProcessing) return;

        const fileInput = document.getElementById('transcription-file');
        if (!fileInput.files.length) {
            AudioTranslateUtils.showNotification('Please select an audio file first.', 'error');
            return;
        }

        this.isProcessing = true;
        const transcribeBtn = document.getElementById('transcribe-btn');
        transcribeBtn.disabled = true;
        transcribeBtn.textContent = 'Processing...';

        const progressContainer = document.getElementById('transcription-progress');
        const progressBar = document.getElementById('transcription-progress-bar');
        const progressPercentage = document.getElementById('transcription-percentage');

        progressContainer.style.display = 'block';

        try {
            // Simulate API call to transcription service
            await this.simulateTranscriptionProcess(progressBar, progressPercentage);
            
            // Show results
            this.showTranscriptionResults();
            AudioTranslateUtils.showNotification('Transcription completed successfully!', 'success');
            
        } catch (error) {
            AudioTranslateUtils.showNotification('Transcription failed. Please try again.', 'error');
            console.error('Transcription error:', error);
        } finally {
            this.isProcessing = false;
            transcribeBtn.disabled = false;
            transcribeBtn.textContent = 'Transcribe Audio';
        }
    }

    simulateTranscriptionProcess(progressBar, progressPercentage) {
        return new Promise((resolve) => {
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 15;
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

    showTranscriptionResults() {
        const resultsContainer = document.getElementById('transcription-results');
        resultsContainer.style.display = 'block';

        // Generate sample transcript data
        this.generateSampleTranscript();
        this.generateSampleSubtitles();
    }

    generateSampleTranscript() {
        const transcriptText = document.getElementById('transcript-text');
        const sampleData = this.getSampleTranscriptionData();
        
        transcriptText.innerHTML = sampleData.transcript.map(line => `
            <div class="transcript-line">
                <div class="transcript-time">${line.start} - ${line.end}</div>
                <div class="transcript-text">${line.text}</div>
            </div>
        `).join('');
    }

    generateSampleSubtitles() {
        const subtitlesText = document.getElementById('subtitles-text');
        const sampleData = this.getSampleTranscriptionData();
        
        subtitlesText.innerHTML = sampleData.subtitles.map((subtitle, index) => `
            <div class="transcript-line">
                <div class="transcript-time">${index + 1}</div>
                <div class="transcript-text">${subtitle.start} --> ${subtitle.end}<br>${subtitle.text}</div>
            </div>
        `).join('');
    }

    getSampleTranscriptionData() {
        return {
            transcript: [
                {
                    start: "00:00",
                    end: "00:05",
                    text: "Welcome to AudioTranslate Pro. This is a demonstration of our automatic transcription service."
                },
                {
                    start: "00:05",
                    end: "00:12",
                    text: "We use advanced speech recognition algorithms to convert your audio into accurate text transcripts."
                },
                {
                    start: "00:12",
                    end: "00:18",
                    text: "You can then download these transcripts in various formats or use them to generate subtitles."
                },
                {
                    start: "00:18",
                    end: "00:25",
                    text: "Our AI technology supports multiple languages and can handle various audio qualities."
                },
                {
                    start: "00:25",
                    end: "00:30",
                    text: "Thank you for trying AudioTranslate Pro!"
                }
            ],
            subtitles: [
                {
                    start: "00:00:00,000",
                    end: "00:00:05,000",
                    text: "Welcome to AudioTranslate Pro."
                },
                {
                    start: "00:00:05,000",
                    end: "00:00:12,000",
                    text: "This is a demonstration of our automatic transcription service."
                },
                {
                    start: "00:00:12,000",
                    end: "00:00:18,000",
                    text: "We use advanced speech recognition algorithms."
                },
                {
                    start: "00:00:18,000",
                    end: "00:00:25,000",
                    text: "Our AI supports multiple languages and audio qualities."
                },
                {
                    start: "00:00:25,000",
                    end: "00:00:30,000",
                    text: "Thank you for trying AudioTranslate Pro!"
                }
            ]
        };
    }

    switchResultTab(tab) {
        // Remove active class from all result tabs and contents
        document.querySelectorAll('.result-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.result-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab and corresponding content
        tab.classList.add('active');
        const resultTabId = tab.getAttribute('data-result-tab');
        document.getElementById(resultTabId).classList.add('active');
    }

    handleDownload(format) {
        // In a real application, this would generate and download the actual file
        const filename = `transcription.${format}`;
        AudioTranslateUtils.showNotification(`Downloading ${filename}...`, 'info');
        
        // Simulate download
        setTimeout(() => {
            AudioTranslateUtils.showNotification(`${filename} downloaded successfully!`, 'success');
        }, 1000);
    }
}
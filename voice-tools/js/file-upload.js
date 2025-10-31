class FileUploadManager {
    constructor() {
        this.uploadAreas = new Map();
        this.init();
    }

    init() {
        // Initialize file upload functionality for different sections
        this.setupTranscriptionUpload();
        this.setupTranslationUpload();
        this.setupBatchUpload();
    }

    setupTranscriptionUpload() {
        const uploadArea = document.getElementById('transcription-upload-area');
        const fileInput = document.getElementById('transcription-file');
        const fileInfo = document.getElementById('transcription-file-info');
        const transcribeBtn = document.getElementById('transcribe-btn');

        this.setupUploadArea(uploadArea, fileInput, fileInfo, transcribeBtn);
    }

    setupTranslationUpload() {
        const uploadArea = document.getElementById('translation-upload-area');
        const fileInput = document.getElementById('translation-file');
        const fileInfo = document.getElementById('translation-file-info');
        const translateBtn = document.getElementById('translate-btn');

        this.setupUploadArea(uploadArea, fileInput, fileInfo, translateBtn);
    }

    setupBatchUpload() {
        const uploadArea = document.getElementById('batch-upload-area');
        const fileInput = document.getElementById('batch-files');
        const fileList = document.getElementById('batch-file-list');
        const processBtn = document.getElementById('process-batch-btn');

        this.setupBatchUploadArea(uploadArea, fileInput, fileList, processBtn);
    }

    setupUploadArea(uploadArea, fileInput, fileInfo, enableButton) {
        if (!uploadArea || !fileInput) return;

        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                this.handleFileSelection(fileInput.files, fileInfo, enableButton);
            }
        });

        fileInput.addEventListener('change', () => {
            this.handleFileSelection(fileInput.files, fileInfo, enableButton);
        });
    }

    setupBatchUploadArea(uploadArea, fileInput, fileList, processBtn) {
        if (!uploadArea || !fileInput) return;

        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', () => {
            this.handleBatchFileSelection(fileInput.files, fileList, processBtn);
        });
    }

    handleFileSelection(files, fileInfo, enableButton) {
        if (files.length > 0) {
            const file = files[0];
            const validation = AudioTranslateUtils.validateFile(
                file, 
                ['audio/mpeg', 'audio/wav', 'audio/m4a', 'audio/ogg'],
                100 * 1024 * 1024 // 100MB
            );

            if (validation.isValid) {
                fileInfo.innerHTML = `
                    <div style="color: var(--secondary);">
                        <p>File selected: <strong>${file.name}</strong> (${AudioTranslateUtils.formatFileSize(file.size)})</p>
                    </div>
                `;
                if (enableButton) enableButton.disabled = false;
                AudioTranslateUtils.showNotification('File uploaded successfully!', 'success');
            } else {
                fileInfo.innerHTML = `
                    <div style="color: var(--danger);">
                        <p>Error: ${validation.errors.join(', ')}</p>
                    </div>
                `;
                if (enableButton) enableButton.disabled = true;
                AudioTranslateUtils.showNotification(validation.errors.join(', '), 'error');
            }
        }
    }

    handleBatchFileSelection(files, fileList, processBtn) {
        if (files.length > 0) {
            let fileListHTML = '<p><strong>Selected files:</strong></p><ul>';
            let totalSize = 0;
            let hasErrors = false;

            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const validation = AudioTranslateUtils.validateFile(
                    file,
                    ['audio/mpeg', 'audio/wav', 'audio/m4a', 'audio/ogg'],
                    50 * 1024 * 1024 // 50MB per file
                );

                totalSize += file.size;

                if (validation.isValid) {
                    fileListHTML += `<li style="color: var(--secondary);">${file.name} (${AudioTranslateUtils.formatFileSize(file.size)})</li>`;
                } else {
                    fileListHTML += `<li style="color: var(--danger);">${file.name} - ${validation.errors.join(', ')}</li>`;
                    hasErrors = true;
                }
            }

            fileListHTML += '</ul>';

            // Check total size
            if (totalSize > 500 * 1024 * 1024) { // 500MB total
                fileListHTML += `<p style="color: var(--danger);">Total size exceeds 500MB limit</p>`;
                hasErrors = true;
            }

            // Check file count
            if (files.length > 10) {
                fileListHTML += `<p style="color: var(--danger);">Maximum 10 files allowed</p>`;
                hasErrors = true;
            }

            fileList.innerHTML = fileListHTML;

            if (processBtn) {
                processBtn.disabled = hasErrors || files.length === 0;
            }

            if (!hasErrors) {
                AudioTranslateUtils.showNotification(`${files.length} files uploaded successfully!`, 'success');
            }
        }
    }
}

// Initialize file upload manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.fileUploadManager = new FileUploadManager();
});
class BatchProcessingManager {
    constructor() {
        this.currentBatch = [];
        this.isProcessing = false;
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        const processBatchBtn = document.getElementById('process-batch-btn');
        if (processBatchBtn) {
            processBatchBtn.addEventListener('click', () => this.processBatch());
        }

        // Batch download buttons
        document.addEventListener('click', (e) => {
            if (e.target.closest('.download-btn') && e.target.closest('#batch-results')) {
                const button = e.target.closest('.download-btn');
                const format = button.getAttribute('data-format');
                this.handleBatchDownload(format);
            }
        });
    }

    async processBatch() {
        if (this.isProcessing) return;

        const fileInput = document.getElementById('batch-files');
        if (!fileInput.files.length) {
            AudioTranslateUtils.showNotification('Please select files to process.', 'error');
            return;
        }

        const operation = document.getElementById('batch-operation').value;
        this.isProcessing = true;

        const processBtn = document.getElementById('process-batch-btn');
        processBtn.disabled = true;
        processBtn.textContent = 'Processing...';

        const progressContainer = document.getElementById('batch-progress');
        const progressBar = document.getElementById('batch-progress-bar');
        const progressPercentage = document.getElementById('batch-percentage');

        progressContainer.style.display = 'block';

        try {
            // Simulate batch processing
            await this.simulateBatchProcess(progressBar, progressPercentage, fileInput.files.length);
            
            // Show results
            this.showBatchResults(operation, fileInput.files);
            AudioTranslateUtils.showNotification('Batch processing completed!', 'success');
            
        } catch (error) {
            AudioTranslateUtils.showNotification('Batch processing failed. Please try again.', 'error');
            console.error('Batch processing error:', error);
        } finally {
            this.isProcessing = false;
            processBtn.disabled = false;
            processBtn.textContent = 'Process Files';
        }
    }

    simulateBatchProcess(progressBar, progressPercentage, fileCount) {
        return new Promise((resolve) => {
            let progress = 0;
            const filesProcessed = Math.min(fileCount, 10); // Max 10 files
            const progressPerFile = 100 / filesProcessed;
            let currentFile = 0;

            const interval = setInterval(() => {
                const fileProgress = Math.random() * 20;
                progress = (currentFile * progressPerFile) + (fileProgress * progressPerFile / 100);

                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                    resolve();
                }

                // Move to next file if current file is done
                if (fileProgress >= 95 && currentFile < filesProcessed - 1) {
                    currentFile++;
                }

                progressBar.style.width = `${progress}%`;
                progressPercentage.textContent = `${Math.round(progress)}%`;
            }, 200);
        });
    }

    showBatchResults(operation, files) {
        const resultsContainer = document.getElementById('batch-results');
        resultsContainer.style.display = 'block';

        const batchOutputs = document.getElementById('batch-outputs');
        
        let resultsHTML = `
            <div style="background: #f9fafb; padding: 1.5rem; border-radius: 8px;">
                <h4>Batch Processing Complete</h4>
                <p>Successfully processed ${files.length} files with operation: <strong>${this.getOperationName(operation)}</strong></p>
                
                <div class="file-results" style="margin-top: 1.5rem;">
                    <h5>Processed Files:</h5>
                    <div style="max-height: 300px; overflow-y: auto;">
        `;

        // Add individual file results
        Array.from(files).forEach((file, index) => {
            resultsHTML += this.createFileResultItem(file, index, operation);
        });

        resultsHTML += `
                    </div>
                </div>
                
                <div class="download-options" style="margin-top: 1.5rem;">
                    <div class="download-btn" data-format="zip">
                        <i>📦</i> Download All as ZIP
                    </div>
                    <div class="download-btn" data-format="report">
                        <i>📊</i> Download Processing Report
                    </div>
                </div>
            </div>
        `;

        batchOutputs.innerHTML = resultsHTML;
    }

    getOperationName(operation) {
        const operations = {
            'transcribe': 'Transcription',
            'translate': 'Translation',
            'both': 'Transcription & Translation'
        };
        return operations[operation] || operation;
    }

    createFileResultItem(file, index, operation) {
        const status = 'completed';
        const fileSize = AudioTranslateUtils.formatFileSize(file.size);
        
        return `
            <div class="file-result-item" style="display: flex; justify-content: between; align-items: center; padding: 0.8rem; background: white; border-radius: 6px; margin-bottom: 0.5rem;">
                <div style="flex-grow: 1;">
                    <div style="font-weight: 500;">${file.name}</div>
                    <div style="font-size: 0.8rem; color: var(--gray);">${fileSize} • ${operation}</div>
                </div>
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                    <span style="color: var(--secondary); font-weight: 500;">✓</span>
                    <span style="color: var(--secondary); font-size: 0.8rem;">Completed</span>
                    <button class="download-btn" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;" data-file-index="${index}">
                        <i>📥</i>
                    </button>
                </div>
            </div>
        `;
    }

    handleBatchDownload(format) {
        const filename = `batch_results.${format}`;
        AudioTranslateUtils.showNotification(`Preparing ${filename} for download...`, 'info');
        
        // Simulate file preparation and download
        setTimeout(() => {
            AudioTranslateUtils.showNotification(`${filename} downloaded successfully!`, 'success');
        }, 1500);
    }

    getBatchSummary() {
        return {
            totalFiles: this.currentBatch.length,
            processedFiles: this.currentBatch.filter(file => file.status === 'completed').length,
            failedFiles: this.currentBatch.filter(file => file.status === 'failed').length,
            totalSize: this.currentBatch.reduce((sum, file) => sum + file.size, 0)
        };
    }

    resetBatch() {
        this.currentBatch = [];
        const fileInput = document.getElementById('batch-files');
        fileInput.value = '';
        
        const fileList = document.getElementById('batch-file-list');
        fileList.innerHTML = '';
        
        const processBtn = document.getElementById('process-batch-btn');
        processBtn.disabled = true;
        
        const resultsContainer = document.getElementById('batch-results');
        resultsContainer.style.display = 'none';
    }
}
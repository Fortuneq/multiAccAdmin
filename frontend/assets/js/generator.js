/**
 * Video Generator Page JavaScript
 * Handles video upload, editing, and export functionality
 */

let currentProject = null;
let uploadedVideo = null;
let uploadedAudio = null;

// Load page data
document.addEventListener('DOMContentLoaded', async () => {
    await loadAccounts();
});

/**
 * Load accounts for dropdown
 */
async function loadAccounts() {
    try {
        const accounts = await api.getAccounts();
        const select = document.getElementById('accountSelect');

        select.innerHTML = '<option value="">Select account...</option>' +
            accounts.map(acc => `
                <option value="${acc.id}">
                    ${acc.username} (${acc.platform})
                </option>
            `).join('');
    } catch (error) {
        console.error('Failed to load accounts:', error);
    }
}

/**
 * Create new project
 */
async function createNewProject() {
    const projectName = prompt('Enter project name:');
    if (!projectName) return;

    showLoader('Creating project...');

    try {
        currentProject = await api.createProject({
            name: projectName,
            status: 'draft'
        });

        hideLoader();
        showNotification('Project created successfully', 'success');
        console.log('Created project:', currentProject);
    } catch (error) {
        hideLoader();
        handleError(error, 'Creating Project');
    }
}

/**
 * Handle video file upload
 */
async function handleVideoUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const uploadArea = document.getElementById('videoUploadArea');
    uploadArea.classList.add('uploading');
    uploadArea.innerHTML = '<i class="ri-loader-4-line"></i><p>Uploading video...</p>';

    try {
        // Upload video to backend
        const result = await api.uploadVideo(file);
        uploadedVideo = result;

        // Update UI
        uploadArea.classList.remove('uploading');
        uploadArea.classList.add('success');
        uploadArea.innerHTML = `<i class="ri-check-line"></i><p>${file.name}</p>`;

        // Update preview
        const preview = document.getElementById('previewScreen');
        const videoURL = URL.createObjectURL(file);
        preview.innerHTML = `<video class="preview-video" src="${videoURL}" controls></video>`;

        // Update timeline
        const videoTrack = document.getElementById('videoTrack');
        videoTrack.innerHTML = `
            <div class="track-segment">
                <i class="ri-video-line"></i>
                ${file.name}
            </div>
        `;

        // Enable export button
        updateExportButton();

        showNotification('Video uploaded successfully', 'success');
    } catch (error) {
        uploadArea.classList.remove('uploading');
        handleError(error, 'Uploading Video');
    }
}

/**
 * Handle audio file upload
 */
async function handleAudioUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const uploadArea = document.getElementById('audioUploadArea');
    uploadArea.classList.add('uploading');
    uploadArea.innerHTML = '<i class="ri-loader-4-line"></i><p>Uploading audio...</p>';

    try {
        uploadedAudio = file;

        // Update UI
        uploadArea.classList.remove('uploading');
        uploadArea.classList.add('success');
        uploadArea.innerHTML = `<i class="ri-check-line"></i><p>${file.name}</p>`;

        // Update timeline
        const audioTrack = document.getElementById('audioTrack');
        audioTrack.innerHTML = `
            <div class="track-segment" style="background: #8B5CF6;">
                <i class="ri-music-line"></i>
                ${file.name}
            </div>
        `;

        showNotification('Audio uploaded successfully', 'success');
    } catch (error) {
        uploadArea.classList.remove('uploading');
        handleError(error, 'Uploading Audio');
    }
}

/**
 * Update volume slider value
 */
function updateVolume(value) {
    document.getElementById('volumeValue').textContent = value + '%';
}

/**
 * Apply video filter
 */
function applyFilter(filterType) {
    if (filterType === 'none') {
        showNotification('Filter removed', 'info');
    } else {
        showNotification(`Applied ${filterType} filter`, 'success');
    }
}

/**
 * Clear timeline
 */
function clearTimeline() {
    if (!confirm('Clear all timeline data?')) return;

    uploadedVideo = null;
    uploadedAudio = null;

    document.getElementById('videoTrack').innerHTML = '<div class="track-empty">No video loaded</div>';
    document.getElementById('audioTrack').innerHTML = '<div class="track-empty">No audio added</div>';
    document.getElementById('subtitleTrack').innerHTML = '<div class="track-empty">No subtitles</div>';
    document.getElementById('previewScreen').innerHTML = `
        <div class="preview-placeholder">
            <i class="ri-video-line"></i>
            <p>Upload a video to start editing</p>
        </div>
    `;

    // Reset upload areas
    document.getElementById('videoUploadArea').classList.remove('success');
    document.getElementById('videoUploadArea').innerHTML = '<i class="ri-upload-cloud-line"></i><p>Click or drag video file</p>';
    document.getElementById('audioUploadArea').classList.remove('success');
    document.getElementById('audioUploadArea').innerHTML = '<i class="ri-music-line"></i><p>Click or drag audio file</p>';

    updateExportButton();
    showNotification('Timeline cleared', 'info');
}

/**
 * Save draft
 */
async function saveDraft() {
    if (!currentProject) {
        showNotification('Please create a project first', 'warning');
        return;
    }

    showLoader('Saving draft...');

    try {
        const settings = collectSettings();

        await api.updateProject(currentProject.id, {
            ...settings,
            status: 'draft'
        });

        hideLoader();
        showNotification('Draft saved successfully', 'success');
    } catch (error) {
        hideLoader();
        handleError(error, 'Saving Draft');
    }
}

/**
 * Export video
 */
async function exportVideo() {
    if (!uploadedVideo) {
        showNotification('Please upload a video first', 'warning');
        return;
    }

    const accountId = document.getElementById('accountSelect').value;
    if (!accountId) {
        showNotification('Please select a target account', 'warning');
        return;
    }

    showLoader('Processing and exporting video...');

    try {
        // Create or update project
        if (!currentProject) {
            currentProject = await api.createProject({
                name: `Project_${Date.now()}`,
                account_id: parseInt(accountId),
                video_path: uploadedVideo.file_path,
                status: 'processing'
            });
        }

        // Collect settings
        const settings = collectSettings();

        // Process video
        await api.processVideo(currentProject.id, settings);

        // Export
        const result = await api.exportVideo(currentProject.id);

        hideLoader();
        showNotification('Video exported successfully!', 'success');
        console.log('Export result:', result);

        // Show success modal
        showModal('Export Complete', `
            <div style="text-align: center; padding: 20px;">
                <i class="ri-check-circle-line" style="font-size: 64px; color: #10B981;"></i>
                <h3 style="margin-top: 20px; margin-bottom: 10px;">Video exported successfully!</h3>
                <p style="color: #6B7280;">Your video has been processed and is ready to upload.</p>
            </div>
        `, [
            {
                text: 'OK',
                action: 'ok',
                className: 'modal-btn-primary',
                onClick: () => {}
            }
        ]);
    } catch (error) {
        hideLoader();
        handleError(error, 'Exporting Video');
    }
}

/**
 * Collect all settings from form
 */
function collectSettings() {
    const subtitleText = document.getElementById('subtitleText').value;
    const volumeSlider = document.getElementById('volumeSlider');
    const filterSelect = document.getElementById('filterSelect');
    const uniquifyToggle = document.getElementById('uniquifyToggle');

    return {
        audio_volume: parseInt(volumeSlider.value),
        filter_type: filterSelect.value,
        subtitle_text: subtitleText,
        uniquify_subtitles: uniquifyToggle.checked,
        audio_path: uploadedAudio ? uploadedAudio.name : null
    };
}

/**
 * Update export button state
 */
function updateExportButton() {
    const exportBtn = document.getElementById('exportBtn');
    exportBtn.disabled = !uploadedVideo;
}

/**
 * Drag and drop handlers
 */
document.addEventListener('DOMContentLoaded', () => {
    const videoArea = document.getElementById('videoUploadArea');
    const audioArea = document.getElementById('audioUploadArea');

    // Video upload area
    videoArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        videoArea.style.borderColor = '#0066FF';
    });

    videoArea.addEventListener('dragleave', () => {
        videoArea.style.borderColor = '';
    });

    videoArea.addEventListener('drop', (e) => {
        e.preventDefault();
        videoArea.style.borderColor = '';

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('video/')) {
            const input = document.getElementById('videoInput');
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            handleVideoUpload({ target: input });
        }
    });

    // Audio upload area
    audioArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        audioArea.style.borderColor = '#0066FF';
    });

    audioArea.addEventListener('dragleave', () => {
        audioArea.style.borderColor = '';
    });

    audioArea.addEventListener('drop', (e) => {
        e.preventDefault();
        audioArea.style.borderColor = '';

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('audio/')) {
            const input = document.getElementById('audioInput');
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            handleAudioUpload({ target: input });
        }
    });

    // Subtitle text updates timeline
    document.getElementById('subtitleText').addEventListener('input', (e) => {
        const track = document.getElementById('subtitleTrack');
        if (e.target.value) {
            track.innerHTML = `
                <div class="track-segment" style="background: #F59E0B;">
                    <i class="ri-text"></i>
                    ${e.target.value.substring(0, 30)}${e.target.value.length > 30 ? '...' : ''}
                </div>
            `;
        } else {
            track.innerHTML = '<div class="track-empty">No subtitles</div>';
        }
    });
});

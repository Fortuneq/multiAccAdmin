/**
 * Utility functions for the admin panel
 */

// ==================== NOTIFICATIONS ====================

/**
 * Show toast notification
 * @param {string} message - Notification message
 * @param {string} type - Type: success, error, warning, info
 * @param {number} duration - Duration in ms (default: 3000)
 */
function showNotification(message, type = 'info', duration = 3000) {
    // Remove existing notifications
    const existing = document.querySelector('.toast-notification');
    if (existing) {
        existing.remove();
    }

    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;

    const iconMap = {
        success: 'ri-checkbox-circle-line',
        error: 'ri-error-warning-line',
        warning: 'ri-alert-line',
        info: 'ri-information-line'
    };

    toast.innerHTML = `
        <i class="${iconMap[type]}"></i>
        <span>${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="ri-close-line"></i>
        </button>
    `;

    document.body.appendChild(toast);

    // Auto remove
    setTimeout(() => {
        if (toast.parentElement) {
            toast.classList.add('toast-fade-out');
            setTimeout(() => toast.remove(), 300);
        }
    }, duration);
}

// ==================== LOADING SPINNER ====================

/**
 * Show loading overlay
 * @param {string} message - Loading message
 */
function showLoader(message = 'Loading...') {
    let loader = document.getElementById('global-loader');

    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'global-loader';
        loader.className = 'loader-overlay';
        loader.innerHTML = `
            <div class="loader-content">
                <div class="loader-spinner"></div>
                <p class="loader-text">${message}</p>
            </div>
        `;
        document.body.appendChild(loader);
    } else {
        loader.querySelector('.loader-text').textContent = message;
        loader.style.display = 'flex';
    }
}

/**
 * Hide loading overlay
 */
function hideLoader() {
    const loader = document.getElementById('global-loader');
    if (loader) {
        loader.style.display = 'none';
    }
}

// ==================== FORMATTERS ====================

/**
 * Format large numbers with K, M suffix
 * @param {number} num
 */
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

/**
 * Format date to readable string
 * @param {string|Date} date
 */
function formatDate(date) {
    const d = new Date(date);
    const now = new Date();
    const diffMs = now - d;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

/**
 * Format engagement rate as percentage
 * @param {number} rate
 */
function formatEngagement(rate) {
    return rate.toFixed(1) + '%';
}

// ==================== MODAL HELPERS ====================

/**
 * Create and show modal dialog
 * @param {string} title - Modal title
 * @param {string} content - Modal HTML content
 * @param {Array} buttons - Array of button configs [{text, onClick, className}]
 */
function showModal(title, content, buttons = []) {
    // Remove existing modals
    const existing = document.querySelector('.modal-overlay');
    if (existing) {
        existing.remove();
    }

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';

    const buttonsHTML = buttons.map(btn =>
        `<button class="modal-btn ${btn.className || ''}" data-action="${btn.action || ''}">${btn.text}</button>`
    ).join('');

    modal.innerHTML = `
        <div class="modal-container">
            <div class="modal-header">
                <h3 class="modal-title">${title}</h3>
                <button class="modal-close">
                    <i class="ri-close-line"></i>
                </button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
            <div class="modal-footer">
                ${buttonsHTML}
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Close handlers
    modal.querySelector('.modal-close').onclick = () => modal.remove();
    modal.onclick = (e) => {
        if (e.target === modal) modal.remove();
    };

    // Button handlers
    buttons.forEach(btn => {
        if (btn.onClick) {
            const btnEl = modal.querySelector(`[data-action="${btn.action}"]`);
            if (btnEl) {
                btnEl.onclick = () => {
                    btn.onClick();
                    if (btn.closeAfter !== false) {
                        modal.remove();
                    }
                };
            }
        }
    });

    return modal;
}

/**
 * Close all modals
 */
function closeModal() {
    const modals = document.querySelectorAll('.modal-overlay');
    modals.forEach(m => m.remove());
}

// ==================== PLATFORM HELPERS ====================

/**
 * Get platform icon class
 * @param {string} platform - Platform name (TikTok/Reels/Shorts)
 */
function getPlatformIcon(platform) {
    const icons = {
        'TikTok': 'ri-tiktok-fill',
        'Reels': 'ri-instagram-fill',
        'Shorts': 'ri-youtube-fill'
    };
    return icons[platform] || 'ri-video-line';
}

/**
 * Get platform color
 * @param {string} platform
 */
function getPlatformColor(platform) {
    const colors = {
        'TikTok': '#000000',
        'Reels': '#E1306C',
        'Shorts': '#FF0000'
    };
    return colors[platform] || '#6B7280';
}

// ==================== STATUS HELPERS ====================

/**
 * Get status badge HTML
 * @param {string} status - online/offline/idle
 */
function getStatusBadge(status) {
    const statusMap = {
        'online': { text: 'Online', class: 'status-online' },
        'offline': { text: 'Offline', class: 'status-offline' },
        'idle': { text: 'Idle', class: 'status-idle' }
    };
    const s = statusMap[status.toLowerCase()] || { text: status, class: '' };
    return `<span class="status-badge ${s.class}"><span class="status-dot"></span> ${s.text}</span>`;
}

// ==================== VALIDATION ====================

/**
 * Validate form data
 * @param {Object} data - Form data to validate
 * @param {Object} rules - Validation rules
 */
function validateForm(data, rules) {
    const errors = {};

    for (const [field, rule] of Object.entries(rules)) {
        const value = data[field];

        if (rule.required && !value) {
            errors[field] = `${field} is required`;
            continue;
        }

        if (rule.minLength && value.length < rule.minLength) {
            errors[field] = `${field} must be at least ${rule.minLength} characters`;
        }

        if (rule.pattern && !rule.pattern.test(value)) {
            errors[field] = rule.message || `${field} is invalid`;
        }
    }

    return {
        isValid: Object.keys(errors).length === 0,
        errors
    };
}

/**
 * Highlight form errors
 * @param {Object} errors - Error object {fieldName: errorMessage}
 */
function showFormErrors(errors) {
    // Clear previous errors
    document.querySelectorAll('.form-error').forEach(el => el.remove());
    document.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));

    // Show new errors
    for (const [field, message] of Object.entries(errors)) {
        const input = document.querySelector(`[name="${field}"]`);
        if (input) {
            input.classList.add('input-error');
            const error = document.createElement('div');
            error.className = 'form-error';
            error.textContent = message;
            input.parentElement.appendChild(error);
        }
    }
}

// ==================== LOCAL STORAGE ====================

/**
 * Save data to localStorage
 * @param {string} key
 * @param {any} data
 */
function saveToStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (e) {
        console.error('Failed to save to localStorage:', e);
    }
}

/**
 * Load data from localStorage
 * @param {string} key
 * @param {any} defaultValue
 */
function loadFromStorage(key, defaultValue = null) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : defaultValue;
    } catch (e) {
        console.error('Failed to load from localStorage:', e);
        return defaultValue;
    }
}

// ==================== DEBOUNCE ====================

/**
 * Debounce function calls
 * @param {Function} func
 * @param {number} wait
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==================== ERROR HANDLER ====================

/**
 * Handle API errors globally
 * @param {Error} error
 * @param {string} context - Context where error occurred
 */
function handleError(error, context = '') {
    console.error(`Error in ${context}:`, error);

    const message = error.message || 'An unexpected error occurred';
    showNotification(message, 'error', 5000);
}

// ==================== AUTO REFRESH ====================

let refreshInterval = null;

/**
 * Start auto-refresh for a function
 * @param {Function} func - Function to call
 * @param {number} interval - Interval in ms (default: 30000)
 */
function startAutoRefresh(func, interval = 30000) {
    stopAutoRefresh();
    refreshInterval = setInterval(func, interval);
}

/**
 * Stop auto-refresh
 */
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
}

// ==================== COPY TO CLIPBOARD ====================

/**
 * Copy text to clipboard
 * @param {string} text
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard', 'success', 2000);
    } catch (err) {
        console.error('Failed to copy:', err);
        showNotification('Failed to copy', 'error');
    }
}

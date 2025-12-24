/**
 * Accounts Page JavaScript
 * Handles account management, CRUD operations, and proxy settings
 */

let currentPlatformFilter = 'all';
let allAccounts = [];

// Load accounts on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadAccounts();
    await loadProxies();
});

/**
 * Load all accounts from API
 */
async function loadAccounts(platform = null) {
    showLoader('Loading accounts...');

    try {
        allAccounts = await api.getAccounts(platform);
        displayAccounts(allAccounts);
        hideLoader();
    } catch (error) {
        hideLoader();
        handleError(error, 'Loading Accounts');
    }
}

/**
 * Display accounts in grid
 */
function displayAccounts(accounts) {
    const grid = document.getElementById('accountsGrid');

    if (!accounts || accounts.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 60px; color: #9CA3AF;">
                <i class="ri-user-line" style="font-size: 48px; margin-bottom: 16px;"></i>
                <p style="font-size: 16px;">No accounts found</p>
                <button onclick="showAddAccountModal()" class="btn-primary" style="margin-top: 20px;">
                    <i class="ri-add-line"></i> Add Your First Account
                </button>
            </div>
        `;
        return;
    }

    grid.innerHTML = accounts.map(account => {
        const platformClass = account.platform ? account.platform.toLowerCase() : 'tiktok';
        const platformIcon = getPlatformIcon(account.platform);
        const statusClass = account.status === 'online' ? 'status-online' : 'status-offline';

        return `
            <div class="account-card" onclick="showAccountDetails(${account.id})">
                <div class="account-header">
                    <div class="platform-icon ${platformClass}">
                        <i class="${platformIcon}"></i>
                    </div>
                    <span class="${statusClass} status-badge">
                        <span class="status-dot"></span>
                        ${account.status || 'offline'}
                    </span>
                </div>

                <div class="account-info">
                    <h3>${account.username || 'N/A'}</h3>
                    <p>${account.platform || 'TikTok'} • ${account.region || 'Global'}</p>
                </div>

                <div class="account-stats">
                    <div class="stat-box">
                        <label>Followers</label>
                        <value>${formatNumber(account.followers || 0)}</value>
                    </div>
                    <div class="stat-box">
                        <label>Videos</label>
                        <value>${account.videos_count || 0}</value>
                    </div>
                    <div class="stat-box">
                        <label>Likes</label>
                        <value>${formatNumber(account.total_likes || 0)}</value>
                    </div>
                    <div class="stat-box">
                        <label>Engagement</label>
                        <value>${formatEngagement(account.engagement_rate || 0)}</value>
                    </div>
                </div>

                <div class="proxy-info">
                    <span class="proxy-dot"></span>
                    <span>${account.proxy_id ? `Proxy #${account.proxy_id}` : 'No proxy configured'}</span>
                </div>

                <div class="account-actions" onclick="event.stopPropagation()">
                    <button class="btn-edit" onclick="editAccount(${account.id})">
                        <i class="ri-edit-line"></i> Edit
                    </button>
                    <button class="btn-delete" onclick="deleteAccount(${account.id})">
                        <i class="ri-delete-bin-line"></i> Delete
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Filter accounts by platform
 */
async function filterByPlatform(platform) {
    currentPlatformFilter = platform;

    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.platform === platform);
    });

    if (platform === 'all') {
        displayAccounts(allAccounts);
    } else {
        const filtered = allAccounts.filter(acc => acc.platform === platform);
        displayAccounts(filtered);
    }
}

/**
 * Search accounts by username
 */
function searchAccounts(query) {
    const filtered = allAccounts.filter(acc =>
        acc.username?.toLowerCase().includes(query.toLowerCase())
    );
    displayAccounts(filtered);
}

/**
 * Show account details panel
 */
async function showAccountDetails(accountId) {
    showLoader('Loading details...');

    try {
        const account = await api.getAccount(accountId);
        const panel = document.getElementById('detailsPanel');
        const content = document.getElementById('detailsContent');

        content.innerHTML = `
            <div style="margin-bottom: 24px;">
                <h4 style="font-size: 16px; font-weight: 600; margin-bottom: 8px;">Username</h4>
                <p style="color: #6B7280;">${account.username}</p>
            </div>

            <div style="margin-bottom: 24px;">
                <h4 style="font-size: 16px; font-weight: 600; margin-bottom: 8px;">Platform</h4>
                <p style="color: #6B7280;">${account.platform}</p>
            </div>

            <div style="margin-bottom: 24px;">
                <h4 style="font-size: 16px; font-weight: 600; margin-bottom: 8px;">Statistics</h4>
                <div class="account-stats">
                    <div class="stat-box">
                        <label>Followers</label>
                        <value>${formatNumber(account.followers || 0)}</value>
                    </div>
                    <div class="stat-box">
                        <label>Videos</label>
                        <value>${account.videos_count || 0}</value>
                    </div>
                </div>
            </div>

            <div style="margin-bottom: 24px;">
                <h4 style="font-size: 16px; font-weight: 600; margin-bottom: 12px;">Proxy Settings</h4>
                <div class="form-group">
                    <label class="form-label">Proxy</label>
                    <select id="proxySelect" class="form-select">
                        <option value="">No proxy</option>
                        <!-- Options populated by loadProxies() -->
                    </select>
                </div>
            </div>

            <button class="btn-primary" style="width: 100%;" onclick="saveAccountSettings(${accountId})">
                <i class="ri-save-line"></i> Save Settings
            </button>
        `;

        panel.style.display = 'block';
        await loadProxiesForSelect(account.proxy_id);
        hideLoader();
    } catch (error) {
        hideLoader();
        handleError(error, 'Loading Account Details');
    }
}

/**
 * Close details panel
 */
function closeDetailsPanel() {
    document.getElementById('detailsPanel').style.display = 'none';
}

/**
 * Load proxies for dropdown
 */
let proxiesList = [];

async function loadProxies() {
    try {
        proxiesList = await api.getProxies();
    } catch (error) {
        console.error('Failed to load proxies:', error);
    }
}

async function loadProxiesForSelect(selectedProxyId = null) {
    const select = document.getElementById('proxySelect');
    if (!select) return;

    select.innerHTML = '<option value="">No proxy</option>' +
        proxiesList.map(proxy => `
            <option value="${proxy.id}" ${proxy.id === selectedProxyId ? 'selected' : ''}>
                ${proxy.type} - ${proxy.host}:${proxy.port}
            </option>
        `).join('');
}

/**
 * Save account settings
 */
async function saveAccountSettings(accountId) {
    const proxyId = document.getElementById('proxySelect').value;

    showLoader('Saving...');

    try {
        await api.updateAccount(accountId, {
            proxy_id: proxyId ? parseInt(proxyId) : null
        });

        hideLoader();
        showNotification('Settings saved successfully', 'success');
        closeDetailsPanel();
        await loadAccounts();
    } catch (error) {
        hideLoader();
        handleError(error, 'Saving Settings');
    }
}

/**
 * Show add account modal
 */
function showAddAccountModal() {
    const modalContent = `
        <div class="form-group">
            <label class="form-label">Username</label>
            <input type="text" id="newUsername" class="form-input" placeholder="@username">
        </div>
        <div class="form-group">
            <label class="form-label">Platform</label>
            <select id="newPlatform" class="form-select">
                <option value="TikTok">TikTok</option>
                <option value="Reels">Instagram Reels</option>
                <option value="Shorts">YouTube Shorts</option>
            </select>
        </div>
        <div class="form-group">
            <label class="form-label">Proxy (optional)</label>
            <select id="newProxy" class="form-select">
                <option value="">No proxy</option>
                ${proxiesList.map(p => `<option value="${p.id}">${p.type} - ${p.host}:${p.port}</option>`).join('')}
            </select>
        </div>
    `;

    showModal('Add New Account', modalContent, [
        {
            text: 'Cancel',
            action: 'cancel',
            className: 'modal-btn-secondary',
            onClick: () => {}
        },
        {
            text: 'Add Account',
            action: 'create',
            className: 'modal-btn-primary',
            onClick: createAccount,
            closeAfter: false
        }
    ]);
}

/**
 * Create new account
 */
async function createAccount() {
    const username = document.getElementById('newUsername').value;
    const platform = document.getElementById('newPlatform').value;
    const proxyId = document.getElementById('newProxy').value;

    if (!username) {
        showNotification('Please enter a username', 'warning');
        return;
    }

    showLoader('Creating account...');
    closeModal();

    try {
        await api.createAccount({
            username,
            platform,
            proxy_id: proxyId ? parseInt(proxyId) : null
        });

        hideLoader();
        showNotification('Account created successfully', 'success');
        await loadAccounts();
    } catch (error) {
        hideLoader();
        handleError(error, 'Creating Account');
    }
}

/**
 * Edit account
 */
async function editAccount(accountId) {
    await showAccountDetails(accountId);
}

/**
 * Delete account
 */
async function deleteAccount(accountId) {
    if (!confirm('Are you sure you want to delete this account?')) {
        return;
    }

    showLoader('Deleting account...');

    try {
        await api.deleteAccount(accountId);
        hideLoader();
        showNotification('Account deleted successfully', 'success');
        await loadAccounts();
    } catch (error) {
        hideLoader();
        handleError(error, 'Deleting Account');
    }
}

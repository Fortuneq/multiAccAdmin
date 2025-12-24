/**
 * API Client for Multi-Account Admin Panel
 * Handles all HTTP requests to FastAPI backend
 */

class APIClient {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    /**
     * Make HTTP request with error handling
     * @private
     */
    async _request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: 'Request failed' }));
                throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Request failed [${endpoint}]:`, error);
            throw error;
        }
    }

    // ==================== ACCOUNTS ====================

    /**
     * Get all accounts with optional platform filter
     * @param {string|null} platform - Filter by platform (TikTok/Reels/Shorts)
     * @param {number} skip - Pagination offset
     * @param {number} limit - Maximum results
     */
    async getAccounts(platform = null, skip = 0, limit = 100) {
        let endpoint = `/api/accounts?skip=${skip}&limit=${limit}`;
        if (platform) {
            endpoint += `&platform=${platform}`;
        }
        return await this._request(endpoint);
    }

    /**
     * Get single account by ID
     * @param {number} accountId
     */
    async getAccount(accountId) {
        return await this._request(`/api/accounts/${accountId}`);
    }

    /**
     * Create new account
     * @param {Object} data - Account data (username, platform, proxy_id, etc.)
     */
    async createAccount(data) {
        return await this._request('/api/accounts', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * Update existing account
     * @param {number} accountId
     * @param {Object} data - Updated account data
     */
    async updateAccount(accountId, data) {
        return await this._request(`/api/accounts/${accountId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    /**
     * Delete account
     * @param {number} accountId
     */
    async deleteAccount(accountId) {
        return await this._request(`/api/accounts/${accountId}`, {
            method: 'DELETE'
        });
    }

    // ==================== PROXIES ====================

    /**
     * Get all proxies
     */
    async getProxies() {
        return await this._request('/api/proxies');
    }

    /**
     * Get single proxy by ID
     * @param {number} proxyId
     */
    async getProxy(proxyId) {
        return await this._request(`/api/proxies/${proxyId}`);
    }

    /**
     * Create new proxy
     * @param {Object} data - Proxy data (type, host, port, username, password)
     */
    async createProxy(data) {
        return await this._request('/api/proxies', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * Update existing proxy
     * @param {number} proxyId
     * @param {Object} data - Updated proxy data
     */
    async updateProxy(proxyId, data) {
        return await this._request(`/api/proxies/${proxyId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    /**
     * Delete proxy
     * @param {number} proxyId
     */
    async deleteProxy(proxyId) {
        return await this._request(`/api/proxies/${proxyId}`, {
            method: 'DELETE'
        });
    }

    /**
     * Test proxy connection
     * @param {number} proxyId
     */
    async testProxy(proxyId) {
        return await this._request(`/api/proxies/${proxyId}/test`, {
            method: 'POST'
        });
    }

    // ==================== VIDEOS ====================

    /**
     * Get all videos with optional account filter
     * @param {number|null} accountId - Filter by account
     */
    async getVideos(accountId = null) {
        let endpoint = '/api/videos';
        if (accountId) {
            endpoint += `?account_id=${accountId}`;
        }
        return await this._request(endpoint);
    }

    /**
     * Get single video by ID
     * @param {number} videoId
     */
    async getVideo(videoId) {
        return await this._request(`/api/videos/${videoId}`);
    }

    /**
     * Upload video file
     * @param {File} file - Video file to upload
     * @param {number|null} accountId - Associated account ID
     */
    async uploadVideo(file, accountId = null) {
        const formData = new FormData();
        formData.append('file', file);
        if (accountId) {
            formData.append('account_id', accountId);
        }

        const url = `${this.baseURL}/api/videos/upload`;
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
            throw new Error(error.detail || `Upload failed: ${response.statusText}`);
        }

        return await response.json();
    }

    /**
     * Delete video
     * @param {number} videoId
     */
    async deleteVideo(videoId) {
        return await this._request(`/api/videos/${videoId}`, {
            method: 'DELETE'
        });
    }

    // ==================== VIDEO GENERATOR ====================

    /**
     * Create new video project
     * @param {Object} data - Project data (name, account_id, video_path, etc.)
     */
    async createProject(data) {
        return await this._request('/api/generator/project', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * Get all video projects
     */
    async getProjects() {
        return await this._request('/api/generator/project');
    }

    /**
     * Get single project by ID
     * @param {number} projectId
     */
    async getProject(projectId) {
        return await this._request(`/api/generator/project/${projectId}`);
    }

    /**
     * Update existing project
     * @param {number} projectId
     * @param {Object} data - Updated project data
     */
    async updateProject(projectId, data) {
        return await this._request(`/api/generator/project/${projectId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    /**
     * Delete project
     * @param {number} projectId
     */
    async deleteProject(projectId) {
        return await this._request(`/api/generator/project/${projectId}`, {
            method: 'DELETE'
        });
    }

    /**
     * Process video with FFmpeg
     * @param {number} projectId
     * @param {Object} settings - Processing settings (audio_path, volume, filter, subtitle, etc.)
     */
    async processVideo(projectId, settings) {
        return await this._request(`/api/generator/project/${projectId}/process`, {
            method: 'POST',
            body: JSON.stringify(settings)
        });
    }

    /**
     * Export processed video
     * @param {number} projectId
     */
    async exportVideo(projectId) {
        return await this._request(`/api/generator/project/${projectId}/export`, {
            method: 'POST'
        });
    }

    // ==================== ANALYTICS ====================

    /**
     * Get dashboard data (overview, charts, top videos)
     */
    async getDashboard() {
        return await this._request('/api/analytics/dashboard');
    }

    /**
     * Get overall statistics
     */
    async getStats() {
        return await this._request('/api/analytics/stats');
    }

    /**
     * Get analytics for specific account
     * @param {number} accountId
     */
    async getAccountAnalytics(accountId) {
        return await this._request(`/api/analytics/account/${accountId}`);
    }

    // ==================== HEALTH ====================

    /**
     * Check API health
     */
    async healthCheck() {
        return await this._request('/health');
    }
}

// Create global instance
const api = new APIClient();

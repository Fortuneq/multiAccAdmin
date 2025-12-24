/**
 * Dashboard Page JavaScript
 * Handles loading and displaying analytics data
 */

// Load dashboard on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadDashboard();
    // Auto-refresh every 30 seconds
    startAutoRefresh(loadDashboard, 30000);
});

/**
 * Main function to load all dashboard data
 */
async function loadDashboard() {
    showLoader('Loading dashboard data...');

    try {
        // Fetch dashboard data from API
        const data = await api.getDashboard();

        // Update all sections
        updateOverviewCards(data.overview);
        updateCharts(data.charts);
        await loadTopVideos();

        hideLoader();
        console.log('Dashboard loaded successfully');
    } catch (error) {
        hideLoader();
        handleError(error, 'Loading Dashboard');
    }
}

/**
 * Update overview cards with data
 * @param {Object} overview - Overview data from API
 */
function updateOverviewCards(overview) {
    const cardsContainer = document.getElementById('overviewCards');

    const cards = [
        {
            icon: 'ri-user-star-fill',
            iconClass: 'icon-blue',
            value: formatNumber(overview.total_accounts || 0),
            label: 'Total Accounts',
            trend: '+12%',
            trendClass: 'trend-up'
        },
        {
            icon: 'ri-user-follow-fill',
            iconClass: 'icon-green',
            value: formatNumber(overview.active_accounts || 0),
            label: 'Active Accounts',
            trend: '+8%',
            trendClass: 'trend-up'
        },
        {
            icon: 'ri-video-fill',
            iconClass: 'icon-purple',
            value: formatNumber(overview.total_videos || 0),
            label: 'Total Videos',
            trend: '+24%',
            trendClass: 'trend-up'
        },
        {
            icon: 'ri-heart-3-fill',
            iconClass: 'icon-orange',
            value: formatEngagement(overview.avg_engagement_rate || 0),
            label: 'Avg Engagement',
            trend: overview.avg_engagement_rate > 5 ? '+5%' : '-2%',
            trendClass: overview.avg_engagement_rate > 5 ? 'trend-up' : 'trend-down'
        }
    ];

    cardsContainer.innerHTML = cards.map(card => `
        <div class="stat-card">
            <div class="stat-header">
                <div class="stat-icon ${card.iconClass}">
                    <i class="${card.icon}"></i>
                </div>
                <div class="trend-badge ${card.trendClass}">
                    <i class="ri-arrow-${card.trendClass === 'trend-up' ? 'up' : 'down'}-line"></i>
                    ${card.trend}
                </div>
            </div>
            <div>
                <div class="stat-value">${card.value}</div>
                <div class="stat-label">${card.label}</div>
            </div>
        </div>
    `).join('');
}

/**
 * Update charts section
 * @param {Object} charts - Chart data from API
 */
function updateCharts(charts) {
    const chartsContainer = document.getElementById('chartsContainer');

    if (!charts || !charts.platform_distribution) {
        chartsContainer.innerHTML = '<div class="chart-placeholder">No chart data available</div>';
        return;
    }

    // Platform distribution chart
    const platformData = charts.platform_distribution || { TikTok: 0, Reels: 0, Shorts: 0 };

    chartsContainer.innerHTML = `
        <div class="chart-card">
            <div class="chart-title">Platform Distribution</div>
            <div class="chart-placeholder">
                <div style="width: 100%; display: flex; flex-direction: column; gap: 12px; padding: 20px;">
                    ${Object.entries(platformData).map(([platform, count]) => `
                        <div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px;">
                                <span>${platform}</span>
                                <span style="font-weight: 600;">${count} accounts</span>
                            </div>
                            <div style="height: 8px; background: #E5E7EB; border-radius: 4px; overflow: hidden;">
                                <div style="height: 100%; width: ${count * 10}%; background: ${getPlatformColor(platform)};"></div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>

        <div class="chart-card">
            <div class="chart-title">Engagement Trend (Last 7 Days)</div>
            <div class="chart-placeholder">
                <div style="width: 100%; height: 220px; display: flex; align-items: flex-end; justify-content: space-around; padding: 20px; gap: 8px;">
                    ${(charts.engagement_trend || [5, 7, 6, 9, 8, 10, 12]).map((value, i) => `
                        <div style="flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px;">
                            <div style="width: 100%; height: ${value * 15}px; background: linear-gradient(180deg, #0066FF, #3B82F6); border-radius: 4px;"></div>
                            <span style="font-size: 11px; color: #6B7280;">Day ${i + 1}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
}

/**
 * Load and display top performing videos
 */
async function loadTopVideos() {
    try {
        const videos = await api.getVideos();
        const tableBody = document.getElementById('videoTableBody');

        if (!videos || videos.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align: center; padding: 40px; color: #9CA3AF;">
                        No videos found
                    </td>
                </tr>
            `;
            return;
        }

        // Sort by views and take top 10
        const topVideos = videos
            .sort((a, b) => (b.views || 0) - (a.views || 0))
            .slice(0, 10);

        tableBody.innerHTML = topVideos.map(video => {
            const engagement = video.likes && video.views
                ? ((video.likes / video.views) * 100).toFixed(1)
                : 0;

            const platformClass = video.platform ? `platform-${video.platform.toLowerCase()}` : 'platform-tiktok';
            const platformIcon = getPlatformIcon(video.platform || 'TikTok');

            return `
                <tr>
                    <td style="font-family: monospace; color: #6B7280;">#${video.id}</td>
                    <td>
                        <span class="platform-badge ${platformClass}">
                            <i class="${platformIcon}"></i>
                            ${video.platform || 'TikTok'}
                        </span>
                    </td>
                    <td>${video.account_id ? `Account #${video.account_id}` : 'N/A'}</td>
                    <td style="font-weight: 600;">${formatNumber(video.views || 0)}</td>
                    <td>${formatNumber(video.likes || 0)}</td>
                    <td>${formatNumber(video.comments || 0)}</td>
                    <td style="color: ${engagement > 5 ? '#059669' : '#D97706'}; font-weight: 700;">
                        ${engagement}%
                    </td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Failed to load videos:', error);
        document.getElementById('videoTableBody').innerHTML = `
            <tr>
                <td colspan="7" style="text-align: center; padding: 40px; color: #EF4444;">
                    Failed to load videos
                </td>
            </tr>
        `;
    }
}

/**
 * Export videos data to CSV
 */
async function exportVideos() {
    try {
        showLoader('Exporting data...');
        const videos = await api.getVideos();

        const csv = [
            ['Video ID', 'Platform', 'Account ID', 'Views', 'Likes', 'Comments', 'Engagement'],
            ...videos.map(v => {
                const engagement = v.likes && v.views
                    ? ((v.likes / v.views) * 100).toFixed(1)
                    : 0;
                return [
                    v.id,
                    v.platform || 'TikTok',
                    v.account_id || 'N/A',
                    v.views || 0,
                    v.likes || 0,
                    v.comments || 0,
                    engagement + '%'
                ];
            })
        ].map(row => row.join(',')).join('\n');

        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `videos_export_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        URL.revokeObjectURL(url);

        hideLoader();
        showNotification('Data exported successfully', 'success');
    } catch (error) {
        hideLoader();
        handleError(error, 'Exporting Data');
    }
}

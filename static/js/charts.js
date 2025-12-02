// Charts and interactive elements for Data Tracking Plan Dashboard

// Modern Color Palette
const COLORS = {
    primary: '#4F46E5', // Indigo 600
    success: '#10B981', // Emerald 500
    warning: '#F59E0B', // Amber 500
    danger: '#EF4444',  // Red 500
    info: '#0EA5E9',    // Sky 500
    secondary: '#64748B', // Slate 500
    purple: '#8B5CF6',  // Violet 500
    pink: '#EC4899',    // Pink 500
    slate: '#475569',   // Slate 600
    light: '#F3F4F6'    // Gray 100
};

// Common Chart Layout Options
const COMMON_LAYOUT = {
    font: { family: 'Inter, sans-serif', color: '#4B5563' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    showlegend: true,
    legend: { orientation: 'h', y: -0.2 },
    margin: { t: 40, b: 40, l: 40, r: 40 },
    hoverlabel: {
        bgcolor: '#FFFFFF',
        bordercolor: '#E5E7EB',
        font: { family: 'Inter, sans-serif', color: '#1F2937' }
    }
};

// Initialize charts when document is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    initializeInteractiveElements();
});

function initializeCharts() {
    createPlatformBreakdownCharts();
    createComparisonCharts();
    createAmplitudeCharts();
}

function createPlatformBreakdownCharts() {
    // Amplitude Events Status Chart
    const amplitudeStatusElement = document.getElementById('amplitude-status-chart');
    if (amplitudeStatusElement && window.amplitudeStatusData) {
        const data = [{
            values: Object.values(window.amplitudeStatusData),
            labels: Object.keys(window.amplitudeStatusData),
            type: 'pie',
            hole: 0.6, // Donut chart
            marker: {
                colors: [COLORS.success, COLORS.danger, COLORS.secondary]
            },
            textinfo: 'label+percent',
            hoverinfo: 'label+value+percent'
        }];
        
        const layout = {
            ...COMMON_LAYOUT,
            title: { text: 'Event Status', font: { size: 16, color: '#111827' } },
            height: 350,
            annotations: [{
                font: { size: 20, weight: 'bold' },
                showarrow: false,
                text: Object.values(window.amplitudeStatusData).reduce((a, b) => a + b, 0),
                x: 0.5,
                y: 0.5
            }]
        };
        
        Plotly.newPlot(amplitudeStatusElement, data, layout, {responsive: true, displayModeBar: false});
    }
    
    // Insider Parameter Types Chart
    const insiderTypesElement = document.getElementById('insider-types-chart');
    if (insiderTypesElement && window.insiderTypesData) {
        const data = [{
            values: Object.values(window.insiderTypesData),
            labels: Object.keys(window.insiderTypesData),
            type: 'pie',
            hole: 0.6,
            marker: {
                colors: [COLORS.primary, COLORS.success, COLORS.warning, COLORS.danger, COLORS.purple]
            },
            textinfo: 'percent',
            hoverinfo: 'label+value+percent'
        }];
        
        const layout = {
            ...COMMON_LAYOUT,
            title: { text: 'Parameter Types', font: { size: 16, color: '#111827' } },
            height: 350
        };
        
        Plotly.newPlot(insiderTypesElement, data, layout, {responsive: true, displayModeBar: false});
    }
    
    // GTM Tags Types Chart
    const gtmTagsElement = document.getElementById('gtm-tags-chart');
    if (gtmTagsElement && window.gtmTagsData) {
        const data = [{
            x: Object.keys(window.gtmTagsData),
            y: Object.values(window.gtmTagsData),
            type: 'bar',
            marker: {
                color: COLORS.warning,
                line: { color: 'transparent' }
            }
        }];
        
        const layout = {
            ...COMMON_LAYOUT,
            title: { text: 'GTM Tag Types', font: { size: 16, color: '#111827' } },
            height: 350,
            xaxis: { tickangle: -45, automargin: true },
            yaxis: { gridcolor: '#F3F4F6' }
        };
        
        Plotly.newPlot(gtmTagsElement, data, layout, {responsive: true, displayModeBar: false});
    }
}

function createComparisonCharts() {
    // Platform Comparison Chart
    const comparisonElement = document.getElementById('platform-comparison-chart');
    if (comparisonElement && window.platformComparisonData) {
        const platforms = window.platformComparisonData;
        
        const data = [{
            x: platforms.map(p => p.name),
            y: platforms.map(p => p.events),
            name: 'Events',
            type: 'bar',
            marker: { color: COLORS.primary, opacity: 0.9, cornerradius: 5 }
        }, {
            x: platforms.map(p => p.name),
            y: platforms.map(p => p.properties),
            name: 'Properties',
            type: 'bar',
            marker: { color: COLORS.success, opacity: 0.9 }
        }];
        
        const layout = {
            ...COMMON_LAYOUT,
            title: { text: 'Platform Comparison', font: { size: 16, color: '#111827' } },
            height: 400,
            barmode: 'group',
            bargap: 0.3,
            xaxis: { gridcolor: 'transparent' },
            yaxis: { gridcolor: '#F3F4F6' }
        };
        
        Plotly.newPlot(comparisonElement, data, layout, {responsive: true, displayModeBar: false});
    }
}

function createAmplitudeCharts() {
    // Amplitude Activity Status Chart
    const activityElement = document.getElementById('amplitude-activity-chart');
    if (activityElement && window.amplitudeActivityData) {
        const data = [{
            values: Object.values(window.amplitudeActivityData),
            labels: Object.keys(window.amplitudeActivityData),
            type: 'pie',
            hole: 0.6,
            marker: {
                colors: [COLORS.success, COLORS.danger, COLORS.secondary]
            },
            textinfo: 'percent',
            hoverinfo: 'label+value+percent'
        }];
        
        const layout = {
            ...COMMON_LAYOUT,
            title: { text: 'Event Activity Status', font: { size: 16, color: '#111827' } },
            height: 350
        };
        
        Plotly.newPlot(activityElement, data, layout, {responsive: true, displayModeBar: false});
    }
    
    // Amplitude Property Types Chart
    const typesElement = document.getElementById('amplitude-types-chart');
    if (typesElement && window.amplitudeTypesData) {
        const data = [{
            values: Object.values(window.amplitudeTypesData),
            labels: Object.keys(window.amplitudeTypesData),
            type: 'pie',
            hole: 0.6,
            marker: {
                colors: [COLORS.primary, COLORS.success, COLORS.warning, COLORS.danger, COLORS.purple, COLORS.info]
            },
            textinfo: 'percent',
            hoverinfo: 'label+value+percent'
        }];
        
        const layout = {
            ...COMMON_LAYOUT,
            title: { text: 'Property Value Types', font: { size: 16, color: '#111827' } },
            height: 350
        };
        
        Plotly.newPlot(typesElement, data, layout, {responsive: true, displayModeBar: false});
    }
    
    // Amplitude Schema Status Chart
    const schemaElement = document.getElementById('amplitude-schema-chart');
    if (schemaElement && window.amplitudeSchemaData) {
        const data = [{
            values: Object.values(window.amplitudeSchemaData),
            labels: Object.keys(window.amplitudeSchemaData),
            type: 'pie',
            hole: 0.6,
            marker: {
                colors: [COLORS.success, COLORS.warning, COLORS.danger]
            },
            textinfo: 'percent',
            hoverinfo: 'label+value+percent'
        }];
        
        const layout = {
            ...COMMON_LAYOUT,
            title: { text: 'Schema Status', font: { size: 16, color: '#111827' } },
            height: 350
        };
        
        Plotly.newPlot(schemaElement, data, layout, {responsive: true, displayModeBar: false});
    }
    
    // Amplitude Categories Chart
    const categoriesElement = document.getElementById('amplitude-categories-chart');
    if (categoriesElement && window.amplitudeCategoriesData) {
        // Sort data by value descending
        const entries = Object.entries(window.amplitudeCategoriesData);
        entries.sort((a, b) => b[1] - a[1]);
        const topEntries = entries.slice(0, 10); // Show top 10
        
        const data = [{
            x: topEntries.map(e => e[0] || 'Uncategorized'),
            y: topEntries.map(e => e[1]),
            type: 'bar',
            marker: {
                color: COLORS.primary,
                opacity: 0.8,
                line: { color: 'transparent' }
            }
        }];
        
        const layout = {
            ...COMMON_LAYOUT,
            title: { text: 'Top Categories', font: { size: 16, color: '#111827' } },
            height: 350,
            margin: { t: 40, b: 80, l: 40, r: 20 },
            xaxis: { tickangle: -45, automargin: true },
            yaxis: { gridcolor: '#F3F4F6' }
        };
        
        Plotly.newPlot(categoriesElement, data, layout, {responsive: true, displayModeBar: false});
    }
}

function initializeInteractiveElements() {
    initializeTooltips();
    initializeDataTables();
    initializeFilters();
}

function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeDataTables() {
    const tables = document.querySelectorAll('.data-table');
    tables.forEach(table => {
        addTableSearch(table);
        addTablePagination(table);
    });
}

function addTableSearch(table) {
    const searchInput = table.closest('.tab-pane')?.querySelector('.table-search') || 
                        table.parentElement.parentElement.querySelector('.table-search'); // Fallback
    
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        let visibleCount = 0;
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                row.style.display = '';
                row.classList.remove('d-none-filter');
                visibleCount++;
            } else {
                row.style.display = 'none';
                row.classList.add('d-none-filter');
            }
        });
        
        // If search is active, hide pagination to avoid confusion
        // or ideally, re-render it. For now, hiding it is safer.
        const pagination = table.parentElement.nextElementSibling;
        if (pagination && pagination.classList.contains('pagination-container')) {
            if (this.value.length > 0) {
                pagination.style.display = 'none';
            } else {
                pagination.style.display = '';
                // Reset to first page when clearing search
                // We need to trigger the click event on page 1
                const firstPageLink = pagination.querySelector('[data-page="1"]');
                if (firstPageLink) firstPageLink.click();
            }
        }
    });
}

function addTablePagination(table) {
    const rowsPerPage = 20;
    const rows = table.querySelectorAll('tbody tr');
    const totalPages = Math.ceil(rows.length / rowsPerPage);
    
    if (totalPages <= 1) return;
    
    // Check if pagination already exists to avoid duplicates
    if (table.parentElement.nextElementSibling?.classList.contains('pagination-container')) {
        return;
    }

    const paginationContainer = document.createElement('div');
    paginationContainer.className = 'pagination-container mt-4 d-flex flex-column align-items-center gap-2';
    
    // Info text
    const infoText = document.createElement('div');
    infoText.className = 'text-muted small';
    infoText.id = `pagination-info-${Math.random().toString(36).substr(2, 9)}`; // Unique ID
    paginationContainer.appendChild(infoText);

    const pagination = document.createElement('nav');
    // Start at page 1
    pagination.innerHTML = createPaginationHTML(1, totalPages);
    
    paginationContainer.appendChild(pagination);
    table.parentElement.after(paginationContainer); 
    
    // Initial update of info text
    updatePaginationInfo(infoText, 1, rowsPerPage, rows.length);
    
    showPage(table, 1, rowsPerPage);
    
    pagination.addEventListener('click', function(e) {
        e.preventDefault();
        const target = e.target.closest('.page-link');
        if (!target || target.parentElement.classList.contains('disabled')) return;
        
        const page = parseInt(target.dataset.page);
        
        if (page) {
            showPage(table, page, rowsPerPage);
            // Re-render pagination to update active state and sliding window
            pagination.innerHTML = createPaginationHTML(page, totalPages);
            updatePaginationInfo(infoText, page, rowsPerPage, rows.length);
        }
    });
}

function updatePaginationInfo(element, page, rowsPerPage, totalRows) {
    if (!element) return;
    const start = (page - 1) * rowsPerPage + 1;
    const end = Math.min(page * rowsPerPage, totalRows);
    element.textContent = `Showing ${start} to ${end} of ${totalRows} entries`;
}

function createPaginationHTML(currentPage, totalPages) {
    let html = '<ul class="pagination">';
    
    // Previous button
    const prevDisabled = currentPage === 1 ? ' disabled' : '';
    const prevPage = Math.max(1, currentPage - 1);
    html += `<li class="page-item${prevDisabled}">
                <a class="page-link" href="#" data-page="${prevPage}" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
             </li>`;
    
    // Smart pagination logic: [1] ... [current-1] [current] [current+1] ... [total]
    const range = [];
    const delta = 2; // Number of pages to show around current page
    
    for (let i = 1; i <= totalPages; i++) {
        if (
            i === 1 || // Always show first
            i === totalPages || // Always show last
            (i >= currentPage - delta && i <= currentPage + delta) // Show around current
        ) {
            range.push(i);
        }
    }
    
    let l;
    for (let i of range) {
        if (l) {
            if (i - l === 2) {
                // If gap is small, fill it
                range.push(l + 1);
            } else if (i - l !== 1) {
                // Add ellipsis
                html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
        }
        
        const activeClass = i === currentPage ? ' active' : '';
        html += `<li class="page-item${activeClass}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                 </li>`;
        l = i;
    }
    
    // Next button
    const nextDisabled = currentPage === totalPages ? ' disabled' : '';
    const nextPage = Math.min(totalPages, currentPage + 1);
    html += `<li class="page-item${nextDisabled}">
                <a class="page-link" href="#" data-page="${nextPage}" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
             </li>`;
    
    html += '</ul>';
    return html;
}

function showPage(table, page, rowsPerPage) {
    const rows = table.querySelectorAll('tbody tr');
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    
    rows.forEach((row, index) => {
        // Skip rows that are filtered out by search
        if (row.classList.contains('d-none-filter')) return;
        
        if (index >= start && index < end) {
             row.classList.remove('d-none');
        } else {
             row.classList.add('d-none');
        }
    });
}

function initializeFilters() {
    const filterDropdowns = document.querySelectorAll('.filter-dropdown');
    
    filterDropdowns.forEach(dropdown => {
        dropdown.addEventListener('change', function() {
            // Find the related table
            const tabPane = this.closest('.tab-pane');
            if (tabPane) {
                const table = tabPane.querySelector('table');
                if (table) {
                    applyFilters(table, tabPane);
                }
            }
        });
    });
}

function applyFilters(table, container) {
    const filters = {};
    container.querySelectorAll('.filter-dropdown').forEach(dropdown => {
        if (dropdown.value) {
            filters[dropdown.dataset.filter] = dropdown.value;
        }
    });
    
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        let shouldShow = true;
        
        Object.keys(filters).forEach(filterKey => {
            const cell = row.dataset[filterKey]; // Use dataset directly
            if (cell && cell !== filters[filterKey]) {
                shouldShow = false;
            }
        });
        
        if (shouldShow) {
            row.classList.remove('d-none-filter');
            row.style.display = ''; 
        } else {
            row.classList.add('d-none-filter');
            row.style.display = 'none';
        }
    });
    
    // Hide pagination when filtering is active (simple solution)
    const pagination = table.parentElement.nextElementSibling;
    if (pagination && pagination.classList.contains('pagination-container')) {
        const hasActiveFilter = Object.keys(filters).length > 0;
        pagination.style.display = hasActiveFilter ? 'none' : '';
        if (!hasActiveFilter) {
             // Reset to page 1
             const firstPageLink = pagination.querySelector('[data-page="1"]');
             if (firstPageLink) firstPageLink.click();
        }
    }
}

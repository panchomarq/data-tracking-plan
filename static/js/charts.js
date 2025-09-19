// Charts and interactive elements for Data Tracking Plan Dashboard

// Initialize charts when document is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    initializeInteractiveElements();
});

function initializeCharts() {
    // Create pie charts for platform breakdowns
    createPlatformBreakdownCharts();
    
    // Create comparison charts
    createComparisonCharts();
    
    // Create Amplitude-specific charts
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
            marker: {
                colors: ['#28a745', '#dc3545', '#6c757d']
            }
        }];
        
        const layout = {
            title: 'Event Status Distribution',
            height: 300,
            margin: { t: 40, b: 40, l: 40, r: 40 }
        };
        
        Plotly.newPlot(amplitudeStatusElement, data, layout, {responsive: true});
    }
    
    // Insider Parameter Types Chart
    const insiderTypesElement = document.getElementById('insider-types-chart');
    if (insiderTypesElement && window.insiderTypesData) {
        const data = [{
            values: Object.values(window.insiderTypesData),
            labels: Object.keys(window.insiderTypesData),
            type: 'pie',
            marker: {
                colors: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1']
            }
        }];
        
        const layout = {
            title: 'Parameter Types Distribution',
            height: 300,
            margin: { t: 40, b: 40, l: 40, r: 40 }
        };
        
        Plotly.newPlot(insiderTypesElement, data, layout, {responsive: true});
    }
    
    // GTM Tags Types Chart
    const gtmTagsElement = document.getElementById('gtm-tags-chart');
    if (gtmTagsElement && window.gtmTagsData) {
        const data = [{
            x: Object.keys(window.gtmTagsData),
            y: Object.values(window.gtmTagsData),
            type: 'bar',
            marker: {
                color: '#ffc107'
            }
        }];
        
        const layout = {
            title: 'GTM Tag Types',
            height: 300,
            margin: { t: 40, b: 60, l: 40, r: 40 },
            xaxis: {
                tickangle: -45
            }
        };
        
        Plotly.newPlot(gtmTagsElement, data, layout, {responsive: true});
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
            marker: { color: '#007bff' }
        }, {
            x: platforms.map(p => p.name),
            y: platforms.map(p => p.properties),
            name: 'Properties/Parameters',
            type: 'bar',
            marker: { color: '#28a745' }
        }];
        
        const layout = {
            title: 'Platform Comparison',
            height: 400,
            barmode: 'group',
            margin: { t: 40, b: 60, l: 40, r: 40 }
        };
        
        Plotly.newPlot(comparisonElement, data, layout, {responsive: true});
    }
}

function initializeInteractiveElements() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize data tables with search and pagination
    initializeDataTables();
    
    // Initialize filter functionality
    initializeFilters();
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeDataTables() {
    // Add search functionality to tables
    const tables = document.querySelectorAll('.data-table');
    
    tables.forEach(table => {
        addTableSearch(table);
        addTablePagination(table);
    });
}

function addTableSearch(table) {
    const searchInput = table.parentElement.querySelector('.table-search');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

function addTablePagination(table) {
    const rowsPerPage = 25;
    const rows = table.querySelectorAll('tbody tr');
    const totalPages = Math.ceil(rows.length / rowsPerPage);
    
    if (totalPages <= 1) return;
    
    // Create pagination controls
    const paginationContainer = document.createElement('div');
    paginationContainer.className = 'pagination-container mt-3';
    
    const pagination = document.createElement('nav');
    pagination.innerHTML = createPaginationHTML(totalPages);
    
    paginationContainer.appendChild(pagination);
    table.parentElement.appendChild(paginationContainer);
    
    // Show first page
    showPage(table, 1, rowsPerPage);
    
    // Add pagination event listeners
    pagination.addEventListener('click', function(e) {
        if (e.target.classList.contains('page-link')) {
            e.preventDefault();
            const page = parseInt(e.target.dataset.page);
            if (page) {
                showPage(table, page, rowsPerPage);
                updatePaginationActive(pagination, page);
            }
        }
    });
}

function createPaginationHTML(totalPages) {
    let html = '<ul class="pagination pagination-sm justify-content-center">';
    
    for (let i = 1; i <= totalPages; i++) {
        const activeClass = i === 1 ? ' active' : '';
        html += `<li class="page-item${activeClass}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                 </li>`;
    }
    
    html += '</ul>';
    return html;
}

function showPage(table, page, rowsPerPage) {
    const rows = table.querySelectorAll('tbody tr');
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    
    rows.forEach((row, index) => {
        row.style.display = (index >= start && index < end) ? '' : 'none';
    });
}

function updatePaginationActive(pagination, activePage) {
    pagination.querySelectorAll('.page-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const activeItem = pagination.querySelector(`[data-page="${activePage}"]`).parentElement;
    activeItem.classList.add('active');
}

function initializeFilters() {
    // Initialize filter dropdowns
    const filterDropdowns = document.querySelectorAll('.filter-dropdown');
    
    filterDropdowns.forEach(dropdown => {
        dropdown.addEventListener('change', function() {
            applyFilters();
        });
    });
}

function applyFilters() {
    // Apply filters to data tables
    const filters = {};
    document.querySelectorAll('.filter-dropdown').forEach(dropdown => {
        if (dropdown.value) {
            filters[dropdown.dataset.filter] = dropdown.value;
        }
    });
    
    // Apply filters to visible tables
    document.querySelectorAll('.data-table tbody tr').forEach(row => {
        let shouldShow = true;
        
        Object.keys(filters).forEach(filterKey => {
            const cell = row.querySelector(`[data-${filterKey}]`);
            if (cell && cell.dataset[filterKey] !== filters[filterKey]) {
                shouldShow = false;
            }
        });
        
        row.style.display = shouldShow ? '' : 'none';
    });
}

function createAmplitudeCharts() {
    // Amplitude Activity Status Chart
    const activityElement = document.getElementById('amplitude-activity-chart');
    if (activityElement && window.amplitudeActivityData) {
        const data = [{
            values: Object.values(window.amplitudeActivityData),
            labels: Object.keys(window.amplitudeActivityData),
            type: 'pie',
            marker: {
                colors: ['#28a745', '#dc3545', '#6c757d']
            }
        }];
        
        const layout = {
            title: 'Event Activity Status',
            height: 300,
            margin: { t: 40, b: 40, l: 40, r: 40 }
        };
        
        Plotly.newPlot(activityElement, data, layout, {responsive: true});
    }
    
    // Amplitude Property Types Chart
    const typesElement = document.getElementById('amplitude-types-chart');
    if (typesElement && window.amplitudeTypesData) {
        const data = [{
            values: Object.values(window.amplitudeTypesData),
            labels: Object.keys(window.amplitudeTypesData),
            type: 'pie',
            marker: {
                colors: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#fd7e14']
            }
        }];
        
        const layout = {
            title: 'Property Value Types',
            height: 300,
            margin: { t: 40, b: 40, l: 40, r: 40 }
        };
        
        Plotly.newPlot(typesElement, data, layout, {responsive: true});
    }
    
    // Amplitude Schema Status Chart
    const schemaElement = document.getElementById('amplitude-schema-chart');
    if (schemaElement && window.amplitudeSchemaData) {
        const data = [{
            values: Object.values(window.amplitudeSchemaData),
            labels: Object.keys(window.amplitudeSchemaData),
            type: 'pie',
            marker: {
                colors: ['#28a745', '#ffc107', '#dc3545']
            }
        }];
        
        const layout = {
            title: 'Schema Status Distribution',
            height: 300,
            margin: { t: 40, b: 40, l: 40, r: 40 }
        };
        
        Plotly.newPlot(schemaElement, data, layout, {responsive: true});
    }
    
    // Amplitude Categories Chart
    const categoriesElement = document.getElementById('amplitude-categories-chart');
    if (categoriesElement && window.amplitudeCategoriesData) {
        const data = [{
            x: Object.keys(window.amplitudeCategoriesData),
            y: Object.values(window.amplitudeCategoriesData),
            type: 'bar',
            marker: {
                color: '#007bff'
            }
        }];
        
        const layout = {
            title: 'Events by Category',
            height: 300,
            margin: { t: 40, b: 80, l: 40, r: 40 },
            xaxis: {
                tickangle: -45,
                title: 'Categories'
            },
            yaxis: {
                title: 'Number of Events'
            }
        };
        
        Plotly.newPlot(categoriesElement, data, layout, {responsive: true});
    }
}

// Utility functions
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function createProgressBar(current, total, className = '') {
    const percentage = total > 0 ? (current / total) * 100 : 0;
    return `
        <div class="progress ${className}" style="height: 8px;">
            <div class="progress-bar" role="progressbar" 
                 style="width: ${percentage}%" 
                 aria-valuenow="${current}" 
                 aria-valuemin="0" 
                 aria-valuemax="${total}">
            </div>
        </div>
        <small class="text-muted">${current} / ${total} (${percentage.toFixed(1)}%)</small>
    `;
}

// Export functions for use in templates
window.ChartUtils = {
    formatNumber,
    createProgressBar
}; 
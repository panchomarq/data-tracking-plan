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
}

function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ---------------------------------------------------------------------------
// DataTableController — unified search + filter + pagination
//
// Replaces the old addTableSearch / applyFilters / showPage functions with a
// single render pipeline:  filter -> search -> paginate visible rows.
// ---------------------------------------------------------------------------

class DataTableController {
    constructor(element) {
        this.element = element;
        this.table = element.tagName === 'TABLE'
            ? element
            : element.querySelector('table');
        if (!this.table) return;

        this.allRows = Array.from(this.table.querySelectorAll('tbody tr'));
        this.rowsPerPage = 20;
        this.currentPage = 1;
        this.searchTerm = '';
        this.activeFilters = {};

        this._findContainer();
        this._bindSearch();
        this._bindFilters();
        this._buildPagination();
        this.render();
    }

    // -- DOM discovery -------------------------------------------------------

    _findContainer() {
        this.container = this.element.closest('.tab-pane')
            || this.element.closest('.card')
            || this.element.parentElement;
    }

    _bindSearch() {
        const input = this.container.querySelector('.table-search');
        if (!input) return;
        this.searchInput = input;
        this._debounceTimer = null;

        input.addEventListener('input', () => {
            clearTimeout(this._debounceTimer);
            this._debounceTimer = setTimeout(() => {
                this.searchTerm = input.value.toLowerCase().trim();
                this.currentPage = 1;
                this.render();
            }, 150);
        });
    }

    _bindFilters() {
        const dropdowns = this.container.querySelectorAll('.filter-dropdown');
        dropdowns.forEach(dd => {
            dd.addEventListener('change', () => {
                this.activeFilters = {};
                this.container.querySelectorAll('.filter-dropdown').forEach(d => {
                    if (d.value) this.activeFilters[d.dataset.filter] = d.value;
                });
                this.currentPage = 1;
                this.render();
            });
        });
    }

    // -- Pagination scaffold -------------------------------------------------

    _buildPagination() {
        this.paginationContainer = document.createElement('div');
        this.paginationContainer.className =
            'pagination-container mt-4 d-flex flex-column align-items-center gap-2';

        this.infoText = document.createElement('div');
        this.infoText.className = 'text-muted small';
        this.paginationContainer.appendChild(this.infoText);

        this.paginationNav = document.createElement('nav');
        this.paginationContainer.appendChild(this.paginationNav);

        const insertAfter = this.element.tagName === 'TABLE'
            ? this.element.parentElement
            : this.element;
        insertAfter.after(this.paginationContainer);

        this.paginationNav.addEventListener('click', (e) => {
            e.preventDefault();
            const link = e.target.closest('.page-link');
            if (!link || link.parentElement.classList.contains('disabled')) return;
            const page = parseInt(link.dataset.page);
            if (page) {
                this.currentPage = page;
                this.render();
            }
        });
    }

    // -- Core render pipeline ------------------------------------------------

    render() {
        const visible = this._applyFiltersAndSearch();
        this._paginate(visible);
        this._updatePaginationUI(visible.length);
        this._updateResultsBadge(visible.length);
        this._showEmptyState(visible.length === 0);
    }

    _applyFiltersAndSearch() {
        const visible = [];
        const filterKeys = Object.keys(this.activeFilters);
        const hasSearch = this.searchTerm.length > 0;

        this.allRows.forEach(row => {
            let passesFilter = true;
            for (const key of filterKeys) {
                if (row.dataset[key] && row.dataset[key] !== this.activeFilters[key]) {
                    passesFilter = false;
                    break;
                }
            }

            let passesSearch = true;
            if (hasSearch && passesFilter) {
                passesSearch = row.textContent.toLowerCase().includes(this.searchTerm);
            }

            if (passesFilter && passesSearch) {
                visible.push(row);
            }
        });

        return visible;
    }

    _paginate(visibleRows) {
        const start = (this.currentPage - 1) * this.rowsPerPage;
        const end = start + this.rowsPerPage;
        const visibleSet = new Set(visibleRows.slice(start, end));

        this.allRows.forEach(row => {
            row.classList.toggle('d-none', !visibleSet.has(row));
            row.style.display = '';
        });
    }

    _updatePaginationUI(totalVisible) {
        const totalPages = Math.max(1, Math.ceil(totalVisible / this.rowsPerPage));
        if (this.currentPage > totalPages) this.currentPage = totalPages;

        if (totalPages <= 1) {
            this.paginationContainer.style.display = 'none';
            return;
        }

        this.paginationContainer.style.display = '';
        this.paginationNav.innerHTML = createPaginationHTML(this.currentPage, totalPages);

        const start = (this.currentPage - 1) * this.rowsPerPage + 1;
        const end = Math.min(this.currentPage * this.rowsPerPage, totalVisible);
        this.infoText.textContent = `Showing ${start} to ${end} of ${totalVisible} results`;
    }

    _updateResultsBadge(totalVisible) {
        if (!this.searchInput) return;
        const isFiltering = this.searchTerm.length > 0
            || Object.keys(this.activeFilters).length > 0;

        let badge = this.searchInput.parentElement.querySelector('.dt-results-badge');
        if (!isFiltering) {
            if (badge) badge.remove();
            return;
        }

        if (!badge) {
            badge = document.createElement('span');
            badge.className = 'dt-results-badge badge bg-primary-custom rounded-pill ms-2';
            badge.style.cssText = 'font-size:.7rem;vertical-align:middle;';
            this.searchInput.parentElement.appendChild(badge);
        }
        badge.textContent = `${totalVisible} found`;
    }

    _showEmptyState(isEmpty) {
        let emptyRow = this.table.querySelector('.dt-empty-row');
        if (!isEmpty) {
            if (emptyRow) emptyRow.remove();
            return;
        }

        if (!emptyRow) {
            const cols = this.table.querySelectorAll('thead th').length || 1;
            emptyRow = document.createElement('tr');
            emptyRow.className = 'dt-empty-row';
            emptyRow.innerHTML = `<td colspan="${cols}" class="text-center text-muted py-5">
                <i class="fas fa-search me-2"></i>No results found</td>`;
            this.table.querySelector('tbody').appendChild(emptyRow);
        }
    }
}

// -- Shared pagination HTML builder (unchanged) ------------------------------

function createPaginationHTML(currentPage, totalPages) {
    let html = '<ul class="pagination">';

    const prevDisabled = currentPage === 1 ? ' disabled' : '';
    const prevPage = Math.max(1, currentPage - 1);
    html += `<li class="page-item${prevDisabled}">
                <a class="page-link" href="#" data-page="${prevPage}" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
             </li>`;

    const range = [];
    const delta = 2;
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - delta && i <= currentPage + delta)) {
            range.push(i);
        }
    }

    let l;
    for (let i of range) {
        if (l) {
            if (i - l === 2) {
                range.push(l + 1);
            } else if (i - l !== 1) {
                html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            }
        }
        const activeClass = i === currentPage ? ' active' : '';
        html += `<li class="page-item${activeClass}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                 </li>`;
        l = i;
    }

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

// -- Bootstrap wiring --------------------------------------------------------

function initializeDataTables() {
    document.querySelectorAll('.data-table').forEach(el => {
        el._dtController = new DataTableController(el);
    });
}

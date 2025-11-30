// API Helper Functions
const API = {
    async fetchJSON(endpoint) {
        try {
            const response = await fetch(endpoint);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`Error fetching ${endpoint}:`, error);
            throw error;
        }
    },
    
    async fetchHTML(endpoint) {
        try {
            const response = await fetch(endpoint);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.text();
        } catch (error) {
            console.error(`Error fetching ${endpoint}:`, error);
            throw error;
        }
    }
};

// Format currency
function formatCurrency(value) {
    return '$' + value.toLocaleString('en-US', { maximumFractionDigits: 0 });
}

// Format percentage
function formatPercent(value) {
    return value.toFixed(1) + '%';
}

// Load visualization into container
async function loadVisualization(endpoint, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = '<p class="loading">Loading visualization</p>';
    
    try {
        const html = await API.fetchHTML(endpoint);
        container.innerHTML = html;
    } catch (error) {
        container.innerHTML = '<p class="loading">Failed to load visualization</p>';
    }
}

// Create table from data
function createTable(data, columns, headerColor = '#667eea') {
    let table = `<table style="width: 100%; border-collapse: collapse;">`;
    table += `<thead><tr style="background: ${headerColor}; color: white;">`;
    
    columns.forEach(col => {
        table += `<th style="padding: 1rem; text-align: ${col.align || 'left'};">${col.label}</th>`;
    });
    
    table += '</tr></thead><tbody>';
    
    data.forEach((row, i) => {
        const bgColor = i % 2 === 0 ? '#f9f9f9' : 'white';
        table += `<tr style="background: ${bgColor};">`;
        
        columns.forEach(col => {
            let value = row[col.key];
            
            if (col.format === 'currency') {
                value = formatCurrency(value);
            } else if (col.format === 'percent') {
                const color = value >= 0 ? 'green' : 'red';
                value = `<span style="color: ${color}; font-weight: bold;">${formatPercent(value)}</span>`;
            }
            
            table += `<td style="padding: 1rem; text-align: ${col.align || 'left'};">${value}</td>`;
        });
        
        table += '</tr>';
    });
    
    table += '</tbody></table>';
    return table;
}

// Export for use in HTML pages
window.API = API;
window.formatCurrency = formatCurrency;
window.formatPercent = formatPercent;
window.loadVisualization = loadVisualization;
window.createTable = createTable;

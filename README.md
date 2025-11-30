# Global Electronics Sales & Marketing Impact

CSCE 5320 Scientific Data Visualization - Project 2

## Overview
Interactive web application analyzing the relationship between marketing campaigns and sales performance for a global electronics retailer. Identifies which campaigns drive the highest ROI across different countries and product categories.

## Features

### 📊 Interactive Dashboards
- **Main Dashboard**: High-level summary with key metrics and regional overview
- **ROI Deep Dive**: Geographic analysis with choropleth maps and scatter plots
- **Product Performance**: Category-level analysis with insights and recommendations

### 📈 Visualizations
- Plotly choropleth map (ROI by country)
- Scatter plots (Marketing Spend vs Revenue)
- Bar charts (Campaign types and categories)
- Altair regional comparison charts

### 🔌 API Endpoints
- `/api/summary` - Overall statistics
- `/api/roi/region` - ROI by country
- `/api/roi/campaign-type` - ROI by campaign type
- `/api/roi/category` - ROI by product category
- `/api/roi/campaigns` - Detailed campaign data

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open browser to:
```
http://localhost:5000
```

## Project Structure
```
.
├── app.py                  # Flask application
├── data_processor.py       # Data merging and ROI calculations
├── visualizations.py       # Plotly and Altair visualizations
├── data-1.csv             # Sales dataset
├── data-2.csv             # Marketing campaign dataset
├── requirements.txt       # Python dependencies
├── static/
│   ├── style.css          # Global styles
│   └── app.js             # Frontend utilities
└── templates/
    ├── index.html         # Main dashboard
    ├── roi_analysis.html  # ROI deep dive page
    └── product_performance.html  # Product analysis page
```

## Datasets

### Sales Dataset (data-1.csv)
- 750 records from 2021-2025
- Countries: USA, Canada, Mexico, Germany, UK
- Categories: Smartphones, Laptops, Gaming Consoles, Audio Devices, Televisions

### Marketing Campaign Dataset (data-2.csv)
- 60 campaigns from 2021-2025
- Campaign Types: Social Media, Digital Ads, Print
- Marketing spend: $7,000 - $26,000 per campaign

## Key Insights
- Only 80 sales matched active campaigns (realistic scenario)
- Print campaigns show best ROI (-62%)
- Televisions category performs best (-61%)
- Negative ROI indicates most sales occur organically

## Technologies
- **Backend**: Python, Flask, Pandas
- **Visualizations**: Plotly, Altair
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: NumPy, Pandas

## Author
CSCE 5320 - Scientific Data Visualization Project

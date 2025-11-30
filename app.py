from flask import Flask, jsonify, render_template
from data_processor import DataProcessor
from visualizations import Visualizations

app = Flask(__name__)

# Initialize data processor and visualizations
processor = DataProcessor()
processor.load_data().merge_datasets()
viz = Visualizations(processor)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "success": True})

@app.route('/api/summary')
def get_summary():
    """Get overall summary statistics"""
    try:
        summary = processor.get_summary_stats()
        return jsonify(summary)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/roi/region')
def get_roi_by_region():
    """Get ROI by region"""
    try:
        data = processor.get_roi_by_region()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/roi/campaign-type')
def get_roi_by_campaign_type():
    """Get ROI by campaign type"""
    try:
        data = processor.get_roi_by_campaign_type()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/roi/category')
def get_roi_by_category():
    """Get ROI by product category"""
    try:
        data = processor.get_roi_by_category()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/roi/campaigns')
def get_campaign_roi():
    """Get detailed ROI for all campaigns"""
    try:
        data = processor.calculate_roi()
        return jsonify(data.to_dict('records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/test')
def test():
    """Test page for debugging"""
    return render_template('test.html')

@app.route('/roi-analysis')
def roi_analysis():
    """ROI deep dive page"""
    return render_template('roi_analysis.html')

@app.route('/product-performance')
def product_performance():
    """Product performance page"""
    return render_template('product_performance.html')

@app.route('/api/viz/choropleth')
def get_choropleth():
    """Get choropleth map HTML"""
    return viz.create_roi_choropleth()

@app.route('/api/viz/scatter')
def get_scatter():
    """Get scatter plot HTML"""
    return viz.create_spend_vs_revenue_scatter()

@app.route('/api/viz/campaign-bar')
def get_campaign_bar():
    """Get campaign type bar chart HTML"""
    return viz.create_campaign_type_bar()

@app.route('/api/viz/category-bar')
def get_category_bar():
    """Get category performance bar chart HTML"""
    return viz.create_category_performance()

@app.route('/api/viz/region-altair')
def get_region_altair():
    """Get Altair region chart HTML"""
    return viz.create_altair_region_chart()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

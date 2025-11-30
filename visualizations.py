import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd
from data_processor import DataProcessor

class Visualizations:
    def __init__(self, processor):
        self.processor = processor
    
    def create_roi_choropleth(self):
        """Create choropleth map showing ROI by country"""
        roi_data = self.processor.get_roi_by_region()
        df = pd.DataFrame(roi_data)
        
        # Map country names to ISO codes
        country_codes = {
            'USA': 'USA',
            'Canada': 'CAN',
            'Mexico': 'MEX',
            'Germany': 'DEU',
            'UK': 'GBR'
        }
        df['iso_alpha'] = df['Country'].map(country_codes)
        
        fig = px.choropleth(
            df,
            locations='iso_alpha',
            color='ROI',
            hover_name='Country',
            hover_data={'Revenue': ':,.2f', 'Marketing_Spend': ':,.2f', 'ROI': ':.2f%', 'iso_alpha': False},
            color_continuous_scale='RdYlGn',
            title='Marketing ROI by Region'
        )
        
        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth'
            ),
            height=500
        )
        
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def create_spend_vs_revenue_scatter(self):
        """Create scatter plot of marketing spend vs revenue"""
        campaign_roi = self.processor.calculate_roi()
        
        # Use absolute ROI for size (can't have negative sizes)
        campaign_roi['ROI_abs'] = campaign_roi['ROI'].abs()
        
        fig = px.scatter(
            campaign_roi,
            x='Marketing_Spend',
            y='Revenue',
            color='Campaign_Type',
            size='ROI_abs',
            hover_data=['Country', 'ProductCategory', 'ROI'],
            title='Marketing Spend vs Revenue by Campaign Type',
            labels={'Marketing_Spend': 'Marketing Spend ($)', 'Revenue': 'Revenue ($)'}
        )
        
        # Add diagonal line for break-even
        max_val = max(campaign_roi['Marketing_Spend'].max(), campaign_roi['Revenue'].max())
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            name='Break-even',
            line=dict(dash='dash', color='gray')
        ))
        
        fig.update_layout(height=500)
        
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def create_campaign_type_bar(self):
        """Create interactive bar chart comparing campaign types with profit"""
        roi_data = self.processor.get_roi_by_campaign_type()
        df = pd.DataFrame(roi_data)
        
        # Calculate profit
        df['Profit'] = df['Revenue'] - df['Marketing_Spend']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df['Campaign_Type'],
            y=df['Revenue'],
            name='Revenue',
            marker_color='#4CAF50',
            text=df['Revenue'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=df['Campaign_Type'],
            y=df['Marketing_Spend'],
            name='Marketing Spend',
            marker_color='#FF6B6B',
            text=df['Marketing_Spend'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Marketing Spend: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            x=df['Campaign_Type'],
            y=df['Profit'],
            name='Profit',
            marker_color='#2196F3',
            text=df['Profit'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Campaign Performance: Revenue, Spend & Profit (Click legend to filter)',
            xaxis_title='Campaign Type',
            yaxis_title='Amount ($)',
            barmode='group',
            height=450,
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            hovermode='x unified'
        )
        
        # Enable click-on-legend to show/hide traces
        fig.update_layout(legend=dict(itemclick='toggle', itemdoubleclick='toggleothers'))
        
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def create_category_performance(self):
        """Create interactive grouped bar chart showing Revenue, Spend & Profit by category"""
        roi_data = self.processor.get_roi_by_category()
        df = pd.DataFrame(roi_data).sort_values('ROI', ascending=False)
        
        # Calculate profit
        df['Profit'] = df['Revenue'] - df['Marketing_Spend']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df['ProductCategory'],
            x=df['Revenue'],
            name='Revenue',
            orientation='h',
            marker_color='#4CAF50',
            text=df['Revenue'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            y=df['ProductCategory'],
            x=df['Marketing_Spend'],
            name='Marketing Spend',
            orientation='h',
            marker_color='#FF6B6B',
            text=df['Marketing_Spend'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Marketing Spend: $%{x:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            y=df['ProductCategory'],
            x=df['Profit'],
            name='Profit',
            orientation='h',
            marker_color='#2196F3',
            text=df['Profit'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Product Category Performance: Revenue, Spend & Profit (Click legend to filter)',
            xaxis_title='Amount ($)',
            yaxis_title='Product Category',
            barmode='group',
            height=450,
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            hovermode='y unified'
        )
        
        # Enable click-on-legend to show/hide traces
        fig.update_layout(legend=dict(itemclick='toggle', itemdoubleclick='toggleothers'))
        
        return fig.to_html(full_html=False, include_plotlyjs=False)
    
    def create_roi_summary_cards(self):
        """Generate summary statistics for dashboard cards"""
        summary = self.processor.get_summary_stats()
        
        return {
            'total_revenue': f"${summary['total_revenue']:,.0f}",
            'total_spend': f"${summary['total_marketing_spend']:,.0f}",
            'overall_roi': f"{summary['overall_roi']:.1f}%",
            'best_campaign': summary['best_campaign_type'],
            'best_campaign_roi': f"{summary['best_campaign_roi']:.1f}%"
        }
    
    def create_altair_region_chart(self):
        """Create simple Altair chart showing ROI by region"""
        roi_data = self.processor.get_roi_by_region()
        df = pd.DataFrame(roi_data)
        
        chart = alt.Chart(df).mark_bar(
            color='#2196F3'
        ).encode(
            x=alt.X('Country:N', title='Country', sort='-y'),
            y=alt.Y('ROI:Q', title='ROI (%)'),
            tooltip=[
                alt.Tooltip('Country:N', title='Country'),
                alt.Tooltip('Revenue:Q', title='Revenue', format='$,.0f'),
                alt.Tooltip('Marketing_Spend:Q', title='Marketing Spend', format='$,.0f'),
                alt.Tooltip('ROI:Q', title='ROI (%)', format='.1f')
            ]
        ).properties(
            title='ROI Comparison by Region',
            width=600,
            height=300
        )
        
        return chart.to_html()

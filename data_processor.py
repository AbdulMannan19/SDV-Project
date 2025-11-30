import pandas as pd
from datetime import datetime

class DataProcessor:
    def __init__(self):
        self.sales_df = None
        self.marketing_df = None
        self.merged_df = None
        
    def load_data(self):
        """Load sales and marketing datasets"""
        self.sales_df = pd.read_csv('data-1.csv')
        self.marketing_df = pd.read_csv('data-2.csv')
        
        # Convert date columns
        self.sales_df['OrderDate'] = pd.to_datetime(self.sales_df['OrderDate'])
        self.marketing_df['Start_Date'] = pd.to_datetime(self.marketing_df['Start_Date'])
        self.marketing_df['End_Date'] = pd.to_datetime(self.marketing_df['End_Date'])
        
        return self
    
    def merge_datasets(self):
        """Merge sales with marketing campaigns based on region, category, and date range"""
        merged_data = []
        
        for _, sale in self.sales_df.iterrows():
            # Find matching campaigns
            matching_campaigns = self.marketing_df[
                (self.marketing_df['Target_Region'] == sale['Country']) &
                (self.marketing_df['Target_Product_Category'] == sale['ProductCategory']) &
                (self.marketing_df['Start_Date'] <= sale['OrderDate']) &
                (self.marketing_df['End_Date'] >= sale['OrderDate'])
            ]
            
            if not matching_campaigns.empty:
                for _, campaign in matching_campaigns.iterrows():
                    merged_data.append({
                        'OrderID': sale['OrderID'],
                        'OrderDate': sale['OrderDate'],
                        'Country': sale['Country'],
                        'ProductCategory': sale['ProductCategory'],
                        'Revenue': sale['Revenue'],
                        'Campaign_ID': campaign['Campaign_ID'],
                        'Campaign_Type': campaign['Campaign_Type'],
                        'Marketing_Spend': campaign['Marketing_Spend']
                    })
        
        self.merged_df = pd.DataFrame(merged_data)
        return self
    
    def calculate_roi(self):
        """Calculate ROI metrics"""
        if self.merged_df is None:
            raise ValueError("Must merge datasets first")
        
        # Group by campaign
        campaign_roi = self.merged_df.groupby('Campaign_ID').agg({
            'Revenue': 'sum',
            'Marketing_Spend': 'first',
            'Campaign_Type': 'first',
            'Country': 'first',
            'ProductCategory': 'first'
        }).reset_index()
        
        campaign_roi['ROI'] = ((campaign_roi['Revenue'] - campaign_roi['Marketing_Spend']) / 
                               campaign_roi['Marketing_Spend'] * 100)
        
        return campaign_roi
    
    def get_roi_by_region(self):
        """Get ROI aggregated by region"""
        roi_data = self.merged_df.groupby('Country').agg({
            'Revenue': 'sum',
            'Marketing_Spend': 'sum'
        }).reset_index()
        
        roi_data['ROI'] = ((roi_data['Revenue'] - roi_data['Marketing_Spend']) / 
                           roi_data['Marketing_Spend'] * 100)
        
        return roi_data.to_dict('records')
    
    def get_roi_by_campaign_type(self):
        """Get ROI by campaign type"""
        roi_data = self.merged_df.groupby('Campaign_Type').agg({
            'Revenue': 'sum',
            'Marketing_Spend': 'sum'
        }).reset_index()
        
        roi_data['ROI'] = ((roi_data['Revenue'] - roi_data['Marketing_Spend']) / 
                           roi_data['Marketing_Spend'] * 100)
        
        return roi_data.to_dict('records')
    
    def get_roi_by_category(self):
        """Get ROI by product category"""
        roi_data = self.merged_df.groupby('ProductCategory').agg({
            'Revenue': 'sum',
            'Marketing_Spend': 'sum'
        }).reset_index()
        
        roi_data['ROI'] = ((roi_data['Revenue'] - roi_data['Marketing_Spend']) / 
                           roi_data['Marketing_Spend'] * 100)
        
        return roi_data.to_dict('records')
    
    def get_summary_stats(self):
        """Get overall summary statistics"""
        total_revenue = self.merged_df['Revenue'].sum()
        total_spend = self.merged_df['Marketing_Spend'].sum()
        overall_roi = ((total_revenue - total_spend) / total_spend * 100)
        
        # Best performing campaign type
        campaign_roi = self.get_roi_by_campaign_type()
        best_campaign = max(campaign_roi, key=lambda x: x['ROI'])
        
        # Top regions
        region_revenue = self.sales_df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
        
        return {
            'total_revenue': float(total_revenue),
            'total_marketing_spend': float(total_spend),
            'overall_roi': float(overall_roi),
            'best_campaign_type': best_campaign['Campaign_Type'],
            'best_campaign_roi': float(best_campaign['ROI']),
            'top_regions': region_revenue.head(3).to_dict()
        }

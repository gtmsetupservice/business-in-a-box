#!/usr/bin/env python3
"""
GTM Cleanup & Management Niche Analyzer
Analyzes keyword data for GTM cleanup/management services based on Reddit pain points
"""

import requests
import base64
import json
import csv
from datetime import datetime

class GTMCleanupNicheAnalyzer:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.credentials = base64.b64encode(f"{login}:{password}".encode()).decode()
        self.location_code = 2840  # United States
        
        # Keywords based on Reddit pain points
        self.gtm_cleanup_keywords = [
            "GTM audit",
            "Google Tag Manager audit",
            "GTM cleanup",
            "Google Tag Manager cleanup", 
            "GTM consultant",
            "Google Tag Manager consultant",
            "GTM fix",
            "Google Tag Manager fix",
            "GTM setup",
            "Google Tag Manager setup",
            "tag manager cleanup",
            "tag manager audit",
            "broken GTM fix",
            "GTM container cleanup",
            "duplicate tracking fix",
            "GTM performance optimization",
            "cross domain tracking setup",
            "GTM troubleshooting",
            "tag manager troubleshooting",
            "analytics tracking fix"
        ]
    
    def analyze_keywords(self):
        """Get keyword data from DataForSEO API"""
        url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
        
        headers = {
            'Authorization': f'Basic {self.credentials}',
            'Content-Type': 'application/json'
        }
        
        payload = json.dumps([{
            "search_partners": False,
            "keywords": self.gtm_cleanup_keywords,
            "location_code": self.location_code,
            "language_code": "en",
            "sort_by": "search_volume",
            "include_adult_keywords": False
        }])
        
        print(f"Analyzing {len(self.gtm_cleanup_keywords)} GTM cleanup keywords...")
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            return None
        
        result_json = response.json()
        
        if 'tasks' not in result_json or not result_json['tasks'] or 'result' not in result_json['tasks'][0]:
            print("No keyword data found.")
            return None
        
        return result_json['tasks'][0]['result']
    
    def calculate_cpa_metrics(self, keyword_data):
        """Calculate CPA and other metrics for GTM cleanup services"""
        if not keyword_data:
            return None
        
        # B2B service conversion rate - higher for specialized technical services
        conversion_rate = 0.035  # 3.5% for technical B2B services
        
        # Service pricing for GTM cleanup (conservative estimates)
        avg_project_value = 2500  # Average cleanup project
        
        metrics = []
        total_volume = 0
        keywords_with_volume = 0
        total_weighted_cpc = 0
        
        for kw in keyword_data:
            keyword = kw.get('keyword', '')
            search_volume = kw.get('search_volume', 0) or 0
            cpc = kw.get('cpc', 0) or 0
            competition_index = kw.get('competition_index', 0) or 0
            
            if search_volume > 0:
                keywords_with_volume += 1
                total_weighted_cpc += cpc * search_volume
            
            # CTR estimates for technical B2B searches
            if competition_index < 30:
                estimated_ctr = 0.40  # Higher CTR for specific technical searches
            elif competition_index < 60:
                estimated_ctr = 0.25
            else:
                estimated_ctr = 0.15
            
            estimated_clicks = search_volume * estimated_ctr
            estimated_conversions = estimated_clicks * conversion_rate
            
            # Calculate monthly spend and CPA
            if estimated_conversions > 0 and cpc > 0:
                monthly_spend = estimated_clicks * cpc
                cpa = monthly_spend / estimated_conversions
                
                # Calculate potential revenue
                monthly_revenue = estimated_conversions * avg_project_value
                roi = ((monthly_revenue - monthly_spend) / monthly_spend * 100) if monthly_spend > 0 else 0
            else:
                monthly_spend = 0
                cpa = 0
                monthly_revenue = 0
                roi = 0
            
            metrics.append({
                'keyword': keyword,
                'search_volume': search_volume,
                'cpc': cpc,
                'competition': kw.get('competition', 'N/A'),
                'competition_index': competition_index,
                'estimated_clicks': round(estimated_clicks, 2),
                'estimated_conversions': round(estimated_conversions, 3),
                'monthly_spend': round(monthly_spend, 2),
                'cpa': round(cpa, 2) if cpa > 0 else 0,
                'monthly_revenue': round(monthly_revenue, 2),
                'roi': round(roi, 1)
            })
            
            total_volume += search_volume
        
        avg_cpc = total_weighted_cpc / total_volume if total_volume > 0 else 0
        
        # Calculate overall metrics
        total_monthly_spend = sum(m['monthly_spend'] for m in metrics)
        total_monthly_conversions = sum(m['estimated_conversions'] for m in metrics)
        total_monthly_revenue = sum(m['monthly_revenue'] for m in metrics)
        
        overall_cpa = total_monthly_spend / total_monthly_conversions if total_monthly_conversions > 0 else 0
        overall_roi = ((total_monthly_revenue - total_monthly_spend) / total_monthly_spend * 100) if total_monthly_spend > 0 else 0
        
        return {
            'keywords': metrics,
            'total_search_volume': total_volume,
            'keywords_with_volume': keywords_with_volume,
            'average_cpc': round(avg_cpc, 2),
            'overall_cpa': round(overall_cpa, 2),
            'total_monthly_spend': round(total_monthly_spend, 2),
            'total_monthly_conversions': round(total_monthly_conversions, 2),
            'total_monthly_revenue': round(total_monthly_revenue, 2),
            'overall_roi': round(overall_roi, 1)
        }
    
    def save_results(self, metrics_data):
        """Save results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save CSV
        csv_filename = f"reports/gtm_cleanup_keywords_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['keyword', 'search_volume', 'cpc', 'competition', 'competition_index', 
                         'estimated_clicks', 'estimated_conversions', 'monthly_spend', 'cpa', 'monthly_revenue', 'roi']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for kw in sorted(metrics_data['keywords'], key=lambda x: x['search_volume'], reverse=True):
                writer.writerow(kw)
        
        # Save text report
        txt_filename = f"reports/gtm_cleanup_analysis_{timestamp}.txt"
        with open(txt_filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("GTM CLEANUP & MANAGEMENT NICHE ANALYSIS\n")
            f.write("="*80 + "\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("MARKET OVERVIEW\n")
            f.write("-"*40 + "\n")
            f.write(f"Total Search Volume: {metrics_data['total_search_volume']:,} monthly searches\n")
            f.write(f"Keywords with Volume: {metrics_data['keywords_with_volume']}/{len(self.gtm_cleanup_keywords)}\n")
            f.write(f"Average CPC: ${metrics_data['average_cpc']}\n")
            f.write(f"Overall CPA: ${metrics_data['overall_cpa']}\n")
            f.write(f"Overall ROI: {metrics_data['overall_roi']}%\n\n")
            
            f.write("FINANCIAL PROJECTIONS\n")
            f.write("-"*40 + "\n")
            f.write(f"Monthly Ad Spend Required: ${metrics_data['total_monthly_spend']:,}\n")
            f.write(f"Expected Monthly Conversions: {metrics_data['total_monthly_conversions']}\n")
            f.write(f"Projected Monthly Revenue: ${metrics_data['total_monthly_revenue']:,}\n\n")
            
            # Top keywords by search volume
            f.write("TOP KEYWORDS BY SEARCH VOLUME\n")
            f.write("-"*40 + "\n")
            top_keywords = sorted([k for k in metrics_data['keywords'] if k['search_volume'] > 0], 
                                key=lambda x: x['search_volume'], reverse=True)
            
            for i, kw in enumerate(top_keywords, 1):
                f.write(f"{i}. {kw['keyword']}\n")
                f.write(f"   Volume: {kw['search_volume']:,} | CPC: ${kw['cpc']} | CPA: ${kw['cpa']}\n")
                if kw['roi'] > 0:
                    f.write(f"   ROI: {kw['roi']}%\n")
                f.write("\n")
            
            # Keywords with no volume
            no_volume_keywords = [k for k in metrics_data['keywords'] if k['search_volume'] == 0]
            if no_volume_keywords:
                f.write("KEYWORDS WITH NO SEARCH VOLUME\n")
                f.write("-"*40 + "\n")
                for kw in no_volume_keywords:
                    f.write(f"• {kw['keyword']}\n")
        
        return csv_filename, txt_filename
    
    def run_analysis(self):
        """Execute complete analysis"""
        print("="*80)
        print("GTM CLEANUP & MANAGEMENT NICHE ANALYSIS")
        print("="*80)
        
        # Get keyword data
        keyword_data = self.analyze_keywords()
        if not keyword_data:
            print("Failed to retrieve keyword data.")
            return None
        
        # Calculate metrics
        metrics_data = self.calculate_cpa_metrics(keyword_data)
        
        # Display summary
        print(f"\nMARKET SUMMARY:")
        print(f"Total Search Volume: {metrics_data['total_search_volume']:,}/month")
        print(f"Keywords with Volume: {metrics_data['keywords_with_volume']}/{len(self.gtm_cleanup_keywords)}")
        print(f"Average CPC: ${metrics_data['average_cpc']}")
        print(f"Overall CPA: ${metrics_data['overall_cpa']}")
        print(f"Overall ROI: {metrics_data['overall_roi']}%")
        print(f"Monthly Ad Spend: ${metrics_data['total_monthly_spend']}")
        
        # Save results
        csv_file, txt_file = self.save_results(metrics_data)
        print(f"\nReports saved:")
        print(f"  CSV: {csv_file}")
        print(f"  Report: {txt_file}")
        
        return metrics_data

if __name__ == "__main__":
    login = "admin@locallyknown.pro"
    password = "74b1f60e9e023e5f"
    
    analyzer = GTMCleanupNicheAnalyzer(login, password)
    results = analyzer.run_analysis()
    
    if results:
        cost = len(analyzer.gtm_cleanup_keywords) * 0.002
        print(f"\nAnalysis cost: ${cost:.3f}")
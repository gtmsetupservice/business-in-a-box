#!/usr/bin/env python3
"""
Automated Niche Analysis Tool
Streamlined version for quick analysis of any niche using DataForSEO API
Based on the WebsiteROIfix.com analysis methodology
"""

import requests
import base64
import json
import csv
import argparse
import sys
from datetime import datetime
from pathlib import Path

class NicheAnalyzer:
    def __init__(self, login, password, output_dir="reports"):
        self.login = login
        self.password = password
        self.credentials = base64.b64encode(f"{login}:{password}".encode()).decode()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Default location (US)
        self.location_code = 2840
        self.location_name = "United States"
        
        # Industry benchmarks (conservative estimates)
        self.benchmarks = {
            'avg_ctr_top_positions': 0.35,
            'avg_ctr_lower_positions': 0.15,
            'b2b_conversion_rate': 0.025,
            'avg_project_value': 4000,
            'monthly_retainer_avg': 1800,
            'project_conversion_rate': 0.30,
            'retainer_conversion_rate': 0.15
        }
    
    def analyze_keywords(self, keywords):
        """Get keyword data from DataForSEO API"""
        url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
        
        headers = {
            'Authorization': f'Basic {self.credentials}',
            'Content-Type': 'application/json'
        }
        
        payload = json.dumps([{
            "search_partners": False,
            "keywords": keywords,
            "location_code": self.location_code,
            "language_code": "en",
            "sort_by": "search_volume",
            "include_adult_keywords": False
        }])
        
        print(f"Analyzing {len(keywords)} keywords...")
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            return None
        
        result_json = response.json()
        
        if 'tasks' not in result_json or not result_json['tasks'] or 'result' not in result_json['tasks'][0]:
            print("No keyword data found.")
            return None
        
        return result_json['tasks'][0]['result']
    
    def analyze_serp(self, keyword):
        """Analyze SERP for a specific keyword"""
        url = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
        
        headers = {
            'Authorization': f'Basic {self.credentials}',
            'Content-Type': 'application/json'
        }
        
        payload = json.dumps([{
            "keyword": keyword,
            "location_code": self.location_code,
            "language_code": "en",
            "device": "desktop",
            "os": "windows",
            "depth": 50
        }])
        
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code != 200:
            return None
        
        result_json = response.json()
        
        if 'tasks' not in result_json or not result_json['tasks'] or 'result' not in result_json['tasks'][0]:
            return None
        
        competitors = []
        serp_features = set()
        
        for item in result_json['tasks'][0]['result']:
            if 'items' in item:
                for result in item['items']:
                    if 'type' in result:
                        serp_features.add(result['type'])
                    
                    if result.get('type') == 'organic':
                        competitors.append({
                            'domain': result.get('domain'),
                            'position': result.get('rank_position'),
                            'title': result.get('title')
                        })
        
        return {
            'competitors': competitors[:10],
            'serp_features': list(serp_features),
            'total_results': len(competitors)
        }
    
    def calculate_metrics(self, keyword_data):
        """Calculate CPA and other metrics"""
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
            
            # Calculate CTR based on competition
            estimated_ctr = self.benchmarks['avg_ctr_top_positions'] if competition_index < 50 else self.benchmarks['avg_ctr_lower_positions']
            
            estimated_clicks = search_volume * estimated_ctr
            estimated_conversions = estimated_clicks * self.benchmarks['b2b_conversion_rate']
            
            # Calculate CPA
            if estimated_conversions > 0 and cpc > 0:
                monthly_spend = estimated_clicks * cpc
                cpa = monthly_spend / estimated_conversions
            else:
                cpa = 0
            
            metrics.append({
                'keyword': keyword,
                'search_volume': search_volume,
                'cpc': cpc,
                'competition_index': competition_index,
                'estimated_clicks': round(estimated_clicks, 2),
                'estimated_conversions': round(estimated_conversions, 3),
                'monthly_spend': round(estimated_clicks * cpc, 2) if cpc > 0 else 0,
                'cpa': round(cpa, 2) if cpa > 0 else 0
            })
            
            total_volume += search_volume
        
        avg_cpc = total_weighted_cpc / total_volume if total_volume > 0 else 0
        
        return {
            'keywords': metrics,
            'total_search_volume': total_volume,
            'keywords_with_volume': keywords_with_volume,
            'average_cpc': round(avg_cpc, 2)
        }
    
    def calculate_roi_projections(self, metrics_data):
        """Calculate ROI projections"""
        total_monthly_spend = sum(k['monthly_spend'] for k in metrics_data['keywords'])
        total_monthly_conversions = sum(k['estimated_conversions'] for k in metrics_data['keywords'])
        
        # Revenue calculations
        monthly_project_revenue = total_monthly_conversions * self.benchmarks['project_conversion_rate'] * self.benchmarks['avg_project_value']
        monthly_retainer_revenue = total_monthly_conversions * self.benchmarks['retainer_conversion_rate'] * self.benchmarks['monthly_retainer_avg']
        
        total_monthly_revenue = monthly_project_revenue + monthly_retainer_revenue
        
        roi_percentage = ((total_monthly_revenue - total_monthly_spend) / total_monthly_spend * 100) if total_monthly_spend > 0 else 0
        
        return {
            'monthly_ad_spend': round(total_monthly_spend, 2),
            'monthly_conversions': round(total_monthly_conversions, 2),
            'monthly_revenue_projection': round(total_monthly_revenue, 2),
            'roi_percentage': round(roi_percentage, 1),
            'payback_months': round(total_monthly_spend / total_monthly_revenue, 1) if total_monthly_revenue > 0 else 'N/A'
        }
    
    def calculate_niche_score(self, metrics_data, roi_projections):
        """Calculate overall niche attractiveness score"""
        volume_score = min(10, metrics_data['total_search_volume'] / 500)
        keyword_diversity_score = min(10, metrics_data['keywords_with_volume'] * 2)
        roi_score = min(10, max(0, roi_projections['roi_percentage'] / 20))
        
        # Simple competition score (inverse of average CPC)
        competition_score = min(10, max(0, 10 - (metrics_data['average_cpc'] / 10)))
        
        overall_score = round((volume_score + keyword_diversity_score + roi_score + competition_score) / 4, 1)
        
        return {
            'overall_score': overall_score,
            'volume_score': round(volume_score, 1),
            'diversity_score': round(keyword_diversity_score, 1),
            'roi_score': round(roi_score, 1),
            'competition_score': round(competition_score, 1)
        }
    
    def generate_recommendation(self, niche_score, roi_projections):
        """Generate go/no-go recommendation"""
        score = niche_score['overall_score']
        roi = roi_projections['roi_percentage']
        
        if score >= 8 and roi > 100:
            return "HIGHLY RECOMMENDED - Strong opportunity with excellent ROI potential"
        elif score >= 6 and roi > 50:
            return "RECOMMENDED - Good opportunity, proceed with focused strategy"
        elif score >= 4 and roi > 0:
            return "MARGINAL - Proceed with caution, consider focused approach"
        else:
            return "NOT RECOMMENDED - Consider alternative niches"
    
    def save_results(self, niche_name, metrics_data, roi_projections, niche_score, recommendation, top_keywords_analysis=None):
        """Save analysis results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save CSV with keyword details
        csv_filename = self.output_dir / f"{niche_name}_keywords_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['keyword', 'search_volume', 'cpc', 'competition_index', 'estimated_clicks', 'estimated_conversions', 'monthly_spend', 'cpa']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for kw in sorted(metrics_data['keywords'], key=lambda x: x['search_volume'], reverse=True):
                writer.writerow(kw)
        
        # Save comprehensive text report
        txt_filename = self.output_dir / f"{niche_name}_analysis_{timestamp}.txt"
        with open(txt_filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write(f"NICHE ANALYSIS REPORT: {niche_name.upper()}\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-"*40 + "\n")
            f.write(f"Overall Niche Score: {niche_score['overall_score']}/10\n")
            f.write(f"Total Search Volume: {metrics_data['total_search_volume']:,}/month\n")
            f.write(f"Keywords with Volume: {metrics_data['keywords_with_volume']}/{len(metrics_data['keywords'])}\n")
            f.write(f"Average CPC: ${metrics_data['average_cpc']}\n")
            f.write(f"Projected ROI: {roi_projections['roi_percentage']}%\n")
            f.write(f"Monthly Budget Required: ${roi_projections['monthly_ad_spend']}\n")
            f.write(f"Recommendation: {recommendation}\n\n")
            
            f.write("SCORE BREAKDOWN\n")
            f.write("-"*40 + "\n")
            f.write(f"Market Volume: {niche_score['volume_score']}/10\n")
            f.write(f"Keyword Diversity: {niche_score['diversity_score']}/10\n")
            f.write(f"ROI Potential: {niche_score['roi_score']}/10\n")
            f.write(f"Competition Level: {niche_score['competition_score']}/10\n\n")
            
            f.write("TOP KEYWORDS\n")
            f.write("-"*40 + "\n")
            top_keywords = sorted([kw for kw in metrics_data['keywords'] if kw['search_volume'] > 0], 
                                key=lambda x: x['search_volume'], reverse=True)[:10]
            
            for i, kw in enumerate(top_keywords, 1):
                f.write(f"{i}. {kw['keyword']}\n")
                f.write(f"   Volume: {kw['search_volume']:,} | CPC: ${kw['cpc']} | CPA: ${kw['cpa']}\n\n")
            
            if top_keywords_analysis:
                f.write("COMPETITIVE ANALYSIS\n")
                f.write("-"*40 + "\n")
                for keyword, analysis in top_keywords_analysis.items():
                    f.write(f"Keyword: {keyword}\n")
                    f.write(f"Top Competitors: {', '.join([c['domain'] for c in analysis['competitors'][:5]])}\n")
                    f.write(f"SERP Features: {', '.join(analysis['serp_features'])}\n\n")
            
            f.write("FINANCIAL PROJECTIONS\n")
            f.write("-"*40 + "\n")
            f.write(f"Monthly Ad Spend: ${roi_projections['monthly_ad_spend']:,}\n")
            f.write(f"Expected Conversions: {roi_projections['monthly_conversions']}\n")
            f.write(f"Revenue Projection: ${roi_projections['monthly_revenue_projection']:,}\n")
            f.write(f"ROI: {roi_projections['roi_percentage']}%\n")
            f.write(f"Payback Period: {roi_projections['payback_months']} months\n\n")
            
            f.write("="*80 + "\n")
        
        return csv_filename, txt_filename
    
    def run_analysis(self, keywords, niche_name, analyze_competition=True):
        """Run complete niche analysis"""
        print(f"\n{'='*80}")
        print(f"NICHE ANALYSIS: {niche_name.upper()}")
        print(f"{'='*80}")
        
        # Step 1: Get keyword data
        keyword_data = self.analyze_keywords(keywords)
        if not keyword_data:
            print("Failed to retrieve keyword data. Check API credentials.")
            return None
        
        # Step 2: Calculate metrics
        print("Calculating metrics and projections...")
        metrics_data = self.calculate_metrics(keyword_data)
        roi_projections = self.calculate_roi_projections(metrics_data)
        niche_score = self.calculate_niche_score(metrics_data, roi_projections)
        recommendation = self.generate_recommendation(niche_score, roi_projections)
        
        # Step 3: Optional competitive analysis
        competitive_analysis = None
        if analyze_competition:
            print("Analyzing competition for top keywords...")
            top_keywords = [kw['keyword'] for kw in sorted(metrics_data['keywords'], 
                           key=lambda x: x['search_volume'], reverse=True) if kw['search_volume'] > 50][:3]
            
            competitive_analysis = {}
            for keyword in top_keywords:
                analysis = self.analyze_serp(keyword)
                if analysis:
                    competitive_analysis[keyword] = analysis
        
        # Step 4: Display summary
        print(f"\n{'='*80}")
        print("ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"Niche Score: {niche_score['overall_score']}/10")
        print(f"ROI Projection: {roi_projections['roi_percentage']}%")
        print(f"Budget Required: ${roi_projections['monthly_ad_spend']:,}/month")
        print(f"Recommendation: {recommendation}")
        
        # Step 5: Save results
        csv_file, txt_file = self.save_results(niche_name, metrics_data, roi_projections, 
                                             niche_score, recommendation, competitive_analysis)
        
        print(f"\nReports saved:")
        print(f"  - Keywords: {csv_file}")
        print(f"  - Analysis: {txt_file}")
        
        return {
            'metrics': metrics_data,
            'roi': roi_projections,
            'score': niche_score,
            'recommendation': recommendation,
            'competitive_analysis': competitive_analysis
        }

def main():
    parser = argparse.ArgumentParser(description='Automated Niche Analysis Tool')
    parser.add_argument('--keywords', nargs='+', required=True, help='Keywords to analyze')
    parser.add_argument('--niche-name', required=True, help='Name of the niche (for file naming)')
    parser.add_argument('--login', required=True, help='DataForSEO API login')
    parser.add_argument('--password', required=True, help='DataForSEO API password')
    parser.add_argument('--output-dir', default='reports', help='Output directory for reports')
    parser.add_argument('--no-competition', action='store_true', help='Skip competitive analysis')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = NicheAnalyzer(args.login, args.password, args.output_dir)
    
    # Run analysis
    results = analyzer.run_analysis(
        keywords=args.keywords,
        niche_name=args.niche_name,
        analyze_competition=not args.no_competition
    )
    
    if results:
        # Calculate approximate cost
        keywords_cost = len(args.keywords) * 0.002
        serp_cost = 3 * 0.006 if not args.no_competition else 0
        total_cost = keywords_cost + serp_cost
        
        print(f"\nEstimated API Cost: ${total_cost:.3f}")
    
    return 0 if results else 1

if __name__ == "__main__":
    sys.exit(main())
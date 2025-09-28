import requests
import base64
import json
import csv
from datetime import datetime

class WebsiteROIAnalyzer:
    def __init__(self):
        self.login = "admin@locallyknown.pro"
        self.password = "74b1f60e9e023e5f"
        self.credentials = base64.b64encode(f"{self.login}:{self.password}".encode()).decode()
        
        self.target_keywords = [
            "website ROI",
            "improve website ROI",
            "website return on investment",
            "fix website profitability",
            "website conversion optimization",
            "website ROI analytics",
            "website profit optimization",
            "increase website returns",
            "website investment return",
            "website ROI measurement"
        ]
        
        self.location_code = 2840  # United States
        self.location_name = "United States"
        
    def analyze_keywords(self):
        """Analyze all target keywords for WebsiteROIfix.com"""
        url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
        
        headers = {
            'Authorization': f'Basic {self.credentials}',
            'Content-Type': 'application/json'
        }
        
        payload = json.dumps([{
            "search_partners": False,
            "keywords": self.target_keywords,
            "location_code": self.location_code,
            "language_code": "en",
            "sort_by": "search_volume",
            "include_adult_keywords": False
        }])
        
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            return None
        
        result_json = response.json()
        
        if 'tasks' not in result_json or not result_json['tasks'] or 'result' not in result_json['tasks'][0]:
            print("No keyword data found.")
            return None
        
        return result_json['tasks'][0]['result']
    
    def analyze_serp_for_keyword(self, keyword):
        """Analyze SERP competition for a specific keyword"""
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
            "depth": 20
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
                            'title': result.get('title'),
                            'position': result.get('rank_position'),
                            'url': result.get('url')
                        })
        
        return {
            'competitors': competitors[:10],
            'serp_features': list(serp_features),
            'total_results': len(competitors)
        }
    
    def calculate_cpa_and_metrics(self, keyword_data):
        """Calculate CPA and other important metrics"""
        if not keyword_data:
            return None
        
        metrics = []
        total_volume = 0
        weighted_cpc = 0
        
        for kw in keyword_data:
            search_volume = kw.get('search_volume', 0) or 0
            cpc = kw.get('cpc', 0) or 0
            competition_index = kw.get('competition_index', 0) or 0
            
            # Estimate click-through rate based on competition
            if competition_index < 30:
                estimated_ctr = 0.05  # 5% CTR for low competition
            elif competition_index < 70:
                estimated_ctr = 0.03  # 3% CTR for medium competition
            else:
                estimated_ctr = 0.02  # 2% CTR for high competition
            
            # Calculate estimated clicks
            estimated_clicks = search_volume * estimated_ctr
            
            # Estimate conversion rate (industry average for ROI/analytics services)
            conversion_rate = 0.025  # 2.5% conversion rate
            
            # Calculate estimated conversions
            estimated_conversions = estimated_clicks * conversion_rate
            
            # Calculate CPA
            if estimated_conversions > 0:
                monthly_spend = estimated_clicks * cpc
                cpa = monthly_spend / estimated_conversions if estimated_conversions > 0 else 0
            else:
                cpa = 0
            
            metrics.append({
                'keyword': kw.get('keyword'),
                'search_volume': search_volume,
                'cpc': cpc,
                'competition': kw.get('competition', 'N/A'),
                'competition_index': competition_index,
                'estimated_clicks': round(estimated_clicks, 2),
                'estimated_conversions': round(estimated_conversions, 2),
                'monthly_spend': round(estimated_clicks * cpc, 2),
                'cpa': round(cpa, 2)
            })
            
            total_volume += search_volume
            weighted_cpc += cpc * search_volume
        
        avg_cpc = weighted_cpc / total_volume if total_volume > 0 else 0
        
        return {
            'keywords': metrics,
            'total_search_volume': total_volume,
            'average_cpc': round(avg_cpc, 2),
            'average_cpa': round(sum(m['cpa'] for m in metrics) / len(metrics), 2) if metrics else 0
        }
    
    def generate_profitability_report(self, metrics_data, serp_analysis=None):
        """Generate comprehensive profitability assessment"""
        
        # Calculate market opportunity score
        total_volume = metrics_data['total_search_volume']
        avg_cpa = metrics_data['average_cpa']
        
        # Assuming average customer lifetime value for ROI consulting services
        avg_customer_value = 5000  # $5000 average project value
        monthly_retainer = 1500  # $1500/month for ongoing services
        
        # Calculate potential monthly revenue
        total_monthly_conversions = sum(kw['estimated_conversions'] for kw in metrics_data['keywords'])
        potential_monthly_revenue = total_monthly_conversions * monthly_retainer
        potential_project_revenue = total_monthly_conversions * 0.3 * avg_customer_value  # 30% convert to projects
        
        # Calculate total potential revenue
        total_potential_revenue = potential_monthly_revenue + potential_project_revenue
        
        # Calculate total monthly ad spend
        total_monthly_spend = sum(kw['monthly_spend'] for kw in metrics_data['keywords'])
        
        # Calculate ROI
        roi_percentage = ((total_potential_revenue - total_monthly_spend) / total_monthly_spend * 100) if total_monthly_spend > 0 else 0
        
        # Market difficulty assessment
        avg_competition = sum(kw['competition_index'] for kw in metrics_data['keywords']) / len(metrics_data['keywords'])
        
        if avg_competition < 40:
            difficulty = "LOW - Excellent opportunity for new entrants"
        elif avg_competition < 70:
            difficulty = "MEDIUM - Competitive but achievable with proper strategy"
        else:
            difficulty = "HIGH - Requires significant investment and expertise"
        
        report = {
            'market_overview': {
                'total_monthly_searches': total_volume,
                'average_cpc': metrics_data['average_cpc'],
                'average_cpa': avg_cpa,
                'market_difficulty': difficulty,
                'competition_score': round(avg_competition, 1)
            },
            'revenue_projections': {
                'estimated_monthly_conversions': round(total_monthly_conversions, 1),
                'potential_monthly_revenue': round(total_potential_revenue, 2),
                'monthly_ad_spend': round(total_monthly_spend, 2),
                'roi_percentage': round(roi_percentage, 1),
                'payback_period_months': round(total_monthly_spend / total_potential_revenue, 1) if total_potential_revenue > 0 else 'N/A'
            },
            'profitability_assessment': {
                'is_profitable': roi_percentage > 50,
                'profitability_score': min(10, round(roi_percentage / 20, 1)),  # Score out of 10
                'recommendation': self._get_recommendation(roi_percentage, avg_competition)
            }
        }
        
        return report
    
    def _get_recommendation(self, roi, competition):
        """Generate strategic recommendation based on metrics"""
        if roi > 100 and competition < 50:
            return "HIGHLY RECOMMENDED - Excellent profit potential with manageable competition. Immediate entry advised."
        elif roi > 50 and competition < 70:
            return "RECOMMENDED - Good profit potential. Focus on SEO and content marketing alongside PPC."
        elif roi > 0 and competition < 80:
            return "CAUTIOUSLY RECOMMENDED - Profitable but competitive. Start with targeted long-tail keywords."
        else:
            return "NOT RECOMMENDED - High competition and low profit margins. Consider alternative niches."
    
    def save_analysis_report(self, metrics_data, profitability_report):
        """Save comprehensive analysis to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed metrics to CSV
        csv_filename = f"websiteroifix_keywords_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['keyword', 'search_volume', 'cpc', 'competition', 'competition_index', 
                         'estimated_clicks', 'estimated_conversions', 'monthly_spend', 'cpa']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for kw in metrics_data['keywords']:
                writer.writerow(kw)
        
        # Save profitability report to text file
        report_filename = f"websiteroifix_profitability_{timestamp}.txt"
        with open(report_filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("WEBSITEROIFIX.COM - NICHE PROFITABILITY ANALYSIS\n")
            f.write("="*80 + "\n")
            f.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("MARKET OVERVIEW\n")
            f.write("-"*40 + "\n")
            mo = profitability_report['market_overview']
            f.write(f"Total Monthly Searches: {mo['total_monthly_searches']:,}\n")
            f.write(f"Average CPC: ${mo['average_cpc']}\n")
            f.write(f"Average CPA: ${mo['average_cpa']}\n")
            f.write(f"Market Difficulty: {mo['market_difficulty']}\n")
            f.write(f"Competition Score: {mo['competition_score']}/100\n\n")
            
            f.write("REVENUE PROJECTIONS\n")
            f.write("-"*40 + "\n")
            rp = profitability_report['revenue_projections']
            f.write(f"Estimated Monthly Conversions: {rp['estimated_monthly_conversions']}\n")
            f.write(f"Potential Monthly Revenue: ${rp['potential_monthly_revenue']:,.2f}\n")
            f.write(f"Monthly Ad Spend: ${rp['monthly_ad_spend']:,.2f}\n")
            f.write(f"ROI Percentage: {rp['roi_percentage']}%\n")
            f.write(f"Payback Period: {rp['payback_period_months']} months\n\n")
            
            f.write("PROFITABILITY ASSESSMENT\n")
            f.write("-"*40 + "\n")
            pa = profitability_report['profitability_assessment']
            f.write(f"Is Profitable: {'YES' if pa['is_profitable'] else 'NO'}\n")
            f.write(f"Profitability Score: {pa['profitability_score']}/10\n")
            f.write(f"Recommendation: {pa['recommendation']}\n\n")
            
            f.write("TOP KEYWORDS BY SEARCH VOLUME\n")
            f.write("-"*40 + "\n")
            sorted_keywords = sorted(metrics_data['keywords'], key=lambda x: x['search_volume'], reverse=True)
            for i, kw in enumerate(sorted_keywords[:5], 1):
                f.write(f"{i}. {kw['keyword']}\n")
                f.write(f"   Volume: {kw['search_volume']:,} | CPC: ${kw['cpc']} | CPA: ${kw['cpa']}\n")
            
            f.write("\n" + "="*80 + "\n")
        
        return csv_filename, report_filename
    
    def run_analysis(self):
        """Execute complete niche analysis"""
        print("="*80)
        print("WEBSITEROIFIX.COM NICHE ANALYSIS")
        print("="*80)
        print(f"Analyzing {len(self.target_keywords)} keywords for profitability...\n")
        
        # Step 1: Analyze keywords
        print("Step 1: Retrieving keyword data...")
        keyword_data = self.analyze_keywords()
        
        if not keyword_data:
            print("Failed to retrieve keyword data. Please check API credentials.")
            return
        
        print(f"✓ Retrieved data for {len(keyword_data)} keywords\n")
        
        # Step 2: Calculate metrics and CPA
        print("Step 2: Calculating CPA and conversion metrics...")
        metrics = self.calculate_cpa_and_metrics(keyword_data)
        print(f"✓ Average CPA: ${metrics['average_cpa']}")
        print(f"✓ Total search volume: {metrics['total_search_volume']:,}/month\n")
        
        # Step 3: Analyze SERP competition for top keyword
        print("Step 3: Analyzing SERP competition...")
        top_keyword = sorted(keyword_data, key=lambda x: x.get('search_volume', 0) or 0, reverse=True)[0]
        serp_data = self.analyze_serp_for_keyword(top_keyword['keyword'])
        
        if serp_data:
            print(f"✓ Found {serp_data['total_results']} competitors")
            print(f"✓ SERP features: {', '.join(serp_data['serp_features'][:5])}\n")
        
        # Step 4: Generate profitability report
        print("Step 4: Generating profitability assessment...")
        profitability_report = self.generate_profitability_report(metrics, serp_data)
        
        # Display summary
        print("\n" + "="*80)
        print("PROFITABILITY SUMMARY")
        print("="*80)
        
        pa = profitability_report['profitability_assessment']
        print(f"\n🎯 Profitability Score: {pa['profitability_score']}/10")
        print(f"💰 ROI: {profitability_report['revenue_projections']['roi_percentage']}%")
        print(f"📊 Market Difficulty: {profitability_report['market_overview']['market_difficulty']}")
        print(f"\n📝 Recommendation: {pa['recommendation']}")
        
        # Save reports
        print("\n" + "="*80)
        csv_file, report_file = self.save_analysis_report(metrics, profitability_report)
        print(f"✓ Detailed metrics saved to: {csv_file}")
        print(f"✓ Profitability report saved to: {report_file}")
        
        return profitability_report

if __name__ == "__main__":
    analyzer = WebsiteROIAnalyzer()
    analyzer.run_analysis()
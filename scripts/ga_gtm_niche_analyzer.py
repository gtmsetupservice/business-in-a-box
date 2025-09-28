#!/usr/bin/env python3
"""
Google Analytics & GTM Specialized Niche Analyzer
Analyzes specific GA/GTM service niches from the niches.md document
"""

import requests
import base64
import json
import csv
from datetime import datetime
from pathlib import Path

class GAGTMNicheAnalyzer:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.credentials = base64.b64encode(f"{login}:{password}".encode()).decode()
        self.location_code = 2840  # United States
        
        # Define niche-specific keyword sets
        self.niche_keywords = {
            'ecommerce_analytics': [
                "ecommerce analytics optimization",
                "Google Analytics ecommerce tracking",
                "shopping cart abandonment analysis",
                "ecommerce conversion rate optimization",
                "online store analytics setup",
                "retail analytics consulting",
                "ecommerce data analysis",
                "GA4 ecommerce implementation"
            ],
            'saas_analytics': [
                "SaaS user journey analysis",
                "software user behavior tracking",
                "SaaS analytics setup",
                "user onboarding analytics",
                "SaaS churn analysis",
                "product analytics consulting",
                "user activation tracking",
                "SaaS conversion funnel"
            ],
            'lead_generation_roi': [
                "lead generation analytics",
                "B2B conversion tracking",
                "marketing attribution analysis",
                "lead scoring analytics",
                "CRM analytics integration",
                "sales funnel analytics",
                "lead generation ROI tracking",
                "marketing qualified leads analytics"
            ],
            'financial_services_cro': [
                "financial services conversion optimization",
                "banking analytics setup",
                "insurance conversion tracking",
                "financial lead generation analytics",
                "mortgage application tracking",
                "fintech analytics consulting",
                "financial services compliance analytics",
                "bank website optimization"
            ],
            'attribution_modeling': [
                "marketing attribution modeling",
                "multi-touch attribution analysis",
                "cross-channel attribution",
                "attribution modeling consulting",
                "marketing mix modeling",
                "data-driven attribution",
                "customer journey attribution",
                "advanced attribution analytics"
            ]
        }
        
        # Service pricing for each niche (based on niches.md)
        self.service_pricing = {
            'ecommerce_analytics': {'setup': 2500, 'monthly': 2500, 'project_rate': 0.4},
            'saas_analytics': {'setup': 3500, 'monthly': 2250, 'project_rate': 0.35},
            'lead_generation_roi': {'setup': 6000, 'monthly': 1500, 'project_rate': 0.3},
            'financial_services_cro': {'setup': 3750, 'monthly': 2000, 'project_rate': 0.4},
            'attribution_modeling': {'setup': 7500, 'monthly': 1000, 'project_rate': 0.25}
        }
    
    def analyze_niche_keywords(self, niche_name, keywords):
        """Analyze keywords for a specific niche"""
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
        
        print(f"Analyzing {niche_name} ({len(keywords)} keywords)...")
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code != 200:
            print(f"Error for {niche_name}: API returned {response.status_code}")
            return None
        
        result_json = response.json()
        
        if 'tasks' not in result_json or not result_json['tasks'] or 'result' not in result_json['tasks'][0]:
            print(f"No data found for {niche_name}")
            return None
        
        return result_json['tasks'][0]['result']
    
    def calculate_niche_metrics(self, niche_name, keyword_data):
        """Calculate metrics specific to GA/GTM services"""
        if not keyword_data:
            return None
        
        # Higher conversion rates for specialized B2B services
        conversion_rate = 0.04  # 4% for specialized consulting vs 2.5% general
        
        metrics = []
        total_volume = 0
        keywords_with_volume = 0
        total_weighted_cpc = 0
        
        pricing = self.service_pricing[niche_name]
        
        for kw in keyword_data:
            keyword = kw.get('keyword', '')
            search_volume = kw.get('search_volume', 0) or 0
            cpc = kw.get('cpc', 0) or 0
            competition_index = kw.get('competition_index', 0) or 0
            
            if search_volume > 0:
                keywords_with_volume += 1
                total_weighted_cpc += cpc * search_volume
            
            # CTR based on specialized keyword intent (typically higher)
            estimated_ctr = 0.45 if competition_index < 40 else 0.25
            
            estimated_clicks = search_volume * estimated_ctr
            estimated_conversions = estimated_clicks * conversion_rate
            
            # Calculate revenue potential
            monthly_revenue = (estimated_conversions * pricing['project_rate'] * pricing['setup'] + 
                             estimated_conversions * (1 - pricing['project_rate']) * pricing['monthly'])
            
            # Calculate CPA and ROI
            if estimated_conversions > 0 and cpc > 0:
                monthly_spend = estimated_clicks * cpc
                cpa = monthly_spend / estimated_conversions
                roi = ((monthly_revenue - monthly_spend) / monthly_spend * 100) if monthly_spend > 0 else 0
            else:
                cpa = 0
                roi = 0
                monthly_spend = 0
            
            metrics.append({
                'keyword': keyword,
                'search_volume': search_volume,
                'cpc': cpc,
                'competition_index': competition_index,
                'estimated_clicks': round(estimated_clicks, 2),
                'estimated_conversions': round(estimated_conversions, 3),
                'monthly_spend': round(monthly_spend, 2),
                'monthly_revenue': round(monthly_revenue, 2),
                'cpa': round(cpa, 2),
                'roi': round(roi, 1)
            })
            
            total_volume += search_volume
        
        avg_cpc = total_weighted_cpc / total_volume if total_volume > 0 else 0
        
        return {
            'niche': niche_name,
            'keywords': metrics,
            'total_search_volume': total_volume,
            'keywords_with_volume': keywords_with_volume,
            'average_cpc': round(avg_cpc, 2),
            'pricing_model': pricing
        }
    
    def calculate_niche_score(self, niche_metrics):
        """Calculate niche attractiveness score for GA/GTM services"""
        # Adjust scoring for specialized B2B services
        volume_score = min(10, niche_metrics['total_search_volume'] / 200)  # Lower volume threshold
        keyword_diversity_score = min(10, niche_metrics['keywords_with_volume'] * 1.5)
        
        # Calculate average ROI across keywords with volume
        roi_keywords = [k for k in niche_metrics['keywords'] if k['search_volume'] > 0 and k['roi'] > 0]
        avg_roi = sum(k['roi'] for k in roi_keywords) / len(roi_keywords) if roi_keywords else 0
        roi_score = min(10, avg_roi / 50)  # Scale ROI to 0-10
        
        # Competition scoring based on CPC
        competition_score = min(10, max(0, 10 - (niche_metrics['average_cpc'] / 15)))
        
        overall_score = round((volume_score + keyword_diversity_score + roi_score + competition_score) / 4, 1)
        
        return {
            'overall_score': overall_score,
            'volume_score': round(volume_score, 1),
            'diversity_score': round(keyword_diversity_score, 1),
            'roi_score': round(roi_score, 1),
            'competition_score': round(competition_score, 1),
            'avg_roi': round(avg_roi, 1)
        }
    
    def analyze_all_niches(self):
        """Analyze all GA/GTM niches"""
        print("="*80)
        print("GOOGLE ANALYTICS & GTM NICHE ANALYSIS")
        print("="*80)
        
        results = {}
        total_cost = 0
        
        for niche_name, keywords in self.niche_keywords.items():
            # Get keyword data
            keyword_data = self.analyze_niche_keywords(niche_name, keywords)
            total_cost += len(keywords) * 0.002  # Track API costs
            
            if keyword_data:
                # Calculate metrics
                niche_metrics = self.calculate_niche_metrics(niche_name, keyword_data)
                niche_score = self.calculate_niche_score(niche_metrics)
                
                results[niche_name] = {
                    'metrics': niche_metrics,
                    'score': niche_score
                }
                
                # Display summary
                print(f"\n{niche_name.replace('_', ' ').title()}")
                print(f"  Score: {niche_score['overall_score']}/10")
                print(f"  Volume: {niche_metrics['total_search_volume']} searches/month")
                print(f"  Keywords: {niche_metrics['keywords_with_volume']}/{len(keywords)} viable")
                print(f"  Avg ROI: {niche_score['avg_roi']}%")
        
        # Generate comparative analysis
        self.generate_comparison_report(results, total_cost)
        
        return results
    
    def generate_comparison_report(self, results, total_cost):
        """Generate comparison report across all niches"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/ga_gtm_niche_comparison_{timestamp}.txt"
        
        # Sort niches by score
        sorted_niches = sorted(results.items(), key=lambda x: x[1]['score']['overall_score'], reverse=True)
        
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("GOOGLE ANALYTICS & GTM NICHE ANALYSIS COMPARISON\n")
            f.write("="*80 + "\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total API Cost: ${total_cost:.3f}\n\n")
            
            f.write("NICHE RANKINGS\n")
            f.write("-" * 50 + "\n")
            
            for i, (niche_name, data) in enumerate(sorted_niches, 1):
                metrics = data['metrics']
                score = data['score']
                pricing = metrics['pricing_model']
                
                f.write(f"{i}. {niche_name.replace('_', ' ').title()}\n")
                f.write(f"   Score: {score['overall_score']}/10\n")
                f.write(f"   Market Volume: {metrics['total_search_volume']:,} searches/month\n")
                f.write(f"   Viable Keywords: {metrics['keywords_with_volume']}/{len(self.niche_keywords[niche_name])}\n")
                f.write(f"   Average CPC: ${metrics['average_cpc']}\n")
                f.write(f"   Average ROI: {score['avg_roi']}%\n")
                f.write(f"   Setup Fee: ${pricing['setup']:,}\n")
                f.write(f"   Monthly Rate: ${pricing['monthly']:,}\n\n")
            
            f.write("DETAILED ANALYSIS\n")
            f.write("-" * 50 + "\n")
            
            for niche_name, data in sorted_niches:
                metrics = data['metrics']
                f.write(f"\n{niche_name.replace('_', ' ').upper()}\n")
                f.write("-" * 30 + "\n")
                
                # Top keywords by volume
                top_keywords = sorted([k for k in metrics['keywords'] if k['search_volume'] > 0], 
                                    key=lambda x: x['search_volume'], reverse=True)[:5]
                
                f.write("Top Keywords:\n")
                for kw in top_keywords:
                    f.write(f"  • {kw['keyword']}: {kw['search_volume']} searches, ")
                    f.write(f"${kw['cpc']} CPC, {kw['roi']}% ROI\n")
                f.write("\n")
            
            # Recommendations
            f.write("RECOMMENDATIONS\n")
            f.write("-" * 50 + "\n")
            
            if sorted_niches:
                top_niche = sorted_niches[0]
                f.write(f"PRIMARY RECOMMENDATION: {top_niche[0].replace('_', ' ').title()}\n")
                f.write(f"Score: {top_niche[1]['score']['overall_score']}/10\n")
                f.write(f"Reasoning: Highest overall score with balanced metrics\n\n")
                
                f.write("NICHE STRATEGY:\n")
                if top_niche[1]['score']['overall_score'] >= 7:
                    f.write("HIGHLY RECOMMENDED - Strong market opportunity\n")
                elif top_niche[1]['score']['overall_score'] >= 5:
                    f.write("RECOMMENDED - Good opportunity with focused approach\n")
                else:
                    f.write("MARGINAL - Requires careful keyword selection\n")
        
        print(f"\nComparison report saved: {filename}")
        print(f"Total analysis cost: ${total_cost:.3f}")

if __name__ == "__main__":
    # Use existing credentials
    login = "admin@locallyknown.pro"
    password = "74b1f60e9e023e5f"
    
    analyzer = GAGTMNicheAnalyzer(login, password)
    results = analyzer.analyze_all_niches()
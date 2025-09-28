#!/usr/bin/env python3
"""
Domain Name SEO Analysis using DataForSEO API
Analyzes exact-match domain potential based on keyword data
"""

import requests
import base64
import json
from datetime import datetime

class DomainKeywordAnalyzer:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.credentials = base64.b64encode(f"{login}:{password}".encode()).decode()
        self.location_code = 2840  # United States
        
        # Available domains and their target keywords
        self.domain_analysis = {
            'gtmauditpro.com': {
                'primary_keywords': ['GTM audit', 'Google Tag Manager audit', 'GTM audit service'],
                'secondary_keywords': ['tag manager audit', 'GTM audit pro', 'professional GTM audit']
            },
            'gtmwordpressexpert.com': {
                'primary_keywords': ['GTM WordPress', 'WordPress GTM setup', 'WordPress tag manager'],
                'secondary_keywords': ['WordPress Google Tag Manager', 'GTM WordPress expert', 'WordPress analytics setup']
            },
            'wordpressgtmexpert.com': {
                'primary_keywords': ['WordPress GTM', 'WordPress Google Tag Manager', 'WordPress tag manager expert'],
                'secondary_keywords': ['WordPress GTM setup', 'WordPress analytics tracking', 'WordPress conversion tracking']
            },
            'tagmanageraudit.com': {
                'primary_keywords': ['tag manager audit', 'Google Tag Manager audit', 'tag manager audit service'],
                'secondary_keywords': ['GTM audit', 'tag manager review', 'tag manager analysis']
            },
            'gtmsetupservice.com': {
                'primary_keywords': ['GTM setup', 'GTM setup service', 'Google Tag Manager setup'],
                'secondary_keywords': ['tag manager setup', 'GTM implementation', 'GTM installation']
            }
        }
        
        # Known data from our previous analyses
        self.known_volumes = {
            'GTM audit': 20,
            'Google Tag Manager audit': 40,
            'GTM setup': 50,
            'Google Tag Manager setup': 260,
            'tag manager audit': 10
        }
        
        # Competition strength from our SERP analysis
        self.competition_data = {
            'GTM audit': {'avg_position': 4.5, 'competitors': 8},
            'Google Tag Manager audit': {'avg_position': 3.5, 'competitors': 7},
            'GTM setup': {'avg_position': 6.0, 'competitors': 8},
            'Google Tag Manager setup': {'avg_position': 5.3, 'competitors': 8},
            'tag manager audit': {'avg_position': 6.0, 'competitors': 8}
        }
    
    def get_keyword_data(self, keywords):
        """Get search volume data for keyword list"""
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
        
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code}")
            return None
        
        result_json = response.json()
        
        if 'tasks' not in result_json or not result_json['tasks']:
            return None
        
        return result_json['tasks'][0]['result'] if result_json['tasks'][0]['result'] else []
    
    def analyze_domain_potential(self):
        """Analyze SEO potential for each domain"""
        domain_scores = []
        
        for domain, data in self.domain_analysis.items():
            print(f"Analyzing: {domain}")
            
            # Get all keywords for this domain
            all_keywords = data['primary_keywords'] + data['secondary_keywords']
            
            # Get keyword data from API
            keyword_results = self.get_keyword_data(all_keywords)
            
            if not keyword_results:
                print(f"No data for {domain}")
                continue
            
            # Calculate domain metrics
            total_volume = 0
            primary_volume = 0
            keyword_count = len([k for k in keyword_results if (k.get('search_volume', 0) or 0) > 0])
            
            competition_score = 0
            seo_difficulty_score = 0
            
            keyword_details = []
            
            for kw_data in keyword_results:
                keyword = kw_data.get('keyword', '')
                volume = kw_data.get('search_volume', 0) or 0
                cpc = kw_data.get('cpc', 0) or 0
                
                total_volume += volume
                
                if keyword in data['primary_keywords']:
                    primary_volume += volume
                
                # Use known competition data where available
                if keyword in self.competition_data:
                    comp_data = self.competition_data[keyword]
                    avg_pos = comp_data['avg_position']
                    competitors = comp_data['competitors']
                    
                    # SEO difficulty (lower position = harder to rank)
                    if avg_pos <= 3:
                        difficulty = 8  # Hard
                    elif avg_pos <= 5:
                        difficulty = 5  # Medium  
                    else:
                        difficulty = 3  # Easy
                        
                    competition_score += difficulty
                    seo_difficulty_score += (10 - avg_pos)  # Higher score = easier
                
                keyword_details.append({
                    'keyword': keyword,
                    'volume': volume,
                    'cpc': cpc,
                    'is_primary': keyword in data['primary_keywords'],
                    'competition_avg_pos': self.competition_data.get(keyword, {}).get('avg_position', 'unknown'),
                    'competitors_count': self.competition_data.get(keyword, {}).get('competitors', 'unknown')
                })
            
            # Calculate scores
            avg_competition = competition_score / len(keyword_results) if keyword_results else 0
            avg_seo_opportunity = seo_difficulty_score / len(keyword_results) if keyword_results else 0
            
            # Domain scoring factors
            exact_match_bonus = 0
            if 'audit' in domain and any('audit' in kw['keyword'] for kw in keyword_details if kw['volume'] > 0):
                exact_match_bonus += 3
            if 'setup' in domain and any('setup' in kw['keyword'] for kw in keyword_details if kw['volume'] > 0):
                exact_match_bonus += 3
            if 'gtm' in domain and any('gtm' in kw['keyword'].lower() for kw in keyword_details if kw['volume'] > 0):
                exact_match_bonus += 2
            if 'wordpress' in domain:
                exact_match_bonus += 1  # Niche differentiation
            
            # Calculate final score
            volume_score = min(total_volume / 50, 10)  # Max 10 points, 50 volume = 1 point
            primary_keyword_score = min(primary_volume / 30, 10)  # Primary keyword importance
            competition_score = max(0, 10 - avg_competition)  # Lower competition = higher score
            opportunity_score = min(avg_seo_opportunity, 10)
            
            total_score = (volume_score + primary_keyword_score + competition_score + 
                         opportunity_score + exact_match_bonus) / 5
            
            domain_scores.append({
                'domain': domain,
                'total_score': round(total_score, 1),
                'total_volume': total_volume,
                'primary_volume': primary_volume,
                'keyword_count': keyword_count,
                'avg_competition': round(avg_competition, 1),
                'exact_match_bonus': exact_match_bonus,
                'keyword_details': sorted(keyword_details, key=lambda x: x['volume'], reverse=True)
            })
        
        return sorted(domain_scores, key=lambda x: x['total_score'], reverse=True)
    
    def save_analysis(self, domain_scores):
        """Save domain analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/domain_seo_analysis_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("DOMAIN NAME SEO POTENTIAL ANALYSIS\n")
            f.write("="*80 + "\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("DOMAIN RANKINGS (by SEO potential)\n")
            f.write("-" * 50 + "\n")
            
            for i, domain_data in enumerate(domain_scores, 1):
                f.write(f"{i}. {domain_data['domain']}\n")
                f.write(f"   SEO Score: {domain_data['total_score']}/10\n")
                f.write(f"   Total Volume: {domain_data['total_volume']}/month\n")
                f.write(f"   Primary Keywords Volume: {domain_data['primary_volume']}/month\n")
                f.write(f"   Keywords with Volume: {domain_data['keyword_count']}\n")
                f.write(f"   Avg Competition Difficulty: {domain_data['avg_competition']}/10\n")
                f.write(f"   Exact Match Bonus: +{domain_data['exact_match_bonus']}\n")
                f.write("\n")
                
                f.write("   Top Keywords:\n")
                for kw in domain_data['keyword_details'][:3]:
                    if kw['volume'] > 0:
                        primary_flag = " (PRIMARY)" if kw['is_primary'] else ""
                        f.write(f"     • {kw['keyword']}: {kw['volume']}/month{primary_flag}\n")
                        f.write(f"       Competition Avg Pos: {kw['competition_avg_pos']}\n")
                f.write("\n")
            
            f.write("RECOMMENDATION\n")
            f.write("-" * 50 + "\n")
            if domain_scores:
                best_domain = domain_scores[0]
                f.write(f"Top Choice: {best_domain['domain']}\n")
                f.write(f"Reasoning: Highest SEO potential score of {best_domain['total_score']}/10\n")
                f.write(f"Primary advantage: {best_domain['primary_volume']}/month in primary keywords\n")
        
        return filename
    
    def run_analysis(self):
        """Execute complete domain analysis"""
        print("="*80)
        print("DOMAIN NAME SEO POTENTIAL ANALYSIS")
        print("="*80)
        
        domain_scores = self.analyze_domain_potential()
        
        if not domain_scores:
            print("No domain data available")
            return None
        
        print(f"\nDOMAIN RANKINGS:")
        print("-" * 40)
        
        for i, domain_data in enumerate(domain_scores, 1):
            print(f"{i}. {domain_data['domain']}")
            print(f"   SEO Score: {domain_data['total_score']}/10")
            print(f"   Total Volume: {domain_data['total_volume']}/month")
            print(f"   Primary Volume: {domain_data['primary_volume']}/month")
            print()
        
        # Save results
        report_file = self.save_analysis(domain_scores)
        print(f"Analysis saved: {report_file}")
        
        # Calculate API cost
        total_keywords = sum(len(data['primary_keywords']) + len(data['secondary_keywords']) 
                           for data in self.domain_analysis.values())
        cost = total_keywords * 0.002
        print(f"API cost: ${cost:.3f}")
        
        return domain_scores

if __name__ == "__main__":
    login = "admin@locallyknown.pro"
    password = "74b1f60e9e023e5f"
    
    analyzer = DomainKeywordAnalyzer(login, password)
    results = analyzer.run_analysis()
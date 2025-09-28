#!/usr/bin/env python3
"""
GTM Cleanup Competition Analysis
Analyzes SERP data for GTM cleanup competitors using DataForSEO API
"""

import requests
import base64
import json
import csv
from datetime import datetime
import time

class GTMCompetitionAnalyzer:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.credentials = base64.b64encode(f"{login}:{password}".encode()).decode()
        self.location_code = 2840  # United States
        
        # Competition research keywords - focusing on services actually offered
        self.competitor_keywords = [
            "GTM consultant",
            "Google Tag Manager consultant", 
            "GTM audit",
            "Google Tag Manager audit",
            "GTM setup service",
            "tag manager implementation",
            "Google Analytics implementation",
            "conversion tracking setup",
            "GTM troubleshooting service",
            "analytics consulting"
        ]
    
    def get_serp_data(self, keyword):
        """Get SERP data for competitor analysis"""
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
            "depth": 20  # Get top 20 results
        }])
        
        print(f"Getting SERP data for: {keyword}")
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            return None
        
        result_json = response.json()
        
        if 'tasks' not in result_json or not result_json['tasks'] or 'result' not in result_json['tasks'][0]:
            print(f"No SERP data found for {keyword}")
            return None
        
        return result_json['tasks'][0]['result']
    
    def analyze_competitors(self):
        """Analyze all competitors across keywords"""
        all_competitors = {}
        keyword_analysis = []
        
        for keyword in self.competitor_keywords:
            serp_data = self.get_serp_data(keyword)
            if not serp_data or not serp_data[0].get('items'):
                continue
            
            # Analyze this keyword's results
            keyword_competitors = []
            for item in serp_data[0]['items'][:10]:  # Top 10 results
                domain = item.get('domain', '')
                title = item.get('title', '')
                url = item.get('url', '')
                position = item.get('rank_group', 0)
                
                if domain and domain not in ['linkedin.com', 'upwork.com', 'fiverr.com', 'facebook.com']:
                    # Track this competitor
                    if domain not in all_competitors:
                        all_competitors[domain] = {
                            'domain': domain,
                            'keywords_ranked': [],
                            'avg_position': 0,
                            'total_positions': 0,
                            'sample_titles': [],
                            'sample_urls': []
                        }
                    
                    all_competitors[domain]['keywords_ranked'].append({
                        'keyword': keyword,
                        'position': position,
                        'title': title,
                        'url': url
                    })
                    all_competitors[domain]['total_positions'] += position
                    
                    if len(all_competitors[domain]['sample_titles']) < 3:
                        all_competitors[domain]['sample_titles'].append(title)
                        all_competitors[domain]['sample_urls'].append(url)
                    
                    keyword_competitors.append({
                        'keyword': keyword,
                        'domain': domain,
                        'position': position,
                        'title': title,
                        'url': url
                    })
            
            keyword_analysis.append({
                'keyword': keyword,
                'competitors': keyword_competitors
            })
            
            # Rate limiting
            time.sleep(1)
        
        # Calculate averages
        for domain in all_competitors:
            comp = all_competitors[domain]
            comp['keywords_count'] = len(comp['keywords_ranked'])
            comp['avg_position'] = round(comp['total_positions'] / comp['keywords_count'], 1)
        
        return all_competitors, keyword_analysis
    
    def classify_competitors(self, competitors):
        """Classify competitors by type and strength"""
        agencies = []
        freelancers = []
        platforms = []
        
        for domain, data in competitors.items():
            # Classification based on domain patterns and ranking strength
            if data['keywords_count'] >= 5 and data['avg_position'] <= 5:
                category = "Major Agency/Specialist"
            elif data['keywords_count'] >= 3 and data['avg_position'] <= 8:
                category = "Established Service Provider"
            elif data['keywords_count'] >= 2:
                category = "Active Competitor"
            else:
                category = "Occasional Player"
            
            competitor_info = {
                'domain': domain,
                'category': category,
                'keywords_count': data['keywords_count'],
                'avg_position': data['avg_position'],
                'sample_titles': data['sample_titles'][:2],  # Top 2 titles
                'strength_score': self.calculate_strength_score(data)
            }
            
            # Simple classification by domain characteristics
            if any(word in domain.lower() for word in ['agency', 'marketing', 'digital', 'media', 'group']):
                agencies.append(competitor_info)
            elif any(word in domain.lower() for word in ['consulting', 'consultant', 'analytics']):
                freelancers.append(competitor_info)
            else:
                platforms.append(competitor_info)
        
        return {
            'agencies': sorted(agencies, key=lambda x: x['strength_score'], reverse=True),
            'freelancers': sorted(freelancers, key=lambda x: x['strength_score'], reverse=True),
            'platforms': sorted(platforms, key=lambda x: x['strength_score'], reverse=True)
        }
    
    def calculate_strength_score(self, data):
        """Calculate competitor strength score"""
        # Score based on keyword count and average position
        position_score = max(0, 20 - data['avg_position'])  # Better position = higher score
        volume_score = min(data['keywords_count'] * 5, 50)  # Max 50 points for keyword coverage
        
        return position_score + volume_score
    
    def save_competition_analysis(self, competitors, classified, keyword_analysis):
        """Save competition analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed CSV
        csv_filename = f"competition/gtm_competition_analysis_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['domain', 'category', 'keywords_count', 'avg_position', 'strength_score', 'sample_titles']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            all_classified = classified['agencies'] + classified['freelancers'] + classified['platforms']
            for comp in sorted(all_classified, key=lambda x: x['strength_score'], reverse=True):
                writer.writerow({
                    'domain': comp['domain'],
                    'category': comp['category'], 
                    'keywords_count': comp['keywords_count'],
                    'avg_position': comp['avg_position'],
                    'strength_score': comp['strength_score'],
                    'sample_titles': ' | '.join(comp['sample_titles'])
                })
        
        # Save detailed report
        txt_filename = f"competition/gtm_competition_report_{timestamp}.txt"
        with open(txt_filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("GTM CLEANUP & MANAGEMENT COMPETITION ANALYSIS\n")
            f.write("="*80 + "\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Executive Summary
            total_competitors = len(competitors)
            major_players = len([c for c in competitors.values() if c['keywords_count'] >= 5 and c['avg_position'] <= 5])
            
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total Unique Competitors Found: {total_competitors}\n")
            f.write(f"Major Players (5+ keywords, top 5 positions): {major_players}\n")
            f.write(f"Keywords Analyzed: {len(self.competitor_keywords)}\n")
            f.write(f"Agencies: {len(classified['agencies'])}\n")
            f.write(f"Freelancers/Consultants: {len(classified['freelancers'])}\n")
            f.write(f"Other Platforms: {len(classified['platforms'])}\n\n")
            
            # Top Competitors
            all_classified = classified['agencies'] + classified['freelancers'] + classified['platforms']
            top_competitors = sorted(all_classified, key=lambda x: x['strength_score'], reverse=True)[:10]
            
            f.write("TOP 10 COMPETITORS BY STRENGTH\n")
            f.write("-" * 40 + "\n")
            for i, comp in enumerate(top_competitors, 1):
                f.write(f"{i}. {comp['domain']}\n")
                f.write(f"   Category: {comp['category']}\n")
                f.write(f"   Keywords Ranking: {comp['keywords_count']}\n")
                f.write(f"   Average Position: {comp['avg_position']}\n")
                f.write(f"   Strength Score: {comp['strength_score']}\n")
                if comp['sample_titles']:
                    f.write(f"   Sample Services: {comp['sample_titles'][0]}\n")
                f.write("\n")
            
            # Market Analysis
            f.write("MARKET ANALYSIS\n")
            f.write("-" * 40 + "\n")
            
            # Competition intensity by keyword
            f.write("Competition Intensity by Keyword:\n")
            for kw_analysis in keyword_analysis:
                competitor_count = len(kw_analysis['competitors'])
                f.write(f"• {kw_analysis['keyword']}: {competitor_count} competitors\n")
            
            f.write(f"\nMarket Gaps:\n")
            low_competition = [kw for kw in keyword_analysis if len(kw['competitors']) <= 3]
            if low_competition:
                for kw in low_competition:
                    f.write(f"• {kw['keyword']} - Only {len(kw['competitors'])} competitors\n")
            else:
                f.write("• No obvious keyword gaps found - competitive market\n")
        
        return csv_filename, txt_filename
    
    def run_analysis(self):
        """Execute complete competition analysis"""
        print("="*80)
        print("GTM CLEANUP & MANAGEMENT COMPETITION ANALYSIS")
        print("="*80)
        
        # Analyze competitors
        competitors, keyword_analysis = self.analyze_competitors()
        
        if not competitors:
            print("No competitor data found.")
            return None
        
        # Classify competitors
        classified = self.classify_competitors(competitors)
        
        # Display summary
        print(f"\nCOMPETITION SUMMARY:")
        print(f"Total Competitors: {len(competitors)}")
        print(f"Agencies: {len(classified['agencies'])}")
        print(f"Freelancers: {len(classified['freelancers'])}")
        print(f"Other Platforms: {len(classified['platforms'])}")
        
        # Show top 3 competitors
        all_classified = classified['agencies'] + classified['freelancers'] + classified['platforms']
        top_3 = sorted(all_classified, key=lambda x: x['strength_score'], reverse=True)[:3]
        
        print(f"\nTOP 3 COMPETITORS:")
        for i, comp in enumerate(top_3, 1):
            print(f"{i}. {comp['domain']} (Score: {comp['strength_score']}, Keywords: {comp['keywords_count']}, Avg Pos: {comp['avg_position']})")
        
        # Save results
        csv_file, txt_file = self.save_competition_analysis(competitors, classified, keyword_analysis)
        print(f"\nAnalysis saved:")
        print(f"  CSV: {csv_file}")
        print(f"  Report: {txt_file}")
        
        return {
            'competitors': competitors,
            'classified': classified,
            'keyword_analysis': keyword_analysis
        }

if __name__ == "__main__":
    login = "admin@locallyknown.pro"
    password = "74b1f60e9e023e5f"
    
    analyzer = GTMCompetitionAnalyzer(login, password)
    results = analyzer.run_analysis()
    
    if results:
        cost = len(analyzer.competitor_keywords) * 0.006  # SERP requests cost $0.006 each
        print(f"\nAnalysis cost: ${cost:.3f}")
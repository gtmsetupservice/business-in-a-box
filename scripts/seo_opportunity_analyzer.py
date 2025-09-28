#!/usr/bin/env python3
"""
SEO Opportunity & Domain/Income Analysis for GTM Niche
Analyzes competitive gaps and calculates income projections
"""

import requests
import base64
import json
from datetime import datetime

class GTMSEOOpportunityAnalyzer:
    def __init__(self):
        # GTM service pricing based on market research
        self.pricing = {
            'gtm_audit': 850,           # One-time audit
            'gtm_cleanup': 1200,        # Container cleanup
            'gtm_setup': 950,           # New implementation  
            'conversion_tracking': 750,  # Tracking setup
            'monthly_maintenance': 400,  # Monthly retainer
            'wordpress_integration': 600, # WP-specific work
            'ga4_migration': 1100,      # GA4 setup with GTM
            'troubleshooting': 125      # Hourly rate
        }
        
        # Market data from our analysis
        self.keyword_volumes = {
            'GTM consultant': 210,
            'Google Tag Manager consultant': 170,
            'GTM audit': 20,
            'Google Tag Manager audit': 40,
            'GTM setup': 50,
            'Google Tag Manager setup': 260
        }
        
        # Competition strength (lower = easier to rank)
        self.competition_strength = {
            'GTM consultant': 3.2,          # Avg position of competitors
            'Google Tag Manager consultant': 3.7,
            'GTM audit': 4.5,
            'Google Tag Manager audit': 3.5,
            'GTM setup': 6.0,
            'Google Tag Manager setup': 5.3
        }
    
    def analyze_seo_opportunity(self):
        """Analyze SEO ranking opportunity"""
        opportunities = []
        
        for keyword, volume in self.keyword_volumes.items():
            competition_pos = self.competition_strength.get(keyword, 5.0)
            
            # SEO difficulty score (1-10, lower = easier)
            if competition_pos >= 6:
                seo_difficulty = 3  # Easy
            elif competition_pos >= 4:
                seo_difficulty = 5  # Medium
            else:
                seo_difficulty = 7  # Hard
            
            # Estimate ranking potential for experienced developer with targeted content
            if seo_difficulty <= 4:
                ranking_estimate = "2-4"  # Top 3 achievable
                traffic_estimate = volume * 0.35  # 35% CTR for positions 2-4
            elif seo_difficulty <= 6:
                ranking_estimate = "4-7"  # First page achievable
                traffic_estimate = volume * 0.15  # 15% CTR for positions 4-7
            else:
                ranking_estimate = "7-10" # Page 1 bottom
                traffic_estimate = volume * 0.05  # 5% CTR for positions 7-10
            
            opportunities.append({
                'keyword': keyword,
                'volume': volume,
                'competition_avg_pos': competition_pos,
                'seo_difficulty': seo_difficulty,
                'ranking_estimate': ranking_estimate,
                'monthly_traffic_estimate': round(traffic_estimate, 1)
            })
        
        return opportunities
    
    def generate_domain_names(self):
        """Generate keyword-stacked domain names"""
        domains = [
            # GTM focused
            "gtmauditpro.com",
            "gtmcleanupexpert.com", 
            "gtmconsultingpro.com",
            "gtmsetupservice.com",
            "gtmwordpressexpert.com",
            
            # Google Tag Manager focused
            "tagmanageraudit.com",
            "tagmanagerexpert.com",
            "tagmanagerconsulting.com",
            "tagmanagersetup.com",
            "tagmanagerwordpress.com",
            
            # Service focused
            "conversiontrackingpro.com",
            "analyticstrackingexpert.com",
            "ga4gtmsetup.com",
            "wordpressgtmexpert.com",
            "gtmtroubleshooter.com"
        ]
        
        # Score domains by keyword match and brandability
        scored_domains = []
        for domain in domains:
            keyword_score = 0
            if 'gtm' in domain.lower():
                keyword_score += 3
            if 'audit' in domain.lower():
                keyword_score += 2
            if 'expert' in domain.lower():
                keyword_score += 1
            if 'pro' in domain.lower():
                keyword_score += 1
            if 'wordpress' in domain.lower():
                keyword_score += 2
            
            brandability = 10 - len(domain.replace('.com', ''))  # Shorter = more brandable
            if brandability < 0:
                brandability = 0
                
            scored_domains.append({
                'domain': domain,
                'keyword_score': keyword_score,
                'brandability': max(brandability, 0),
                'total_score': keyword_score + max(brandability, 0)
            })
        
        return sorted(scored_domains, key=lambda x: x['total_score'], reverse=True)
    
    def calculate_income_projections(self, seo_opportunities):
        """Calculate solopreneur income projections"""
        # Conservative conversion rates for technical B2B services
        conversion_rates = {
            'audit': 0.08,      # 8% of traffic converts to audit
            'setup': 0.05,      # 5% converts to setup work
            'consulting': 0.03,  # 3% converts to consulting
            'maintenance': 0.02  # 2% converts to monthly retainer
        }
        
        total_monthly_traffic = sum(opp['monthly_traffic_estimate'] for opp in seo_opportunities)
        
        # Project conversions by service type
        audit_conversions = total_monthly_traffic * conversion_rates['audit']
        setup_conversions = total_monthly_traffic * conversion_rates['setup'] 
        consulting_conversions = total_monthly_traffic * conversion_rates['consulting']
        maintenance_conversions = total_monthly_traffic * conversion_rates['maintenance']
        
        # Revenue calculations
        monthly_revenue = {
            'audits': audit_conversions * self.pricing['gtm_audit'],
            'setups': setup_conversions * self.pricing['gtm_setup'],
            'consulting': consulting_conversions * self.pricing['gtm_cleanup'],
            'maintenance': maintenance_conversions * self.pricing['monthly_maintenance'],
        }
        
        total_monthly = sum(monthly_revenue.values())
        annual_revenue = total_monthly * 12
        
        # Solopreneur capacity limits
        max_monthly_projects = 8  # Realistic for solo operation
        max_monthly_revenue = max_monthly_projects * 950  # Average project value
        
        realistic_monthly = min(total_monthly, max_monthly_revenue)
        realistic_annual = realistic_monthly * 12
        
        return {
            'traffic_projections': {
                'total_monthly_traffic': round(total_monthly_traffic, 1),
                'audit_leads': round(audit_conversions, 1),
                'setup_leads': round(setup_conversions, 1),
                'consulting_leads': round(consulting_conversions, 1),
                'maintenance_leads': round(maintenance_conversions, 1)
            },
            'revenue_projections': {
                'theoretical_monthly': round(total_monthly, 0),
                'theoretical_annual': round(annual_revenue, 0),
                'realistic_monthly': round(realistic_monthly, 0),
                'realistic_annual': round(realistic_annual, 0),
                'capacity_limited': total_monthly > max_monthly_revenue
            },
            'service_breakdown': {k: round(v, 0) for k, v in monthly_revenue.items()}
        }
    
    def run_analysis(self):
        """Execute complete analysis"""
        print("="*80)
        print("GTM NICHE SEO OPPORTUNITY & INCOME ANALYSIS")
        print("="*80)
        
        # SEO Analysis
        seo_opportunities = self.analyze_seo_opportunity()
        
        print("\nSEO OPPORTUNITY ANALYSIS:")
        print("-" * 50)
        for opp in seo_opportunities:
            print(f"• {opp['keyword']}")
            print(f"  Volume: {opp['volume']:,}/month | Difficulty: {opp['seo_difficulty']}/10")
            print(f"  Ranking Potential: Position {opp['ranking_estimate']}")
            print(f"  Traffic Estimate: {opp['monthly_traffic_estimate']}/month")
            print()
        
        # Domain Analysis
        domains = self.generate_domain_names()
        
        print("TOP DOMAIN NAME RECOMMENDATIONS:")
        print("-" * 50)
        for i, domain in enumerate(domains[:5], 1):
            print(f"{i}. {domain['domain']}")
            print(f"   Keyword Score: {domain['keyword_score']}/10")
            print(f"   Brandability: {domain['brandability']}/10")
            print(f"   Total Score: {domain['total_score']}/20")
            print()
        
        # Income Projections
        income_data = self.calculate_income_projections(seo_opportunities)
        
        print("INCOME PROJECTIONS (Solopreneur):")
        print("-" * 50)
        print(f"Monthly Traffic: {income_data['traffic_projections']['total_monthly_traffic']}")
        print(f"Monthly Leads: {sum([income_data['traffic_projections']['audit_leads'], income_data['traffic_projections']['setup_leads'], income_data['traffic_projections']['consulting_leads']]):.1f}")
        print()
        print("REALISTIC INCOME (Capacity Limited):")
        print(f"Monthly Revenue: ${income_data['revenue_projections']['realistic_monthly']:,}")
        print(f"Annual Revenue: ${income_data['revenue_projections']['realistic_annual']:,}")
        print()
        print("SERVICE BREAKDOWN:")
        for service, revenue in income_data['service_breakdown'].items():
            print(f"  {service.title()}: ${revenue:,}/month")
        
        return {
            'seo_opportunities': seo_opportunities,
            'domains': domains,
            'income_projections': income_data
        }

if __name__ == "__main__":
    analyzer = GTMSEOOpportunityAnalyzer()
    results = analyzer.run_analysis()
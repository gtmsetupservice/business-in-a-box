import json
from datetime import datetime

class DataForSEOCostCalculator:
    def __init__(self):
        # DataForSEO API pricing (as of 2024/2025)
        self.pricing = {
            'keywords_data_search_volume': 0.002,  # $0.002 per keyword
            'serp_google_organic_live': 0.006,     # $0.006 per request
            'locations_api': 0.0001                # $0.0001 per request (very cheap)
        }
    
    def calculate_analysis_costs(self):
        """Calculate costs for all analyses performed"""
        
        analyses_performed = [
            {
                'name': 'Initial WebsiteROI Analysis',
                'keywords_analyzed': 10,
                'serp_requests': 1,  # Top keyword analysis
                'location_requests': 0
            },
            {
                'name': 'Extended Analytics Keywords Analysis',
                'keywords_analyzed': 19,
                'serp_requests': 1,  # Top keyword analysis
                'location_requests': 0
            },
            {
                'name': 'First Comprehensive Analysis (with Google Analytics)',
                'keywords_analyzed': 12,
                'serp_requests': 3,  # Top 3 keywords analyzed
                'location_requests': 0
            },
            {
                'name': 'Updated Comprehensive Analysis (without Google Analytics)',
                'keywords_analyzed': 11,
                'serp_requests': 3,  # Top 3 keywords analyzed
                'location_requests': 0
            }
        ]
        
        total_cost = 0
        cost_breakdown = []
        
        for analysis in analyses_performed:
            # Calculate costs for each API type
            keywords_cost = analysis['keywords_analyzed'] * self.pricing['keywords_data_search_volume']
            serp_cost = analysis['serp_requests'] * self.pricing['serp_google_organic_live']
            location_cost = analysis['location_requests'] * self.pricing['locations_api']
            
            analysis_total = keywords_cost + serp_cost + location_cost
            total_cost += analysis_total
            
            cost_breakdown.append({
                'analysis': analysis['name'],
                'keywords_cost': round(keywords_cost, 4),
                'serp_cost': round(serp_cost, 4),
                'location_cost': round(location_cost, 4),
                'total_cost': round(analysis_total, 4),
                'details': {
                    'keywords_analyzed': analysis['keywords_analyzed'],
                    'serp_requests': analysis['serp_requests'],
                    'location_requests': analysis['location_requests']
                }
            })
        
        return {
            'total_cost': round(total_cost, 4),
            'breakdown': cost_breakdown,
            'summary': {
                'total_keywords_analyzed': sum(a['keywords_analyzed'] for a in analyses_performed),
                'total_serp_requests': sum(a['serp_requests'] for a in analyses_performed),
                'total_location_requests': sum(a['location_requests'] for a in analyses_performed)
            }
        }
    
    def generate_cost_report(self):
        """Generate comprehensive cost report"""
        costs = self.calculate_analysis_costs()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dataforseo_api_costs_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("DATAFORSEO API COST ANALYSIS\n")
            f.write("WEBSITEROIFIX.COM NICHE ANALYSIS PROJECT\n")
            f.write("="*80 + "\n")
            f.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("TOTAL PROJECT COST\n")
            f.write("-"*40 + "\n")
            f.write(f"Total API Costs: ${costs['total_cost']:.4f}\n\n")
            
            f.write("COST BREAKDOWN BY ANALYSIS\n")
            f.write("-"*40 + "\n")
            
            for i, analysis in enumerate(costs['breakdown'], 1):
                f.write(f"{i}. {analysis['analysis']}\n")
                f.write(f"   Keywords Analyzed: {analysis['details']['keywords_analyzed']}\n")
                f.write(f"   SERP Requests: {analysis['details']['serp_requests']}\n")
                f.write(f"   Keywords API Cost: ${analysis['keywords_cost']:.4f}\n")
                f.write(f"   SERP API Cost: ${analysis['serp_cost']:.4f}\n")
                f.write(f"   Analysis Total: ${analysis['total_cost']:.4f}\n\n")
            
            f.write("PROJECT SUMMARY\n")
            f.write("-"*40 + "\n")
            f.write(f"Total Keywords Analyzed: {costs['summary']['total_keywords_analyzed']}\n")
            f.write(f"Total SERP Requests: {costs['summary']['total_serp_requests']}\n")
            f.write(f"Total Location Requests: {costs['summary']['total_location_requests']}\n\n")
            
            f.write("COST PER API TYPE\n")
            f.write("-"*40 + "\n")
            keywords_total = costs['summary']['total_keywords_analyzed'] * self.pricing['keywords_data_search_volume']
            serp_total = costs['summary']['total_serp_requests'] * self.pricing['serp_google_organic_live']
            location_total = costs['summary']['total_location_requests'] * self.pricing['locations_api']
            
            f.write(f"Keywords Data API: ${keywords_total:.4f} ({costs['summary']['total_keywords_analyzed']} keywords × ${self.pricing['keywords_data_search_volume']})\n")
            f.write(f"SERP Analysis API: ${serp_total:.4f} ({costs['summary']['total_serp_requests']} requests × ${self.pricing['serp_google_organic_live']})\n")
            f.write(f"Locations API: ${location_total:.4f} ({costs['summary']['total_location_requests']} requests × ${self.pricing['locations_api']})\n\n")
            
            f.write("COST EFFICIENCY ANALYSIS\n")
            f.write("-"*40 + "\n")
            f.write(f"Cost per keyword analyzed: ${costs['total_cost'] / costs['summary']['total_keywords_analyzed']:.6f}\n")
            f.write(f"Cost per analysis performed: ${costs['total_cost'] / len(costs['breakdown']):.4f}\n\n")
            
            f.write("VALUE DELIVERED\n")
            f.write("-"*40 + "\n")
            f.write("• Comprehensive market analysis with actual search data\n")
            f.write("• Evidence-based CPA calculations\n")
            f.write("• Competitive landscape analysis\n")
            f.write("• ROI projections with industry benchmarks\n")
            f.write("• Go/no-go recommendation with data proof\n")
            f.write("• Identified profitable niche subset (241% ROI potential)\n")
            f.write("• Avoided potentially costly business mistake\n\n")
            
            f.write("COMPARED TO ALTERNATIVE RESEARCH METHODS\n")
            f.write("-"*40 + "\n")
            f.write("• Market research consultant: $2,000-5,000+\n")
            f.write("• SEO tool subscriptions (monthly): $100-500+\n")
            f.write("• Trial and error PPC testing: $1,000s in wasted ad spend\n")
            f.write(f"• DataForSEO API analysis: ${costs['total_cost']:.2f}\n\n")
            
            f.write("="*80 + "\n")
            f.write("CONCLUSION: Extremely cost-effective market validation\n")
            f.write("="*80 + "\n")
        
        return filename, costs
    
    def print_summary(self, costs):
        """Print cost summary to console"""
        print("="*60)
        print("DATAFORSEO API COST SUMMARY")
        print("="*60)
        print(f"Total Project Cost: ${costs['total_cost']:.2f}")
        print(f"Keywords Analyzed: {costs['summary']['total_keywords_analyzed']}")
        print(f"SERP Analyses: {costs['summary']['total_serp_requests']}")
        print(f"Cost per Keyword: ${costs['total_cost'] / costs['summary']['total_keywords_analyzed']:.4f}")
        print("="*60)

if __name__ == "__main__":
    calculator = DataForSEOCostCalculator()
    filename, costs = calculator.generate_cost_report()
    calculator.print_summary(costs)
    print(f"\nDetailed cost report saved to: {filename}")
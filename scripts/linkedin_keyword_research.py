#!/usr/bin/env python3
"""
LinkedIn and GTM Service Keyword Research
Uses DataForSEO API to research keywords for LinkedIn strategy and GTM services
"""

import requests
import base64
import json
from datetime import datetime
import statistics

# DataForSEO credentials from .env
LOGIN = "admin@locallyknown.pro"
PASSWORD = "74b1f60e9e023e5f"

# Encode credentials
credentials = base64.b64encode(f"{LOGIN}:{PASSWORD}".encode()).decode()

def get_keyword_data(keywords):
    """Get search volume and metrics for keywords"""
    
    url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
    
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }
    
    payload = [{
        "keywords": keywords,
        "location_code": 2840,  # United States
        "language_code": "en"
    }]
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None

def get_related_keywords(seed_keyword):
    """Get related keywords for a seed keyword"""
    
    url = "https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live"
    
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }
    
    payload = [{
        "keyword": seed_keyword,
        "location_code": 2840,
        "language_code": "en",
        "limit": 50,
        "filters": [
            ["keyword_data.keyword_info.search_volume", ">", 100]
        ]
    }]
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API Error: {e}")
        return None

def analyze_keywords():
    """Main analysis function"""
    
    print("=" * 80)
    print("LINKEDIN & GTM SERVICE KEYWORD RESEARCH")
    print("=" * 80)
    print()
    
    # LinkedIn Strategy Keywords
    linkedin_keywords = [
        "linkedin lead generation",
        "linkedin b2b marketing",
        "linkedin outreach strategy",
        "linkedin sales navigator",
        "linkedin content strategy",
        "linkedin authority building",
        "linkedin warm leads",
        "linkedin strategic visibility",
        "linkedin inbound marketing",
        "linkedin thought leadership"
    ]
    
    # GTM Service Keywords
    gtm_keywords = [
        "gtm setup service",
        "google tag manager consultant",
        "gtm implementation",
        "broken conversion tracking",
        "google ads tracking not working",
        "ga4 setup service",
        "conversion tracking fix",
        "gtm debugging service",
        "tag manager expert",
        "analytics tracking broken"
    ]
    
    # Combined strategic keywords
    strategic_keywords = [
        "b2b linkedin marketing agency",
        "linkedin ads conversion tracking",
        "linkedin pixel implementation",
        "b2b lead generation service",
        "marketing analytics consultant",
        "conversion tracking specialist",
        "revenue attribution service",
        "marketing data consultant"
    ]
    
    all_keywords = linkedin_keywords + gtm_keywords + strategic_keywords
    
    print(f"Analyzing {len(all_keywords)} keywords...")
    print(f"Estimated API cost: ${len(all_keywords) * 0.002:.2f}")
    print()
    
    # Get keyword data
    data = get_keyword_data(all_keywords)
    
    if not data:
        print("Error: No data returned from API")
        return
    
    print(f"API Response Status: {data.get('status_code')}")
    print(f"API Response Message: {data.get('status_message')}")
    
    if data.get("status_code") != 20000:
        print(f"Error fetching keyword data: {data}")
        return
    
    results = []
    
    print(f"Number of tasks: {len(data.get('tasks', []))}")
    
    for task in data.get("tasks", []):
        if task.get("result"):
            for item in task["result"]:
                # Check if item is the keyword data directly
                keyword = item.get("keyword", "")
                volume = int(item.get("search_volume", 0) if item.get("search_volume") is not None else 0)
                cpc = float(item.get("cpc", 0) if item.get("cpc") is not None else 0)
                
                # Convert competition text to numeric
                comp_text = item.get("competition", "LOW")
                if comp_text == "LOW":
                    competition = 0.25
                elif comp_text == "MEDIUM":
                    competition = 0.5
                elif comp_text == "HIGH":
                    competition = 0.75
                else:
                    competition = float(comp_text) if isinstance(comp_text, (int, float, str)) and comp_text != "" else 0.5
                    
                # Calculate opportunity score
                if volume > 0 and cpc > 0:
                    # High volume, high CPC, low competition = high opportunity
                    opportunity_score = (volume * cpc) / (competition + 0.1)
                else:
                    opportunity_score = 0
                
                if keyword:  # Only add if keyword exists
                    results.append({
                        "keyword": keyword,
                        "volume": volume,
                        "cpc": cpc,
                        "competition": competition,
                        "opportunity_score": opportunity_score,
                        "category": "LinkedIn" if keyword in linkedin_keywords else 
                                   "GTM" if keyword in gtm_keywords else "Strategic"
                    })
    
    # Sort by opportunity score
    results.sort(key=lambda x: x["opportunity_score"], reverse=True)
    
    # Display results by category
    print("TOP LINKEDIN STRATEGY KEYWORDS")
    print("-" * 80)
    print(f"{'Keyword':<40} {'Volume':>10} {'CPC':>10} {'Competition':>12} {'Opportunity':>12}")
    print("-" * 80)
    
    linkedin_results = [r for r in results if r["category"] == "LinkedIn"]
    for r in linkedin_results[:10]:
        print(f"{r['keyword']:<40} {r['volume']:>10,} ${r['cpc']:>9.2f} {r['competition']:>12.2f} {r['opportunity_score']:>12,.0f}")
    
    print()
    print("TOP GTM SERVICE KEYWORDS")
    print("-" * 80)
    print(f"{'Keyword':<40} {'Volume':>10} {'CPC':>10} {'Competition':>12} {'Opportunity':>12}")
    print("-" * 80)
    
    gtm_results = [r for r in results if r["category"] == "GTM"]
    for r in gtm_results[:10]:
        print(f"{r['keyword']:<40} {r['volume']:>10,} ${r['cpc']:>9.2f} {r['competition']:>12.2f} {r['opportunity_score']:>12,.0f}")
    
    print()
    print("TOP STRATEGIC COMBINATION KEYWORDS")
    print("-" * 80)
    print(f"{'Keyword':<40} {'Volume':>10} {'CPC':>10} {'Competition':>12} {'Opportunity':>12}")
    print("-" * 80)
    
    strategic_results = [r for r in results if r["category"] == "Strategic"]
    for r in strategic_results[:10]:
        print(f"{r['keyword']:<40} {r['volume']:>10,} ${r['cpc']:>9.2f} {r['competition']:>12.2f} {r['opportunity_score']:>12,.0f}")
    
    # Calculate insights
    print()
    print("KEY INSIGHTS")
    print("-" * 80)
    
    # Average metrics by category
    for category in ["LinkedIn", "GTM", "Strategic"]:
        cat_results = [r for r in results if r["category"] == category]
        if cat_results:
            avg_volume = statistics.mean([r["volume"] for r in cat_results])
            avg_cpc = statistics.mean([r["cpc"] for r in cat_results if r["cpc"] > 0])
            avg_competition = statistics.mean([r["competition"] for r in cat_results])
            
            print(f"\n{category} Keywords:")
            print(f"  Average Search Volume: {avg_volume:,.0f}")
            print(f"  Average CPC: ${avg_cpc:.2f}")
            print(f"  Average Competition: {avg_competition:.2f}")
    
    # Find sweet spot keywords (high volume, high CPC, low competition)
    sweet_spot = [r for r in results if r["volume"] > 500 and r["cpc"] > 5 and r["competition"] < 0.5]
    
    if sweet_spot:
        print()
        print("SWEET SPOT KEYWORDS (High Volume, High CPC, Low Competition)")
        print("-" * 80)
        for r in sweet_spot[:5]:
            print(f"- {r['keyword']}: {r['volume']:,} searches, ${r['cpc']:.2f} CPC, {r['competition']:.2f} competition")
    
    # Get related keywords for top opportunity
    related_data = None
    if results:
        top_keyword = results[0]["keyword"]
        print()
        print(f"EXPLORING RELATED KEYWORDS FOR: '{top_keyword}'")
        print("-" * 80)
        
        related_data = get_related_keywords(top_keyword)
        
        if related_data and related_data.get("status_code") == 20000:
            related_keywords = []
            
            for task in related_data.get("tasks", []):
                if task.get("result"):
                    for item in task["result"][:10]:
                        keyword_data = item.get("keyword_data", {})
                        keyword = keyword_data.get("keyword", "")
                        info = keyword_data.get("keyword_info", {})
                        
                        related_keywords.append({
                            "keyword": keyword,
                            "volume": info.get("search_volume", 0),
                            "cpc": info.get("cpc", 0)
                        })
            
            for r in related_keywords[:10]:
                print(f"- {r['keyword']}: {r['volume']:,} searches, ${r['cpc']:.2f} CPC")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/linkedin_gtm_keywords_{timestamp}.csv"
    
    with open(filename, "w") as f:
        f.write("Keyword,Volume,CPC,Competition,Opportunity Score,Category\n")
        for r in results:
            f.write(f"{r['keyword']},{r['volume']},{r['cpc']},{r['competition']},{r['opportunity_score']},{r['category']}\n")
    
    print()
    print(f"Results saved to: {filename}")
    
    # Calculate total API cost
    api_cost = len(all_keywords) * 0.002
    if related_data:
        api_cost += 0.01  # Related keywords cost
    
    print(f"Total API cost: ${api_cost:.3f}")

if __name__ == "__main__":
    analyze_keywords()
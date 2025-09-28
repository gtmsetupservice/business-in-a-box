#!/usr/bin/env python3
"""
GTM-Focused Keyword Research
Pure GTM, GA4, and conversion tracking keywords only
"""

import requests
import base64
import json
from datetime import datetime

# DataForSEO credentials
LOGIN = "admin@locallyknown.pro"
PASSWORD = "74b1f60e9e023e5f"
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

def analyze_gtm_keywords():
    """Analyze pure GTM and tracking keywords"""
    
    print("=" * 80)
    print("GTM SERVICE KEYWORD RESEARCH - TECHNICAL FOCUS")
    print("=" * 80)
    print()
    
    # Core GTM Keywords
    gtm_core = [
        "gtm consultant",
        "google tag manager consultant",
        "gtm expert",
        "gtm specialist", 
        "gtm freelancer",
        "gtm developer",
        "tag manager consultant",
        "tag manager expert",
        "gtm implementation service",
        "gtm setup service"
    ]
    
    # Tracking Problem Keywords
    tracking_problems = [
        "conversion tracking not working",
        "google ads conversion tracking broken",
        "facebook pixel not working",
        "analytics not tracking conversions",
        "gtm not firing",
        "tags not firing",
        "google analytics broken",
        "ga4 not working",
        "ecommerce tracking broken",
        "form tracking not working"
    ]
    
    # GTM Fix/Debug Keywords  
    gtm_fixes = [
        "fix gtm",
        "fix google tag manager",
        "gtm debugging",
        "gtm troubleshooting",
        "fix conversion tracking",
        "fix google analytics",
        "repair conversion tracking",
        "gtm audit",
        "tag manager audit",
        "gtm health check"
    ]
    
    # GA4 Specific
    ga4_keywords = [
        "ga4 consultant",
        "ga4 setup service",
        "ga4 implementation",
        "ga4 expert",
        "ga4 migration service",
        "universal analytics to ga4",
        "ga4 ecommerce setup",
        "ga4 conversion tracking",
        "ga4 configuration",
        "google analytics 4 consultant"
    ]
    
    # Technical Implementation
    technical_keywords = [
        "server side gtm",
        "server side tracking",
        "gtm container setup",
        "dataLayer implementation",
        "enhanced ecommerce tracking",
        "cross domain tracking",
        "gtm wordpress",
        "gtm shopify",
        "custom javascript gtm",
        "gtm api integration"
    ]
    
    all_keywords = gtm_core + tracking_problems + gtm_fixes + ga4_keywords + technical_keywords
    
    print(f"Analyzing {len(all_keywords)} GTM-focused keywords...")
    print(f"Estimated API cost: ${len(all_keywords) * 0.002:.2f}")
    print()
    
    # Get keyword data
    data = get_keyword_data(all_keywords)
    
    if not data:
        print("Error: No data returned from API")
        return
    
    if data.get("status_code") != 20000:
        print(f"API Error: {data.get('status_message')}")
        return
    
    results = []
    
    for task in data.get("tasks", []):
        if task.get("result"):
            for item in task["result"]:
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
                    competition = 0.5
                
                # Calculate opportunity score
                if volume > 0 and cpc > 0:
                    opportunity_score = (volume * cpc) / (competition + 0.1)
                else:
                    opportunity_score = 0
                
                # Determine category
                if keyword in gtm_core:
                    category = "GTM Core"
                elif keyword in tracking_problems:
                    category = "Tracking Problems"
                elif keyword in gtm_fixes:
                    category = "GTM Fixes"
                elif keyword in ga4_keywords:
                    category = "GA4"
                elif keyword in technical_keywords:
                    category = "Technical"
                else:
                    category = "Other"
                
                if keyword:
                    results.append({
                        "keyword": keyword,
                        "volume": volume,
                        "cpc": cpc,
                        "competition": competition,
                        "opportunity_score": opportunity_score,
                        "category": category
                    })
    
    # Sort by opportunity score
    results.sort(key=lambda x: x["opportunity_score"], reverse=True)
    
    # Display results
    print("TOP GTM SERVICE OPPORTUNITIES")
    print("-" * 100)
    print(f"{'Keyword':<45} {'Volume':>10} {'CPC':>10} {'Competition':>12} {'Opportunity':>12}")
    print("-" * 100)
    
    for r in results[:20]:
        if r["volume"] > 0:  # Only show keywords with search volume
            print(f"{r['keyword']:<45} {r['volume']:>10,} ${r['cpc']:>9.2f} {r['competition']:>12.2f} {r['opportunity_score']:>12,.0f}")
    
    # Category breakdown
    print()
    print("CATEGORY BREAKDOWN")
    print("-" * 100)
    
    for category in ["GTM Core", "Tracking Problems", "GTM Fixes", "GA4", "Technical"]:
        cat_results = [r for r in results if r["category"] == category and r["volume"] > 0]
        if cat_results:
            total_volume = sum([r["volume"] for r in cat_results])
            avg_cpc = sum([r["cpc"] for r in cat_results]) / len(cat_results) if cat_results else 0
            print(f"\n{category}:")
            print(f"  Keywords with volume: {len(cat_results)}")
            print(f"  Total search volume: {total_volume:,}")
            print(f"  Average CPC: ${avg_cpc:.2f}")
            print(f"  Top keyword: {cat_results[0]['keyword']} ({cat_results[0]['volume']:,} searches)")
    
    # High-value keywords (high CPC)
    high_value = [r for r in results if r["cpc"] > 20]
    if high_value:
        print()
        print("HIGH-VALUE KEYWORDS (CPC > $20)")
        print("-" * 100)
        for r in high_value[:10]:
            print(f"{r['keyword']}: ${r['cpc']:.2f} CPC, {r['volume']:,} searches")
    
    # Emergency/urgent keywords
    urgent_keywords = [r for r in results if any(word in r["keyword"].lower() for word in ["broken", "not working", "fix", "repair"])]
    if urgent_keywords:
        print()
        print("URGENT/EMERGENCY KEYWORDS (High Intent)")
        print("-" * 100)
        for r in urgent_keywords[:10]:
            if r["volume"] > 0:
                print(f"{r['keyword']}: {r['volume']:,} searches, ${r['cpc']:.2f} CPC")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/gtm_focused_keywords_{timestamp}.csv"
    
    with open(filename, "w") as f:
        f.write("Keyword,Volume,CPC,Competition,Opportunity Score,Category\n")
        for r in results:
            f.write(f"{r['keyword']},{r['volume']},{r['cpc']},{r['competition']},{r['opportunity_score']},{r['category']}\n")
    
    print()
    print(f"Results saved to: {filename}")
    print(f"Total API cost: ${len(all_keywords) * 0.002:.3f}")

if __name__ == "__main__":
    analyze_gtm_keywords()
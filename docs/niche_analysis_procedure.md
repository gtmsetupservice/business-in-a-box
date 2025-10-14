# DataForSEO Niche Analysis Procedure

## Overview

This procedure outlines the comprehensive methodology for conducting evidence-based niche analysis using the DataForSEO API. This process was developed and refined through the WebsiteROIfix.com analysis project.

## Prerequisites

### Required Accounts & Setup
- DataForSEO API account with active credentials
- Python 3.7+ environment
- Required libraries: `requests`, `base64`, `json`, `csv`, `datetime`

### API Credentials
```python
login = "your_dataforseo_login"
password = "your_dataforseo_password"
```

## Step-by-Step Procedure

### Phase 1: Initial Setup & Planning

#### 1.1 Define Target Keywords
- Start with 10-20 keywords related to your niche
- Include both broad and specific terms
- Consider service-based vs product-based keywords

**Example Keyword Categories:**
```
Core Service Terms:
- "analytics consulting"
- "website analytics services"
- "data analysis"

Specific Service Terms:
- "website data analysis"
- "data analytics expertise"
- "site analytics services"

ROI/Value Terms:
- "analytics ROI"
- "profitable analytics"
- "analytics return on investment"
```

#### 1.2 Set Location Parameters
```python
location_code = 2840  # United States
location_name = "United States"
```

### Phase 2: Data Collection

#### 2.1 Keywords Data Collection
**API Endpoint:** `/v3/keywords_data/google_ads/search_volume/live`

**Request Parameters:**
```json
{
  "search_partners": false,
  "keywords": ["keyword1", "keyword2", ...],
  "location_code": 2840,
  "language_code": "en",
  "sort_by": "search_volume",
  "include_adult_keywords": false
}
```

**Cost:** $0.002 per keyword

#### 2.2 SERP Analysis
**API Endpoint:** `/v3/serp/google/organic/live/advanced`

**For each high-volume keyword (>50 searches):**
```json
{
  "keyword": "target_keyword",
  "location_code": 2840,
  "language_code": "en",
  "device": "desktop",
  "os": "windows",
  "depth": 100
}
```

**Cost:** $0.006 per request

### Phase 3: Data Analysis

#### 3.1 Keyword Filtering & Prioritization
**Filter criteria:**
- Minimum search volume: 10+ monthly searches
- Maximum CPC threshold: Set based on budget
- Competition level assessment

**Priority scoring:**
1. Search volume (higher = better)
2. CPC cost (lower = better)
3. Competition index (lower = better)

#### 3.2 CPA Calculations
**Formula:**
```
CPA = (Monthly Clicks × CPC) / Expected Conversions

Where:
- Monthly Clicks = Search Volume × CTR
- CTR = 35% (positions 1-3) or 15% (positions 4-10)
- Conversion Rate = 2.5% (B2B services industry standard)
```

#### 3.3 Competitive Analysis
**For each priority keyword:**
- Identify top 10 organic competitors
- Estimate domain authority (High/Medium/Low)
- Document SERP features present
- Calculate SEO difficulty score

**Domain Authority Estimation:**
- High (70-100): Wikipedia, LinkedIn, major brands
- Medium (40-69): Industry blogs, consulting sites
- Low (0-39): Small businesses, new domains

### Phase 4: Financial Modeling

#### 4.1 Revenue Projections
**Service Pricing Assumptions:**
```python
avg_project_value = 4000      # One-time projects
monthly_retainer_rate = 1800  # Ongoing services
project_conversion_rate = 0.3  # 30% of leads → projects
retainer_conversion_rate = 0.15 # 15% → monthly clients
```

#### 4.2 ROI Calculations
```python
monthly_revenue = (conversions × project_rate × project_value) + 
                 (conversions × retainer_rate × monthly_retainer)
roi_percentage = ((monthly_revenue - monthly_ad_spend) / monthly_ad_spend) × 100
```

### Phase 5: Decision Framework

#### 5.1 Scoring Matrix
**Niche Attractiveness Score (0-10):**
- Market Volume: `min(10, total_search_volume / 500)`
- Keyword Diversity: `min(10, keywords_with_volume × 2)`
- Competition Level: `10 - (avg_difficulty_score / 10)`
- ROI Potential: `min(10, roi_percentage / 20)`

#### 5.2 Decision Thresholds
- **8.0+ Score:** HIGHLY RECOMMENDED - Proceed with confidence
- **6.0-7.9:** RECOMMENDED - Good opportunity, proceed with strategy
- **4.0-5.9:** MARGINAL - Proceed with caution, focused approach
- **Below 4.0:** NOT RECOMMENDED - Consider alternative niches

### Phase 6: Quality Control & Validation

#### 6.1 Outlier Detection
**Critical Check:** Identify high-CPA outliers that skew analysis
- Calculate CPA range and identify outliers (>3x median)
- Run analysis with and without outliers
- Document impact on overall metrics

#### 6.2 Assumption Validation
**Validate key assumptions:**
- Industry conversion rates
- Service pricing models
- Competition assessment accuracy
- Market size estimations

### Phase 7: Reporting & Documentation

#### 7.1 Executive Summary Format
```
Overall Niche Attractiveness Score: X.X/10
Projected CPA Range: $XXX - $XXX
Profitability Assessment: [PROFITABLE/MARGINAL/NOT RECOMMENDED]

Score Breakdown:
• Market Volume: X.X/10
• Keyword Diversity: X.X/10  
• Competition Level: X.X/10
• ROI Potential: X.X/10
```

#### 7.2 Required Report Sections
1. **Executive Summary**
2. **Keyword Analysis** (detailed metrics table)
3. **Competitive Landscape** (top competitors, difficulty)
4. **Paid Advertising Assessment** (CPC, budget, ROI)
5. **Organic Search Potential** (difficulty, timeline)
6. **Conversion Funnel Analysis** (rates, CAC, projections)
7. **Recommendations** (go/no-go, priority keywords, strategy)

### Phase 8: Cost Management

#### 8.1 API Cost Tracking
**Typical Project Costs:**
- Initial analysis (10 keywords + 1 SERP): ~$0.026
- Comprehensive analysis (15 keywords + 3 SERPs): ~$0.048
- **Total project cost: ~$0.15 for 50+ keywords analyzed**

#### 8.2 Cost Optimization Tips
- Batch keyword requests (up to 50 per call)
- Limit SERP analysis to top 3-5 keywords
- Use location filtering to avoid unnecessary requests

## Quality Assurance Checklist

### Before Starting Analysis:
- [ ] Keywords list is comprehensive and relevant
- [ ] API credentials are valid and have sufficient balance
- [ ] Location targeting is appropriate for business
- [ ] Industry benchmarks are researched and documented

### During Analysis:
- [ ] All API responses are properly validated
- [ ] Error handling is in place for failed requests
- [ ] Data is being stored in structured format
- [ ] Intermediate results are being validated

### After Analysis:
- [ ] Outlier keywords identified and impact assessed
- [ ] All assumptions are clearly documented
- [ ] Results are compared against industry benchmarks
- [ ] Cost tracking is complete and accurate
- [ ] Reports are generated in standardized format

## Common Pitfalls & Solutions

### Pitfall 1: High-CPA Outliers
**Problem:** Single expensive keyword skews entire analysis
**Solution:** Always run analysis with and without outliers

### Pitfall 2: Overestimating Conversion Rates
**Problem:** Using optimistic conversion assumptions
**Solution:** Use conservative industry benchmarks (2.5% for B2B)

### Pitfall 3: Ignoring Competition Context
**Problem:** Focusing only on search volume and CPC
**Solution:** Always analyze SERP competitors and features

### Pitfall 4: Inadequate Budget Planning
**Problem:** Underestimating required ad spend
**Solution:** Calculate minimum viable budget for meaningful results

## File Organization

```
project_directory/
├── docs/
│   ├── niche_analysis_procedure.md
│   └── api_documentation.md
├── reports/
│   ├── comprehensive_analysis_YYYYMMDD_HHMMSS.txt
│   ├── keyword_data_YYYYMMDD_HHMMSS.csv
│   ├── api_costs_YYYYMMDD_HHMMSS.txt
│   └── comparison_reports.txt
├── scripts/
│   ├── comprehensive_niche_report.py
│   ├── keyword_analyzer.py
│   └── cost_calculator.py
└── CLAUDE.md
```

## Success Metrics

### Process Success:
- Analysis completed within budget (<$0.50 for comprehensive study)
- All key metrics calculated with documented assumptions
- Clear go/no-go recommendation with supporting data

### Business Success:
- Avoided unprofitable niches (negative ROI identification)
- Identified profitable opportunities (>100% ROI potential)
- Provided actionable keyword and budget recommendations

---

## Revision History

**v1.0** - Initial procedure based on WebsiteROIfix.com analysis
**Date:** 2025-08-28
**Author:** Analysis developed through Claude Code
**Cost:** $0.15 total for complete methodology development
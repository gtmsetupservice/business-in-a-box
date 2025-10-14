# Niche Analysis Tool - Usage Guide

## Quick Start

### Prerequisites
1. DataForSEO API account with credentials
2. Python 3.7+ installed
3. Required libraries: `requests` (install with `pip install requests`)

### Basic Usage

```bash
python scripts/niche_analyzer.py \
  --keywords "analytics consulting" "website analytics" "data analysis" \
  --niche-name "analytics-services" \
  --login "your_dataforseo_login" \
  --password "your_dataforseo_password"
```

## Command Line Arguments

### Required Arguments
- `--keywords`: Space-separated list of keywords to analyze
- `--niche-name`: Name for the niche (used in file names)
- `--login`: Your DataForSEO API login
- `--password`: Your DataForSEO API password

### Optional Arguments
- `--output-dir`: Directory for output files (default: `reports`)
- `--no-competition`: Skip competitive analysis to save costs

## Example Usage Scenarios

### 1. Quick Analysis (Keywords Only)
```bash
python scripts/niche_analyzer.py \
  --keywords "seo consulting" "seo services" "search optimization" \
  --niche-name "seo-consulting" \
  --login "admin@example.com" \
  --password "your_password" \
  --no-competition
```
**Cost:** ~$0.006 for 3 keywords

### 2. Full Analysis with Competition
```bash
python scripts/niche_analyzer.py \
  --keywords "web development" "website design" "custom websites" "web apps" \
  --niche-name "web-development" \
  --login "admin@example.com" \
  --password "your_password"
```
**Cost:** ~$0.026 (4 keywords + 3 SERP analyses)

### 3. Large Keyword Set
```bash
python scripts/niche_analyzer.py \
  --keywords "marketing consulting" "digital marketing" "marketing strategy" \
           "marketing automation" "marketing analytics" "marketing roi" \
           "marketing optimization" "marketing campaigns" \
  --niche-name "marketing-consulting" \
  --login "admin@example.com" \
  --password "your_password"
```
**Cost:** ~$0.034 (8 keywords + 3 SERP analyses)

## Output Files

The tool generates two files in the specified output directory:

### 1. Keyword Details (CSV)
**Format:** `{niche-name}_keywords_{timestamp}.csv`

**Contains:**
- Keyword
- Search volume
- CPC
- Competition index
- Estimated clicks
- Estimated conversions
- Monthly spend
- CPA

### 2. Analysis Report (TXT)
**Format:** `{niche-name}_analysis_{timestamp}.txt`

**Contains:**
- Executive summary with niche score
- Score breakdown by category
- Top keywords ranked by volume
- Competitive analysis (if enabled)
- Financial projections
- Go/no-go recommendation

## Interpreting Results

### Niche Attractiveness Score
- **8.0-10.0:** Highly Recommended - Strong opportunity
- **6.0-7.9:** Recommended - Good opportunity with strategy
- **4.0-5.9:** Marginal - Proceed with caution
- **0.0-3.9:** Not Recommended - Consider alternatives

### ROI Interpretation
- **>200%:** Excellent opportunity
- **100-200%:** Very good opportunity
- **50-100%:** Good opportunity with proper execution
- **0-50%:** Marginal opportunity
- **<0%:** Unprofitable - avoid

### Budget Guidelines
- **<$1,000/month:** Accessible for small businesses
- **$1,000-$5,000/month:** Moderate investment required
- **$5,000-$15,000/month:** Significant investment needed
- **>$15,000/month:** High-investment niche

## Cost Management

### Typical Costs by Analysis Size
- **10 keywords, no competition:** $0.02
- **15 keywords + competition:** $0.048
- **25 keywords + competition:** $0.068
- **50 keywords + competition:** $0.118

### Cost Optimization Tips
1. **Group related keywords:** Analyze similar niches together
2. **Skip competition for quick validation:** Use `--no-competition` flag
3. **Start small:** Begin with 5-10 core keywords
4. **Batch similar analyses:** Analyze related niches in same session

## Advanced Usage

### Environment Variables
Set credentials as environment variables for security:

```bash
export DATAFORSEO_LOGIN="your_login"
export DATAFORSEO_PASSWORD="your_password"

python scripts/niche_analyzer.py \
  --keywords "keyword1" "keyword2" \
  --niche-name "test-niche" \
  --login "$DATAFORSEO_LOGIN" \
  --password "$DATAFORSEO_PASSWORD"
```

### Automation Scripts
Create a batch analysis script:

```bash
#!/bin/bash
# batch_analysis.sh

NICHES=(
  "seo-consulting:seo consulting,seo services,seo optimization"
  "web-development:web development,website design,web apps"
  "digital-marketing:digital marketing,online marketing,marketing strategy"
)

for niche_data in "${NICHES[@]}"; do
  niche_name=$(echo $niche_data | cut -d: -f1)
  keywords=$(echo $niche_data | cut -d: -f2 | tr ',' ' ')
  
  python scripts/niche_analyzer.py \
    --keywords $keywords \
    --niche-name "$niche_name" \
    --login "$DATAFORSEO_LOGIN" \
    --password "$DATAFORSEO_PASSWORD"
done
```

## Troubleshooting

### Common Issues

#### 1. API Authentication Error
```
Error: API returned status code 401
```
**Solution:** Check your DataForSEO login credentials

#### 2. Insufficient Balance
```
Error: API returned status code 40001
```
**Solution:** Add funds to your DataForSEO account

#### 3. No Data Found
```
No keyword data found.
```
**Solution:** Check if keywords are valid and have search volume

#### 4. Rate Limiting
```
Error: API returned status code 429
```
**Solution:** Wait a moment and retry, or contact DataForSEO support

### Debugging
Enable verbose output by modifying the script to print API responses:

```python
# Add after API response
print("API Response:", response.text)
```

## Best Practices

### Keyword Selection
1. **Include variations:** Use plural/singular forms
2. **Mix broad and specific:** Combine general and niche-specific terms
3. **Consider user intent:** Include both informational and commercial terms
4. **Geographic relevance:** Add location-based keywords if applicable

### Analysis Frequency
- **Initial research:** Comprehensive analysis with competition
- **Quick validation:** Keywords-only analysis
- **Competitive updates:** Monthly SERP analysis for top keywords
- **Market changes:** Full re-analysis quarterly

### Data Management
1. **Organize by date:** Use timestamped file names
2. **Archive old reports:** Move to dated folders
3. **Compare over time:** Track niche evolution
4. **Document assumptions:** Note any custom parameters used

## Support & Resources

### Getting Help
- **DataForSEO API Docs:** https://docs.dataforseo.com/
- **Pricing Information:** https://dataforseo.com/apis/pricing
- **Technical Support:** support@dataforseo.com

### Extending the Tool
The analyzer is designed to be modular. Common extensions:
- **Custom industry benchmarks:** Modify conversion rates
- **Additional metrics:** Add keyword difficulty scoring
- **Export formats:** Add JSON or Excel output
- **Visualization:** Generate charts and graphs
- **Alerting:** Email reports automatically

---

**Last Updated:** 2025-08-28
**Version:** 1.0
**Tested With:** DataForSEO API v3, Python 3.8+
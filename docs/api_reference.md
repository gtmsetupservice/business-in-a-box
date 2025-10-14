# DataForSEO API Reference for Niche Analysis

## API Endpoints Used

### 1. Keywords Data API
**Endpoint:** `https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live`

**Method:** POST

**Cost:** $0.002 per keyword

**Purpose:** Get search volume, CPC, and competition data for keywords

**Request Format:**
```json
[{
  "search_partners": false,
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "location_code": 2840,
  "language_code": "en",
  "sort_by": "search_volume",
  "include_adult_keywords": false
}]
```

**Response Fields Used:**
- `keyword`: The analyzed keyword
- `search_volume`: Monthly search volume
- `cpc`: Average cost per click
- `competition`: Competition level (LOW/MEDIUM/HIGH)
- `competition_index`: Numeric competition score (0-100)
- `monthly_searches`: Historical monthly data

### 2. SERP Analysis API
**Endpoint:** `https://api.dataforseo.com/v3/serp/google/organic/live/advanced`

**Method:** POST

**Cost:** $0.006 per request

**Purpose:** Analyze organic search results and competitors

**Request Format:**
```json
[{
  "keyword": "target keyword",
  "location_code": 2840,
  "language_code": "en",
  "device": "desktop",
  "os": "windows",
  "depth": 100
}]
```

**Response Fields Used:**
- `items[].type`: Result type (organic, local_pack, etc.)
- `items[].domain`: Competitor domain
- `items[].title`: Result title
- `items[].rank_position`: Position in results
- `items[].url`: Result URL
- `items[].description`: Meta description

### 3. Locations API (Optional)
**Endpoint:** `https://api.dataforseo.com/v3/serp/google/locations/us`

**Method:** GET

**Cost:** $0.0001 per request

**Purpose:** Get location codes for geographic targeting

## Authentication

**Method:** Basic Authentication

**Format:**
```python
credentials = base64.b64encode(f"{login}:{password}".encode()).decode()
headers = {
    'Authorization': f'Basic {credentials}',
    'Content-Type': 'application/json'
}
```

## Rate Limits & Best Practices

### Rate Limits
- Keywords API: Up to 50 keywords per request
- SERP API: 1 request per keyword
- No strict rate limiting, but costs accumulate per request

### Optimization Tips
1. **Batch Keywords:** Always send maximum keywords per request
2. **Selective SERP Analysis:** Only analyze top 3-5 keywords
3. **Error Handling:** Implement retry logic for failed requests
4. **Cost Monitoring:** Track API costs throughout analysis

## Error Handling

### Common Error Responses
```json
{
  "status_code": 40001,
  "status_message": "Insufficient balance",
  "tasks": []
}
```

### Error Handling Strategy
```python
if response.status_code != 200:
    print(f"Error: API returned status code {response.status_code}")
    print(response.text)
    return None

if 'tasks' not in result_json or not result_json['tasks']:
    print("No data found in API response")
    return None
```

## Sample Code Implementation

### Keywords Analysis Function
```python
def get_keyword_data(keywords, location_code=2840):
    url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
    
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }
    
    payload = json.dumps([{
        "search_partners": False,
        "keywords": keywords,
        "location_code": location_code,
        "language_code": "en",
        "sort_by": "search_volume",
        "include_adult_keywords": False
    }])
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code != 200:
        return None
    
    result_json = response.json()
    
    if 'tasks' not in result_json or not result_json['tasks']:
        return None
    
    return result_json['tasks'][0]['result']
```

### SERP Analysis Function
```python
def analyze_serp(keyword, location_code=2840):
    url = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
    
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }
    
    payload = json.dumps([{
        "keyword": keyword,
        "location_code": location_code,
        "language_code": "en",
        "device": "desktop",
        "os": "windows",
        "depth": 100
    }])
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code != 200:
        return None
    
    result_json = response.json()
    
    if 'tasks' not in result_json or not result_json['tasks']:
        return None
    
    return result_json['tasks'][0]['result']
```

## Location Codes Reference

### Common US Locations
- **United States (National):** 2840
- **California:** 1012
- **New York:** 1023
- **Texas:** 1001
- **Florida:** 1009

### Finding Location Codes
Use the locations endpoint to find specific codes:
```
GET https://api.dataforseo.com/v3/serp/google/locations/us
```

## Data Processing Guidelines

### Keyword Data Processing
```python
for kw in keyword_data:
    search_volume = kw.get('search_volume', 0) or 0
    cpc = kw.get('cpc', 0) or 0
    competition_index = kw.get('competition_index', 0) or 0
    
    # Handle None values that can break calculations
    if search_volume is None: search_volume = 0
    if cpc is None: cpc = 0
```

### SERP Data Processing
```python
competitors = []
serp_features = set()

for item in serp_result:
    if 'items' in item:
        for result in item['items']:
            if 'type' in result:
                serp_features.add(result['type'])
            
            if result.get('type') == 'organic':
                competitors.append({
                    'domain': result.get('domain'),
                    'position': result.get('rank_position'),
                    'title': result.get('title')
                })
```

## Cost Calculation

### API Cost Tracking
```python
def calculate_api_costs(keywords_count, serp_requests):
    keywords_cost = keywords_count * 0.002
    serp_cost = serp_requests * 0.006
    total_cost = keywords_cost + serp_cost
    
    return {
        'keywords_cost': keywords_cost,
        'serp_cost': serp_cost,
        'total_cost': total_cost
    }
```

### Typical Project Costs
- **10 keywords + 1 SERP:** $0.026
- **20 keywords + 3 SERPs:** $0.058
- **50 keywords + 5 SERPs:** $0.130

## Response Time & Performance

### Expected Response Times
- **Keywords API:** 1-3 seconds for 50 keywords
- **SERP API:** 2-5 seconds per request
- **Locations API:** <1 second

### Optimization for Speed
1. Use concurrent requests where possible
2. Implement connection pooling
3. Cache location data
4. Process results incrementally

## Documentation & Support

### Official Documentation
- DataForSEO API Documentation: https://docs.dataforseo.com/
- Pricing: https://dataforseo.com/apis/pricing
- Support: support@dataforseo.com

### Code Examples Repository
All working code examples are available in the project's `scripts/` directory.

---

**Last Updated:** 2025-08-28
**API Version:** v3
**Tested With:** DataForSEO production environment
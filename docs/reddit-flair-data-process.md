# Process to Retrieve Full Reddit Flair Data

## Overview
The current Reddit MCP tool returns simplified data without flair information. To get complete flair data from r/GoogleTagManager posts, we need to use Reddit's official API directly.

---

## Prerequisites

### 1. Reddit API Credentials
- **Reddit Account** with verified email
- **Reddit App Registration** at https://www.reddit.com/prefs/apps
- **Client ID** (found under app name)
- **Client Secret** (shown when creating app)
- **User Agent** string (required for all API calls)

### 2. API Access Type
- **Script App** - For personal use, authenticated as yourself
- **Web App** - For production use with OAuth flow
- **Installed App** - For desktop applications

---

## Process Steps

### Step 1: Register Reddit Application
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - **Name**: GTM_Flair_Analyzer
   - **App type**: Script (for testing)
   - **Description**: Analyze GTM subreddit post flairs
   - **About URL**: (leave blank for script)
   - **Redirect URI**: http://localhost:8080 (for script)
4. Save Client ID and Secret

### Step 2: Authentication Setup
```python
import requests
import base64

# Reddit API credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
USERNAME = 'your_reddit_username'
PASSWORD = 'your_reddit_password'
USER_AGENT = 'GTMFlairAnalyzer/1.0 by YourUsername'

# Get access token
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
data = {
    'grant_type': 'password',
    'username': USERNAME,
    'password': PASSWORD
}
headers = {'User-Agent': USER_AGENT}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
```

### Step 3: Retrieve Posts with Flair Data
```python
# Setup authenticated headers
headers = {
    'Authorization': f'bearer {TOKEN}',
    'User-Agent': USER_AGENT
}

# Get posts from r/GoogleTagManager
response = requests.get(
    'https://oauth.reddit.com/r/GoogleTagManager/new',
    headers=headers,
    params={'limit': 25}
)

posts_data = response.json()
```

### Step 4: Extract Complete Flair Information
```python
for post in posts_data['data']['children']:
    post_data = post['data']
    
    flair_info = {
        'title': post_data['title'],
        'author': post_data['author'],
        'created_utc': post_data['created_utc'],
        'score': post_data['score'],
        'num_comments': post_data['num_comments'],
        'url': post_data['url'],
        
        # FLAIR DATA FIELDS
        'link_flair_text': post_data.get('link_flair_text'),
        'link_flair_css_class': post_data.get('link_flair_css_class'),
        'link_flair_type': post_data.get('link_flair_type'),
        'link_flair_template_id': post_data.get('link_flair_template_id'),
        'link_flair_text_color': post_data.get('link_flair_text_color'),
        'link_flair_background_color': post_data.get('link_flair_background_color'),
        
        # Author flair
        'author_flair_text': post_data.get('author_flair_text'),
        'author_flair_css_class': post_data.get('author_flair_css_class'),
        
        # Post metadata
        'is_self': post_data['is_self'],
        'selftext': post_data.get('selftext', ''),
        'distinguished': post_data.get('distinguished'),
        'stickied': post_data['stickied'],
        'locked': post_data['locked']
    }
```

---

## Expected JSON Response Structure

```json
{
  "kind": "Listing",
  "data": {
    "children": [
      {
        "kind": "t3",
        "data": {
          "title": "How to push to datalayer if form directs upon submit?",
          "name": "t3_1n8kf91",
          "author": "Ok-Violinist-6760",
          "created_utc": 1725538560,
          "score": 1,
          "num_comments": 10,
          "permalink": "/r/GoogleTagManager/comments/1n8kf91/...",
          "url": "https://reddit.com/r/GoogleTagManager/comments/1n8kf91/...",
          "selftext": "If a form redirects to another page...",
          
          "link_flair_text": "Question",
          "link_flair_css_class": "question",
          "link_flair_type": "text",
          "link_flair_template_id": "abc123",
          "link_flair_text_color": "dark",
          "link_flair_background_color": "#46d160",
          
          "author_flair_text": "GTM Certified",
          "author_flair_css_class": "certified",
          "author_flair_template_id": "def456",
          
          "is_self": true,
          "distinguished": null,
          "stickied": false,
          "locked": false,
          "subreddit": "GoogleTagManager",
          "subreddit_id": "t5_2sukd"
        }
      }
    ]
  }
}
```

---

## Common Flair Types in r/GoogleTagManager

Based on typical technical subreddit patterns, expect flairs like:

### Post Flairs
- **Question** - Asking for help
- **Discussion** - General discussion topics
- **Tutorial** - Educational content
- **News** - GTM updates/announcements
- **Solved** - Questions that have been answered
- **Bug** - Reporting GTM issues
- **Resource** - Sharing useful links/tools

### Author Flairs
- **Beginner** - New to GTM
- **Intermediate** - Some experience
- **Expert** - Advanced knowledge
- **Certified** - Google certified
- **Developer** - Technical implementation focus

---

## Rate Limiting & Best Practices

### Reddit API Limits
- **60 requests per minute** for OAuth authenticated requests
- **30 requests per minute** for non-OAuth requests
- Always include User-Agent header
- Respect 429 (Too Many Requests) responses

### Implementation Tips
1. **Cache responses** to avoid repeated API calls
2. **Use pagination** with `after` parameter for large datasets
3. **Store flair templates** separately (they rarely change)
4. **Batch process** posts rather than real-time fetching

---

## Alternative: PRAW (Python Reddit API Wrapper)

For easier implementation, use PRAW:

```python
import praw

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=USERNAME,
    password=PASSWORD
)

subreddit = reddit.subreddit('GoogleTagManager')

for submission in subreddit.new(limit=25):
    print(f"Title: {submission.title}")
    print(f"Flair: {submission.link_flair_text}")
    print(f"Author Flair: {submission.author_flair_text}")
    print("---")
```

---

## Data Analysis Opportunities

Once you have flair data, you can:

1. **Categorize problems** - Which flairs indicate need for professional help
2. **Track trends** - Are "Question" flairs increasing?
3. **Identify experts** - Users with "Expert" or "Certified" flairs
4. **Response patterns** - Which flairs get most engagement
5. **Content gaps** - What questions aren't getting "Solved" flairs

This data can inform your content strategy and help identify high-value prospects who need GTM help.
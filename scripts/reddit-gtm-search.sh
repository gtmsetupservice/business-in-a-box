#!/bin/bash

# Reddit GTM Search Script
# Searches Reddit for Google Tag Manager content and parses with jq

set -e

# Configuration
USER_AGENT="GTMSearch/1.0"
SEARCH_QUERY="google+tag+manager"
LIMIT=25
SORT="new"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -s, --subreddit SUBREDDIT  Search specific subreddit (default: all)"
    echo "  -l, --limit NUMBER         Limit results (default: 25, max: 100)"
    echo "  -o, --sort METHOD          Sort by: new|hot|top|relevance (default: new)"
    echo "  -a, --auth                 Use authenticated request (requires env vars)"
    echo "  -h, --help                 Show this help message"
    echo ""
    echo "Environment variables for authenticated requests:"
    echo "  REDDIT_CLIENT_ID"
    echo "  REDDIT_CLIENT_SECRET"
    echo "  REDDIT_USERNAME"
    echo "  REDDIT_PASSWORD"
    exit 1
}

# Function to get Reddit access token
get_access_token() {
    if [[ -z "$REDDIT_CLIENT_ID" || -z "$REDDIT_CLIENT_SECRET" || -z "$REDDIT_USERNAME" || -z "$REDDIT_PASSWORD" ]]; then
        echo -e "${RED}Error: Missing Reddit credentials in environment variables${NC}"
        echo "Required: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD"
        exit 1
    fi

    echo -e "${YELLOW}Getting Reddit access token...${NC}"
    
    TOKEN_RESPONSE=$(curl -s -X POST \
        -d "grant_type=password&username=$REDDIT_USERNAME&password=$REDDIT_PASSWORD" \
        --user "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" \
        -H "User-Agent: $USER_AGENT" \
        https://www.reddit.com/api/v1/access_token)
    
    ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')
    
    if [[ "$ACCESS_TOKEN" == "null" || -z "$ACCESS_TOKEN" ]]; then
        echo -e "${RED}Error: Failed to get access token${NC}"
        echo "Response: $TOKEN_RESPONSE"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Access token obtained${NC}"
}

# Function to search Reddit (non-authenticated)
search_reddit_basic() {
    local url="https://www.reddit.com"
    
    if [[ -n "$SUBREDDIT" ]]; then
        url="$url/r/$SUBREDDIT"
    fi
    
    url="$url/search.json?q=google+tag+manager&sort=$SORT&limit=$LIMIT"
    
    if [[ -n "$SUBREDDIT" ]]; then
        url="$url&restrict_sr=1"
    fi
    
    echo -e "${YELLOW}Searching Reddit (basic): $url${NC}"
    
    curl -s -H "User-Agent: $USER_AGENT" "$url"
}

# Function to search Reddit (authenticated)
search_reddit_auth() {
    local url="https://oauth.reddit.com"
    
    if [[ -n "$SUBREDDIT" ]]; then
        url="$url/r/$SUBREDDIT"
    fi
    
    url="$url/search?q=$SEARCH_QUERY&sort=$SORT&limit=$LIMIT"
    
    if [[ -n "$SUBREDDIT" ]]; then
        url="$url&restrict_sr=1"
    fi
    
    echo -e "${YELLOW}Searching Reddit (authenticated): $url${NC}"
    
    curl -s -H "Authorization: bearer $ACCESS_TOKEN" \
         -H "User-Agent: $USER_AGENT" \
         "$url"
}

# Function to parse and display results
parse_results() {
    local json_data="$1"
    
    # Debug: Show raw response
    echo -e "${YELLOW}Debug - Raw API Response:${NC}"
    echo "$json_data" | head -5
    echo ""
    
    # Check if response is valid JSON
    if ! echo "$json_data" | jq . > /dev/null 2>&1; then
        echo -e "${RED}Error: Invalid JSON response from Reddit API${NC}"
        echo "Full response:"
        echo "$json_data"
        return
    fi
    
    # Check if we have valid data
    local post_count=$(echo "$json_data" | jq -r '.data.children | length')
    
    if [[ "$post_count" == "0" || "$post_count" == "null" ]]; then
        echo -e "${RED}No results found or API error${NC}"
        echo "Raw response:"
        echo "$json_data" | jq .
        return
    fi
    
    echo -e "\n${GREEN}Found $post_count posts:${NC}\n"
    
    # Parse each post
    echo "$json_data" | jq -r '
        .data.children[] | 
        .data | 
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" +
        "📝 \(.title)\n" +
        "👤 Author: u/\(.author)\n" +
        "📊 Score: \(.score) | 💬 Comments: \(.num_comments)\n" +
        "📅 Posted: \(.created_utc | strftime("%Y-%m-%d %H:%M:%S"))\n" +
        "🏷️  Post Flair: \(.link_flair_text // "None")\n" +
        "👥 Author Flair: \(.author_flair_text // "None")\n" +
        "🏠 Subreddit: r/\(.subreddit)\n" +
        "🔗 URL: \(.url)\n" +
        if .selftext != "" then "📄 Text: \(.selftext[:200])...\n" else "" end
    '
}

# Parse command line arguments
SUBREDDIT=""
USE_AUTH=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--subreddit)
            SUBREDDIT="$2"
            shift 2
            ;;
        -l|--limit)
            LIMIT="$2"
            shift 2
            ;;
        -o|--sort)
            SORT="$2"
            shift 2
            ;;
        -a|--auth)
            USE_AUTH=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Validate sort parameter
if [[ ! "$SORT" =~ ^(new|hot|top|relevance)$ ]]; then
    echo -e "${RED}Error: Invalid sort method. Use: new|hot|top|relevance${NC}"
    exit 1
fi

# Validate limit
if [[ ! "$LIMIT" =~ ^[0-9]+$ ]] || [[ "$LIMIT" -gt 100 || "$LIMIT" -lt 1 ]]; then
    echo -e "${RED}Error: Limit must be a number between 1 and 100${NC}"
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is not installed. Install with: brew install jq${NC}"
    exit 1
fi

# Main execution
echo -e "${BLUE}Reddit GTM Search Tool${NC}"
echo -e "${BLUE}═══════════════════════${NC}"
echo "Search Query: $SEARCH_QUERY"
echo "Subreddit: ${SUBREDDIT:-"All"}"
echo "Limit: $LIMIT"
echo "Sort: $SORT"
echo "Authentication: $([ "$USE_AUTH" = true ] && echo "Yes" || echo "No")"
echo ""

# Get results
if [[ "$USE_AUTH" == true ]]; then
    get_access_token
    RESULTS=$(search_reddit_auth)
else
    RESULTS=$(search_reddit_basic)
fi

# Parse and display
parse_results "$RESULTS"

echo -e "\n${GREEN}Search complete!${NC}"
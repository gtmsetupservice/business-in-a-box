#!/bin/bash

# Business-in-a-Box Client Initialization Script
# Usage: ./init-client.sh [business-type] [client-name] [niche] [client-location]

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Check arguments
if [ $# -lt 3 ]; then
    print_error "Usage: $0 [business-type] [client-name] [niche] [client-location]"
    echo "Business types: locallyknown-pro, gtm-setups"
    echo "Example: $0 locallyknown-pro 'Smiths Plumbing' 'plumbing' 'Denver, CO'"
    exit 1
fi

BUSINESS_TYPE="$1"
CLIENT_NAME="$2"
CLIENT_NICHE="$3"
CLIENT_LOCATION="${4:-Unknown}"

# Validate business type
if [[ "$BUSINESS_TYPE" != "locallyknown-pro" && "$BUSINESS_TYPE" != "gtm-setups" ]]; then
    print_error "Invalid business type. Must be 'locallyknown-pro' or 'gtm-setups'"
    exit 1
fi

print_header "Business-in-a-Box Client Initialization"
print_status "Business Type: $BUSINESS_TYPE"
print_status "Client Name: $CLIENT_NAME"
print_status "Client Niche: $CLIENT_NICHE"
print_status "Client Location: $CLIENT_LOCATION"

# Create safe directory name
CLIENT_DIR=$(echo "$CLIENT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
PROJECT_DIR="/Volumes/Samsung/mo/prod/projects/clients/$CLIENT_DIR"

print_status "Project directory: $PROJECT_DIR"

# Check if project already exists
if [ -d "$PROJECT_DIR" ]; then
    print_warning "Project directory already exists: $PROJECT_DIR"
    read -p "Do you want to continue and overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cancelled by user"
        exit 0
    fi
    rm -rf "$PROJECT_DIR"
fi

# Create project directory
print_status "Creating project directory..."
mkdir -p "$PROJECT_DIR"

# Copy template based on business type
print_status "Copying $BUSINESS_TYPE template..."
cp -r "templates/$BUSINESS_TYPE/"* "$PROJECT_DIR/"

# Copy shared components
print_status "Copying shared components..."
cp -r agents "$PROJECT_DIR/"
cp -r procedures "$PROJECT_DIR/"
cp -r crm "$PROJECT_DIR/"
cp -r scripts "$PROJECT_DIR/"

# Load configuration
CONFIG_FILE="config/$BUSINESS_TYPE.json"
if [ ! -f "$CONFIG_FILE" ]; then
    print_error "Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Create client-specific configuration
print_status "Creating client configuration..."
CLIENT_CONFIG="$PROJECT_DIR/client-config.json"
cat > "$CLIENT_CONFIG" << EOF
{
  "client": {
    "name": "$CLIENT_NAME",
    "niche": "$CLIENT_NICHE",
    "location": "$CLIENT_LOCATION",
    "created_date": "$(date -u +%Y-%m-%d)",
    "project_directory": "$PROJECT_DIR"
  },
  "business_type": "$BUSINESS_TYPE",
  "template_source": "$(pwd)/templates/$BUSINESS_TYPE"
}
EOF

# Customize CLAUDE.md with client information
print_status "Customizing agent instructions..."
sed -i.bak "s/{{CLIENT_NAME}}/$CLIENT_NAME/g" "$PROJECT_DIR/CLAUDE.md"
sed -i.bak "s/{{CLIENT_NICHE}}/$CLIENT_NICHE/g" "$PROJECT_DIR/CLAUDE.md"
sed -i.bak "s/{{CLIENT_LOCATION}}/$CLIENT_LOCATION/g" "$PROJECT_DIR/CLAUDE.md"
rm "$PROJECT_DIR/CLAUDE.md.bak"

# Initialize CRM database for client
print_status "Initializing client CRM database..."
cd "$PROJECT_DIR"

# Remove existing database and create fresh one
rm -f crm/gtm_crm.db

# Initialize database with client information
if [ -f "crm/init_database.sql" ]; then
    sqlite3 crm/gtm_crm.db < crm/init_database.sql

    # Add client record
    sqlite3 crm/gtm_crm.db << EOF
INSERT INTO clients (name, industry, location, business_type, created_date, status)
VALUES ('$CLIENT_NAME', '$CLIENT_NICHE', '$CLIENT_LOCATION', '$BUSINESS_TYPE', datetime('now'), 'active');
EOF
    print_status "CRM database initialized with client record"
else
    print_warning "CRM initialization file not found, skipping database setup"
fi

# Business-specific customizations
if [ "$BUSINESS_TYPE" = "locallyknown-pro" ]; then
    print_status "Applying LocallyKnown.pro customizations..."

    # Update Jekyll config
    if [ -f "_config.yml" ]; then
        sed -i.bak "s/title: .*/title: $CLIENT_NAME/g" _config.yml
        sed -i.bak "s/description: .*/description: Professional website for $CLIENT_NAME in $CLIENT_LOCATION/g" _config.yml
        rm _config.yml.bak
    fi

    # Create niche-specific content directory
    mkdir -p "content/niche-templates/$CLIENT_NICHE"

elif [ "$BUSINESS_TYPE" = "gtm-setups" ]; then
    print_status "Applying GTM Setups customizations..."

    # Create tracking assessment directory
    mkdir -p "assessments/$CLIENT_NICHE"

    # Set up emergency response configuration
    cat > "emergency-config.json" << EOF
{
  "client": "$CLIENT_NAME",
  "domain": "TBD",
  "emergency_level": "standard",
  "response_sla": "8 hours",
  "service_package": "audit"
}
EOF
fi

# Create project structure
print_status "Creating project structure..."
mkdir -p logs reports deliverables

# Create initial project log
cat > "logs/project-init.log" << EOF
Project Initialization Log
=========================
Date: $(date)
Business Type: $BUSINESS_TYPE
Client: $CLIENT_NAME
Niche: $CLIENT_NICHE
Location: $CLIENT_LOCATION
Project Directory: $PROJECT_DIR

Template Applied: $BUSINESS_TYPE
CRM Database: Initialized
Configuration: Complete
Status: Ready for agent activation

Next Steps:
1. Load appropriate agents using: load [agent-name]
2. Review client requirements
3. Begin phase 1 of service delivery
EOF

print_header "Initialization Complete"
print_status "Client project created successfully!"
print_status "Project directory: $PROJECT_DIR"
print_status "Next steps:"
echo "  1. cd \"$PROJECT_DIR\""
echo "  2. Review client-config.json"

if [ "$BUSINESS_TYPE" = "locallyknown-pro" ]; then
    echo "  3. load competitor research"
    echo "  4. Begin $19.95 website service workflow"
elif [ "$BUSINESS_TYPE" = "gtm-setups" ]; then
    echo "  3. load gtm prospect"
    echo "  4. Begin GTM emergency assessment"
fi

print_status "Business-in-a-box setup complete! 🚀"
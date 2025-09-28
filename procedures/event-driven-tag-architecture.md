# Event-Driven Tag Architecture

## Pattern Overview

The Event-Driven Tag Architecture is a decoupled GTM implementation pattern that separates event detection from analytics processing using the dataLayer as an event bus.

## Architecture Components

### 1. Setup Layer (DOM Instrumentation)
- **Custom HTML Tag**: Contains JavaScript code to set up observers/listeners
- **DOM Ready Trigger**: Fires once per page to initialize the detection mechanism
- **Purpose**: Establishes event detection without concerning itself with analytics

### 2. Event Bridge (DataLayer)
- **DataLayer Push**: Detection code pushes structured events to dataLayer
- **Event Format**: Consistent event naming and parameter structure
- **Purpose**: Acts as message bus between detection and processing layers

### 3. Parameter Extraction Layer
- **Data Layer Variables**: Extract specific values from dataLayer events
- **Variable Naming**: DLV - [parameter_name] convention
- **Purpose**: Makes event data accessible to tags

### 4. Analytics Processing Layer
- **GA4 Event Tag**: Configured to send events to Google Analytics
- **Custom Event Trigger**: Listens for specific dataLayer events
- **Event Parameters**: Maps Data Layer Variables to GA4 parameters
- **Purpose**: Transforms dataLayer events into analytics hits

## Implementation Example: Section Visibility Tracking

### Step 1: Create Custom HTML Tag
**Tag Name**: Section Visibility Observer Setup
**Tag Type**: Custom HTML
```html
<script>
if (!window.gtmSectionObserver) {
    window.gtmSectionObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                window.dataLayer = window.dataLayer || [];
                dataLayer.push({
                    'event': 'section_in_view',
                    'section_id': entry.target.id,
                    'section_name': entry.target.id,
                    'visibility_threshold': '50%',
                    'page_location': window.location.href
                });
            }
        });
    }, {
        threshold: 0.5,
        rootMargin: '0px'
    });

    document.querySelectorAll('[id^="Section-"]').forEach(function(section) {
        window.gtmSectionObserver.observe(section);
    });
}
</script>
```
**Trigger**: DOM Ready

### Step 2: Create Data Layer Variables
1. **Variable Name**: DLV - section_id
   - **Variable Type**: Data Layer Variable
   - **Data Layer Variable Name**: section_id

2. **Variable Name**: DLV - section_name
   - **Variable Type**: Data Layer Variable
   - **Data Layer Variable Name**: section_name

### Step 3: Create Custom Event Trigger
**Trigger Name**: Section View Event Trigger
- **Trigger Type**: Custom Event
- **Event name**: section_in_view
- **Use regex matching**: Unchecked
- **Fire on**: All Custom Events

### Step 4: Create GA4 Event Tag
**Tag Name**: Section in View GA4 Event
- **Tag Type**: Google Analytics: GA4 Event
- **Configuration Tag**: {{GA4 Configuration}}
- **Event Name**: section_view
- **Event Parameters**:
  - section_id: {{DLV - section_id}}
  - section_name: {{DLV - section_name}}
- **Trigger**: Section View Event Trigger

## Benefits of This Pattern

### 1. Separation of Concerns
- Detection logic is isolated from analytics implementation
- Changes to analytics don't affect detection code
- Multiple analytics platforms can consume the same events

### 2. Reusability
- Same dataLayer events can trigger multiple tags
- Easy to add additional analytics platforms (Facebook, LinkedIn, etc.)
- Parameters are available to all tags through Data Layer Variables

### 3. Debugging Advantages
- Each layer can be tested independently
- DataLayer events visible in GTM Preview mode
- Clear event flow: Detection → DataLayer → Trigger → Tag

### 4. Maintainability
- Clear structure makes troubleshooting easier
- Changes are isolated to specific components
- Documentation is straightforward

## Common Use Cases

### 1. Scroll Tracking
- Observer detects scroll depth milestones
- Pushes scroll_depth events to dataLayer
- GA4 tag sends scroll engagement metrics

### 2. Form Interaction Tracking
- Listeners detect form field interactions
- Pushes form_interaction events with field details
- Analytics tags track form engagement funnel

### 3. Video Engagement
- Video player API integration
- Pushes video_play, video_progress events
- Multiple tags can track video metrics

### 4. Dynamic Content Visibility
- Tracks when dynamic elements become visible
- Useful for lazy-loaded content
- Measures actual content consumption

## Best Practices

### 1. Event Naming Conventions
- Use snake_case for event names
- Be descriptive but concise
- Maintain consistency across implementations

### 2. Parameter Structure
- Always include timestamp or page_location
- Use consistent parameter names across events
- Document expected parameters

### 3. Performance Considerations
- Initialize observers only once
- Use appropriate thresholds for visibility
- Limit the number of observed elements

### 4. Testing Protocol
1. Verify observer initialization in browser console
2. Check dataLayer pushes are occurring
3. Confirm GTM trigger is firing
4. Validate GA4 events in DebugView

## Troubleshooting Guide

### Event Not Appearing in DataLayer
- Check if Custom HTML tag fired (GTM Preview)
- Verify DOM Ready trigger is active
- Console test the observer setup

### Trigger Not Firing
- Confirm event name matches exactly (case-sensitive)
- Check for typos or extra spaces
- Verify "Use regex matching" setting

### Parameters Not Captured
- Create Data Layer Variables for each parameter
- Ensure variable names match dataLayer structure
- Test variables in GTM Preview mode

### GA4 Events Not Sending
- Verify GA4 Configuration tag is present
- Check Measurement ID is correct
- Confirm network requests in browser DevTools

## Summary

The Event-Driven Tag Architecture provides a robust, scalable approach to GTM implementations by decoupling event detection from analytics processing. This pattern enables flexibility, maintainability, and clear debugging pathways while supporting multiple analytics platforms from a single event source.
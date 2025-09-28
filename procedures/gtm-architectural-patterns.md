# GTM Architectural Patterns

## Table of Contents
1. [Enhanced Ecommerce Data Layer Pattern](#1-enhanced-ecommerce-data-layer-pattern)
2. [Virtual Page View Pattern](#2-virtual-page-view-pattern)
3. [Generic Event Pattern](#3-generic-event-pattern)
4. [Cookie Consent Layer Pattern](#4-cookie-consent-layer-pattern)
5. [Error Tracking Pattern](#5-error-tracking-pattern)
6. [User ID Synchronization Pattern](#6-user-id-synchronization-pattern)
7. [Scroll Depth Milestone Pattern](#7-scroll-depth-milestone-pattern)
8. [Form Analytics Pattern](#8-form-analytics-pattern)
9. [Custom Dimension Enrichment Pattern](#9-custom-dimension-enrichment-pattern)
10. [Debug Mode Pattern](#10-debug-mode-pattern)
11. [Engagement Time Pattern](#11-engagement-time-pattern)
12. [A/B Test Variant Pattern](#12-ab-test-variant-pattern)
13. [External Campaign Pattern](#13-external-campaign-pattern)
14. [Lazy Load Visibility Pattern](#14-lazy-load-visibility-pattern)
15. [Cross-Domain Tracking Pattern](#15-cross-domain-tracking-pattern)

---

## 1. Enhanced Ecommerce Data Layer Pattern

### Purpose
Standardizes all ecommerce tracking through a structured dataLayer format that multiple analytics platforms can consume.

### Implementation
```javascript
// Product impression
dataLayer.push({
  'event': 'view_item_list',
  'ecommerce': {
    'currency': 'USD',
    'value': 150.00,
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'affiliation': 'Online Store',
      'coupon': '',
      'discount': 10.00,
      'index': 0,
      'item_brand': 'Brand',
      'item_category': 'Category',
      'item_category2': 'Subcategory',
      'item_list_id': 'related_products',
      'item_list_name': 'Related Products',
      'item_variant': 'Blue',
      'location_id': 'hero_banner',
      'price': 50.00,
      'quantity': 1
    }]
  }
});

// Purchase
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': '12345',
    'value': 150.00,
    'tax': 10.00,
    'shipping': 5.00,
    'currency': 'USD',
    'coupon': 'SUMMER_SALE',
    'items': [/* item objects */]
  }
});
```

### GTM Configuration
- **Variables**: Create ecommerce object variables
- **Triggers**: Custom events (view_item, add_to_cart, purchase)
- **Tags**: GA4 Ecommerce events, Facebook Pixel, Google Ads conversions

### Benefits
- Single source of truth for all ecommerce data
- Platform-agnostic data structure
- Simplified debugging and maintenance

---

## 2. Virtual Page View Pattern

### Purpose
Enables proper page tracking in Single Page Applications where traditional page loads don't occur.

### Implementation
```javascript
// On route change in SPA
window.history.pushState = function() {
  const originalPushState = window.history.pushState;
  return function() {
    originalPushState.apply(window.history, arguments);
    dataLayer.push({
      'event': 'virtual_page_view',
      'page_location': window.location.href,
      'page_title': document.title,
      'page_path': window.location.pathname
    });
  };
}();
```

### GTM Configuration
- **Trigger**: Custom Event = virtual_page_view
- **Tag**: GA4 Configuration with page_view event
- **Variables**: Page Path, Page Title from dataLayer

### Use Cases
- React/Vue/Angular applications
- AJAX-loaded content
- Progressive web apps
- Multi-step forms

---

## 3. Generic Event Pattern

### Purpose
Single flexible tag handles multiple event types dynamically, reducing tag proliferation.

### Implementation
```javascript
// Generic event push
dataLayer.push({
  'event': 'generic_event',
  'event_category': 'engagement',
  'event_action': 'scroll',
  'event_label': '50_percent',
  'event_value': 50,
  'custom_parameters': {
    'page_section': 'hero',
    'user_type': 'returning'
  }
});
```

### GTM Configuration
```javascript
// Custom JavaScript Variable for event name
function() {
  return {{DLV - event_category}} + '_' + {{DLV - event_action}};
}
```

- **Single GA4 Tag**: Dynamically pulls event name and parameters
- **Lookup Table**: Maps generic events to specific names
- **Regex Triggers**: Route events based on patterns

### Benefits
- Dramatically reduces tag count
- Easier maintenance
- Consistent event structure

---

## 4. Cookie Consent Layer Pattern

### Purpose
Ensures GDPR/CCPA compliance by controlling tag firing based on user consent.

### Implementation
```javascript
// Initial consent state
dataLayer.push({
  'event': 'consent_update',
  'consent_state': {
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'functionality_storage': 'granted',
    'personalization_storage': 'denied',
    'security_storage': 'granted'
  }
});

// After user grants consent
dataLayer.push({
  'event': 'consent_granted',
  'consent_state': {
    'analytics_storage': 'granted',
    'ad_storage': 'granted'
  }
});
```

### GTM Configuration
- **Consent Variables**: Check consent state
- **Trigger Groups**: Require consent for specific tags
- **Exception Triggers**: Block tags when consent denied
- **Consent Mode**: Built-in GA4 consent features

### Compliance Features
- Automatic tag pausing
- Consent banner integration
- Audit trail in dataLayer
- Regional consent rules

---

## 5. Error Tracking Pattern

### Purpose
Captures JavaScript errors and application errors for monitoring and debugging.

### Implementation
```javascript
// Global error handler
window.addEventListener('error', function(e) {
  dataLayer.push({
    'event': 'javascript_error',
    'error_message': e.message,
    'error_source': e.filename,
    'error_lineno': e.lineno,
    'error_colno': e.colno,
    'error_stack': e.error ? e.error.stack : 'N/A',
    'error_type': 'javascript',
    'page_location': window.location.href,
    'user_agent': navigator.userAgent
  });
});

// Application error tracking
function trackError(error, context) {
  dataLayer.push({
    'event': 'application_error',
    'error_message': error.message,
    'error_context': context,
    'error_severity': error.severity || 'medium',
    'error_timestamp': new Date().toISOString()
  });
}
```

### GTM Configuration
- **Error Tags**: Send to GA4, Sentry, or error monitoring service
- **Sampling**: Limit error tracking to percentage of users
- **Filters**: Exclude known/irrelevant errors

---

## 6. User ID Synchronization Pattern

### Purpose
Enables cross-device tracking and user-level analysis across platforms.

### Implementation
```javascript
// On user login (server-side rendered)
dataLayer.push({
  'event': 'user_login',
  'user_id': 'user_12345',
  'user_properties': {
    'user_type': 'premium',
    'registration_date': '2024-01-15',
    'lifetime_value': 500,
    'subscription_status': 'active'
  }
});
```

### GTM Configuration
- **User ID Variable**: Persistent across all tags
- **User Properties**: Custom dimensions in GA4
- **Cross-Domain**: Include user ID in linker
- **Privacy**: Hash user IDs before sending

### Benefits
- Unified user journey tracking
- Accurate conversion attribution
- Enhanced remarketing audiences

---

## 7. Scroll Depth Milestone Pattern

### Purpose
Tracks meaningful scroll engagement beyond basic percentage thresholds.

### Implementation
```javascript
// Advanced scroll tracking
(function() {
  const milestones = [25, 50, 75, 90, 100];
  const triggered = new Set();
  let maxScroll = 0;

  function trackScroll() {
    const scrollPercent = Math.round(
      (window.scrollY + window.innerHeight) /
      document.body.scrollHeight * 100
    );

    maxScroll = Math.max(maxScroll, scrollPercent);

    milestones.forEach(milestone => {
      if (scrollPercent >= milestone && !triggered.has(milestone)) {
        triggered.add(milestone);
        dataLayer.push({
          'event': 'scroll_milestone',
          'scroll_depth': milestone,
          'max_scroll_depth': maxScroll,
          'time_to_scroll': Date.now() - window.loadTime,
          'content_height': document.body.scrollHeight,
          'viewport_height': window.innerHeight
        });
      }
    });
  }

  let scrollTimer;
  window.addEventListener('scroll', function() {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(trackScroll, 100);
  });
})();
```

### Features
- Debounced scroll events
- Time to scroll metrics
- Content height awareness
- Session-based deduplication

---

## 8. Form Analytics Pattern

### Purpose
Comprehensive form interaction tracking for conversion optimization.

### Implementation
```javascript
// Form interaction tracking
document.querySelectorAll('form').forEach(form => {
  let formStarted = false;
  let fieldsInteracted = new Set();
  let startTime = null;

  form.addEventListener('focusin', function(e) {
    if (!formStarted) {
      formStarted = true;
      startTime = Date.now();
      dataLayer.push({
        'event': 'form_start',
        'form_id': form.id || 'unnamed_form',
        'form_name': form.name,
        'form_classes': form.className,
        'form_action': form.action
      });
    }

    if (e.target.name) {
      fieldsInteracted.add(e.target.name);
    }
  });

  form.addEventListener('submit', function(e) {
    dataLayer.push({
      'event': 'form_submit',
      'form_id': form.id || 'unnamed_form',
      'fields_interacted': Array.from(fieldsInteracted),
      'time_to_complete': Date.now() - startTime,
      'form_method': form.method
    });
  });
});
```

### Metrics Tracked
- Form starts vs submissions
- Field-level interaction
- Time to complete
- Abandonment points
- Error messages

---

## 9. Custom Dimension Enrichment Pattern

### Purpose
Enriches all tracking with contextual data from server-side or page content.

### Implementation
```javascript
// Server-side data injection (in page template)
dataLayer.push({
  'event': 'page_metadata',
  'page_data': {
    'content_type': 'article',
    'author': 'John Doe',
    'publish_date': '2024-01-15',
    'word_count': 1500,
    'category': 'Technology',
    'tags': ['GTM', 'Analytics', 'Tracking'],
    'paywall_status': 'free',
    'experiment_variants': {
      'homepage_test': 'variant_b',
      'cta_color': 'green'
    }
  },
  'user_data': {
    'membership_level': 'gold',
    'account_age_days': 365,
    'content_preferences': ['tech', 'business'],
    'engagement_score': 85
  }
});
```

### GTM Configuration
- **Variables**: Extract each dimension
- **Tags**: Include dimensions as custom parameters
- **Triggers**: No change needed - data available globally

---

## 10. Debug Mode Pattern

### Purpose
Enables detailed logging and testing without affecting production data.

### Implementation
```javascript
// Debug mode initialization
const debugMode = new URLSearchParams(window.location.search).has('debug');

if (debugMode) {
  dataLayer.push({'debug_mode': true});

  // Override dataLayer.push to log everything
  const originalPush = dataLayer.push;
  dataLayer.push = function() {
    console.group('🔍 DataLayer Push');
    console.log('Event:', arguments[0]);
    console.trace('Stack trace');
    console.groupEnd();
    return originalPush.apply(dataLayer, arguments);
  };

  // Enable GTM Preview mode programmatically
  document.cookie = 'gtm_debug=x; path=/';
}
```

### Features
- URL parameter activation (?debug=true)
- Console logging for all events
- Test tag firing
- Performance metrics
- Prevents production data pollution

---

## 11. Engagement Time Pattern

### Purpose
Accurately measures engaged time on page, not just presence.

### Implementation
```javascript
// Engagement time tracker
(function() {
  let totalEngagedTime = 0;
  let lastEngagedTime = Date.now();
  let isEngaged = true;
  let heartbeatInterval;

  const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];

  function startEngagement() {
    if (!isEngaged) {
      isEngaged = true;
      lastEngagedTime = Date.now();
    }
  }

  function stopEngagement() {
    if (isEngaged) {
      isEngaged = false;
      totalEngagedTime += Date.now() - lastEngagedTime;
    }
  }

  events.forEach(event => {
    document.addEventListener(event, startEngagement);
  });

  // User is idle after 30 seconds
  let idleTimer;
  function resetIdleTimer() {
    clearTimeout(idleTimer);
    startEngagement();
    idleTimer = setTimeout(stopEngagement, 30000);
  }

  events.forEach(event => {
    document.addEventListener(event, resetIdleTimer);
  });

  // Send heartbeat every 15 seconds
  heartbeatInterval = setInterval(function() {
    if (isEngaged) {
      totalEngagedTime += Date.now() - lastEngagedTime;
      lastEngagedTime = Date.now();
    }

    dataLayer.push({
      'event': 'engagement_heartbeat',
      'engaged_time_seconds': Math.round(totalEngagedTime / 1000),
      'is_engaged': isEngaged
    });
  }, 15000);
})();
```

### Metrics
- True engaged time
- Idle detection
- Engagement patterns
- Attention quality scores

---

## 12. A/B Test Variant Pattern

### Purpose
Tracks experiment variants across all analytics for proper test analysis.

### Implementation
```javascript
// Google Optimize or custom A/B test integration
dataLayer.push({
  'event': 'experiment_view',
  'experiment_id': 'homepage_hero_test',
  'variant_id': 'variant_b',
  'experiments': {
    'homepage_hero': 'variant_b',
    'button_color': 'green',
    'pricing_display': 'monthly'
  }
});

// Include in all subsequent events
window.activeExperiments = {
  'homepage_hero': 'variant_b',
  'button_color': 'green'
};

// Conversion tracking with variant
dataLayer.push({
  'event': 'conversion',
  'conversion_type': 'signup',
  'experiment_variants': window.activeExperiments
});
```

### Integration Points
- Google Optimize
- VWO
- Optimizely
- Custom testing frameworks
- Server-side experiments

---

## 13. External Campaign Pattern

### Purpose
Enhanced campaign tracking beyond standard UTM parameters.

### Implementation
```javascript
// Enhanced campaign parsing
(function() {
  const urlParams = new URLSearchParams(window.location.search);
  const campaignData = {
    // Standard UTMs
    'utm_source': urlParams.get('utm_source'),
    'utm_medium': urlParams.get('utm_medium'),
    'utm_campaign': urlParams.get('utm_campaign'),
    'utm_term': urlParams.get('utm_term'),
    'utm_content': urlParams.get('utm_content'),

    // Extended parameters
    'campaign_id': urlParams.get('cid'),
    'ad_group': urlParams.get('adgroup'),
    'keyword': urlParams.get('keyword'),
    'placement': urlParams.get('placement'),
    'creative_id': urlParams.get('creative'),
    'audience': urlParams.get('audience'),

    // QR code tracking
    'qr_code': urlParams.get('qr'),
    'qr_location': urlParams.get('qr_loc'),

    // Email campaign
    'email_id': urlParams.get('eid'),
    'email_list': urlParams.get('list'),

    // Calculated fields
    'landing_page': window.location.pathname,
    'referrer': document.referrer,
    'entry_time': new Date().toISOString()
  };

  // Only push if campaign parameters exist
  if (campaignData.utm_source || campaignData.campaign_id) {
    dataLayer.push({
      'event': 'campaign_entry',
      'campaign_data': campaignData
    });

    // Store in session for attribution
    sessionStorage.setItem('campaign_data', JSON.stringify(campaignData));
  }
})();
```

### Features
- Extended parameter support
- QR code campaign tracking
- Email campaign integration
- Session-level attribution
- Multi-touch attribution support

---

## 14. Lazy Load Visibility Pattern

### Purpose
Tracks when lazy-loaded content actually becomes visible and loads.

### Implementation
```javascript
// Lazy load visibility tracking
(function() {
  const lazyImages = document.querySelectorAll('img[loading="lazy"]');
  const lazyIframes = document.querySelectorAll('iframe[loading="lazy"]');

  const visibilityObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const element = entry.target;

        // Track when element becomes visible
        dataLayer.push({
          'event': 'lazy_content_visible',
          'content_type': element.tagName.toLowerCase(),
          'content_src': element.src || element.dataset.src,
          'content_alt': element.alt || '',
          'load_timing': performance.now(),
          'viewport_position': {
            'top': entry.boundingClientRect.top,
            'visible_ratio': entry.intersectionRatio
          }
        });

        // Track when content actually loads
        element.addEventListener('load', function() {
          dataLayer.push({
            'event': 'lazy_content_loaded',
            'content_type': element.tagName.toLowerCase(),
            'content_src': element.src,
            'load_duration': performance.now() - entry.time,
            'content_size': this.naturalWidth ?
              `${this.naturalWidth}x${this.naturalHeight}` : 'N/A'
          });
        });

        visibilityObserver.unobserve(element);
      }
    });
  }, {
    rootMargin: '50px'
  });

  lazyImages.forEach(img => visibilityObserver.observe(img));
  lazyIframes.forEach(iframe => visibilityObserver.observe(iframe));
})();
```

### Metrics
- Content visibility timing
- Load performance
- Viewport position at load
- Failed loads
- Bandwidth impact

---

## 15. Cross-Domain Tracking Pattern

### Purpose
Maintains user sessions across multiple domains and subdomains.

### Implementation
```javascript
// Cross-domain linker setup
(function() {
  const domains = ['domain1.com', 'domain2.com', 'checkout.domain1.com'];

  // Get or create client ID
  function getClientId() {
    const match = document.cookie.match('(?:^|;)\\s*_ga=([^;]*)');
    return match ? decodeURIComponent(match[1]) : null;
  }

  // Add linker parameters to cross-domain links
  document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (!link) return;

    const linkDomain = new URL(link.href).hostname;
    if (domains.includes(linkDomain) && linkDomain !== window.location.hostname) {
      e.preventDefault();

      const clientId = getClientId();
      const timestamp = Date.now();
      const linkerParam = `_gl=${clientId}*${timestamp}`;

      const separator = link.href.includes('?') ? '&' : '?';
      const decoratedUrl = `${link.href}${separator}${linkerParam}`;

      dataLayer.push({
        'event': 'cross_domain_link',
        'link_domain': linkDomain,
        'client_id': clientId
      });

      window.location.href = decoratedUrl;
    }
  });

  // Parse linker on destination domain
  const urlParams = new URLSearchParams(window.location.search);
  const linkerParam = urlParams.get('_gl');
  if (linkerParam) {
    const [clientId, timestamp] = linkerParam.split('*');

    // Validate timestamp (within last 2 minutes)
    if (Date.now() - parseInt(timestamp) < 120000) {
      dataLayer.push({
        'event': 'cross_domain_arrival',
        'source_client_id': clientId,
        'link_age_ms': Date.now() - parseInt(timestamp)
      });
    }
  }
})();
```

### Configuration Requirements
- GA4 Configuration for all domains
- Cookie domain settings
- Referral exclusion list
- Consistent measurement IDs

---

## Pattern Selection Guide

### For E-commerce Sites
- Enhanced Ecommerce Data Layer Pattern
- Cross-Domain Tracking Pattern (for separate checkout domains)
- Form Analytics Pattern
- External Campaign Pattern

### For Content/Publishing Sites
- Scroll Depth Milestone Pattern
- Engagement Time Pattern
- Custom Dimension Enrichment Pattern
- Lazy Load Visibility Pattern

### For Single Page Applications
- Virtual Page View Pattern
- Error Tracking Pattern
- User ID Synchronization Pattern

### For Lead Generation
- Form Analytics Pattern
- External Campaign Pattern
- A/B Test Variant Pattern
- Cookie Consent Layer Pattern

### For Debugging/Development
- Debug Mode Pattern
- Error Tracking Pattern
- Generic Event Pattern (for rapid prototyping)

---

## Best Practices for All Patterns

### 1. Documentation
- Document all custom events in a data dictionary
- Include example payloads
- Specify required vs optional parameters

### 2. Testing
- Use GTM Preview mode for all implementations
- Test in multiple browsers
- Verify data in GA4 DebugView
- Check for console errors

### 3. Performance
- Debounce high-frequency events
- Use sampling for non-critical tracking
- Minimize DOM queries
- Lazy-load tracking scripts

### 4. Privacy
- Respect user consent choices
- Avoid tracking PII
- Implement data retention policies
- Use appropriate data anonymization

### 5. Maintenance
- Regular audits of tracking implementation
- Monitor for broken events
- Version control GTM containers
- Document changes and reasons
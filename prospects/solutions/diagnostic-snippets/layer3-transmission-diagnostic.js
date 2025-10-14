/**
 * Layer 3 (Transmission) Diagnostic Suite
 * For identifying data transmission failures between client and server
 * Used for: Server-side GTM, GA4 collection endpoint issues
 */

// 1. Server-Side GTM Transport URL Checker
(() => {
  console.log('🔍 Checking Server-Side GTM Transport...');

  const entries = performance.getEntriesByType('resource');
  const serverUrls = ['stape.io', 'gtm-server', 'sgtm', 'server-side'];

  let serverRequests = [];
  serverUrls.forEach(url => {
    const matches = entries.filter(e => e.name.includes(url));
    if (matches.length > 0) {
      serverRequests = serverRequests.concat(matches);
    }
  });

  if (serverRequests.length > 0) {
    console.log(`✅ Found ${serverRequests.length} server requests:`);
    serverRequests.forEach(req => {
      console.log(`  - ${req.name.split('?')[0]}`);
      console.log(`    Status: ${req.responseStatus || 'pending'}`);
      console.log(`    Duration: ${req.duration.toFixed(2)}ms`);
    });
  } else {
    console.log('❌ No server-side requests detected');
    console.log('Check: Transport URL configuration in GA4 Config tag');
  }

  return {
    serverRequestsFound: serverRequests.length,
    details: serverRequests.map(r => ({
      url: r.name.split('?')[0],
      status: r.responseStatus,
      duration: r.duration
    }))
  };
})();

// 2. GA4 Collection Endpoint Monitor
(() => {
  console.log('📊 Monitoring GA4 Collection Requests...');

  const observer = new PerformanceObserver((list) => {
    list.getEntries().forEach((entry) => {
      if (entry.name.includes('/g/collect') || entry.name.includes('/gtag/js')) {
        const url = new URL(entry.name);
        const params = Object.fromEntries(url.searchParams);

        console.log(`🌐 GA4 Request Detected:`);
        console.log(`  Event: ${params.en || params.t || 'unknown'}`);
        console.log(`  Status: ${entry.responseStatus || 'pending'}`);
        console.log(`  Measurement ID: ${params.tid || 'not found'}`);

        if (params.ep && params.ep.value) {
          console.log(`  Value: ${params.ep.value}`);
        }

        if (entry.responseStatus && entry.responseStatus !== 204) {
          console.warn(`  ⚠️ Unexpected status: ${entry.responseStatus}`);
        }
      }
    });
  });

  observer.observe({entryTypes: ['resource']});

  // Check last 10 requests
  const recent = performance.getEntriesByType('resource')
    .filter(e => e.name.includes('/g/collect'))
    .slice(-10);

  return {
    monitoring: 'active',
    recentRequests: recent.length,
    message: 'Check console for live GA4 requests'
  };
})();

// 3. Network Failure Detector
(() => {
  console.log('🔌 Checking for Network/Blocking Issues...');

  const blockedDomains = [
    'google-analytics.com',
    'googletagmanager.com',
    'doubleclick.net'
  ];

  const results = {};

  blockedDomains.forEach(domain => {
    const requests = performance.getEntriesByType('resource')
      .filter(e => e.name.includes(domain));

    if (requests.length === 0) {
      results[domain] = '❌ No requests (possibly blocked)';
    } else {
      const failed = requests.filter(r => r.responseStatus >= 400);
      if (failed.length > 0) {
        results[domain] = `⚠️ ${failed.length} failed requests`;
      } else {
        results[domain] = `✅ ${requests.length} successful requests`;
      }
    }
  });

  // Check for ad blocker indicators
  const adBlockerSignals = {
    gtag: typeof gtag !== 'undefined',
    ga: typeof ga !== 'undefined',
    dataLayer: typeof dataLayer !== 'undefined'
  };

  console.log('Domain Status:', results);
  console.log('Script Availability:', adBlockerSignals);

  return {
    domainStatus: results,
    scriptsLoaded: adBlockerSignals,
    likelyBlocked: Object.values(results).some(v => v.includes('❌'))
  };
})();

// 4. Client ID and Session Continuity Check
(() => {
  console.log('🔗 Checking Client ID and Session Continuity...');

  const cookies = document.cookie.split(';').map(c => c.trim());
  const gaCookie = cookies.find(c => c.startsWith('_ga='));
  const gclawCookie = cookies.find(c => c.includes('_gcl_aw='));

  const clientId = gaCookie ? gaCookie.split('.').slice(-2).join('.') : null;
  const gclid = gclawCookie ? gclawCookie.split('=')[1] : null;

  // Check if GCLID is fake (consent mode issue)
  const isFakeGclid = gclid && (gclid.includes('fake') || gclid.includes('GCL.'));

  const result = {
    clientId: clientId || 'Not found',
    gclid: gclid || 'Not found',
    gclidStatus: isFakeGclid ? '⚠️ Fake GCLID (consent issue)' : '✅ Valid GCLID',
    sessionContinuity: clientId ? '✅ Session tracking active' : '❌ No session tracking'
  };

  console.log('Client Tracking:', result);

  if (isFakeGclid) {
    console.warn('⚠️ Fake GCLID detected - check consent mode configuration');
  }

  return result;
})();

// 5. Comprehensive Transmission Health Check
(() => {
  console.log('🏥 Running Comprehensive Transmission Health Check...');

  const health = {
    ga4Requests: 0,
    serverRequests: 0,
    failedRequests: 0,
    blockedDomains: [],
    consentIssues: false
  };

  const resources = performance.getEntriesByType('resource');

  // Count GA4 requests
  health.ga4Requests = resources.filter(r =>
    r.name.includes('/g/collect')).length;

  // Count server-side requests
  health.serverRequests = resources.filter(r =>
    r.name.includes('stape.io') ||
    r.name.includes('gtm-server')).length;

  // Count failed requests
  health.failedRequests = resources.filter(r =>
    (r.name.includes('google') || r.name.includes('gtm')) &&
    r.responseStatus >= 400).length;

  // Check for blocking
  const expectedDomains = ['googletagmanager.com', 'google-analytics.com'];
  expectedDomains.forEach(domain => {
    if (!resources.some(r => r.name.includes(domain))) {
      health.blockedDomains.push(domain);
    }
  });

  // Check consent
  const gclid = document.cookie.match(/_gcl_aw=([^;]+)/);
  health.consentIssues = gclid && gclid[1].includes('fake');

  // Generate diagnosis
  const issues = [];
  if (health.ga4Requests === 0) issues.push('No GA4 data being sent');
  if (health.serverRequests === 0) issues.push('Server-side GTM not receiving data');
  if (health.failedRequests > 0) issues.push(`${health.failedRequests} failed requests`);
  if (health.blockedDomains.length > 0) issues.push('Domains being blocked');
  if (health.consentIssues) issues.push('Consent mode blocking conversions');

  const status = issues.length === 0 ? '✅ Healthy' : `❌ Issues: ${issues.join(', ')}`;

  console.log('Transmission Health:', {
    status,
    ...health,
    diagnosis: issues
  });

  return {
    status,
    metrics: health,
    issues,
    recommendation: issues.length > 0 ?
      'Layer 3 transmission failures detected - professional diagnosis recommended' :
      'Transmission layer functioning normally'
  };
})();
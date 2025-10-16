# Debugging-Tools-For-Each-Layer

## **Layer 1: Physical (Infrastructure)**
**Primary Tools:**
- **Chrome DevTools Network tab** - Check for failed requests, DNS issues
- **Browser console** - Look for CORS errors, SSL certificate warnings
- **Command line tools** - `nslookup`, `ping`, `traceroute` for connectivity
- **Chrome's Security tab** - Verify SSL certificates

**Specific checks:**
- Network tab: Look for red/failed requests to googletagmanager.com
- Console errors mentioning "blocked" or "CORS"
- Test direct URLs: `https://www.googletagmanager.com/gtm.js?id=GTM-XXXXX`

## **Layer 2: Data Link (Browser Environment)** 
**Primary Tools:**
- **Chrome DevTools Application tab** - Check cookies, local storage
- **Browser settings** - Verify JavaScript/cookie permissions
- **Tag Assistant Legacy** - Browser compatibility checks
- **Console** - JavaScript engine errors

**Specific checks:**
- Application tab: Verify GA/GTM cookies are being set
- Console: JavaScript errors before GTM loads
- Privacy settings: Third-party cookie blocking

## **Layer 3: Network (Script Loading)**
**Primary Tools:**
- **Chrome DevTools Network tab** - Script loading verification
- **Chrome DevTools Sources tab** - Verify scripts loaded
- **Performance tab** - Script loading timing
- **Console** - Script loading errors

**Specific checks:**
- Network tab: Verify gtm.js and gtag.js return 200 status
- Sources tab: Confirm GTM container code is present
- Timeline: Check script loading sequence

## **Layer 4: Transport (Data Transmission)**
**Primary Tools:**
- **Chrome DevTools Network tab** - Monitor collect/mp/collect requests
- **GA4 DebugView** - Real-time event verification
- **GTM Preview mode** - Tag firing confirmation
- **Measurement Protocol Validation Server** - Server-side validation

**Specific checks:**
- Network tab: Filter for "collect" or "mp/collect" requests
- GA4 DebugView: Verify events are received by Google
- Check HTTP status codes (200 = success)

## **Layer 5: Session (Tag Management)**
**Primary Tools:**
- **GTM Preview mode** - Primary debugging tool for tags
- **GTM Debug Console** - Tag firing sequence
- **Chrome console** - dataLayer inspection
- **Tag Assistant (Legacy)** - Tag verification

**Specific checks:**
- GTM Preview: Step through tag firing logic
- Console: `dataLayer` array inspection
- Debug console: Trigger evaluation results

## **Layer 6: Presentation (Data Processing)**
**Primary Tools:**
- **GA4 DebugView** - Event structure validation
- **Chrome console** - dataLayer structure verification
- **GTM Preview mode** - Variable value inspection
- **Real-time reports** - Data formatting verification

**Specific checks:**
- DebugView: Parameter names and values
- Console: dataLayer event structure
- Preview mode: Variable resolution values

## **Layer 7: Application (Business Logic)**
**Primary Tools:**
- **GA4 standard reports** - Business metric validation
- **GA4 Explore reports** - Custom analysis
- **Google Analytics Intelligence** - Anomaly detection
- **Data Studio/Looker Studio** - Cross-platform validation

**Specific checks:**
- Standard reports: Goal/conversion alignment
- Explore reports: Segment-specific validation
- Attribution reports: Channel attribution accuracy
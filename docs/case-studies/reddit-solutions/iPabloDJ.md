# Reddit Solution: NextJS/React Apps Lost All GTM Tracking

**User:** u/iPabloDJ  
**Post URL:** https://reddit.com/r/GoogleTagManager/comments/1nd5wvp/  
**Problem:** "Recent changes in Google Tag Manager do not send data"  
**Date:** September 10, 2025

## Response

I use a systematic diagnostic approach, and your NextJS/React tracking failure is a Layer 1: Infrastructure issue.

**Layer 1** covers the fundamental loading of GTM itself. When GTM Preview says "no tag installed" despite your implementation, it means the container isn't initializing properly. This is especially common with NextJS due to its hybrid rendering approach.

## The NextJS/React GTM Problem

The "recent changes" you mentioned likely refer to Google's updated GTM snippet requirements for SPAs. NextJS apps need special handling because:
- Server-side rendering (SSR) vs client-side hydration timing
- React's strict mode in development can break GTM
- App Router vs Pages Router have different integration points

## Quick Diagnostic

Run this in your browser console on any page:

```javascript
// Check GTM initialization in NextJS
(() => {
  const checks = {
    gtmScript: !!document.querySelector('script[src*="googletagmanager.com"]'),
    dataLayer: typeof dataLayer !== 'undefined',
    gtmObject: typeof google_tag_manager !== 'undefined',
    containerId: window.dataLayer?.find(item => item['gtm.start'])?.['gtm.uniqueEventId'],
    reactRoot: !!document.getElementById('__next'),
    hydrated: !!window.__NEXT_DATA__
  };
  
  console.table(checks);
  
  if (!checks.gtmObject && checks.gtmScript) {
    console.error('GTM script loaded but not initialized - typical NextJS timing issue');
  }
  
  // Check if GTM is being blocked
  const blockedResources = performance.getEntriesByType('resource')
    .filter(r => r.name.includes('googletagmanager') && r.transferSize === 0);
  
  if (blockedResources.length > 0) {
    console.error('GTM requests blocked:', blockedResources);
  }
  
  return 'See console for GTM initialization status';
})();
```

## The Root Cause

NextJS with App Router (13.4+) changed how scripts load. Your GTM implementation is likely using the old method that no longer works.

## The Fix for NextJS App Router

### Option 1: Using Next.js Script Component (Recommended)

In your `app/layout.tsx`:

```javascript
import Script from 'next/script'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head />
      <body>
        {/* GTM Script with NextJS optimization */}
        <Script
          id="gtm-script"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{
            __html: `
              (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
              new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
              j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
              'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
              })(window,document,'script','dataLayer','GTM-XXXXXX');
            `,
          }}
        />
        
        {/* GTM noscript */}
        <noscript>
          <iframe
            src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXX"
            height="0"
            width="0"
            style={{ display: 'none', visibility: 'hidden' }}
          />
        </noscript>
        
        {children}
      </body>
    </html>
  )
}
```

### Option 2: For Pages Router

In `_app.tsx`:

```javascript
import { useEffect } from 'react'
import { useRouter } from 'next/router'
import Script from 'next/script'

function MyApp({ Component, pageProps }) {
  const router = useRouter()
  
  useEffect(() => {
    // Handle route changes for GTM
    const handleRouteChange = (url) => {
      window.dataLayer?.push({
        event: 'pageview',
        page: url,
      })
    }
    
    router.events.on('routeChangeComplete', handleRouteChange)
    return () => {
      router.events.off('routeChangeComplete', handleRouteChange)
    }
  }, [router.events])
  
  return (
    <>
      <Script
        id="gtm-script"
        strategy="afterInteractive"
        dangerouslySetInnerHTML={{
          __html: `
            (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
            new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
            'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
            })(window,document,'script','dataLayer','GTM-XXXXXX');
          `,
        }}
      />
      <Component {...pageProps} />
    </>
  )
}
```

### Option 3: Using @next/third-parties (Newest Method)

Google now recommends their official package:

```bash
npm install @next/third-parties
```

Then in your layout or app:

```javascript
import { GoogleTagManager } from '@next/third-parties/google'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <GoogleTagManager gtmId="GTM-XXXXXX" />
      </body>
    </html>
  )
}
```

## Why It Broke "Recently"

1. **Next.js 13.4+ App Router** changed script loading behavior
2. **React 18 Strict Mode** in development can double-fire or block GTM
3. **Google's changes** to how GTM validates container installation

## Immediate Fix

If you need tracking working NOW while you implement the proper fix:

1. Temporarily disable React Strict Mode in `next.config.js`:
```javascript
module.exports = {
  reactStrictMode: false, // Temporary for debugging
}
```

2. Clear your `.next` cache: `rm -rf .next`
3. Rebuild: `npm run build`

## Validation

After implementing:
- GTM Preview should show "Connected"
- Analytics should receive data within 30 seconds
- No console errors about GTM initialization

This is a critical infrastructure issue that typically takes 2-4 hours to properly fix and test across all your NextJS/React apps. The key is using Next.js's Script component with the correct strategy.
# Reddit Solution: Purchase Events Not in DataLayer

**User:** u/SquareLengthiness435  
**Post URL:** https://reddit.com/r/GoogleTagManager/comments/1ndqiye/  
**Problem:** "Why don't I see purchase event in data layer when I make Purchase?"  
**Date:** September 11, 2025

## Response

I use a 4-layer diagnostic system for tracking issues, and yours falls squarely in Layer 2: Implementation.

**Layer 2 issues** are when GTM loads correctly but the configuration within GTM or the data being sent to it is broken. This includes missing dataLayer pushes, incorrect trigger timing, or platform integrations not sending data.

For your purchase tracking, here's the diagnostic:

## Step 1: Check what events exist in dataLayer

Run this on your order confirmation page:

```javascript
// See ALL events in your dataLayer
dataLayer.filter(d => d.event).map(d => d.event)
```

## Step 2: Check if purchase data exists but uses different format

```javascript
// Check for common e-commerce patterns
(() => {
  const patterns = ['purchase', 'transaction', 'order_complete', 'checkout_complete'];
  const found = dataLayer.filter(item => {
    return patterns.some(p => 
      item.event?.includes(p) || 
      item.ecommerce?.purchase ||
      item.transactionId
    );
  });
  console.log('E-commerce events found:', found.length > 0 ? found : 'None');
  console.log('All dataLayer:', dataLayer);
})();
```

## Step 3: Verify your platform's integration

Most e-commerce platforms need explicit GTM integration enabled:
- **WooCommerce**: Needs GTM4WP plugin or similar
- **Shopify**: Needs Google & YouTube app with dataLayer enabled
- **Custom builds**: Need manual dataLayer.push() on purchase completion

The fact you see nothing in dataLayer means your platform isn't pushing purchase data at all. This isn't a GTM configuration issue - it's that the data never arrives.

Which e-commerce platform are you using? That determines the exact fix needed.
# GTM Debugging Procedure - THE ONLY WAY TO START

## THE GOLDEN RULE: Record First, Build Second

**NEVER create triggers based on assumptions. ALWAYS start with dataLayer monitoring to record exactly what happens, then build triggers from that evidence.**

## Why This Approach is Critical

- **Eliminates guesswork** - You see exactly what fires
- **Reveals actual element classes** - Not what you think they should be  
- **Shows real event names** - Custom events, gtm.click, etc.
- **Identifies timing issues** - Events that don't fire at all
- **Prevents broken tracking** - Build on facts, not assumptions

**This 2-minute debugging step prevents hours of troubleshooting later.**

## Step 1: Set Up DataLayer Monitoring (MANDATORY)

**Paste this code in browser console on the target website:**

```javascript
// Monitor all dataLayer events
window.dataLayer = window.dataLayer || [];
var originalPush = window.dataLayer.push;
window.dataLayer.push = function() {
  console.log('DataLayer Push:', arguments[0]);
  return originalPush.apply(window.dataLayer, arguments);
};

console.log('DataLayer monitoring active. Perform actions on the website...');
```

## Step 2: Test ALL Target Actions and Find Patterns

**Perform EVERY action you want to track** - don't test just one example.

**CRITICAL: Record the COMPLETE dataLayer output for each action** - copy the entire object, don't summarize.

### Professional Methodology Example:
1. **Test all buttons on the site** (header CTA, footer buttons, form buttons, etc.)
2. **Record dataLayer output for each**
3. **Find common patterns** - what class appears in ALL button clicks?
4. **Build trigger based on the common pattern** 

**Example findings:**
- Button 1: `gtm.elementClasses: 'kb-button kt-button button kb-adv-form-submit-button...'`
- Button 2: `gtm.elementClasses: 'kb-button kt-button button kb-btn41_47a7f1-a0...'`
- Button 3: `gtm.elementClasses: 'kb-button kt-button button wp-block-kadence...'`

**Common pattern:** `kb-button` appears in all → Use this for trigger condition

### Example: What We Learn From Real DataLayer Output

**Instead of assuming:** "It's probably a button with class 'btn'"

**DataLayer shows reality:**
```javascript
{
  event: 'gtm.click', 
  gtm.element: span.kt-btn-inner-text,  // ← You clicked the INNER span, not button!
  gtm.elementClasses: 'kt-btn-inner-text', // ← This is the actual class to target
  gtm.elementUrl: '',
  gtm.triggers: '4,5'
}
```

**Key Insight:** You clicked the text span INSIDE the button, not the button wrapper. Your trigger must match `kt-btn-inner-text`, not `btn` or `button`.

## Step 3: Analyze DataLayer Output

### Example Button Click Output:
```javascript
DataLayer Push: {
  event: 'gtm.click', 
  gtm.element: button.kb-button.kt-button.button.kb-adv-form-submit-button.kb-btnd894fa-ee.kt-btn-size-standard.kt…, 
  gtm.elementClasses: 'kb-button kt-button button kb-adv-form-submit-butt…al-fill kt-btn-has-text-true kt-btn-has-svg-false', 
  gtm.elementId: '', 
  gtm.elementTarget: '', 
  gtm.elementUrl: 'https://gtmsetupservice.com/contact/',
  ...
}
```

### Key Information to Extract:
- **Event Name**: `gtm.click` (use for trigger type)
- **Element Classes**: `kb-button kt-button button` (use for CSS selector)
- **Element Type**: `button` (use for element matching)
- **Additional Properties**: `gtm.elementUrl`, `gtm.elementId`, etc.

## Step 4: Create Trigger Based on DataLayer Evidence

### If Event is `gtm.click`:
- **Trigger Type**: Click - All Elements
- **This trigger fires on**: Some Clicks
- **Fire this trigger when**: Click Classes contains `kb-button` (or whatever classes you observed)

### If Event is Custom (like `form_submit`):
- **Trigger Type**: Custom Event
- **Event Name**: `form_submit` (or whatever event name you observed)

### If Event is `gtm.scrollDepth`:
- **Trigger Type**: Scroll Depth
- **Configure based on observed thresholds**

## Step 5: Validate Variables Work

**In GTM Preview Mode, check these variables return data:**
- `{{Click Element}}` - Should show the HTML element
- `{{Click Classes}}` - Should show CSS classes from dataLayer
- `{{Click Text}}` - Should show button text
- `{{Click URL}}` - Should show link destination

**If variables are empty, the element doesn't match your trigger conditions.**

## Common DataLayer Events by Action Type

### Button/Link Clicks:
```javascript
{event: 'gtm.click', gtm.elementClasses: '...', gtm.elementUrl: '...'}
```
**Trigger Type**: Click - All Elements

### Form Submissions:
```javascript
{event: 'form_submit', form_id: '...', form_name: '...'}
```
**Trigger Type**: Custom Event with event name `form_submit`

### Scroll Tracking:
```javascript
{event: 'gtm.scrollDepth', gtm.scrollThreshold: 75}
```
**Trigger Type**: Scroll Depth

### Video Interactions:
```javascript
{event: 'gtm.video', gtm.videoProvider: 'youtube', gtm.videoTitle: '...'}
```
**Trigger Type**: YouTube Video or Custom Event

## Step 6: Test and Validate

1. **Create trigger based on dataLayer evidence**
2. **Create tag with trigger attached**
3. **Use GTM Preview Mode**
4. **Perform the action**
5. **Verify tag fires in "Tags Fired" section**
6. **Check GA4 DebugView for event**

## Critical Rules

### ❌ NEVER DO THIS:
- Guess CSS selectors without testing
- Create triggers before checking dataLayer
- Assume elements have specific classes
- Copy triggers from other sites without validation

### ✅ ALWAYS DO THIS:
- Monitor dataLayer first
- Use exact event names from dataLayer output
- Match trigger conditions to observed data
- Test every trigger in Preview Mode
- Validate events appear in GA4 DebugView

## Emergency Troubleshooting

### If No DataLayer Events Fire:
1. Check if GTM container is installed
2. Verify GTM Preview Mode is active
3. Test with simpler actions (page views always work)
4. Check browser console for JavaScript errors

### If DataLayer Events Fire But Trigger Doesn't Match:
1. Copy exact `gtm.elementClasses` from dataLayer
2. Use "contains" instead of "equals" for class matching
3. Check for typos in trigger conditions
4. Test with broader matching conditions

### If Trigger Fires But Variables Are Empty:
1. Element doesn't match the built-in variable conditions
2. Use GTM Preview Variables tab to see actual values
3. Create custom JavaScript variables if needed

## Documentation Template

**For every trigger created, document the dataLayer evidence:**
```
Action Tested: [Button click on "Contact Us"]
DataLayer Output: [Paste complete dataLayer object - NEVER summarize this]
Trigger Type: [Click - All Elements]
Trigger Conditions: [Click Classes contains "kt-btn-inner-text"] ← Based on dataLayer evidence
Variables Used: [{{Click Text}}, {{Click URL}}, {{Click Classes}}]
Test Result: [✅ Fires correctly / ❌ Does not fire]
```

## The Professional Approach

**This is how professional GTM implementations are built:**

1. **Record dataLayer evidence FIRST**
2. **Build triggers based on that evidence**  
3. **Test and validate**
4. **Document the evidence for future reference**

**This approach transforms you from "GTM guesser" to "GTM professional" - you work with facts, not assumptions.**

---

**REMEMBER: This 5-minute debugging process saves hours of guesswork and prevents broken tracking implementations.**
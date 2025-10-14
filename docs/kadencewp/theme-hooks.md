# Kadence Theme Hooks Reference

A comprehensive list of action hooks available in the Kadence WordPress theme for developers and AI assistants.

## Body Structure Hooks

### Site Wrapper
- `kadence_before_wrapper` - Before the main site wrapper
- `kadence_after_wrapper` - After the main site wrapper

## Header Hooks

### Header Container
- `kadence_before_header` - Before the entire header area
- `kadence_after_header` - After the entire header area
- `kadence_replace_header` - Replace the entire header (use with caution)
- `kadence_header` - Main header hook

### Header Sections
- `kadence_top_header` - Top header bar area
- `kadence_main_header` - Main header area (logo, navigation)
- `kadence_bottom_header` - Bottom header area
- `kadence_mobile_header` - Mobile-specific header

### Branding & Navigation
- `kadence_site_branding` - Logo and site title area
- `before_kadence_logo_output` - Before logo output
- `kadence_primary_navigation` - Primary navigation menu area

## Content Area Hooks

### Content Wrapper
- `kadence_before_content` - Before all content (after header)
- `kadence_after_content` - After all content (before footer)

### Main Content & Sidebar
- `kadence_before_main_content` - Before main content area
- `kadence_after_main_content` - After main content area
- `kadence_before_sidebar` - Before sidebar
- `kadence_after_sidebar` - After sidebar

### Hero/Title Areas
- `kadence_entry_hero` - Above page/post title (use priority for positioning)
- `kadence_entry_archive_hero` - Above archive title (use priority for positioning)

## Single Post/Page Hooks

### Inner Content Structure
- `kadence_single_before_inner_content` - Before post/page inner content
- `kadence_single_after_inner_content` - After post/page inner content

### Title Area
- `kadence_single_before_entry_header` - Before title area container
- `kadence_single_before_entry_title` - Before the actual title
- `kadence_single_after_entry_title` - After the actual title
- `kadence_single_after_entry_header` - After title area container

### Content Area
- `kadence_single_before_entry_content` - Before post/page content
- `kadence_single_after_entry_content` - After post/page content

## Archive Page Hooks

### Archive Structure
- `kadence_before_archive_content` - Before archive content
- `kadence_archive_before_entry_header` - Before archive title area
- `kadence_archive_after_entry_header` - After archive title area

## Comments Hooks

### Comments Structure
- `kadence_before_comments` - Before entire comments section
- `kadence_after_comments` - After entire comments section
- `kadence_before_comments_list` - Before comments list
- `kadence_after_comments_list` - After comments list

## Footer Hooks

### Footer Container
- `kadence_before_footer` - Before the entire footer area
- `kadence_after_footer` - After the entire footer area
- `kadence_footer` - Main footer hook

### Footer Sections
- `kadence_top_footer` - Top footer area
- `kadence_main_footer` - Main footer area (widgets)
- `kadence_bottom_footer` - Bottom footer area (copyright)

## Special Page Hooks

### 404 Error Page
- `kadence_404_before_inner_content` - Before 404 page content
- `kadence_404_after_inner_content` - After 404 page content

### Mobile Navigation
- `kadence_before_mobile_navigation_popup` - Before mobile menu popup
- `kadence_after_mobile_navigation_popup` - After mobile menu popup

### Account Login Modal
- `kadence_before_account_login_popup` - Before login popup
- `kadence_after_account_login_popup` - After login popup
- `kadence_before_account_login_inner_popup` - Before inner login popup content
- `kadence_after_account_login_inner_popup` - After inner login popup content

## Post Loop Hooks

### Loop Structure
- `kadence_loop_entry` - Individual loop entry
- `kadence_loop_entry_thumbnail` - Loop entry featured image
- `kadence_loop_entry_content` - Loop entry content area
- `kadence_before_loop_entry_meta` - Before loop entry metadata
- `kadence_after_loop_entry_meta` - After loop entry metadata

## Kadence Blocks Post Grid/Carousel Hooks

### Post Block Structure
- `kadence_blocks_post_loop_start` - Start of post block loop
- `kadence_blocks_post_loop_header` - Post block header area
- `kadence_blocks_post_loop_header_meta` - Post block header metadata
- `kadence_blocks_post_loop_content` - Post block content area
- `kadence_blocks_post_loop_footer_start` - Start of post block footer
- `kadence_blocks_post_loop_footer_end` - End of post block footer
- `kadence_blocks_post_loop_end` - End of post block loop

## Common Use Cases for GTM/Analytics

### Best Hooks for Analytics/GTM Injection:
- **Header scripts**: `kadence_before_header` (priority 1)
- **Body scripts**: `kadence_after_header` (priority 1)
- **Footer scripts**: `kadence_before_footer` (priority 1)
- **Admin bars**: `kadence_before_wrapper` or `kadence_after_wrapper`

### Hook Priority Guidelines:
- **Priority 1-5**: Critical functionality (GTM, analytics)
- **Priority 10**: Default priority
- **Priority 20+**: Non-critical additions

## Usage Example:
```php
// Add content to header
add_action('kadence_before_header', 'my_custom_function', 1);

function my_custom_function() {
    // Your code here
}
```

## Finding Additional Hooks:
Search for `do_action` in `/wp-content/themes/kadence/` directory for complete hook list.
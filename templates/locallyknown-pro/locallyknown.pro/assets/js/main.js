// LocallyKnown.pro Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Form handler
    const form = document.getElementById('contact-form');
    const submitBtn = document.getElementById('submit-btn');
    const successMsg = document.getElementById('form-success');
    const errorMsg = document.getElementById('form-error');

    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Disable submit button
            submitBtn.disabled = true;
            submitBtn.innerHTML = 'Submitting...';

            // Hide previous messages
            if (successMsg) successMsg.classList.add('hidden');
            if (errorMsg) errorMsg.classList.add('hidden');

            // Collect form data
            const formData = new FormData(form);
            const data = {};

            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }

            // Prepare payload for FluentCRM
            const payload = {
                email: data.email,
                first_name: data.name.split(' ')[0],
                last_name: data.name.split(' ').slice(1).join(' '),
                phone: data.phone,
                tags: ['jekyll-lead', 'website-foundation', 'locallyknown-pro'],
                custom_fields: {
                    website: data.website,
                    business_type: data.business_type,
                    competitors: data.competitors,
                    service_type: data.service_type,
                    source_domain: data.source_domain,
                    form_submitted: new Date().toISOString()
                },
                lists: [2] // Jekyll leads list
            };

            try {
                // Send to FluentCRM API
                const authString = btoa('fluent:RxEt Hnzh kH8x dmps pbxd S607');
                const response = await fetch('https://getlocallyknown.com/wp-json/fluent-crm/v2/contacts', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Basic ' + authString
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    // Track successful form submission
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'generate_lead', {
                            'currency': 'USD',
                            'value': 4500,
                            'service_type': 'jekyll_foundation',
                            'business_type': data.business_type
                        });
                    }

                    // Track in GTM dataLayer
                    if (typeof dataLayer !== 'undefined') {
                        dataLayer.push({
                            'event': 'form_submission',
                            'form_name': 'jekyll_foundation_form',
                            'service_type': 'jekyll_foundation',
                            'business_type': data.business_type,
                            'conversion_value': 4500
                        });
                    }

                    // Show success message
                    if (successMsg) successMsg.classList.remove('hidden');
                    form.reset();
                } else {
                    throw new Error('Form submission failed');
                }

            } catch (error) {
                console.error('Form submission error:', error);
                if (errorMsg) errorMsg.classList.remove('hidden');

                // Track form error
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'form_error', {
                        'service_type': 'jekyll_foundation',
                        'error_type': 'submission_failed'
                    });
                }
            } finally {
                // Re-enable submit button
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Get My Digital Foundation - $4,500';
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
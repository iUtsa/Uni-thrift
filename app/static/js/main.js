// Main JavaScript file for Student Marketplace

document.addEventListener('DOMContentLoaded', function() {

    // Auto dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('[role="alert"]');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.classList.add('opacity-0');
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Sticky header - add shadow on scroll
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) {
                header.classList.add('shadow-lg');
            } else {
                header.classList.remove('shadow-lg');
            }
        });
    }

    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('#mobile-menu-toggle');
    const mobileMenu = document.querySelector('#mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Initialize tooltips if any
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', e => {
            const content = e.target.getAttribute('data-tooltip');
            const tooltipEl = document.createElement('div');
            tooltipEl.className = 'absolute z-50 bg-gray-800 text-white text-xs rounded py-1 px-2 -mt-8';
            tooltipEl.textContent = content;
            
            // Position the tooltip
            e.target.style.position = 'relative';
            e.target.appendChild(tooltipEl);
        });
        
        tooltip.addEventListener('mouseleave', e => {
            const tooltipEl = e.target.querySelector('.absolute');
            if (tooltipEl) {
                tooltipEl.remove();
            }
        });
    });

    // Price range input (if exists)
    const priceRange = document.querySelector('#price-range');
    const priceOutput = document.querySelector('#price-output');
    
    if (priceRange && priceOutput) {
        priceRange.addEventListener('input', () => {
            priceOutput.textContent = `$${priceRange.value}`;
        });
    }

    // Initialize any dropdowns in the page
    const dropdownToggleButtons = document.querySelectorAll('[data-dropdown-toggle]');
    
    dropdownToggleButtons.forEach(button => {
        const targetId = button.getAttribute('data-dropdown-toggle');
        const targetDropdown = document.getElementById(targetId);
        
        if (targetDropdown) {
            button.addEventListener('click', () => {
                targetDropdown.classList.toggle('hidden');
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', e => {
                if (!button.contains(e.target) && !targetDropdown.contains(e.target)) {
                    targetDropdown.classList.add('hidden');
                }
            });
        }
    });

    // Implement "Back to Top" functionality
    const backToTopButton = document.querySelector('#back-to-top');
    
    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTopButton.classList.remove('hidden');
            } else {
                backToTopButton.classList.add('hidden');
            }
        });
        
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Form validation (if needed)
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', e => {
            let hasError = false;
            
            // Check required fields
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    e.preventDefault();
                    hasError = true;
                    
                    // Add error styling
                    field.classList.add('border-red-500');
                    
                    // Get or create error message
                    let errorMessage = field.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                        errorMessage = document.createElement('p');
                        errorMessage.className = 'text-red-500 text-xs mt-1 error-message';
                        field.parentNode.insertBefore(errorMessage, field.nextSibling);
                    }
                    
                    errorMessage.textContent = 'This field is required';
                } else {// Remove error styling if it was previously added
                    field.classList.remove('border-red-500');
                    
                    // Remove error message if it exists
                    const errorMessage = field.nextElementSibling;
                    if (errorMessage && errorMessage.classList.contains('error-message')) {
                        errorMessage.remove();
                    }
                }
            });
            
            // Email validation
            const emailFields = form.querySelectorAll('input[type="email"]');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            emailFields.forEach(field => {
                if (field.value.trim() && !emailRegex.test(field.value.trim())) {
                    e.preventDefault();
                    hasError = true;
                    
                    // Add error styling
                    field.classList.add('border-red-500');
                    
                    // Get or create error message
                    let errorMessage = field.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                        errorMessage = document.createElement('p');
                        errorMessage.className = 'text-red-500 text-xs mt-1 error-message';
                        field.parentNode.insertBefore(errorMessage, field.nextSibling);
                    }
                    
                    errorMessage.textContent = 'Please enter a valid email address';
                }
            });
            
            // Password match validation (if applicable)
            const password = form.querySelector('input[name="password"]');
            const passwordConfirm = form.querySelector('input[name="password2"]');
            
            if (password && passwordConfirm) {
                if (password.value !== passwordConfirm.value) {
                    e.preventDefault();
                    hasError = true;
                    
                    // Add error styling
                    passwordConfirm.classList.add('border-red-500');
                    
                    // Get or create error message
                    let errorMessage = passwordConfirm.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                        errorMessage = document.createElement('p');
                        errorMessage.className = 'text-red-500 text-xs mt-1 error-message';
                        passwordConfirm.parentNode.insertBefore(errorMessage, passwordConfirm.nextSibling);
                    }
                    
                    errorMessage.textContent = 'Passwords do not match';
                }
            }
            
            if (hasError) {
                // Scroll to the first error
                const firstError = form.querySelector('.border-red-500');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    });
});


// Simple automatic slideshow
document.addEventListener('DOMContentLoaded', function() {
    const slideshows = document.querySelectorAll('.slideshow-container');
    
    slideshows.forEach(function(slideshow) {
      const slides = slideshow.querySelectorAll('.slide');
      const indicators = slideshow.querySelectorAll('.indicator');
      let currentSlide = 0;
      const slideInterval = 4000; // Change slides every 4 seconds
      
      // Two options to run the slideshow:
      
      // Option 1: Using CSS animations (simpler, add these classes)
      slides.forEach(slide => {
        slide.classList.add('slide-animated');
      });
      
      // Option 2: Using JavaScript for more control
      function showSlide(n) {
        // Hide all slides
        slides.forEach(slide => {
          slide.classList.remove('active');
        });
        
        // Remove active class from all indicators
        indicators.forEach(indicator => {
          indicator.classList.remove('active');
        });
        
        // Show the current slide
        slides[n].classList.add('active');
        
        // Highlight current indicator
        if (indicators.length > 0) {
          indicators[n].classList.add('active');
        }
      }
      
      // Initialize the first slide
      showSlide(currentSlide);
      
      // Set up automatic slideshow
      setInterval(function() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
      }, slideInterval);
      
      // Optional: Add click event to indicators
      indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
          currentSlide = index;
          showSlide(currentSlide);
        });
      });
    });
  });
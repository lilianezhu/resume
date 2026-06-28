// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Toggle mobile menu
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }

    // Close mobile menu when a link is clicked
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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

    // CTA Button animation
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('click', function() {
            // Scroll to about section
            document.querySelector('#about').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    }

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe cards and items
    document.querySelectorAll('.card, .activity-card, .subject-item').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });

    // Add scroll class to navbar
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.15)';
        } else {
            navbar.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        }
    });

    // Animate skill bars on scroll
    const skillBars = document.querySelectorAll('.skill-bar');
    const skillObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const skillFill = entry.target.querySelector('.skill-fill');
                skillFill.style.animation = 'fillSkill 1.5s ease-out forwards';
                skillObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    skillBars.forEach(bar => {
        skillObserver.observe(bar);
    });

    // Add animation style for skill fill
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fillSkill {
            from {
                width: 0 !important;
            }
        }
    `;
    document.head.appendChild(style);

    // Contact card hover effect
    const contactCards = document.querySelectorAll('.contact-card');
    contactCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Add active state to navigation links based on scroll position
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('section');
        const scrollPosition = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });

    // Stat counter animation
    const statBoxes = document.querySelectorAll('.stat-box p');
    const countObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                countObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    function animateCounter(element) {
        const finalValue = parseFloat(element.textContent);
        const isDecimal = element.textContent.includes('.');
        let currentValue = 0;
        const increment = finalValue / 50;

        const counter = setInterval(function() {
            currentValue += increment;
            if (currentValue >= finalValue) {
                element.textContent = isDecimal ? finalValue.toFixed(1) : Math.round(finalValue);
                clearInterval(counter);
            } else {
                element.textContent = isDecimal ? currentValue.toFixed(1) : Math.round(currentValue);
            }
        }, 20);
    }

    statBoxes.forEach(box => {
        countObserver.observe(box);
    });

    // Interactive activity cards
    const activityCards = document.querySelectorAll('.activity-card');
    activityCards.forEach((card, index) => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) rotateZ(1deg)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotateZ(0deg)';
        });
    });

    // Log page load
    console.log('Resume website loaded successfully!');
    console.log('Welcome to the student resume. Explore all sections to learn more.');
});

// Prevent console errors
window.addEventListener('error', function(e) {
    console.error('An error occurred:', e.error);
});

// Add page visibility API to pause animations when tab is not active
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        console.log('Page hidden');
    } else {
        console.log('Page visible');
    }
});

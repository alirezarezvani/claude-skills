// ===== Mobile Navigation Toggle =====
const mobileToggle = document.getElementById('mobileToggle');
const navLinks = document.getElementById('navLinks');

mobileToggle.addEventListener('click', () => {
  navLinks.classList.toggle('active');
  mobileToggle.classList.toggle('active');
});

// Close mobile nav on link click
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('active');
    mobileToggle.classList.remove('active');
  });
});

// ===== Navbar Scroll Effect =====
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// ===== FAQ Accordion =====
document.querySelectorAll('.faq-question').forEach(button => {
  button.addEventListener('click', () => {
    const item = button.parentElement;
    const isActive = item.classList.contains('active');

    // Close all other FAQ items
    document.querySelectorAll('.faq-item').forEach(faq => {
      faq.classList.remove('active');
      faq.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
    });

    // Toggle current item
    if (!isActive) {
      item.classList.add('active');
      button.setAttribute('aria-expanded', 'true');
    }
  });
});

// ===== Smooth Scroll for anchor links =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const targetId = anchor.getAttribute('href');
    if (targetId === '#') return;

    const target = document.querySelector(targetId);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// ===== Form Validation & Submission =====
const form = document.getElementById('cashOfferForm');
const formSuccess = document.getElementById('formSuccess');

if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();

    // Clear previous errors
    form.querySelectorAll('.form-group').forEach(group => {
      group.classList.remove('error');
      const existing = group.querySelector('.error-message');
      if (existing) existing.remove();
    });

    let isValid = true;

    // Validate required fields
    const requiredFields = [
      { id: 'fullName', label: 'Full name is required' },
      { id: 'phone', label: 'Phone number is required' },
      { id: 'email', label: 'Email address is required' },
      { id: 'address', label: 'Property address is required' }
    ];

    requiredFields.forEach(field => {
      const input = document.getElementById(field.id);
      if (!input.value.trim()) {
        isValid = false;
        showError(input, field.label);
      }
    });

    // Validate email format
    const emailInput = document.getElementById('email');
    if (emailInput.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value)) {
      isValid = false;
      showError(emailInput, 'Please enter a valid email address');
    }

    // Validate phone format (basic)
    const phoneInput = document.getElementById('phone');
    const phoneDigits = phoneInput.value.replace(/\D/g, '');
    if (phoneInput.value.trim() && phoneDigits.length < 10) {
      isValid = false;
      showError(phoneInput, 'Please enter a valid 10-digit phone number');
    }

    if (isValid) {
      // Collect form data
      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());

      // Log submission (replace with actual backend endpoint)
      console.log('Form submitted:', data);

      // Show success message
      form.style.display = 'none';
      formSuccess.style.display = 'block';

      // Scroll to success message
      formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });
}

function showError(input, message) {
  const group = input.closest('.form-group');
  group.classList.add('error');

  const errorEl = document.createElement('div');
  errorEl.className = 'error-message';
  errorEl.textContent = message;
  group.appendChild(errorEl);
}

// ===== Phone Number Formatting =====
const phoneInput = document.getElementById('phone');
if (phoneInput) {
  phoneInput.addEventListener('input', (e) => {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 10) value = value.slice(0, 10);

    if (value.length >= 6) {
      value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
    } else if (value.length >= 3) {
      value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
    }

    e.target.value = value;
  });
}

// ===== Intersection Observer for Scroll Animations =====
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -40px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe all cards and sections for entrance animations
document.querySelectorAll(
  '.step-card, .situation-card, .testimonial-card, .comp-row, .faq-item'
).forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  observer.observe(el);
});

// Add animation class styles
const style = document.createElement('style');
style.textContent = `.animate-in { opacity: 1 !important; transform: translateY(0) !important; }`;
document.head.appendChild(style);

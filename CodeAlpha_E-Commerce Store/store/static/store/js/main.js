document.addEventListener('DOMContentLoaded', function () {
    const animatedItems = document.querySelectorAll('[data-animate]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    animatedItems.forEach((item, index) => {
        item.style.setProperty('--delay', `${index * 120}ms`);
        observer.observe(item);
    });

    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            navbar.classList.toggle('navbar-scrolled', window.scrollY > 40);
        });
    }
});

function changeQuantity(inputId, delta) {
    const input = document.getElementById(inputId);
    if (!input) return;
    let value = parseInt(input.value, 10) || 1;
    value += delta;
    if (input.min) value = Math.max(value, parseInt(input.min, 10));
    if (input.max) value = Math.min(value, parseInt(input.max, 10));
    input.value = value;
}

function pulseButton(button) {
    if (!button) return;
    button.classList.add('pulse');
    setTimeout(() => button.classList.remove('pulse'), 360);
}

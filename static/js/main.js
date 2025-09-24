// Main JavaScript for Meu Novo Amigo Pet

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

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

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Image lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Search form enhancement
    const searchForm = document.querySelector('form[method="get"]');
    if (searchForm) {
        const inputs = searchForm.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                // Auto-submit form when filters change
                if (this.type !== 'text' || this.value.length >= 3) {
                    searchForm.submit();
                }
            });
        });
    }

    // Pet card hover effects
    document.querySelectorAll('.pet-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Back to top button
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary position-fixed';
    backToTopButton.style.cssText = `
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: none;
        box-shadow: 0 4px 15px rgba(0,123,255,0.3);
    `;
    document.body.appendChild(backToTopButton);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Loading states for buttons
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        button.addEventListener('click', function(e) {
            const form = this.form;
            if (form && form.checkValidity()) {
                // Permitir que o formulário seja enviado primeiro
                setTimeout(() => {
                    this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processando...';
                    this.disabled = true;
                }, 100);
            }
        });
    });

    // Confirmation dialogs
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(e) {
            const message = this.dataset.confirm || 'Tem certeza que deseja continuar?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Copy to clipboard functionality
    document.querySelectorAll('[data-copy]').forEach(button => {
        button.addEventListener('click', function() {
            const text = this.dataset.copy;
            navigator.clipboard.writeText(text).then(() => {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Copiado!';
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            });
        });
    });

    // Dynamic form fields
    document.querySelectorAll('[data-add-field]').forEach(button => {
        button.addEventListener('click', function() {
            const template = document.querySelector(this.dataset.addField);
            const container = document.querySelector(this.dataset.target);
            const clone = template.content.cloneNode(true);
            container.appendChild(clone);
        });
    });

    // Remove dynamic form fields
    document.addEventListener('click', function(e) {
        if (e.target.matches('[data-remove-field]')) {
            e.target.closest('.dynamic-field').remove();
        }
    });

    // File upload preview
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.querySelector(`[data-preview="${input.name}"]`);
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Search suggestions (if needed)
    const searchInputs = document.querySelectorAll('input[data-suggestions]');
    searchInputs.forEach(input => {
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                // Implement search suggestions here
                console.log('Searching for:', this.value);
            }, 300);
        });
    });

    // Initialize animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .stats-card').forEach(el => {
        observer.observe(el);
    });
});

// Utility functions
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    const container = document.querySelector('.toast-container') || createToastContainer();
    container.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length >= 11) {
        value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (value.length >= 7) {
        value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
    } else if (value.length >= 3) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    }
    input.value = value;
}

// Initialize phone formatting
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('input[type="tel"], input[name*="telefone"]').forEach(input => {
        input.addEventListener('input', function() {
            formatPhoneNumber(this);
        });
    });
});

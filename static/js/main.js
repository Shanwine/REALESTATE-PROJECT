// EstateHub – Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('show'));
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 991 && !sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }

    // Auto-dismiss alerts after 4 seconds
    document.querySelectorAll('.alert-dismissible').forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 4000);
    });

    // Favorite toggle via AJAX
    document.querySelectorAll('.btn-favorite-ajax').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.dataset.url;
            const icon = this.querySelector('i');
            fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                .then(r => r.json())
                .then(data => {
                    if (data.is_favorited) {
                        icon.className = 'bi bi-heart-fill';
                        icon.style.color = '#ef4444';
                    } else {
                        icon.className = 'bi bi-heart';
                        icon.style.color = '';
                    }
                });
        });
    });

    // Image preview for file inputs
    const imgInput = document.getElementById('id_images') || document.querySelector('input[name="images"]');
    const previewContainer = document.getElementById('imagePreview');
    if (imgInput && previewContainer) {
        imgInput.addEventListener('change', function() {
            previewContainer.innerHTML = '';
            Array.from(this.files).forEach(file => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.style.cssText = 'width:80px;height:80px;object-fit:cover;border-radius:8px;border:1px solid var(--border);';
                    previewContainer.appendChild(img);
                };
                reader.readAsDataURL(file);
            });
        });
    }
});

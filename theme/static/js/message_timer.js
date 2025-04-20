
document.addEventListener('DOMContentLoaded', function() {
    // Get all toast elements
    const toasts = document.querySelectorAll('.toast');

    // Set timeout to remove each toast after X seconds (e.g., 5000ms = 5 seconds)
    toasts.forEach(function(toast) {
        setTimeout(function() {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.5s ease';
        
            // Remove from DOM after fade out completes
            setTimeout(function() {
                toast.remove();
            }, 500);
        }, 5000); // 5 seconds
    });
});

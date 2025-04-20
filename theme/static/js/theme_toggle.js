document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.querySelector('.theme-controller');
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    // Set initial theme
    document.documentElement.setAttribute('data-theme', savedTheme);
    themeToggle.checked = savedTheme === 'dracula';
    
    // Update theme when toggled
    themeToggle.addEventListener('change', function() {
        const theme = this.checked ? 'dracula' : 'light';
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    });
});

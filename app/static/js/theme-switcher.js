class ThemeSwitcher {
    constructor() {

        this.theme = localStorage.getItem('finhealth-theme') || 'dark';
        this.init();
    }

    init() {
        // Apply theme immediately
        this.applyTheme(this.theme);
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.createToggleButton());
        } else {
            this.createToggleButton();
        }
    }

    applyTheme(theme) {
        // Set data-theme on html element
        document.documentElement.setAttribute('data-theme', theme);
        this.theme = theme;
        localStorage.setItem('finhealth-theme', theme);
        
        console.log(`✅ Theme applied: ${theme}`);
    }

    toggleTheme() {
        const newTheme = this.theme === 'dark' ? 'light' : 'dark';
        this.applyTheme(newTheme);
        this.updateToggleButton();
        
        // Add transition class
        document.body.style.transition = 'all 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    createToggleButton() {
        const navbar = document.querySelector('.navbar-nav');
        if (!navbar) {
            console.warn('⚠️ Navbar not found');
            return;
        }

        // Check if button already exists
        if (document.getElementById('theme-toggle-container')) {
            return;
        }

        const themeToggle = document.createElement('li');
        themeToggle.id = 'theme-toggle-container';
        themeToggle.style.cssText = 'list-style: none;';
        
        themeToggle.innerHTML = `
            <button id="theme-toggle" class="btn btn-sm" style="
                padding: 0.5rem;
                background: var(--dark-card);
                border: 1px solid var(--dark-border);
                border-radius: var(--radius);
                display: flex;
                align-items: center;
                gap: 0.5rem;
                color: var(--text-primary);
                transition: all 0.3s ease;
            " title="${this.theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}">
                ${this.getThemeIcon()}
            </button>
        `;
        
        // Insert at beginning of navbar
        navbar.insertBefore(themeToggle, navbar.firstChild);

        // Add click event
        const button = document.getElementById('theme-toggle');
        button.addEventListener('click', () => {
            this.toggleTheme();
        });
        
        // Add hover effect
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'scale(1.05)';
            button.style.borderColor = 'var(--primary-color)';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'scale(1)';
            button.style.borderColor = 'var(--dark-border)';
        });
        
        console.log('✅ Theme toggle button created');
    }

    updateToggleButton() {
        const button = document.getElementById('theme-toggle');
        if (button) {
            button.innerHTML = this.getThemeIcon();
            button.title = this.theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
        }
    }

    getThemeIcon() {
        if (this.theme === 'dark') {
            // Sun icon for switching to light
            return `
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <circle cx="12" cy="12" r="5"/>
                    <path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
                </svg>
            `;
        } else {
            // Moon icon for switching to dark
            return `
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M21.64 13a1 1 0 00-1.05-.14 8.05 8.05 0 01-3.37.73 8.15 8.15 0 01-8.14-8.1 8.59 8.59 0 01.25-2A1 1 0 008 2.36a10.14 10.14 0 1014 11.69 1 1 0 00-.36-1.05z"/>
                </svg>
            `;
        }
    }
}

// Initialize theme switcher when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (window.location.pathname.includes('dashboard')) {
            window.themeSwitcher = new ThemeSwitcher();
        }
    });
} else {
    if (window.location.pathname.includes('dashboard')) {
        window.themeSwitcher = new ThemeSwitcher();
    }
}
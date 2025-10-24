// CodeClash Main JavaScript

// Utility function to show notifications with accessibility support
function showNotification(message, type = 'info') {
    const colors = {
        success: 'bg-green-600 border-green-500',
        error: 'bg-red-600 border-red-500',
        info: 'bg-blue-600 border-blue-500',
        warning: 'bg-yellow-600 border-yellow-500'
    };
    
    const icons = {
        success: 'bi-check-circle-fill',
        error: 'bi-x-circle-fill',
        info: 'bi-info-circle-fill',
        warning: 'bi-exclamation-triangle-fill'
    };
    
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-4 rounded-xl shadow-2xl z-50 border-2 transition-all duration-300`;
    notification.setAttribute('role', type === 'error' ? 'alert' : 'status');
    notification.setAttribute('aria-live', type === 'error' ? 'assertive' : 'polite');
    notification.innerHTML = `
        <div class="flex items-center gap-3">
            <i class="bi ${icons[type]} text-xl" aria-hidden="true"></i>
            <span class="font-medium">${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" 
                    class="cursor-pointer ml-2 hover:bg-white/20 rounded p-1 transition-colors focus:outline-none focus:ring-2 focus:ring-white"
                    aria-label="Close notification">
                <i class="bi bi-x-lg" aria-hidden="true"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateY(0)';
        notification.style.opacity = '1';
    }, 10);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(-20px)';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Format time display
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

// Validate code before submission
function validateCode(code) {
    if (!code || code.trim().length === 0) {
        return { valid: false, message: 'Code cannot be empty' };
    }
    
    if (code.includes('pass') && code.trim().endsWith('pass')) {
        return { valid: false, message: 'Please implement the function' };
    }
    
    return { valid: true };
}

// Copy text to clipboard with better feedback
function copyToClipboard(text) {
    if (!navigator.clipboard) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            showNotification('Copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy:', err);
            showNotification('Failed to copy', 'error');
        }
        
        document.body.removeChild(textArea);
        return;
    }
    
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showNotification('Failed to copy', 'error');
    });
}

// Keyboard shortcuts handler with better accessibility
document.addEventListener('keydown', (e) => {
    // Skip if user is typing in an input field
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) {
        return;
    }
    
    // Ctrl/Cmd + Enter to run code (if on match page)
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const runBtn = document.getElementById('runBtn');
        if (runBtn && !runBtn.disabled) {
            e.preventDefault();
            runBtn.click();
        }
    }
    
    // Ctrl/Cmd + S to submit (if on match page)
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const submitBtn = document.getElementById('submitBtn');
        if (submitBtn && !submitBtn.disabled) {
            submitBtn.click();
        }
    }
    
    // Press '?' to show keyboard shortcuts (future feature)
    if (e.key === '?' && !e.shiftKey) {
        e.preventDefault();
        showKeyboardShortcuts();
    }
});

// Show keyboard shortcuts modal (placeholder for future implementation)
function showKeyboardShortcuts() {
    const shortcuts = [
        { key: 'Ctrl/Cmd + Enter', description: 'Run code' },
        { key: 'Ctrl/Cmd + S', description: 'Submit solution' },
        { key: 'H', description: 'Toggle hints' },
        { key: 'P', description: 'Select Python (on language page)' },
        { key: 'J', description: 'Select Java (on language page)' },
        { key: 'F/E/A/D', description: 'Select difficulty level' },
        { key: '?', description: 'Show this help' }
    ];
    
    console.log('Keyboard Shortcuts:', shortcuts);
    showNotification('Check console for keyboard shortcuts', 'info');
}

// Auto-resize textarea with better performance
function autoResizeTextarea(textarea) {
    if (!textarea) return;
    
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Enhanced tooltip system with ARIA support
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        // Add ARIA attributes
        element.setAttribute('aria-describedby', `tooltip-${Math.random().toString(36).substr(2, 9)}`);
        
        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            const tooltipId = e.target.getAttribute('aria-describedby');
            tooltip.id = tooltipId;
            tooltip.className = 'absolute bg-gray-800 text-white text-sm px-4 py-2 rounded-lg shadow-xl z-50 border border-gray-600';
            tooltip.setAttribute('role', 'tooltip');
            tooltip.textContent = e.target.dataset.tooltip;
            
            // Position tooltip
            const rect = e.target.getBoundingClientRect();
            tooltip.style.position = 'fixed';
            tooltip.style.top = (rect.top - 40) + 'px';
            tooltip.style.left = rect.left + 'px';
            
            document.body.appendChild(tooltip);
        });
        
        element.addEventListener('mouseleave', (e) => {
            const tooltipId = e.target.getAttribute('aria-describedby');
            const tooltip = document.getElementById(tooltipId);
            if (tooltip) tooltip.remove();
        });
        
        // Also show tooltip on focus for keyboard users
        element.addEventListener('focus', (e) => {
            e.target.dispatchEvent(new Event('mouseenter'));
        });
        
        element.addEventListener('blur', (e) => {
            e.target.dispatchEvent(new Event('mouseleave'));
        });
    });
}

// Syntax highlighting for code (basic) with better contrast
function highlightCode(code) {
    // Basic Python syntax highlighting with AAA contrast colors
    const keywords = ['def', 'return', 'if', 'else', 'elif', 'for', 'while', 'in', 'and', 'or', 'not', 'pass', 'break', 'continue', 'class', 'import', 'from', 'as', 'try', 'except', 'finally', 'with', 'lambda', 'yield'];
    
    let highlighted = code;
    keywords.forEach(keyword => {
        const regex = new RegExp(`\\b${keyword}\\b`, 'g');
        highlighted = highlighted.replace(regex, `<span class="text-purple-300 font-semibold">${keyword}</span>`);
    });
    
    return highlighted;
}

// Confirm before leaving page during active match
let isMatchActive = false;

window.addEventListener('beforeunload', (e) => {
    if (isMatchActive) {
        e.preventDefault();
        e.returnValue = 'You have an active match. Are you sure you want to leave?';
        return e.returnValue;
    }
});

// Detect user's preferred color scheme (for future dark/light mode)
function detectColorScheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
        console.log('User prefers light mode');
        // Could add light mode support here
    }
}

// Detect reduced motion preference
function detectReducedMotion() {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        console.log('User prefers reduced motion');
        document.documentElement.classList.add('reduce-motion');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('CodeClash initialized');
    initTooltips();
    detectColorScheme();
    detectReducedMotion();
    
    // Announce page title to screen readers
    const pageTitle = document.querySelector('h1');
    if (pageTitle) {
        console.log('Current page:', pageTitle.textContent);
    }
});

// Service Worker registration for future PWA support
if ('serviceWorker' in navigator) {
    // Commented out for now - can be enabled when PWA is implemented
    // navigator.serviceWorker.register('/sw.js').then(() => {
    //     console.log('Service Worker registered');
    // });
}

// Export functions for use in other scripts
window.CodeClash = {
    showNotification,
    formatTime,
    validateCode,
    copyToClipboard,
    highlightCode,
    autoResizeTextarea,
    showKeyboardShortcuts,
    db: {
        saveSolvedChallenge: async (challenge) => {
            if (typeof SolvedChallengesDB !== 'undefined') {
                return await SolvedChallengesDB.save(challenge);
            }
            throw new Error('Database not initialized');
        },
        getChallengeById: async (problemNumber) => {
            if (typeof SolvedChallengesDB !== 'undefined') {
                return await SolvedChallengesDB.getById(problemNumber);
            }
            throw new Error('Database not initialized');
        },
        getAllSolved: async () => {
            if (typeof SolvedChallengesDB !== 'undefined') {
                return await SolvedChallengesDB.getAll();
            }
            throw new Error('Database not initialized');
        },
        getStats: async () => {
            if (typeof SolvedChallengesDB !== 'undefined') {
                return await SolvedChallengesDB.getStats();
            }
            throw new Error('Database not initialized');
        }
    }
};

// Make notification function globally available for inline onclick handlers
window.showNotification = showNotification;

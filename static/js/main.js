// CodeClash Main JavaScript

// Utility function to show notifications
function showNotification(message, type = 'info') {
    const colors = {
        success: 'bg-green-600',
        error: 'bg-red-600',
        info: 'bg-blue-600',
        warning: 'bg-yellow-600'
    };
    
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-slide-in`;
    notification.innerHTML = `
        <div class="flex items-center gap-2">
            <i class="bi bi-info-circle"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
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

// Copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showNotification('Failed to copy', 'error');
    });
}

// Keyboard shortcuts handler
document.addEventListener('keydown', (e) => {
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
        const submitBtn = document.getElementById('submitBtn');
        if (submitBtn && !submitBtn.disabled) {
            e.preventDefault();
            submitBtn.click();
        }
    }
});

// Auto-resize textarea
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Initialize tooltips (if needed)
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute bg-gray-900 text-white text-sm px-3 py-2 rounded shadow-lg z-50';
            tooltip.textContent = e.target.dataset.tooltip;
            tooltip.style.top = e.target.offsetTop - 40 + 'px';
            tooltip.style.left = e.target.offsetLeft + 'px';
            e.target.parentElement.appendChild(tooltip);
        });
        
        element.addEventListener('mouseleave', (e) => {
            const tooltip = e.target.parentElement.querySelector('.absolute');
            if (tooltip) tooltip.remove();
        });
    });
}

// Syntax highlighting for code (basic)
function highlightCode(code) {
    // Basic Python syntax highlighting
    const keywords = ['def', 'return', 'if', 'else', 'elif', 'for', 'while', 'in', 'and', 'or', 'not', 'pass', 'break', 'continue', 'class', 'import', 'from', 'as', 'try', 'except', 'finally', 'with', 'lambda', 'yield'];
    
    let highlighted = code;
    keywords.forEach(keyword => {
        const regex = new RegExp(`\\b${keyword}\\b`, 'g');
        highlighted = highlighted.replace(regex, `<span class="text-purple-400">${keyword}</span>`);
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

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('CodeClash initialized');
    initTooltips();
});

// Export functions for use in other scripts
window.CodeClash = {
    showNotification,
    formatTime,
    validateCode,
    copyToClipboard,
    highlightCode
};

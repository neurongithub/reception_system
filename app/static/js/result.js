// ==================== SIDEBAR TOGGLE ====================

const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
const sidebarClose = document.getElementById('sidebarClose');

// Open sidebar
if (menuBtn) {
    menuBtn.addEventListener('click', function() {
        sidebar.classList.add('active');
        document.body.classList.add('sidebar-open');
    });
}

// Close sidebar
if (sidebarClose) {
    sidebarClose.addEventListener('click', function() {
        sidebar.classList.remove('active');
        document.body.classList.remove('sidebar-open');
    });
}

// Close sidebar when clicking on overlay
document.addEventListener('click', function(event) {
    if (sidebar.classList.contains('active') && 
        !sidebar.contains(event.target) && 
        !menuBtn.contains(event.target)) {
        sidebar.classList.remove('active');
        document.body.classList.remove('sidebar-open');
    }
});

// ==================== REFRESH BUTTON ====================

const refreshBtn = document.getElementById('refreshBtn');

if (refreshBtn) {
    refreshBtn.addEventListener('click', function() {
        refreshBtn.classList.add('spinning');
        setTimeout(() => {
            location.reload();
        }, 800);
    });
}

// ==================== STATISTICS DATA ====================

// یمی‌توانید این داده‌ها را از backend دریافت کنید
document.addEventListener('DOMContentLoaded', function() {
    // نمایش داده‌های نمونه
    document.getElementById('total-accepted').textContent = '250';
    document.getElementById('battalion-count').textContent = '3';
    document.getElementById('company-count').textContent = '15';
    document.getElementById('total-capacity').textContent = '500';
    document.getElementById('results-count').textContent = '250';
});

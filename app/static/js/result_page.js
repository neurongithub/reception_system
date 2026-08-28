/**
 * ===================================================
 * صفحه نتایج - نتایج لحظه ای پذیرش فراگیران
 * ===================================================
 */

// ==================== SIDEBAR TOGGLE ====================

document.addEventListener('DOMContentLoaded', function() {

    const menuBtn = document.getElementById('menuBtn');
    const sidebar = document.getElementById('sidebar');
    const sidebarClose = document.getElementById('sidebarClose');

    // باز کردن sidebar با کلیک بر menu button
    if (menuBtn) {
        menuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            sidebar.classList.add('active');
            document.body.classList.add('sidebar-open');
        });
    }

    // بسته کردن sidebar با کلیک بر دکمه بستن
    if (sidebarClose) {
        sidebarClose.addEventListener('click', function() {
            sidebar.classList.remove('active');
            document.body.classList.remove('sidebar-open');
        });
    }

    // بسته کردن sidebar با کلیک روی overlay
    document.addEventListener('click', function(event) {
        if (sidebar && sidebar.classList.contains('active')) {
            if (!sidebar.contains(event.target) && !menuBtn.contains(event.target)) {
                sidebar.classList.remove('active');
                document.body.classList.remove('sidebar-open');
            }
        }
    });

    // بسته کردن sidebar با فشار کلید ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && sidebar && sidebar.classList.contains('active')) {
            sidebar.classList.remove('active');
            document.body.classList.remove('sidebar-open');
        }
    });

    // کلیک بر لینک‌های sidebar برای بستن آن
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // حذف کلاس active از تمام لینک‌ها
            navLinks.forEach(l => l.classList.remove('active'));
            // اضافه کردن کلاس active به لینک فعلی
            this.classList.add('active');

            // بستن sidebar
            sidebar.classList.remove('active');
            document.body.classList.remove('sidebar-open');
        });
    });

});

// ==================== LOGOUT BUTTON ====================

document.addEventListener('DOMContentLoaded', function() {

    const logoutBtn = document.getElementById('logoutBtn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            // تایید خروج
            if (confirm('آیا می‌خواهید از سامانه خارج شوید؟')) {
                // می‌توانید به صفحه لاگین منتقل شوید
                // window.location.href = '/logout';
                console.log('خروج از سامانه...');
            }
        });
    }

});

// ==================== REFRESH BUTTON ====================

document.addEventListener('DOMContentLoaded', function() {

    const refreshBtn = document.getElementById('refreshBtn');

    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            // اضافه کردن کلاس spin برای انیمیشن
            refreshBtn.classList.add('spinning');

            // بعد از 800ms صفحه را تازه کنید
            setTimeout(() => {
                location.reload();
            }, 800);
        });
    }

});

// ==================== STATISTICS DATA ====================

document.addEventListener('DOMContentLoaded', function() {

    /**
     * نمایش داده‌های نمونه در statistics cards
     * می‌توانید این داده‌ها را از backend دریافت کنید
     */

    const statsData = {
        totalAccepted: 250,
        battalionCount: 3,
        companyCount: 15,
        totalCapacity: 500,
        resultsCount: 250,
        acceptanceStatus: 'پذیرش‌شده'
    };

    // بروزرسانی Statistics Cards
    const totalAcceptedElement = document.getElementById('total-accepted');
    if (totalAcceptedElement) {
        totalAcceptedElement.textContent = statsData.totalAccepted;
    }

    const battalionCountElement = document.getElementById('battalion-count');
    if (battalionCountElement) {
        battalionCountElement.textContent = statsData.battalionCount;
    }

    const companyCountElement = document.getElementById('company-count');
    if (companyCountElement) {
        companyCountElement.textContent = statsData.companyCount;
    }

    const totalCapacityElement = document.getElementById('total-capacity');
    if (totalCapacityElement) {
        totalCapacityElement.textContent = statsData.totalCapacity;
    }

    const acceptanceStatusElement = document.getElementById('acceptance-status');
    if (acceptanceStatusElement) {
        acceptanceStatusElement.textContent = statsData.acceptanceStatus;
    }

    const resultsCountElement = document.getElementById('results-count');
    if (resultsCountElement) {
        resultsCountElement.textContent = statsData.resultsCount;
    }

});

// ==================== FILTERS FORM HANDLER ====================

document.addEventListener('DOMContentLoaded', function() {

    const filtersForm = document.querySelector('.filters-form');

    if (filtersForm) {
        // هنگام ارسال فرم فیلترها
        filtersForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // دریافت مقادیر فیلترها
            const filters = {
                battalion: document.getElementById('battalion_filter').value,
                company: document.getElementById('company_filter').value,
                religion: document.getElementById('religion_filter').value,
                province: document.getElementById('province_filter').value,
                healthStatus: document.getElementById('health_status_filter').value
            };

            console.log('فیلترهای انتخاب شده:', filters);

            // ارسال درخواست به backend (برای بعد)
            // fetchResults(filters);
        });

        // ری‌ست فیلترها
        const resetBtn = filtersForm.querySelector('button[type="reset"]');
        if (resetBtn) {
            resetBtn.addEventListener('click', function() {
                console.log('فیلترها پاک شدند');
            });
        }
    }

});

// ==================== TABLE HANDLER ====================

document.addEventListener('DOMContentLoaded', function() {

    const resultsTable = document.querySelector('.results-table table');

    if (resultsTable) {
        /**
         * می‌توانید اینجا داده‌های جدول را از backend دریافت کنید
         * و اینجا نمایش دهید
         */

        // مثال: اضافه کردن رو به جدول
        function addRowToTable(data) {
            const tbody = resultsTable.querySelector('tbody');
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${data.nationalCode}</td>
                <td>${data.firstName}</td>
                <td>${data.lastName}</td>
                <td>${data.battalion}</td>
                <td>${data.company}</td>
                <td>${data.status}</td>
            `;

            tbody.appendChild(row);
        }

        // می‌توانید از این تابع استفاده کنید برای اضافه کردن داده‌ها
        // addRowToTable({ nationalCode: '1234567890', firstName: 'علی', lastName: 'احمدی', battalion: 1, company: 1, status: 'پذیرش‌شده' });
    }

});

// ==================== UTILITY FUNCTIONS ====================

/**
 * تابع برای فچ کردن نتایج از سرور
 * @param {Object} filters - فیلترهای جستجو
 */
function fetchResults(filters) {
    // این تابع برای بعد است
    console.log('دریافت نتایج با فیلترهای:', filters);
}

/**
 * تابع برای به‌روزرسانی شمارنده نتایج
 * @param {Number} count - تعداد نتایج
 */
function updateResultsCount(count) {
    const countElement = document.getElementById('results-count');
    if (countElement) {
        countElement.textContent = count;
    }
}

/**
 * تابع برای نمایش پیام خطا
 * @param {String} message - متن پیام
 */
function showError(message) {
    console.error('خطا:', message);
    // می‌توانید یک modal یا alert نمایش دهید
}

/**
 * تابع برای نمایش پیام موفقیت
 * @param {String} message - متن پیام
 */
function showSuccess(message) {
    console.log('موفق:', message);
    // می‌توانید یک toast notification نمایش دهید
}

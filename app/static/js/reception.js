

function updateAllocationBox() {
    const battalionSelect = document.getElementById('battalion_option');
    const companySelect = document.getElementById('company_option');
    const battalionValue = document.getElementById('allocation-battalion');
    const companyValue = document.getElementById('allocation-company');
    const allocationValue = document.getElementById('allocation-value');
    const courseCodeInput = document.getElementById('current-course-code');

    if (!battalionSelect || !companySelect || !allocationValue) {
        return;
    }

    const battalion = battalionSelect.value;
    const company = companySelect.value;
    const courseCode = courseCodeInput ? courseCodeInput.value : '';

    const battalionLabel = battalionSelect.selectedOptions[0]?.textContent?.trim() || 'نامشخص';
    const companyLabel = companySelect.selectedOptions[0]?.textContent?.trim() || 'نامشخص';

    if (battalionValue) {
        battalionValue.textContent = battalion ? battalionLabel : '-';
    }

    if (companyValue) {
        companyValue.textContent = company ? companyLabel : '-';
    }

    if (!courseCode || !battalion || !company) {
        allocationValue.textContent = 'تخصیصی ثبت نشده است';
        return;
    }

    const url = new URL('/dashboard/reception/allocation/', window.location.origin);
    url.searchParams.set('course_code', courseCode);
    url.searchParams.set('battalion', battalion);
    url.searchParams.set('company', company);

    fetch(url)
        .then(response => response.json())
        .then(data => {
            allocationValue.textContent = data.allocation || 'تخصیصی ثبت نشده است';
        })
        .catch(() => {
            allocationValue.textContent = 'تخصیصی ثبت نشده است';
        });
}


document.addEventListener('DOMContentLoaded', function () {
    const battalionSelect = document.getElementById('battalion_option');
    const companySelect = document.getElementById('company_option');
    const birthDateInput = document.getElementById('birth_date');

    if (battalionSelect) {
        battalionSelect.addEventListener('change', updateAllocationBox);
    }

    if (companySelect) {
        companySelect.addEventListener('change', updateAllocationBox);
    }

    if (birthDateInput && window.jQuery && $.fn.persianDatepicker) {
        $(birthDateInput).persianDatepicker({
            format: 'YYYY/MM/DD',
            initialValue: false,
            autoClose: true,
            responsive: true,
            inline: false,
            position: 'auto'
        });
    }

    updateAllocationBox();
});


//keyboard short cuts for reception buttons 
document.addEventListener("keydown", function (event) {

    switch (event.key) {

        case "F1":
            event.preventDefault();
            document.getElementById("btn-help").click();
            break;

        case "F2":
            event.preventDefault();
            document.getElementById("btn-first").click();
            break;

        case "F3":
            event.preventDefault();
            document.getElementById("btn-list").click();
            break;

        case "F4":
            event.preventDefault();
            document.getElementById("btn-manual").click();
            break;

        // case "F5":
        //     event.preventDefault();
        //     document.getElementById("btn-clothes").click();
        //     break;

        case "F6":
            event.preventDefault();
            document.getElementById("btn-clear").click();
            break;

        case "Escape":
            event.preventDefault();
            history.back();
            break;
    }

});


// manual reception modal 
const manualModal = document.getElementById('manual-reception-modal'); // modal element
const openManualModalButton = document.getElementById('btn-manual'); // open modal buttonn 
const closeManualModalButton = document.getElementById('close-manual-btn'); // close modal button
const closeManualHeaderButton = document.getElementById('close-manual-header-btn'); // close modal button in header
const manualModalForm = document.querySelector('#manual-reception-form')

function closeManualModal() {
    if (manualModal) {
        manualModal.style.display = 'none';
        manualModalForm.reset ()

    }
}

if (openManualModalButton && manualModal) {
    openManualModalButton.addEventListener('click', function () {
        manualModal.style.display = 'flex';
    });
}

if (closeManualModalButton) {
    closeManualModalButton.addEventListener('click', closeManualModal);
}

if (closeManualHeaderButton) {
    closeManualHeaderButton.addEventListener('click', closeManualModal);
}

window.addEventListener("click", (event) => {
    if (manualModal && event.target === manualModal) {
        manualModal.style.display = "none";
    }
});


window.addEventListener('DOMContentLoaded', event => {
    // Activate feather
    feather.replace();

    // Enable tooltips globally
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable popovers globally
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sidenav-toggled'));
        });
    }

    // Close side navigation when width < LG
    const sidenavContent = document.body.querySelector('#layoutSidenav_content');
    if (sidenavContent) {
        sidenavContent.addEventListener('click', event => {
            const BOOTSTRAP_LG_WIDTH = 992;
            if (window.innerWidth >= 992) {
                return;
            }
            if (document.body.classList.contains("sidenav-toggled")) {
                document.body.classList.toggle("sidenav-toggled");
            }
        });
    }

    window.addEventListener('load', (event) => {
        let datatableSelector = document.querySelector('.datatable-selector')
        let datatableInput = document.querySelector('.datatable-input')
        let datatableInfo = document.querySelector('.datatable-info')
        if (datatableSelector) {
            datatableSelector.nextSibling.data = entriesPerPageText
        }
        if (datatableInput) {
            datatableInput.placeholder = `${searchText}...`
        }
        if (datatableInfo) {
            let datatableInfoNumbers = datatableInfo.innerText.match(/\d+/g)
            datatableInfo.innerText = `${showingText} ${datatableInfoNumbers[0]}-${datatableInfoNumbers[1]} ${entriesText}. ${totalText} ${datatableInfoNumbers[2]}`
        }

    });


    document.querySelectorAll('input').forEach(function (element) {
        if (!element.checkValidity()) {
            element.setCustomValidity(element.getAttribute('title'))
        } else {
            element.setCustomValidity("");
        }
        element.addEventListener('input', function (event) {
            if (!event.currentTarget.checkValidity()) {
                event.currentTarget.setCustomValidity(event.currentTarget.getAttribute('title'))
            }
            event.currentTarget.setCustomValidity("");
        })
    })

    document.querySelectorAll('select').forEach(function (element) {
        if (!element.checkValidity()) {
            element.setCustomValidity(element.getAttribute('title'))
        } else {
            element.setCustomValidity("");
        }
        element.addEventListener('change', function (event) {
            if (!event.currentTarget.checkValidity()) {
                event.currentTarget.setCustomValidity(event.currentTarget.getAttribute('title'))
            }
            event.currentTarget.setCustomValidity("");
        })
    })

    document.querySelectorAll('textarea').forEach(function (element) {
        if (!element.checkValidity()) {
            element.setCustomValidity(element.getAttribute('title'))
        } else {
            element.setCustomValidity("");
        }
        element.addEventListener('input', function (event) {
            if (!event.currentTarget.checkValidity()) {
                event.currentTarget.setCustomValidity(event.currentTarget.getAttribute('title'))
            }
            event.currentTarget.setCustomValidity("");
        })
    })
});

const swalCustom = Swal.mixin({
    customClass: {
        confirmButton: 'btn btn-success',
        cancelButton: 'btn btn-danger'
    },
    buttonsStyling: false
})

function successAlert(message) {
    swalCustom.fire({
        icon: 'success',
        text: message,
        confirmButtonText: okText
    })
}

function errorAlert(message) {
    swalCustom.fire({
        icon: 'error',
        text: message,
        showCancelButton: true,
        showConfirmButton: false,
        cancelButtonText: okText
    })
}

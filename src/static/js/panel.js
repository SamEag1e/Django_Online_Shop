document.addEventListener('DOMContentLoaded', function () {
    initializeNavigation();
    handleInternalNavClicks();
    handlePopstate();
});

function initializeNavigation() {
    const mobileNav = document.getElementById('mobile_user_panel');
    const desktopNav = document.getElementById('desktop_user_panel');

    if (mobileNav) {
        const mobileNavItems = mobileNav.querySelectorAll('.nav-item');
        handleNavClick(mobileNavItems);
    }

    if (desktopNav) {
        const desktopNavItems = desktopNav.querySelectorAll('.nav-item');
        handleNavClick(desktopNavItems);
    }

    const urlParams = new URLSearchParams(window.location.search);
    const sectionFromUrl = urlParams.get('section');
    setInitialActiveState(sectionFromUrl);
}

function handleNavClick(navItems) {
    navItems.forEach(function (item) {
        if (item.id === 'logout') return;

        item.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopPropagation();

            const sectionId = item.id;
            updateUrlWithSection(sectionId);
            loadSectionContent(sectionId);
            updateActiveState(sectionId);
        });
    });
}

function updateUrlWithSection(sectionId) {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('section', sectionId);
    window.history.pushState({ section: sectionId }, '', currentUrl);
}

function loadSectionContent(sectionId) {
    const sectionUrl = document.getElementById(sectionId).querySelector('a').href;

    showLoader();

    fetch(sectionUrl)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newContent = doc.querySelector('#panel_content').innerHTML;

            document.getElementById('panel_content').innerHTML = newContent;
            handleInternalNavClicks();
            hideLoader();
        })
        .catch(error => {
            console.error('Error fetching the section content:', error);
            hideLoader();
        });
}

function updateActiveState(section) {
    const allNavItems = document.querySelectorAll('.nav-item');
    allNavItems.forEach(function (nav) {
        nav.classList.remove('active');
    });

    const clickedItems = document.querySelectorAll(`#${section}`);
    clickedItems.forEach(function (nav) {
        nav.classList.add('active');
    });
}

function setInitialActiveState(section) {
    if (!section || document.querySelectorAll(`#${section}`).length === 0) {
        section = 'profile';
    }

    loadSectionContent(section);
    updateActiveState(section);
}

function handleInternalNavClicks() {
    const internalNavButtons = document.querySelectorAll('.internal-nav-btn');
    internalNavButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const sectionUrl = button.href;
            showLoader();

            fetch(sectionUrl)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newContent = doc.querySelector('#panel_content').innerHTML;

                    document.getElementById('panel_content').innerHTML = newContent;
                    handleInternalNavClicks();
                    hideLoader();
                })
                .catch(error => {
                    console.error('Error fetching the internal section content:', error);
                    hideLoader();
                });
        });
    });

    handleFormSubmissions();
}

function handleFormSubmissions() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
        if (!form.hasAttribute('data-no-ajax')) {
            form.addEventListener('submit', function (event) {
                event.preventDefault();
                const formData = new FormData(form);
                const actionUrl = form.action;

                showLoader();

                fetch(actionUrl, {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.text())
                    .then(html => {
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        const newContent = doc.querySelector('#panel_content').innerHTML;

                        document.getElementById('panel_content').innerHTML = newContent;
                        handleInternalNavClicks();
                        hideLoader();
                    })
                    .catch(error => {
                        console.error('Error submitting form via AJAX:', error);
                        hideLoader();
                    });
            });
        }
    });
}

function handlePopstate() {
    window.addEventListener('popstate', function (event) {
        const sectionFromUrl = new URLSearchParams(window.location.search).get('section');
        setInitialActiveState(sectionFromUrl);
    });
}

function showLoader() {
    document.getElementById('panel-content-loader').classList.remove('d-none');
}

function hideLoader() {
    document.getElementById('panel-content-loader').classList.add('d-none');
}

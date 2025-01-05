document.addEventListener('DOMContentLoaded', function() {
    function handleNavClick(navItems) {
        navItems.forEach(function(item) {
            // Skip the logout item
            if (item.id === 'logout') {
                return;
            }

            item.addEventListener('click', function(event) {
                event.preventDefault();
                event.stopPropagation();

                // Update the URL with the section parameter
                var sectionId = item.id;
                var currentUrl = new URL(window.location.href);
                currentUrl.searchParams.set('section', sectionId);
                window.history.pushState({ section: sectionId }, '', currentUrl);

                // Load the section content
                loadSectionContent(sectionId);

                // Update the active state
                updateActiveState(sectionId);
            });
        });
    }

    function loadSectionContent(sectionId) {
        var sectionUrl = document.getElementById(sectionId).querySelector('a').href;

        showLoader();

        fetch(sectionUrl)
            .then(response => response.text())
            .then(html => {
                var parser = new DOMParser();
                var doc = parser.parseFromString(html, 'text/html');
                var newContent = doc.querySelector('#panel_content').innerHTML;

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
        var allNavItems = document.querySelectorAll('.nav-item');
        allNavItems.forEach(function(nav) {
            nav.classList.remove('active');
        });

        var clickedItems = document.querySelectorAll(`#${section}`);
        clickedItems.forEach(function(nav) {
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
        var internalNavButtons = document.querySelectorAll('.internal-nav-btn');
        internalNavButtons.forEach(function(button) {
            button.addEventListener('click', function(event) {
                event.preventDefault();

                var sectionUrl = button.href;

                showLoader();

                fetch(sectionUrl)
                    .then(response => response.text())
                    .then(html => {
                        var parser = new DOMParser();
                        var doc = parser.parseFromString(html, 'text/html');
                        var newContent = doc.querySelector('#panel_content').innerHTML;

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

        var forms = document.querySelectorAll('form');
        forms.forEach(function(form) {
            if (!form.hasAttribute('data-no-ajax')) {
                form.addEventListener('submit', function(event) {
                    event.preventDefault();
                    var formData = new FormData(form);
                    var actionUrl = form.action;

                    showLoader();

                    fetch(actionUrl, {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.text())
                    .then(html => {
                        var parser = new DOMParser();
                        var doc = parser.parseFromString(html, 'text/html');
                        var newContent = doc.querySelector('#panel_content').innerHTML;

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

    var mobileNav = document.getElementById('mobile_user_panel');
    if (mobileNav) {
        var mobileNavItems = mobileNav.querySelectorAll('.nav-item');
        handleNavClick(mobileNavItems);
    }

    var desktopNav = document.getElementById('desktop_user_panel');
    if (desktopNav) {
        var desktopNavItems = desktopNav.querySelectorAll('.nav-item');
        handleNavClick(desktopNavItems);
    }

    var urlParams = new URLSearchParams(window.location.search);
    var sectionFromUrl = urlParams.get('section');
    setInitialActiveState(sectionFromUrl);

    window.addEventListener('popstate', function(event) {
        var sectionFromUrl = new URLSearchParams(window.location.search).get('section');
        setInitialActiveState(sectionFromUrl);
    });

    handleInternalNavClicks();

    function showLoader() {
        document.getElementById('panel-content-loader').classList.remove('d-none');
    }

    function hideLoader() {
        document.getElementById('panel-content-loader').classList.add('d-none');
    }
});

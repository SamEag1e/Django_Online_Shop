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
        fetch(sectionUrl)
            .then(response => response.text())
            .then(html => {
                var parser = new DOMParser();
                var doc = parser.parseFromString(html, 'text/html');
                var newContent = doc.querySelector('#panel_content').innerHTML;

                document.getElementById('panel_content').innerHTML = newContent;
            })
            .catch(error => {
                console.error('Error fetching the section content:', error);
            });
    }

    function updateActiveState(section) {
        // Remove 'active' class from all nav items
        var allNavItems = document.querySelectorAll('.nav-item');
        allNavItems.forEach(function(nav) {
            nav.classList.remove('active');
        });

        // Add 'active' class to the clicked nav item
        var clickedItems = document.querySelectorAll(`#${section}`);
        clickedItems.forEach(function(nav) {
            nav.classList.add('active');
        });
    }

    // Set initial active state for both navs
    function setInitialActiveState(section) {
        // Default section if not provided or invalid
        if (!section || document.querySelectorAll(`#${section}`).length === 0) {
            section = 'profile';
        }

        // Load the initial section content
        loadSectionContent(section);

        // Add 'active' class to initial active items
        updateActiveState(section);
    }

    // Mobile nav
    var mobileNav = document.getElementById('mobile_user_panel');
    if (mobileNav) {
        var mobileNavItems = mobileNav.querySelectorAll('.nav-item');
        handleNavClick(mobileNavItems);
    }

    // Desktop nav
    var desktopNav = document.getElementById('desktop_user_panel');
    if (desktopNav) {
        var desktopNavItems = desktopNav.querySelectorAll('.nav-item');
        handleNavClick(desktopNavItems);
    }

    // Get the section variable from URL
    var urlParams = new URLSearchParams(window.location.search);
    var sectionFromUrl = urlParams.get('section');
    setInitialActiveState(sectionFromUrl);

    // Handle browser back/forward button events
    window.addEventListener('popstate', function(event) {
        var sectionFromUrl = new URLSearchParams(window.location.search).get('section');
        setInitialActiveState(sectionFromUrl);
    });
});

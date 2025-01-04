document.addEventListener('DOMContentLoaded', function() {
    function handleNavClick(navItems) {
        navItems.forEach(function(item) {
            if (item.id === 'logout') {
                return;
            }

            item.addEventListener('click', function(event) {
                event.preventDefault();
                event.stopPropagation();

                navItems.forEach(function(nav) {
                    nav.classList.remove('active');
                });

                item.classList.add('active');
            });
        });
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
});

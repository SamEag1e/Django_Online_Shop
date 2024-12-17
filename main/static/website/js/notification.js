document.addEventListener('DOMContentLoaded', function () {
    const notifications = document.querySelectorAll('.notification');

    notifications.forEach(notification => {
        setTimeout(() => {
            notification.classList.add('fade');

            setTimeout(() => notification.remove(), 500);
        }, 4000);
    });
});
// Run Countdown Timer Script
$(document).ready(function () {
    countdown('countdownB', 0, 0, 0, 300);
});

// OTP Input Callback
const continueButton = document.querySelector("#submit");
continueButton.addEventListener("click", (e) => {
    updateValue(inputs);
});
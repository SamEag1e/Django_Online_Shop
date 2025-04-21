$(document).ready(function () {
    let $slider = $(".catRange");
    let $minPrice = $("input[name='min_price']");
    let $maxPrice = $("input[name='max_price']");
    let $form = $("#collapsePrice form");

    // Initialize slider with values
    let minValue = parseInt($minPrice.val()) || 100000;
    let maxValue = parseInt($maxPrice.val()) || 30000000;

    $slider.slider({
        id: "slider5b",
        min: 100000,
        max: 30000000,
        range: true,
        step: 10000,
        value: [minValue, maxValue],
        rtl: true,
        formatter: function (val) {
            return val[0] + " تومان " + "  تا   " + val[1] + " تومان ";
        }
    });

    // Update inputs when slider moves
    $slider.on("slide slideStop", function (event) {
        let values = event.value;
        $minPrice.val(values[0]);
        $maxPrice.val(values[1]);
    });

    // Sync slider with input changes
    $minPrice.on("input", function () {
        let newMin = parseInt($minPrice.val()) || 100000;
        let currentMax = $maxPrice.val() || 30000000;
        $slider.slider("setValue", [newMin, currentMax]);
    });

    $maxPrice.on("input", function () {
        let currentMin = $minPrice.val() || 100000;
        let newMax = parseInt($maxPrice.val()) || 30000000;
        $slider.slider("setValue", [currentMin, newMax]);
    });

    // Prevent form submission if both are empty
    $form.on("submit", function (e) {
        let min = $minPrice.val().trim();
        let max = $maxPrice.val().trim();

        if (!min && !max) {
            e.preventDefault();
            return;
        }

        // Remove empty fields from GET request
        if (!min) $minPrice.prop("disabled", true);
        if (!max) $maxPrice.prop("disabled", true);

        setTimeout(() => {
            $minPrice.prop("disabled", false);
            $maxPrice.prop("disabled", false);
        }, 1000);
    });
});

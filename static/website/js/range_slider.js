$(document).ready(function () {
    ////slider range
    $(".catRange").slider({
        id: "slider5b",
        min: 100000,
        max: 30000000,
        range: true,
        step: 10000,
        value: [100000, 30000000],
        rtl: 'false',
        formatter: function formatter(val) {
            if (Array.isArray(val)) {
                return val[0] + " تومان " + "  تا   " + val[1] + " تومان ";
            } else {
                return val;
            }
        },
    });
});
/* Copyright (c) 2014, Siemens Coporate Technology and Arizona Geological Survey */
$(document).ready(function () {
    var ngds = ngds || (ngds = { });

    ngds.ratings = {};


    ngds.ratings.rating_helper_tooltip = function (rating) {
        console.log(rating);
    };

    ngds.ratings.fetch_text = function (rating) {
        return {
            "1": "Very Poor",
            "2": "Poor",
            "3": "Fair",
            "4": "Good",
            "5": "Very Good"
        }[rating];
    };

    $("#search-review a").on("mouseover", function (ev) {
        var rating_value = $(this).attr("data-rating-value");
        if (typeof rating_value === "undefined") {
            return;
        }

        var rval = Number(rating_value);

        if (isNaN(rval)) {
            return;
        }

        $(".ratings-helper").empty();
        var para = $("<p/>", {"text": ngds.ratings.fetch_text(rating_value)});
        $(".ratings-helper").append(para);
    });

    $(".ratings").mouseleave(function () {
        $(".ratings-helper").empty();
    });
});

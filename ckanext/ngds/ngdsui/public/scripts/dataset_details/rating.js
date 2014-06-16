/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
$(document).ready(function () {
    var ngds = ngds || (ngds = { });

    ngds.ratings = {};


    ngds.ratings.rating_helper_tooltip = function (rating) {
        console.log(rating);
    };

    ngds.ratings.fetch_text = function (rating) {
        return {
            "1": "Errors or inappropriate content",
            "2": "Content not what I expected",
            "3": "Doesn't include information I need",
            "4": "Good enough to download",
            "5": "Just what I needed"
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

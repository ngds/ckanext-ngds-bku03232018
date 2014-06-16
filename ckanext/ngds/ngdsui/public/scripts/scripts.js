/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
var ngds = ngds || { };

(function () {
    $(document).ready(function () {


        $("#search-review img").on("mouseover", function () {

        });


        /* This is for user management - Role changes (manage_users.html) - Start*/
        var prev_val;

        $('.dropdown').focus(function () {
            prev_val = $(this).val();
        }).change(function () {
                $(this).blur() // Firefox fix as suggested by AgDude
                var success = confirm('Are you sure you want to change the role?');
                if (success) {
                    var formid = "#" + $(this)[0].id.substr(5);
                    $(formid).submit();
                    // Other changed code would be here...
                }
                else {
                    $(this).val(prev_val);
                    //alert('unchanged');
                    return false;
                }
            });
        /* This is for user management - Role changes (manage_users.html) - End*/

        $('#read-only-form :input').attr('readonly', 'readonly');
        $('#read-only-form :checkbox').attr('disabled', 'disabled');

        var $unique = $('input.unique');
        $unique.click(function () {
            $unique.filter(':checked').not(this).removeAttr('checked');
        });


        $("#manage-nodes-table tr:odd").css("background-color", "#fff6f6");

        $(".not-implemented").click(function (event) { // Handle portions of the UI that haven't been implemented yet, display a div that says 'Not implemented Yet'.
            ngds.not_implemented_popup_active = true;
            $("#not-implemented-popup").show();
            return false;
        });

        $(document).click(function () { // Handle clicks on the document level.

            if (ngds.not_implemented_popup_active === true) { // If The not implemented yet popup is active, hide it.
                ngds.not_implemented_popup_active = false;
                $("#not-implemented-popup").hide();
            }

            if (isLoginPopupVisible()) { // If the login popup is active, hide it.
                $(".login-popup").hide();
            }

        });

        $(document).keyup(function (e) { // On ESC hide the Not Implemented Yet popup, if it's visible.
            if (e.keyCode === 27 && ngds.not_implemented_popup_active) {
                $("#not-implemented-popup").hide();
            }
        });

        (function () { // Handle login popup events.

            $(".login-in").click(function () { // When clicked, toggle between visible and hidden.
                if (isLoginPopupVisible()) {
                    $(".login-popup").hide();
                }
                else {
                    $(".login-popup").show();
                }
                return false;
            });

            $(document).keyup(function (e) { // On ESC toggle between visible and hidden.
                if (e.keyCode === 27 && isLoginPopupVisible()) {
                    $(".login-popup").hide();
                }
            });

            $("#login-popup").click(function () { // Prevent the click event propagating upwards to document and resulting in the login popup being hidden
                // when a click occurs inside the div.
                return false;
            });

        })();


        /*		var accordions = $(".accordion");

         for(var i=0;i<accordions.length;i++) {
         $(accordions[i]).accordion({
         autoHeight:false,
         heightStyle:"content"
         });
         }*/

        function isLoginPopupVisible() {
            return ($(".login-popup").css('display') !== 'none');
        }


        $('#field-lang-select').change(function () {
            $("#change-language").click();
        });

    });

})();

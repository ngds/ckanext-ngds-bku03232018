$(document).ready(function () {
    /*$("[data-rs]").each(function () {

    });*/

    $("button[data-add-rs-maintainer]").click(function (ev) {
        ngds.responsible_parties.add_new(this.title, "#field-maintainer");
    });

    $("button[data-add-rs-author]").click(function(ev){
       ngds.responsible_parties.add_new(this.title, "#field-authors")
    });

    ngds.responsible_parties = {
        'add_new': function (popup_title, field_name) {
            console.log("responsible_parties.add_new( ," + field_name + ")");
            var template = [
                '<div class="modal" style="top: 10%">',
                    '<div class="modal-header">',
                        '<button type="button" class="close" data-dismiss="modal">×</button>',
                        '<h3>',  popup_title ,'</h3>',
                    '</div>',
                    '<div class="modal-body">',
                        '<div class="add-responsible">',
                            '<label id="rs_name_lbl" for="rs_name">Name<sup class="mandatory">*</sup></label><input type="text" id="rs_name" /></div>',
                        '<div class="add-responsible" style="margin-top: 0">',
                            '<div class="add-err-label"/><div id="rs_name_err" class="missing-field-hide">Missing Field</div></div>',

                        '<div class="add-responsible">',
                            '<label id="rs_email_lbl" for="rs_email">Email<sup class="mandatory">*</sup></label><input type="email" id="rs_email" /></div>',
                        '<div class="add-responsible" style="margin-top: 0">',
                            '<div class="add-err-label"/><div id="rs_email_err" class="missing-field-hide">Missing Field</div><div id="rs_email_dup" class="missing-field-hide">Email Already Exists</div></div>',

                        '<div class="add-responsible">',
                            '<label for="rs_org">Organization</label><input type="text" id="rs_org" /></div>',
                        '<div class="add-responsible">',
                            '<label for="rs_phone">Phone</label><input type="text" id="rs_phone" /></div>',
                        '<div class="add-responsible">',
                            '<label for="rs_street">Street Address</label><input type="text" id="rs_street" /></div>',
                        '<div class="add-responsible">',
                            '<label for="rs_city">City</label><input type="text" id="rs_city" /></div>',
                        '<div class="add-responsible">',
                            '<label for="rs_state">State</label><input type="text" id="rs_state" /></div>',
                        '<div class="add-responsible">',
                            '<label for="rs_zip">Zipcode</label><input type="text" id="rs_zip" /></div>',
                        '<div class="add-responsible">',
                            '<label for="rs_country">Country</label><input type="text" id="rs_country" /></div>',
                    '</div>',
                    '<div class="modal-footer">',
                        '<button class="btn btn-cancel">Cancel</button>',
                        '<button class="btn btn-primary">Confirm</button>',
                    '</div>',
                '</div>'
            ].join('');

            var element = $(template);
            var modal = element.modal({'show': true});

            element.on('click', '.btn-primary', function (ev) {
                    ev.preventDefault();

                var missing_required = false;

                $(".modal #rs_email_dup").removeClass("missing-field-show").addClass("missing-field-hide");
                $(".modal #rs_email").removeClass("required");
                $(".modal #rs_email_lbl").removeClass("required");

                // Verify Required Fields
                if ($(".modal #rs_name").val()=="") {
                    $(".modal #rs_name").addClass("required");
                    $(".modal #rs_name_lbl").addClass("required");
                    $(".modal #rs_name_err").addClass("missing-field-show").removeClass("missing-field-hide");
                    missing_required = true;
                }
                else {
                    $(".modal #rs_name").removeClass("required");
                    $(".modal #rs_name_lbl").removeClass("required");
                    $(".modal #rs_name_err").removeClass("missing-field-show").addClass("missing-field-hide");
                }

                if ($(".modal #rs_email").val()=="") {
                    $(".modal #rs_email").addClass("required");
                    $(".modal #rs_email_lbl").addClass("required");
                    $(".modal #rs_email_err").addClass("missing-field-show").removeClass("missing-field-hide");
                    $(".modal #rs_email_dup").removeClass("required");
                    missing_required = true;
                }
                else {
                    $(".modal #rs_email").removeClass("required");
                    $(".modal #rs_email_lbl").removeClass("required");
                    $(".modal #rs_email_err").removeClass("missing-field-show").addClass("missing-field-hide");
                }

                // Add Data to responsible_party table
                if (!missing_required){
                    var json_data = JSON.stringify({
                            "model": "ResponsibleParty",
                            "process": "create",
                            "data": {
                                "name": $(".modal #rs_name").val(),
                                "email": $(".modal #rs_email").val() ,
                                "organization": $(".modal #rs_org").val(),
                                "phone": $(".modal #rs_phone").val(),
                                "street": $(".modal #rs_street").val(),
                                "city": $(".modal #rs_city").val(),
                                "state": $(".modal #rs_state").val(),
                                "zip": $(".modal #rs_zip").val(),
                                "country": $(".modal #rs_country").val()

                            }
                        });

                    //alert(json_data);

                    $.ajax({
                        'url': '/api/action/additional_metadata',
                        'type': 'POST',
                        'data': json_data,
                        'success': function (response) {
                            console.log(response);
                            // TODO: Add newly created name to input box
                            // TODO: // $(field_name).val($(field_name).val() + "," + $(".modal #rs_name").val());
                            modal.modal('hide');
                            modal.remove();
                        },
                        'error': function (request, status, err) {
                            // need to detect cause of error
                            // if "duplicate" then do the following

                            $(".modal #rs_email").addClass("required");
                            $(".modal #rs_email_lbl").addClass("required");
                            $(".modal #rs_email_dup").addClass("missing-field-show").removeClass("missing-field-hide");
                        }
                    });

                    }
                }
            );

            element.on('click', '.btn-cancel', function (ev) {
                    ev.preventDefault();
                    modal.modal('hide');
                    modal.remove();
            });

        }
    };
});
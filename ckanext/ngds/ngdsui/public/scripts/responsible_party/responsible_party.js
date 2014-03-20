/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
$(document).ready(function () {


    //  Since the "opts" property is not yet defined when then $(document).ready() function runs, need to set timer
    //  interval to watch for existence of "opts" before overriding initSelection() (a member of opts).  This applies
    //  to both #field-authors and #field-maintainer elements

    var timeoutAuthors = setInterval(cleanupAuthors, 10);
    function cleanupAuthors(){
        if ($("#field-authors").data("select2") && $("#field-authors").data("select2").opts) {
            clearInterval(timeoutAuthors);
            ngds.responsible_parties.overrideInitSelection("#field-authors");
            $("#field-authors").trigger("change");
        }
    }

    var timeoutMaintainer = setInterval(cleanupMaintainer, 10);
    function cleanupMaintainer(){
        if ($("#field-maintainer").data("select2") && $("#field-maintainer").data("select2").opts) {
            clearInterval(timeoutMaintainer);
            ngds.responsible_parties.overrideInitSelection("#field-maintainer");
            $("#field-maintainer").trigger("change");
        }
    }


    $("#field-authors").on("change", function(e){
        //console.log("#field-authors - change event: " + JSON.stringify({val:e.val, added: e.added, removed: e.removed}));
        if (e.added && (e.added.id == e.added.text)) {
            // since id==text, this is a select of new item (not from responsible_parties table)
            ngds.responsible_parties.add_new("Add New Author", "#field-authors", e.added);
        }
        if (e.removed) {
            // For reasons unknown, when overriding initSelection, removal no longer updates element.val() properly
            // so need to reconstruct from newly updated select2("data")
            var data = $("#field-authors").select2("data");
            if (data.length>0){
                var val = data[0].id;
                for (var i=1; i<data.length; i++) {
                    val += "," + data[i].id;
                }
                $("#field-authors").val(val);
            }
            else {
                $("#field-authors").val('');
            }
        }

        // cleanup json array brackets (missing or misplaced)
        var raw_val = $("#field-authors").val();
        raw_val = raw_val.replace(/\[/g,'').replace(/\]/g,'').replace(/^s+|\s+$/g,"");  // remove [,], and trim whitespace
        if (raw_val[0]==',') {
            raw_val = raw_val.substring(1);
        }
        $("#field-authors").val("[" + raw_val + "]");
    });

    $("#field-maintainer").on("change", function(e){
        //console.log("#field-maintainer - change event: " + JSON.stringify({val:e.val, added: e.added, removed: e.removed}));
        try {
            $.parseJSON(e.val);  // if parses successfully, then already well-formed and not a new Responsible Party
        }
        catch(err) {
            ngds.responsible_parties.add_new("Add New Maintainer", "#field-maintainer", e.val);
        }
    });


    ngds.responsible_parties = {

        'initSelection': function (element, callback) {
            var data = [];
            try {
                var party = $.parseJSON(element.val());
                if (party instanceof Array){
                    $.each(party, function (index, value){
                        data.push({id: JSON.stringify(value), text: value.name});
                    });
                    // remove contents from val() - if left - end up with double entries with misplaced []
                    element.val('');
                    callback(data);
                    // cleanup json array brackets []
                    if ($(element).data("select2").opts.multiple && $(element).val()[0]!="[") {
                        $(element).val( "[" + $(element).val() + "]");
                    }
                }
                else {
                    callback({id: JSON.stringify(party), text: party.name});
                }
            }
            catch(err){

            }
        },


        'overrideInitSelection':function (field_name) {
            //console.log(field_name + ": override initSelection()");
            $(field_name).data("select2").opts.initSelection = ngds.responsible_parties.initSelection;

            $(field_name).data("select2").opts.formatSelection = function(data, container) {
                try {
                    var party = JSON.parse(data.id);
                    return "<span title='" + party.name + "\n" + party.email + "'>" + data.text + "</span>";
                }
                catch(err) {
                    return data.text;
                }
            }
        },

        'add_new': function (popup_title, field_name, new_value) {
            //console.log("responsible_parties.add_new( ," + field_name + ")");
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

            var new_val = (new_value.id || new_value);

            if (new_val.indexOf("@")>=0) {
                $("#rs_email").val(new_val);
            }
            else {
                $("#rs_name").val(new_val);
            }



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

                    $.ajax({
                        'url': '/api/action/additional_metadata',
                        'type': 'POST',
                        'data': json_data,
                        'success': function (response) {
                            var new_id = {name: $("#rs_name").val(), email: $("#rs_email").val()};
                            var new_data;


                            if ($(field_name).data("select2").opts.multiple) {  // update id of last item, otherwise just replace

                                var data = $(field_name).data("select2").data();
                                data[data.length-1].id = JSON.stringify(new_id);
                                data[data.length-1].text = new_id.name;

                                var val = "[" + data[0].id;
                                for (var i=1; i<data.length; i++){
                                    val += "," + data[i].id;
                                }
                                val += "]";
                                $(field_name).val(val);
                                $(field_name).trigger("change");

                            }
                            else {
//                                $(field_name).data("select2").data(new_id);
                                $(field_name).val(JSON.stringify(new_id));
                                $(field_name).trigger("change");
                            }

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
            });

            element.on('click', '.btn-cancel', function (ev) {
                ev.preventDefault();
                if ($(field_name).data("select2").opts.multiple) { // data is array, remove last
                    var cur_data = $(field_name).data("select2").data();
                    cur_data.pop();
                    $(field_name).data("select2").data(cur_data);
                }
                else { // single item which must be removed
                    $(field_name).data("select2").data('');
                }
                modal.modal('hide');
                modal.remove();
            });

        }
    };

});

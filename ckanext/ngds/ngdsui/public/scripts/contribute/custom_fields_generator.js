/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
$(document).ready(function () {

    $("[rel=tooltip]").tooltip({ placement: 'right'});

    (function stage_setup() {
        ngds.util.state['prev_resource_type'] = $("[name=resource_format]:checked").val();
        ngds.util.state['versions'] = {};
        ngds.util.state['versions_dom'] = {};
        ngds.util.state['layers'] = {};
        ngds.util.state['layers_dom'] = {};
        if ($("[name=content_model_version]").length > 0 && $("[name=content_model_version]").parent().parent().attr("class").indexOf("error") !== -1) {
            $("[name=content_model_version]").prop("selectedIndex", -1);
            // Disobedient select box.
        }
        ngds.util.state['first-load'] = true;
    })();

    (function init_memorizer() {
        ngds.memorizer = (function () {

            var memory = {

            };

            var memorize = function (master_key, field_key, value) {
                if (typeof memory[master_key] === 'undefined') {
                    memory[master_key] = {};
                }
                memory[master_key][field_key] = value;
            };

            var remind = function (master_key, field_key) {
                if (typeof memory[master_key] === 'undefined') {
                    return '';
                }
                if (typeof memory[master_key][field_key] === 'undefined') {
                    return '';
                }

                return memory[master_key][field_key];
            };

            return {
                'memorize': memorize,
                'remind': remind
            }
        })();
    })();

    ngds.memorize_additional_fields = function (master_key) {
        $(".additional-resource-fields input").each(function () {
            if ($(this).attr("class") === "select2-input") {
                return;
            }
            if ($(this).attr("data-module") === 'autocomplete') {
                var key = $(this).attr("name");
                var value = $(this).select2("data");
                ngds.memorizer.memorize(master_key, key, value);
            }
            else if ($(this).val() !== "") {
                var key = $(this).attr("name");
                var value = $(this).val();
                ngds.memorizer.memorize(master_key, key, value);
            }
        });

        $(".additional-resource-fields select").each(function () {
            if ($(this).val() !== "") {
                if ($(this).attr("data-module") === 'autocomplete') {
                    var key = $(this).attr("name");
                    var value = $(this).select2("data");
                    ngds.memorizer.memorize(master_key, key, value);
                }
                else {
                    var key = $(this).attr("name");
                    var value = $(this).val();
                    ngds.memorizer.memorize(master_key, key, value);
                }
            }
        });

        $(".additional-resource-fields textarea").each(function () {
            if ($(this).val() !== "") {
                var key = $(this).attr("name");
                var value = $(this).val();
                ngds.memorizer.memorize(master_key, key, value);
            }
        });
    };

    ngds.restore_additional_fields = function (master_key) {

        $(".additional-resource-fields input").each(function () {

            if ($(this).attr("class") === "select2-input") {
                return;
            }
            var key = $(this).attr("name");
            var rvalue = ngds.memorizer.remind(master_key, key);
            if (rvalue !== '') {
                if (typeof rvalue === "object") {
                    $(this).val(JSON.stringify(rvalue));
                }
                if ($(this).attr("data-module") === 'autocomplete') {
                    $(this).select2("data", rvalue);
                }
                else {
                    $(this).val(rvalue);
                }
            }
        });

        $(".additional-resource-fields textarea").each(function () {
            var key = $(this).attr("name");
            var rvalue = ngds.memorizer.remind(master_key, key);
            if (rvalue !== '') {
                $(this).val(rvalue);
            }
        });

        $(".additional-resource-fields select").each(function () {
            var key = $(this).attr("name");

            var rvalue = ngds.memorizer.remind(master_key, key);

            if (rvalue === '') {
                return;
            }

            var options = $(this).children().filter("option");

            if ($(this).attr("data-module") === "autocomplete") {
                $(this).select2("data", rvalue);
            }
            else {
                options.each(function () {
                    if ($(this).val() === rvalue) {
                        $(this).prop("selected", true);
                    }
                });
            }
        });
    };

    $("[data-module=resource-upload-field] label").click(function (ev) {
        var for_attr = $(ev.currentTarget).attr("for");
        if (for_attr !== "field-resource-type-upload") {
            var resource_type = $("#" + $(ev.currentTarget).attr("for")).val();

            ngds.memorize_additional_fields(ngds.util.state['prev_resource_type']);
            ngds.util.state['prev_resource_type'] = resource_type;
            ngds.resource_type_change(resource_type);
        }
        var resource_type = $("#" + $(ev.currentTarget).attr("for")).val();
        if (resource_type === 'structured') {
            $(".validate-message").remove();
            var html = '<div class="validate-message">';
                html += '<div class="message" style="padding-top:20px;text-align:center;font-size:15px;color:red;">';
                html += '<a href="http://schemas.usgin.org/validate/cm" target="_blank"'
                html += 'rel="tooltip" title="Use this service to make sure your structured data conforms to USGIN specifications.">';
                html += 'Click here to validate your dataset first!'
                html += '</div></a></div>';
            $(ev.currentTarget).parent().after(html);
        } else if (resource_type === 'data-service') {
            $(".validate-message").remove();
            var html = '<div class="validate-message">';
                html += '<div class="message" style="padding-top:20px;text-align:center;font-size:15px;">';
                html += '<a href="http://schemas.usgin.org/validate/wfs" target="_blank"'
                html += 'rel="tooltip" title="Use this service to make sure your data service conforms to USGIN specifications.">';
                html += 'Click here to validate your data service first!'
                html += '</div></a></div>';
            $(ev.currentTarget).parent().after(html);
        } else {
            $(".validate-message").remove();
        }

    });

    ngds.load_content_model_widget = function (resource_type) {
        ngds.initialize_content_model_widget(function () {
            if (typeof $("#field-content-model")[0] !== 'undefined') {
                ckan.module.initializeElement($("#field-content-model")[0]);
            }

            if (typeof $("[name=content_model_uri]").val() !== 'undefined' && $("[name=content_model_uri]").val() !== "None") {
                var val = $("[name=content_model_uri]").val();
                var versions_dom = ngds.util.state['versions_dom'][val];
                if (typeof versions_dom !== 'undefined') {
                    $("[name=content_model_version]").empty();
                    for (var i = 0; i < versions_dom.length; i++) {
                        $("[name=content_model_version]").append(versions_dom[i]);
                    }
                }
            }

            function load_content_model_versions(content_model_uri) {
                $("#field-content-model-version").select2("destroy");
                var val = content_model_uri;
                var option_constructor = function (version) {
                    var option = {
                        'tag': 'option',
                        'attributes': {
                            'value': version['uri'],
                            'text': version['version']
                        }
                    };
                    return ngds.util.dom_element_constructor(option);
                };

                if (content_model_uri === 'None' || content_model_uri === 'none') {
                    $("[name=content_model_version]").empty();
                    $("[name=content_model_version]").append(option_constructor({"uri": "None", "version": "None"}));
                    $("#field-content-model-version").select2();
                    if ($("[name=content_model_version]").val()) {
                        loadContentModelLayers($("[name=content_model_version]").val());
                    }
                } else if (typeof ngds.util.state['versions'][val] === 'undefined') {
                    $.ajax({
                        'url': '/api/action/get_content_model_version_for_uri',
                        'data': JSON.stringify({
                            'cm_uri': val
                        }),
                        'type': 'POST',
                        'success': function (response) {
                            var versions = response.result;
                            ngds.util.state['versions'][val] = versions;
                            var versions_dom = ngds.util.state['versions_dom'][val] = [];
                            $("[name=content_model_version]").empty();

                            for (var i = 0; i < versions.length; i++) {
                                $("[name=content_model_version]").append(option_constructor(versions[i]));
                                versions_dom.push(option_constructor(versions[i]));
                            }
                            if (ngds.memorizer.remind("structured", "content_model_version") !== "") {
                                $("#field-content-model-version option").filter("[value=" + ngds.memorizer.remind("structured", "content_model_version")['id'] + "]").prop("selected", true);
                            }
                            $("#field-content-model-version").select2();
                            if ($("[name=content_model_version]").val()) {
                                loadContentModelLayers($("[name=content_model_version]").val());
                            }
                        }

                    });
                } else {
                    var versions_dom = ngds.util.state['versions_dom'][val];
                    $("[name=content_model_version]").empty();
                    for (var i = 0; i < versions_dom.length; i++) {
                        $("[name=content_model_version]").append(versions_dom[i]);
                    }
                }

            };

            function loadContentModelLayers(content_model_uri) {
                $("#field-content-model-layer").select2("destroy");
                var val = content_model_uri;
                var optionConstructor = function (this_data) {
                    var option = {
                        'tag': 'option',
                        'attributes': {
                            'value': this_data['layer'],
                            'text': this_data['layer']
                        }
                    };
                    return ngds.util.dom_element_constructor(option);
                };
                if (content_model_uri === 'None' || content_model_uri === 'none') {
                    $("[name=content_model_layer]").empty();
                    $("[name=content_model_layer]").append(optionConstructor({"layer": "None", "layer": "None"}));
                    $("#field-content-model-layer").select2();
                } else if (typeof ngds.util.state['layers'][val] === 'undefined') {
                    $.ajax({
                        'url': '/api/action/get_content_model_layers_for_uri',
                        'data': JSON.stringify({'cm_uri': val}),
                        'type': 'POST',
                        'success': function (response) {
                            var versions = response.result;
                            ngds.util.state['layers'][val] = versions;
                            var layersDom = ngds.util.state['layers_dom'][val] = [];
                            $("[name=content_model_layer]").empty();

                            var selector = $('#field-content-model-version').val().split(/[\s\/]+/).pop();

                            for (var i = 0; i < versions['versions'][selector].length; i++) {
                                var this_data = {'layer': versions['versions'][selector][i]};
                                $("[name=content_model_layer]").append(optionConstructor(this_data));
                                layersDom.push(optionConstructor(this_data));
                            }

                            if (ngds.memorizer.remind("structured", "content_model_version") !== "") {
                                $("#field-content-model-layer option").filter("[value=" + ngds.memorizer.remind("structured", "content_model_version")["id"] + "]").prop("selected", true);
                            }
                            $("#field-content-model-layer").select2();
                        }
                    });
                } else {
                    var layersDom = ngds.util.state['layers_dom'][val];
                    $("[name=content_model_layer]").empty();
                    for (var i = 0; i < layersDom.length; i++) {
                        $("[name=content_model_layer]").append(layersDom[i]);
                    }
                }
            };

            $("[name=content_model_uri]").on('change', function (ev) {
                var val = ev.val;
                $("[name=content_model_version]").select2("destroy");
                $("[name=content_model_version]").empty();
                $("[name=content_model_version]").select2();
                load_content_model_versions(val);
            });

            $("[name=content_model_version]").on('change', function (e) {
                var val = e.val;
                $("[name=content_model_layer]").select2("destroy");
                $("[name=content_model_layer]").empty();
                $("[name=content_model_layer]").select2();
                loadContentModelLayers(val);
            });

            ngds.restore_additional_fields(resource_type);

            if ($("[name=content_model_uri]").length > 0) {
                load_content_model_versions($("[name=content_model_uri]").val());
            }

        });
        $("[name=content_model_version]").select2();
        $("[name=content_model_layer]").select2();

        if (resource_type===undefined) {
            $(".resource-upload-field").css("display", "none");
        }
        ngds.setup_responsible_party();

    };

    ngds.resource_type_change = function (resource_type) {
        $(".additional-resource-fields").empty();
        construct_form_objects();

        if (resource_type === 'structured') {
            $(".additional-resource-fields").replaceWith(ngds.forms.structured_form.form);
            ngds.load_content_model_widget("structured");
            ckan.module.initializeElement($("#field-distributor")[0]);
            ckan.module.initializeElement($("#field-format")[0]);
            $(".resource-upload-field").css("display", "inline-block");
        }

        if (resource_type === 'unstructured') {
            $(".additional-resource-fields").replaceWith(ngds.forms.unstructured_form.form);
            ckan.module.initializeElement($("#field-distributor")[0]);
            ckan.module.initializeElement($("#field-format")[0]);
            $(".resource-upload-field").css("display", "inline-block");
        }

        if (resource_type === 'offline-resource') {
            $(".additional-resource-fields").replaceWith(ngds.forms.offline_form.form);
            ckan.module.initializeElement($("#field-distributor")[0]);
            $(".resource-upload-field").css("display", "none");
        }

        if (resource_type === 'data-service') {
            $(".additional-resource-fields").replaceWith(ngds.forms.data_service_form.form);
            ckan.module.initializeElement($("#field-distributor")[0]);
            ckan.module.initializeElement($("#field-protocol")[0]);
            $(".resource-upload-field").css("display", "none");
        }

        ngds.setup_responsible_party();

        ngds.restore_additional_fields(resource_type);


    };


    //  Setup handler, format override for Distributor (Responsible Party).
    var ngds_override_distrib_timer;
    ngds.setup_responsible_party = function() {

        if ($("#field-distributor").length) {
            // Add handler to add new Responsible Party (brings up dialog to fill-in email, etc.)
            // make sure any previously attached handler is removed.
            try {
                $("#field-distributor").off("change", ngds.distributor_on_change);
            }
            catch(err){}
            $("#field-distributor").on("change", ngds.distributor_on_change);

            // Since $("#field-distributor").data("select2").opts not yet defined, need to setup
            // a recurring timer to check for it's existence, then override initSelection()
            if(!ngds_override_distrib_timer)
                ngds_override_distrib_timer = setInterval(ngds.override_distrib_initSelection, 10);
        }
    }

    ngds.distributor_on_change = function(e){
        try {
            $.parseJSON(e.val);  // if parses successfully, then already well formed and not a new Responsible Party
        }
        catch(err) {
            ngds.responsible_parties.add_new("Add New Distributor", "#field-distributor", e.val);
        }
    }

    // Need to override the select2 initSelection() function for #field-distributor since value is JSON string rather Name.
    ngds.override_distrib_initSelection = function() {
        if ($("#field-distributor").data("select2") && $("#field-distributor").data("select2").opts){
            clearInterval(ngds_override_distrib_timer);
            ngds_override_distrib_timer = undefined;
            ngds.responsible_parties.overrideInitSelection("#field-distributor");
            $("#field-distributor").trigger("change");
        }
    };

    ngds.load_content_model_widget($("[name=resource_format]:checked").val());
});

ngds.initialize_content_model_widget = function (callback) {

    if (typeof ngds.util.state['content_models'] === 'undefined') {
        $.ajax({
            'url': '/api/action/get_content_models_for_ui',
            'type': 'POST',
            'data': JSON.stringify({"dummy": "dummy"}),
            'success': function (response) {
                ngds.util.state['content_models'] = response.result;
                var option_constructor = function (content_model) {
                    var option = {
                        'tag': 'option',
                        'attributes': {
                            'value': content_model['uri'],
                            'text': content_model['title']
                        }
                    };
                    return ngds.util.dom_element_constructor(option);
                };

                var content_models = ngds.util.state['content_models'];
                var content_models_dom = ngds.util.state['content_models_dom'] = [];
                var none = option_constructor({"uri": "None", "title": "None"});

                $("[name=content_model_uri]").append(none);
                content_models_dom.push(none);

                for (var i = 0; i < content_models.length; i++) {
                    $("[name=content_model_uri]").append(option_constructor(content_models[i]));
                    content_models_dom.push(option_constructor(content_models[i]));
                }
                callback();
            }
        })
    }
    else {
        var content_models_dom = ngds.util.state['content_models_dom'];

        for (var i = 0; i < content_models_dom.length; i++) {
            $("[name=content_model_uri]").append(content_models_dom[i]);
        }
        callback();
    }

};


function construct_form_objects() {
    ngds.forms = {};
    ngds.forms.structured_form = {};
    ngds.forms.unstructured_form = {};
    ngds.forms.offline_form = {};
    ngds.forms.data_service_form = {};

    ngds.forms.structured_form.form = ngds.util.dom_element_constructor(structured_form_raw);

    ngds.forms.unstructured_form.form = ngds.util.dom_element_constructor(unstructured_form_raw);

    ngds.forms.offline_form.form = ngds.util.dom_element_constructor(offline_form_raw);

    ngds.forms.data_service_form.form = ngds.util.dom_element_constructor(data_service_raw);

};


var structured_form_raw = {
    'tag': 'div',
    'attributes': {
        'class': 'additional-resource-fields'
    },
    'children': [
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-full'
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-content-model',
                        'text': 'Content Model'
                    }
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls'
                    },
                    'children': [
                        {
                            'tag': 'select',
                            'attributes': {
                                'id': 'field-content-model',
                                'type': 'text',
                                'name': 'content_model_uri',
                                'placeholder': 'Ex: Borehole Lithology Intercepts',
                                'data-module': "autocomplete"
                            }
                        }
                    ]
                }
            ]
        },
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-full'
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-content-model-version',
                        'text': 'Content Model Version'
                    }
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls'
                    },
                    'children': [
                        {
                            'tag': 'select',
                            'attributes': {
                                'id': 'field-content-model-version',
                                'type': 'text',
                                'name': 'content_model_version',
                                'placeholder': 'Ex: 1.1',
//                                'data-module': "autocomplete"
                            }
                        }
                    ]
                }
            ]
        },
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-full'
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-content-model-layer',
                        'text': 'Content Model Layer'
                    }
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls'
                    },
                    'children': [
                        {
                            'tag': 'select',
                            'attributes': {
                                'id': 'field-content-model-layer',
                                'type': 'text',
                                'name': 'content_model_layer'
                            }
                        }
                    ]
                }
            ]
        },
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-full'
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-distributor',
                        'text': 'Distributor'
                    },
                    'children': [
                        {
                             'tag': 'span',
                            'attributes': {
                                'class': 'mandatory',
                                'text': ' *'}
                        }
                    ]
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls'
                    },
                    'children': [
                        {
                            'tag': 'input',
                            'attributes': {
                                'id': 'field-distributor',
                                'type': 'text',
                                'name': 'distributor',
                                'placeholder': 'Ex: ' +
                                    'John Doe',
                                'data-module-label': "name",
                                'data-module': "autocomplete",
                                'data-module-source': "responsible_parties?q=?",
                                'data-module-key': "value"
                            }
                        }
                    ]
                }
            ]
        },
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-full'
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-format',
                        'text': 'Format'
                    }
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls'
                    },
                    'children': [
                        {
                            'tag': 'input',
                            'attributes': {
                                'id': 'field-format',
                                'type': 'text',
                                'name': 'format',
                                'placeholder': 'eg. CSV, XML or JSON',
                                'data-module': 'autocomplete',
                                'data-module-source': "/api/2/util/resource/format_autocomplete?incomplete=?"
                            }
                        }
                    ]
                }
            ]
        }

    ]
};


var data_service_raw = {
    'tag': 'div',
    'attributes': {
        'class': 'additional-resource-fields'
    },
    'children': [
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-full'
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-distributor',
                        'text': 'Distributor'
                    },
                    'children': [
                        {
                             'tag': 'span',
                            'attributes': {
                                'class': 'mandatory',
                                'text': ' *'}
                        }
                    ]
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls'
                    },
                    'children': [
                        {
                            'tag': 'input',
                            'attributes': {
                                'id': 'field-distributor',
                                'type': 'text',
                                'name': 'distributor',
                                'placeholder': 'Ex: ' +
                                    'John Doe',
                                'data-module-label': "name",
                                'data-module': "autocomplete",
                                'data-module-source': "responsible_parties?q=?",
                                'data-module-key': "value"
                            }
                        }
                    ]
                }
            ]
        },
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-medium'
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-protocol',
                        'text': 'Protocol'
                    }
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls'
                    },
                    'children': [
                        {
                            'tag': 'select',
                            'attributes': {
                                'id': 'field-protocol',
                                'name': 'protocol',
                                'placeholder': 'Ex: WMS',
                                'data-module': "autocomplete"
                            },
                            'children': [
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'WMS',
                                        'value': 'OGC:WMS'
                                    }
                                },
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'WFS',
                                        'value': 'OGC:WFS'
                                    }
                                },
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'ESRI Map Service',
                                        'value': 'ESRI'
                                    }
                                },
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'CSW',
                                        'value': 'OGC:CSW'
                                    }
                                },
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'SOS',
                                        'value': 'OGC:SOS'
                                    }
                                },
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'OPeNDAP',
                                        'value': 'OPeNDAP'
                                    }
                                },
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'Other',
                                        'value': 'other'
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-full'
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-layer',
                        'text': 'Layer'
                    }
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls'
                    },
                    'children': [
                        {
                            'tag': 'input',
                            'attributes': {
                                'type': 'text',
                                'name': 'layer',
                                'id': 'field-layer',
                                'placeholder': 'A layer name that can be used to access this resource using the protocol selected above. Eg. A Geoserver WMS layer.'
                            }
                        }
                    ]
                }
            ]
        }
    ]};


var unstructured_form_raw = {
    'tag': 'div',
    'attributes': {
        'class': 'additional-resource-fields'
    },
    'children': [
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-full'
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-distributor',
                        'text': 'Distributor'
                    },
                    'children': [
                        {
                             'tag': 'span',
                            'attributes': {
                                'class': 'mandatory',
                                'text': ' *'}
                        }
                    ]
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls'
                    },
                    'children': [
                        {
                            'tag': 'input',
                            'attributes': {
                                'id': 'field-distributor',
                                'type': 'text',
                                'name': 'distributor',
                                'placeholder': 'Ex: ' +
                                    'John Doe',
                                'data-module-label': "name",
                                'data-module': "autocomplete",
                                'data-module-source': "responsible_parties?q=?",
                                'data-module-key': "value"
                            }
                        }
                    ]
                }
            ]
        },
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-full'
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-format',
                        'text': 'Format'
                    }
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls'
                    },
                    'children': [
                        {
                            'tag': 'input',
                            'attributes': {
                                'id': 'field-format',
                                'type': 'text',
                                'name': 'format',
                                'placeholder': 'eg. CSV, XML or JSON',
                                'data-module': 'autocomplete',
                                'data-module-source': "/api/2/util/resource/format_autocomplete?incomplete=?"
                            }
                        }
                    ]
                }
            ]
        }

    ]};


var offline_form_raw = {
    'tag': 'div',
    'attributes': {
        'class': 'additional-resource-fields'
    },
    'children': [
        {
            'tag': 'div',
            'attributes': {
                'class': 'control-group control-full'
            },
            'children': [
                    {
                        'tag': 'label',
                        'attributes': {
                            'class': 'control-label',
                            'for': 'field-distributor',
                            'text': 'Distributor'
                        },
                        'children': [
                            {
                                 'tag': 'span',
                                'attributes': {
                                    'class': 'mandatory',
                                    'text': ' *'}
                            }
                        ]
                    },
                    {
                        'tag': 'div',
                        'attributes': {
                            'class': 'controls'
                        },
                        'children': [
                            {
                                'tag': 'input',
                                'attributes': {
                                    'id': 'field-distributor',
                                    'type': 'text',
                                    'name': 'distributor',
                                    'placeholder': 'Ex: ' +
                                        'John Doe',
                                    'data-module-label': "name",
                                    'data-module': "autocomplete",
                                    'data-module-source': "responsible_parties?q=?",
                                    'data-module-key': "value"
                                }
                            }
                        ]
                },
                {
                    'tag': 'label',
                    'attributes': {
                        'class': 'control-label',
                        'for': 'field-ordering-procedure',
                        'text': 'Ordering Procedure'
                    },
                        'children': [
                            {
                                 'tag': 'span',
                                'attributes': {
                                    'class': 'mandatory',
                                    'text': ' *'}
                            }
                        ]
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'controls editor'
                    },
                    'children': [
                        {
                            'tag': 'textarea',
                            'attributes': {
                                'id': 'field-ordering-procedure',
                                'name': 'ordering_procedure',
                                'placeholder': 'Indicate how a person can go about obtaining this resource.',
                                'cols': '20',
                                'rows': '5'
                            }
                        }
                    ]

                }

            ]
        }
    ]};


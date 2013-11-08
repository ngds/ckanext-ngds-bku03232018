$(document).ready(function () {
    (function stage_setup() {
        ngds.util.state['prev_resource_type'] = $("[name=resource_format]:checked").val();
        ngds.util.state['versions'] = {};
        ngds.util.state['versions_dom'] = {};
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

    });

    ngds.load_content_model_widget = function (resource_type) {
        ngds.initialize_content_model_widget(function () {
            if (typeof $("#field-content-model")[0] !== 'undefined') {
                ckan.module.initializeElement($("#field-content-model")[0]);
            }
//            if (typeof $("#field-content-model-version")[0] !== 'undefined') {
//
//                ckan.module.initializeElement($("#field-content-model-version")[0]);
//            }

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
//                if (ngds.memorizer.remind('structured', 'content_model_version') === "") {
//                    return;
//                }
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

                if (typeof ngds.util.state['versions'][val] === 'undefined') {
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
                            else {
//                                $("[name=content_model_version]").prop("selectedIndex", -1);
                            }
                            $("#field-content-model-version").select2();
                        }

                    });
                }
                else {
                    var versions_dom = ngds.util.state['versions_dom'][val];
                    $("[name=content_model_version]").empty();
                    for (var i = 0; i < versions_dom.length; i++) {
                        $("[name=content_model_version]").append(versions_dom[i]);
                    }
//                    $("[name=content_model_version]").prop("selectedIndex", -1);
                }
            };

            $("[name=content_model_uri]").on('change', function (ev) {
                console.log("here");
                var val = ev.val;
                console.log(val);
                if (val === "None" || val==="none") {
                    $("[name=content_model_version]").select2("destroy");
                    $("[name=content_model_version]").empty();
                    $("[name=content_model_version]").select2();
                    return;
                }

                load_content_model_versions(val);
            });

            ngds.restore_additional_fields(resource_type);

            if ($("[name=content_model_uri]").length > 0 && $("[name=content_model_uri]").val() !== "None" && $("[name=content_model_uri]").val() !== "none") {
                load_content_model_versions($("[name=content_model_uri]").val());
            }
        });
        $("[name=content_model_version]").select2();
    };

    ngds.resource_type_change = function (resource_type) {
        $(".additional-resource-fields").empty();
        construct_form_objects();

        if (resource_type === 'structured') {
            $(".additional-resource-fields").replaceWith(ngds.forms.structured_form.form);
            ngds.load_content_model_widget("structured");
            ckan.module.initializeElement($("#field-distributor")[0]);
            ckan.module.initializeElement($("#field-format")[0]);
        }

        if (resource_type === 'unstructured') {
            $(".additional-resource-fields").replaceWith(ngds.forms.unstructured_form.form);
            ckan.module.initializeElement($("#field-distributor")[0]);
            ckan.module.initializeElement($("#field-format")[0]);
        }

        if (resource_type === 'offline-resource') {
            $(".additional-resource-fields").replaceWith(ngds.forms.offline_form.form);
        }

        if (resource_type === 'data-service') {
            $(".additional-resource-fields").replaceWith(ngds.forms.data_service_form.form);
            ckan.module.initializeElement($("#field-distributor")[0]);
            ckan.module.initializeElement($("#field-protocol")[0]);
        }

        ngds.restore_additional_fields(resource_type);
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
                var none = option_constructor({"uri": "None", "title": "none"});

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
                        'for': 'field-distributor',
                        'text': 'Distributor'
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
                                        'value': 'esri_map_service'
                                    }
                                },
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'CSW',
                                        'value': 'csw'
                                    }
                                },
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'SOS',
                                        'value': 'sos'
                                    }
                                },
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'Open DAP',
                                        'value': 'opendap'
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
                        'for': 'field-ordering-procedure',
                        'text': 'Ordering Procedure'
                    }
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


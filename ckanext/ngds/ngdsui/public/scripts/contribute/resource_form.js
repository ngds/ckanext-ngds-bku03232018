var populate_content_models = function () {
    var content_model_combo = $(".content_model");
    if (typeof options === 'undefined') {
        options = [];
        options.push($('<option/>', {value: 'none', text: 'None'}).appendTo(content_model_combo));
        for (var val in content_models) {
            options.push($('<option/>', {value: val, text: content_models[val].title}).appendTo(content_model_combo));
        }
        return;
    }

    for (var i = 0; i < options.length; i++) {
        options[i].appendTo(content_model_combo);
    }
};


var populate_content_model_versions = function () {
    var marker = $(".content_model_marker");
    var content_model_combo = $(".content_model");
    if (content_model_combo.val() === 'none') { // If the value is 'none', then don't populate any versions.
        return;
    }

    $('.content_model_version_marker').remove();

    var content_model_version_struct = [
        {
            'label': 'Version',
            'div_classes': ['content_model_version_marker'],
            'inputs': [
                {
                    'tag': 'select',
                    'attributes': {
                        'class': 'structured-input content_model_version',
                        'name': 'content_model_version'
                    }
                }
            ]
        }
    ];
    content_model_combo.after(form_generator(content_model_version_struct));

    var content_model_version_combo = $(".content_model_version");
    var content_model_selected = content_model_combo.val();

    for (var i = 0; i < content_models[content_model_selected].versions.length; i++) {
        $('<option/>', {value: content_models[content_model_selected].versions[i].uri, text: content_models[content_model_selected].versions[i].version}).appendTo(content_model_version_combo);
    }
};

$("#file").on('change', function (ev) {
    var timestamp = new Date().toISOString();
    var file = $("#file").val();
    var filename = file.substring(file.lastIndexOf("\\") + 1);
    $("#key1").val(timestamp + "/" + filename);
    $("#key2").val(timestamp + "/" + filename);
    $("#resource_type").val($("[name=resource_format]:checked").val());
    $("#file-upload-form").submit();
});

var populate_form = function (data) {
    for (property in data) {
        if ($("[name=" + property + "]").length > 0) {
            if (property === 'distributor') {

            }
            $("[name=" + property + "]").val(data[property]);
        }
    }
};

var activate_populate_form = function (data) {
    render_forms(data['resource_format']);
    populate_form(data);
    $("#resource_type-selection").prop("disabled", true);
    $("input[type=radio]").prop("disabled", true);
    var name = get_prop($("#field-url").val(), 'name');
    var file_extension = get_prop($("#field-url").val(), 'extension');
    $("[name=name]").val(name);
    $("[name=format]").val(file_extension);
};

var get_prop = function (url, what) {
    if (typeof url === 'undefined' || url.length === 0) {
        return '';
    }
    var sp = url.substring(url.lastIndexOf('/') + 1);
    if (what === 'name') {
        return sp.split('.')[0];
    }
    if (what === 'extension') {
        return sp.split('.')[1];
    }
};


position_file_uploader();
var render_forms = function (value) {
        $(".form-body").empty();
        if (value === 'structured' || value === 'unstructured') {
            $("[name=upload_type_selection]").prop("checked", true);
        }
        else {
            $("[name=upload_type_selection]").prop("checked", false);
        }
        if (value === "structured") {
            $("#resource_type-structured").prop("checked", true);
            $(".form-body").replaceWith(form_generator(ngds.form.structured_form_fields));
            position_file_uploader("#field-url");
            populate_content_models();
            $(".form-body").on("change", ".content_model", function () { // When the content model combo's value changes, populate the content model versions into the content_model_version combo box.
                populate_content_model_versions();
            });
        }

        if (value === "unstructured") {
            $("#resource_type-unstructured").prop("checked", true);
            $(".form-body").replaceWith(form_generator(ngds.form.unstructured_form_fields));
            position_file_uploader("#field-url");
        }

        if (value === "offline-resource") {
            $("#offline-resource").prop("checked", true);
            $(".form-body").replaceWith(form_generator(ngds.form.offline_form_fields));
            position_file_uploader();
        }

        if (value === "data-service") {
            $(".form-body").replaceWith(form_generator(ngds.form.data_service_form_fields));
            position_file_uploader();
        }

        if (value === "data-service" || value === "unstructured" || value === "structured") {
            responsibilified = new ngds.responsible_party();
            responsibilified.responsibilify({
                'rs_name': '#distributor_name',
                'rs_email': '#distributor_email',
                'rs_fake': '#distributor_fake',
                'rs': '#distributor',
                'slug_container': '.distributor-tag'
            }, function (dict) {
                $("[name='distributor_name']").val(dict['name']);
                $("[name='distributor_email']").val(dict['email']);
            });
        }

        ngds.publish("Forms.reinitialize", {});
    }
    ;
$('input[name="resource_format"]').on('change', function (ev) {
    var id = ev.currentTarget.id;
    var value = "";
    if (id === "resource_type-unstructured") {
        value = 'unstructured';
    }
    if (id === "resource_type-structured") {
        value = 'structured';
    }
    if (id === "offline-resource") {
        value = 'offline-resource';
    }
    if (id === "data-service") {
        value = 'data-service';
    }

    render_forms(value);
});

$("#go-metadata").click(function () {
    $.ajax({
        'url': '/ngds/contribute/validate_resource',
        'data': $(".dataset-form").serializeArray(),
        'success': function (response) {
            if (response.success === true) {
                $(".dataset-form").append($("<input/>", {'type': 'hidden', 'name': 'save', 'value': 'go-metadata'}));
                $(".dataset-form").submit();
            }
            else {
                ngds.publish('Notifications.received', response);
            }
        }
    });
});


if (typeof continuation !== 'undefined') {
    for (var i = 0; i < continuation.length; i++) {
        $("[name=" + continuation['field'] + "]").val(continuation['value']);
    }
}
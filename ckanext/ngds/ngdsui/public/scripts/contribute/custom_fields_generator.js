$(document).ready(function () {
    console.log(ngds.util);
    construct_form_objects();


    $("[name=resource_format]").on('change', function (ev) {
        var resource_type = ev.currentTarget.value;

        $(".additional-resource-fields").empty();

        if (resource_type === 'unstructured') {
            $(".additional-resource-fields").append(ngds.forms.unstructured_form.form);
        }

        if (resource_type === 'offline-resource') {
            $(".additional-resource-fields").append(ngds.forms.offline_form.form);
        }

    });
});


function construct_form_objects() {
    ngds.forms = {};
    ngds.forms.unstructured_form = {};
    ngds.forms.offline_form = {};

    ngds.forms.unstructured_form.form = ngds.util.dom_element_constructor(unstructured_form_raw);
    ngds.forms.unstructured_form.values = {};

    ngds.forms.offline_form.form = ngds.util.dom_element_constructor(offline_form_raw);
    ngds.forms.offline_form.values = {};
};


var unstructured_form_raw = {
    'tag': 'div',
    'attributes': {
        'class': 'control-group control-full'
    },
    'children': [
        {
            'tag': 'label',
            'attributes': {
                'class': 'control-label',
                'for': 'distributor',
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
                        'placeholder': 'John Doe'
                    }
                }
            ]
        }
    ]
};


var offline_form_raw = {
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
                        'cols':'20',
                        'rows':'5'
                    }
                }
            ]

        }

    ]
};


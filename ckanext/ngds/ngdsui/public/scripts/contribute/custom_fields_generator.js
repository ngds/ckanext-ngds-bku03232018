$(document).ready(function () {
    $("[name=ngds_resource_type]").on('change', function (ev) {
        var resource_type = ev.currentTarget.value;
        if (resource_type === 'unstructured') {
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
            var unstructured_form = ngds.util.dom_element_constructor(unstructured_form_raw);
            $(".form-actions").before(unstructured_form);
        }
    });
});

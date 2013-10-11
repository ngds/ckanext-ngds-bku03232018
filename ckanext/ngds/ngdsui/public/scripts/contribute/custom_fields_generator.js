$(document).ready(function () {

    $("[name=resource_format]").on('change', function (ev) {
        var resource_type = ev.currentTarget.value;

        $(".additional-resource-fields").empty();
        construct_form_objects();

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

    });
});


function construct_form_objects() {
    ngds.forms = {};
    ngds.forms.unstructured_form = {};
    ngds.forms.offline_form = {};
    ngds.forms.data_service_form = {};

    ngds.forms.unstructured_form.form = ngds.util.dom_element_constructor(unstructured_form_raw);
    ngds.forms.unstructured_form.values = {};

    ngds.forms.offline_form.form = ngds.util.dom_element_constructor(offline_form_raw);
    ngds.forms.offline_form.values = {};

    ngds.forms.data_service_form.form = ngds.util.dom_element_constructor(data_service_raw);
    ngds.forms.data_service_form.values = {};
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
                                        'value': 'wms'
                                    }
                                },
                                {
                                    'tag': 'option',
                                    'attributes': {
                                        'text': 'WFS',
                                        'value': 'wfs'
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


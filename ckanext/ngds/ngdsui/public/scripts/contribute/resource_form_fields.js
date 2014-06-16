/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
var form_generator = function (form) {

    var input_groups = [];
    var final_inputs = {
        'tag': 'div',
        'attributes': {
            'class': 'form-body'
        }
    };


    for (var i = 0; i < form.length; i++) {
        var item = form[i];

        var input_group = {
            'tag': 'div',
            'attributes': {
                'class': (function (item) {
                    if (typeof item['div_classes'] !== 'undefined') {
                        return 'input-group ' + item['div_classes'].join(" ");
                    }
                    return 'input-group';
                })(item)
            }

        };

        var sp_label = {
            'tag': 'div',
            'attributes': {
                'class': (function (item) {
                    if (typeof item['label_div_classes'] !== 'undefined') {
                        return 'sp-label ' + item['label_div_classes'].join(" ");
                    }
                    return 'sp-label';
                })(item)
            },
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'text': item['label']
                    }
                }
            ]
        };

        var inputs = item['inputs'];

        input_group['children'] = [sp_label];
        for (var j = 0; j < inputs.length; j++) {
            input_group['children'].push(inputs[j]);
        }

        input_groups.push(input_group);

    }
    final_inputs['children'] = input_groups;
    return ngds.util.dom_element_constructor(final_inputs);
};

ngds.rs_generator = function (fields, cls, party_type) {

    var form_items = [];
    var buttons = [];
    for (var field_index in fields) {
        var field = fields[field_index];

        if (typeof field['button'] !== 'undefined') {
            var button = {
                'tag': 'button',
                'attributes': {
                    'type': 'button',
                    'class': field['class'],
                    'id': field['id'],
                    'text': field['button']
                }
            };
            buttons.push(button);
            continue;
        }

        var form_item = {
            'tag': 'div',
            'children': [
                {
                    'tag': 'label',
                    'attributes': {
                        'class': field['label_class'],
                        'text': field['label']
                    }
                },
                {
                    'tag': 'input',
                    'attributes': {
                        'name': field['input_name'],
                        'type': 'text',
                        'class': 'small ' + field['input_class'],
                        'id': field['input_id']
                    }
                }
            ]
        };
        form_items.push(form_item);
    }

    var pre_dom_rs = {
        'tag': 'div',
        'attributes': {
            'class': 'add-responsible-party ' + cls
        },
        children: [
            {
                'tag': 'h4',
                'attributes': {
                    'text': 'Create ' + party_type
                }
            },
            {
                'tag': 'div',
                'attributes': {
                    'class': 'tab'
                },
                'children':form_items
            },
            {
                'tag':'div',
                'attributes':{
                    'class':'rsactions'
                },
                'children':buttons
            }
        ]
    };

    return ngds.util.dom_element_constructor(pre_dom_rs);
};


ngds.form = {};

ngds.form.structured_form_fields = [
    {
        'label': 'Resource URL',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Eg. http://example.com/myresource.txt or upload a file instead',
                    'id': 'field-url',
                    'name': 'url',
                    'class': 'structured-input',
                    'title': 'A URL for this resource or upload a file'
                }
            }
        ]
    },
    {
        'label': 'Name',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Eg. Well Log Headers',
                    'id': 'field-name',
                    'name': 'name',
                    'class': 'structured-input',
                    'title': 'A name for this resource'
                }
            }
        ]
    },
    {
        'label': 'Content Model',
        'div_classes': ['content_model_marker'],
        'inputs': [
            {
                'tag': 'select',
                'attributes': {
//                    'data-module': 'autocomplete',
                    'name': 'content_model_uri',
                    'class': 'structured-input content_model',
                    'title': 'A content model pertaining to this resource'
                }
            }
        ]
    },
    {
        'label': 'Description',
        'label_div_classes': ['description-label-div'],
        'inputs': [
            {
                'tag': 'textarea',
                'attributes': {
                    'rows': '4',
                    'placeholder': 'Eg. A description of this resource.',
                    'cols': '1',
                    'name': 'description',
                    'id': 'description',
                    'class': 'structured_input',
                    'title': 'Describe this resource'
                }
            }
        ]
    },
    {
        'label': 'Distributor',
        'div_classes': ['distributor'],
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Begin typing a distributor\'s name and suggestions will be made. Create one by clicking on the + icon to the right.',
                    'id': 'distributor_fake',
                    'class': 'structured-input',
                    'title': 'The distributor for this resource'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor',
                    'name': 'distributor'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor_name'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor_email'
                }
            },
            {
                'tag': 'div',
                'attributes': {
                    'class': 'distributor-tag retreived-tags'
                }
            }
        ]
    },
    {
        'label': 'Format',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Eg. csv',
                    'name': 'format',
                    'class': 'structured-input',
                    'title': 'The file format of this resource'
                }
            }
        ]
    }
];

ngds.form.unstructured_form_fields = [
    {
        'label': 'Resource URL',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Eg. http://example.com/myresource.txt or upload a file instead',
                    'id': 'field-url',
                    'name': 'url',
                    'class': 'structured-input',
                    'title': 'A URL for this resource or upload a file'
                }
            }
        ]
    },
    {
        'label': 'Name',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'name': 'name',
                    'id': 'field-name',
                    'placeholder': 'Eg. Well Log Headers',
                    'class': 'structured-input',
                    'title': 'A name for this resource'
                }
            }
        ]
    },
    {
        'label': 'Description',
        'label_div_classes': ['description-label-div'],
        'inputs': [
            {
                'tag': 'textarea',
                'attributes': {
                    'rows': '4',
                    'cols': '1',
                    'name': 'description',
                    'placeholder': 'Eg. A description of this resource.',
                    'id': 'description',
                    'class': 'structured_input',
                    'title': 'Describe this resource'
                }
            }
        ]
    },
    {
        'label': 'Distributor',
        'div_classes': ['distributor'],
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Begin typing a distributor\'s name and suggestions will be made. Create one by clicking on the + icon to the right.',
                    'id': 'distributor_fake',
                    'class': 'structured-input',
                    'title': 'The distributor for this resource'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor',
                    'name': 'distributor'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor_name'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor_email'
                }
            },
            {
                'tag': 'div',
                'attributes': {
                    'class': 'distributor-tag retreived-tags'
                }
            }
        ]
    },
    {
        'label': 'Format',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Eg. csv',
                    'name': 'format',
                    'class': 'structured-input',
                    'title': 'The file format of this resource'
                }
            }
        ]
    }
];

ngds.form.offline_form_fields = [
    {
        'label': 'Resource URL',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Eg. http://example.com/myresource.txt or upload a file instead',
                    'id': 'field-url',
                    'name': 'url',
                    'class': 'structured-input',
                    'title': 'A URL for this resource or upload a file'
                }
            }
        ]
    },
    {
        'label': 'Name',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'id': 'field-name',
                    'name': 'name',
                    'placeholder': 'Eg. Well Log Headers',
                    'class': 'structured-input',
                    'title': 'A name for this resource'
                }
            }
        ]
    },
    {
        'label': 'Description',
        'label_div_classes': ['description-label-div'],
        'inputs': [
            {
                'tag': 'textarea',
                'attributes': {
                    'rows': '4',
                    'cols': '1',
                    'name': 'description',
                    'placeholder': 'Eg. A description of this resource.',
                    'id': 'description',
                    'class': 'structured_input',
                    'title': 'Describe this resource'
                }
            }
        ]
    },


    {
        'label': 'Distributor',
        'div_classes': ['distributor'],
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Begin typing a distributor\'s name and suggestions will be made. Create one by clicking on the + icon to the right.',
                    'id': 'distributor_fake',
                    'class': 'structured-input',
                    'title': 'The distributor for this resource'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor',
                    'name': 'distributor'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor_name'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor_email'
                }
            },
            {
                'tag': 'div',
                'attributes': {
                    'class': 'distributor-tag retreived-tags'
                }
            }
        ]
    },

    {
        'label': 'Ordering Procedure',
        'label_div_classes': ['description-label-div'],
        'inputs': [
            {
                'tag': 'textarea',
                'attributes': {
                    'rows': '4',
                    'cols': '1',
                    'name': 'ordering_procedure',
                    'class': 'structured_input',
                    'title': 'How can one go about obtaining this resource?',
                    'placeholder': 'Indicate how a person can go about obtaining this resource.'
                }
            }
        ]
    }

];


ngds.form.data_service_form_fields = [
    {
        'label': 'Resource URL',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Eg. http://example.com/myresource.txt or upload a file instead',
                    'id': 'field-url',
                    'name': 'url',
                    'class': 'structured-input',
                    'title': 'A URL for this resource or upload a file'
                }
            }
        ]
    },
    {
        'label': 'Name',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'Eg. Well Log Headers',
                    'id': 'field-name',
                    'name': 'name',
                    'class': 'structured-input',
                    'title': 'A name for this resource'
                }
            }
        ]
    },
    {
        'label': 'Description',
        'label_div_classes': ['description-label-div'],
        'inputs': [
            {
                'tag': 'textarea',
                'attributes': {
                    'rows': '4',
                    'cols': '1',
                    'placeholder': 'Eg. A description of this resource.',
                    'name': 'description',
                    'id': 'description',
                    'class': 'structured_input',
                    'title': 'Describe this resource'
                }
            }
        ]
    },
    {
        'label': 'Distributor',
        'div_classes': ['distributor'],
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'id': 'distributor_fake',
                    'placeholder': 'Begin typing a distributor\'s name and suggestions will be made. Create one by clicking on the + icon to the right.',
                    'class': 'structured-input',
                    'title': 'The distributor for this resource'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor',
                    'name': 'distributor'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor_name'
                }
            },
            {
                'tag': 'input',
                'attributes': {
                    'type': 'hidden',
                    'id': 'distributor_email'
                }
            },
            {
                'tag': 'div',
                'attributes': {
                    'class': 'distributor-tag retreived-tags'
                }
            }
        ]
    },
    {
        'label': 'Protocol',
        'inputs': [
            {
                'tag': 'select',
                'attributes': {
                    'name': 'protocol',
                    'class': 'structured-input',
                    'title': 'What protocol is used to access this resource?'
                }, 'children': [
                {
                    'tag': 'option',
                    'attributes': {
                        'value': 'OGC:WMS',
                        'text': 'WMS'
                    }
                },
                {
                    'tag': 'option',
                    'attributes': {
                        'value': 'OGC:WFS',
                        'text': 'WFS'
                    }
                },
                {
                    'tag': 'option',
                    'attributes': {
                        'value': 'OGC:WCS',
                        'text': 'WCS'
                    }
                },
                {
                    'tag': 'option',
                    'attributes': {
                        'value': 'ESRI',
                        'text': 'ESRI Map Service'
                    }
                },
                {
                    'tag': 'option',
                    'attributes': {
                        'value': 'OGC:CSW',
                        'text': 'CSW'
                    }
                },
                {
                    'tag': 'option',
                    'attributes': {
                        'value': 'OGC:SOS',
                        'text': 'SOS'
                    }
                },
                {
                    'tag': 'option',
                    'attributes': {
                        'value': 'OPeNDAP',
                        'text': 'OPeNDAP'
                    }
                },
                {
                    'tag': 'option',
                    'attributes': {
                        'value': 'other',
                        'text': 'Other'
                    }
                }
            ]
            }
        ]
    },
    {
        'label': 'Layer',
        'inputs': [
            {
                'tag': 'input',
                'attributes': {
                    'type': 'text',
                    'placeholder': 'A layer name that can be used to access this resource using the protocol selected above. Eg. A Geoserver WMS layer.',
                    'name': 'layer',
                    'class': 'structured-input',
                    'title': 'Layer name if any for this resource'
                }
            }
        ]
    }
];


var position_file_uploader = function (selector) {
    if (typeof selector === 'undefined') {
        $(".resource-upload-field").addClass("display-none");
        return;
    }

    var ref = $(selector);
    var r_width = ref.width();
    var file_upload = $(".resource-upload-field");
    file_upload.css("position", "absolute");
    ref.css("width", r_width - 120);
    file_upload.css("left", ref.position().left + ref.width() + 20);
    file_upload.css("top", ref.position().top);
    file_upload.show();
};


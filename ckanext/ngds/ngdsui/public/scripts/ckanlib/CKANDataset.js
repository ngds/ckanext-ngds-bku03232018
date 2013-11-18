/*
 *	@author - Vivek
 *	Exposes a set of functions and objects to work with datasets obtained from ckan.
 */

ngds.ckandataset = function (raw) {

    var me = this;
    this.dataset = raw;

    (function (raw) {
        if (raw === null || typeof raw === 'undefined') {
            throw "Passed in object was null or undefined.";
        }
    })(raw);

    _ckan_dataset = {
        construct: function () {
            var spatial_extra;
            $.each(raw.extras, function (index, val) {
                if (val.key === 'spatial') {
                    spatial_extra = val.value;
                }
            });
            var geojson = $.parseJSON(spatial_extra);
            var description = raw.notes;

            var popup_skeleton = {
                'tag': 'div',
                'children': [
                    {
                        'tag': 'p',
                        'attributes': {
                            'class': 'title'
                        },
                        'children': [
                            {
                                'tag': 'a',
                                'attributes': {
                                    'href': '/dataset/' + raw.name,
                                    'text': raw.title,
                                    'target': '_blank',
                                    'class': 'title'
                                }
                            }
                        ]
                    },
                    {
                        'tag': 'p',
                        'attributes': {
                            'style': 'margin-bottom:3px; margin-top:3px;',
                            'text': (function () {
                                var notes = ngds.util.get_n_chars(description, 150);
                                if (notes !== "") {
                                    return notes;
                                } else {
                                    return "No description.";
                                }
                            })(),
                            'class': 'description'
                        }
                    },
                    {
                        'tag': 'p',
                        'attributes': {
                            'text': raw.num_resources + (function (n) {
                                if (n === 1) {
                                    return " resource";
                                } else {
                                    return " resources";
                                }
                            })(raw.num_resources),
                            'class': 'resources'
                        }
                    }
                ]
            };
            var tag_div = {
                'tag': 'div',
                'attributes': {
                    'class': 'tags'
                },
                'children': [{
                    'tag':'span',
                    'attributes':{
                        'text':'Tags : '
                    }
                }]
            };

            popup_skeleton['children'].push(tag_div);
            var counter = 0;

            for (var i = 0; i < raw.tags.length; i++) {
                if (counter > 5) {
                    break;
                }
                var tag = raw.tags[i];
                var display_name = tag['display_name'];
                if (display_name.length > 25) {
                    continue;
                }
                tag_div['children'].push({
                    'tag': 'div',
                    'attributes': {
                        'class': 'ngds-tag',
                        'text': display_name
                    }
                });
                counter++;
            }

            var popupHTML = ngds.util.dom_element_constructor(popup_skeleton)[0].innerHTML;

            return {
                getGeoJSON: function () { // return the geojson feature associated with the dataset.
                    return geojson;
                },
                map: {
                    getPopupHTML: function () { // return a html popup of a dataset's metadata that is to be displayed when an icon or feature is clicked.
                        return popupHTML;
                    }
                },
                get_feature_type: function () {
                    return geojson;
                }
            }
        }
    }
    return _ckan_dataset.construct();
};

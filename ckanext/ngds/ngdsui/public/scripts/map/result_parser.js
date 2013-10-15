ngds.render_search_results = function (topic, result) { //Subscription - 'Map.result_received'
    var seq = new ngds.util.sequence_generator();
    var count = result['count'];
    var results = result['results'];
    var query = result['query'];
    ngds.log("Received " + count + " results : " + results, results);
    $(".results").remove();
    var clazz = "results visibility-managed";
    ngds.util.state['colorify'] = {
//    Colors for different map search results.
    };

    if (ngds.Map.is_fullscreen() === true) {
        clazz = clazz + " large";
    }

    $(".map-search-results").prepend($("<div/>", {"class": clazz, "id": "results"}));

    var wms_mapping = {

    };

    for (var i = 0; i < results.length; i++) {
        var is_wms_present = false;
        for (var j = 0; j < results[i].resources.length; j++) {
            var resource = results[i].resources[j];
            if (resource.protocol === 'OGC:WMS') {
                is_wms_present = true;
                wms_mapping[results[i].id] = wms_mapping[results[i].id] || ( wms_mapping[results[i].id] = [ ] );
                var layer_name = resource.layer_name;
                wms_mapping[results[i].id].push({
                    'id': resource.id,
                    'url': resource.url.split('?')[0],
                    'layer': layer_name,
                    'name': resource.description
                });
            }
        }

        results[i]["type"] = results[i]["type"][0].toUpperCase() + results[i]["type"].slice(1, results[i]["type"].length);

        var skeleton = {
            'tag': 'div',
            'attributes': {
                'class': 'result result-' + seq.next()
            },
            'children': [
                {
                    'tag': 'p',
                    'attributes': {
                        'class': 'description-wrapper description',
                        'text': ngds.util.get_n_chars(results[i]['title'], 30)
                    },
                    'children': [
                    ]

                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'additional-dataset-info'
                    },
                    'children': [
                        {
                            'tag': 'p',
                            'attributes': {
                                'class': 'type',
                                'text': results[i]['type']
                            }
                        },
                        {
                            'tag': 'p',
                            'attributes': {
                                'class': 'published',
                                'text': "Published " + (function (date_obj) {
                                    var date = date_obj.getUTCDate();
                                    var month = date_obj.getUTCMonth() + 1;
                                    var year = date_obj.getFullYear();
                                    return ([month, date, year].join("/"));
                                })(new Date(results[i]['metadata_created']))
                            }
                        }
                    ]
                },
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'visibility-toggler'
                    },
                    'children': [
                        {
                            'tag': 'button',
                            'attributes': {
//                                'text': "T",
                                'class': 'visible',
                                'data-seq': seq.current(),
                                'title': 'Hide/Show this result on the map'
                            }
                        }
                    ]
                }
            ]
        };

        var dataset_resources = {
            'tag': 'div',
            'attributes': {
                class: 'dataset-resources'
            }
        };

        if (is_wms_present === true) {
            dataset_resources.children = [];
            dataset_resources.children.push({
                'tag': 'button',
                'attributes': {
                    'class': 'wms ngds-slug',
                    'text': 'WMS',
                    'id': results[i].id
                }
            });
        }
        skeleton.children.push(dataset_resources);
        var shaped_loop_scope = ngds.ckandataset(results[i]).get_feature_type()['type'];
        var marker_container = { };
        var alph_seq = seq.current('alph');


        if (shaped_loop_scope === 'Point') {
            marker_container = {
                'tag': 'div',
                'attributes': {
                    'class': 'result-marker-container marker-' + seq.current()
                },
                'priority': 1,
                'children': [
                    {
                        'tag': 'div',
                        'attributes': {
                            'class': 'red-marker'
                        }
                    }
                ]
            };
        }

        else {
            var color = ngds.util.rotate_color();
            ngds.util.state['colorify'][seq.current()] = color;
            marker_container = {
                'tag': 'div',
                'attributes': {
                    'class': 'red-box',
                    'style': "background-color:" + color
                },
                'priority': 1

            };

        }
        ngds.publish('Map.feature_received', {
            'feature': results[i],
            'seq': seq.current(),
            'alph_seq': alph_seq
        });

        skeleton['children'].push(marker_container);

        var dom_node = ngds.util.dom_element_constructor(skeleton);
        $('.results').append(dom_node);

    }

    var reader = ngds.util.dom_element_constructor({
            'tag': 'div',
            'attributes': {
                'class': 'results-text visibility-managed'
            },
            'children': [
                {   'tag': 'div',
                    'attributes': {
                        'class': 'search-tools'
                    },
                    'children': [
                        {
                            'tag': 'div',
                            'attributes': {
                                'class': 'visibility-toggler'
                            },
                            'children': [
                                (function (count) {
                                    if (Number(count) !== 0) {
                                        return {
                                            'tag': 'button',
                                            'attributes': {
                                                'class': 'visible',
                                                'title': 'Hide/Show all results on the map.',
                                                'data-seq': 0
                                            }
                                        }
                                        return;
                                    }
                                })(count)

                            ]

                        },
                        {
                            'tag': 'div',
                            'attributes': {
                                'class': 'clear-map-state'
                            },
                            'children': [
                                {
                                    'tag': 'button',
                                    'attributes': {
                                        'class': 'clear-map-state',
                                        'title': 'Clear search'
                                    }
                                }
                            ]

                        }
                    ]},
                {
                    'tag': 'div',
                    'attributes': {
                        'class': 'reader'
                    },
                    'children': [
                        {
                            'tag': 'p',
                            'attributes': {
                                'text': 'Found ' + count + (function (count) {
                                    if (Number(count) === 1) {
                                        return " result";
                                    }
                                    return " results";
                                }(count)) + (function (count, query) {

                                    if (query !== "") {
                                        if (query !== "" && query.match(/near/) !== null) {
                                            var sp = [];
                                            if (query.match(/ near /) !== null) {
                                                sp = query.split(" near ");
                                            }
                                            else {
                                                sp = query.split("near ");
                                            }
                                            if (sp[0] === "") {
                                                return " near " + sp[1];
                                            }
                                            else {
                                                return " for \"" + sp[0] + "\"" + " near " + sp[1];
                                            }
                                        }
                                        if (query !== "") {
                                            return " for \"" + query + "\""
                                        }
                                    } else {
                                        return "";
                                    }
                                })
                                    (count, query),
                                'class': 'reader'
                            }
                        }
                    ]
                }

            ]
        }
    );
    $('.results').before(reader);

    var inc = inc || (inc = 0);

    $(".wms").click(function (ev) {
        var id = ev.currentTarget.id;
        var label_prefix = '';
        try {
            var label_prefix = $(ev.currentTarget).siblings().find("img").next()[0].textContent + " : ";
        }
        catch (e) {

        }

        for (var k = 0; k < wms_mapping[id].length; k++) {
            var layer_to_add = L.tileLayer.wms(wms_mapping[id][k].url, {
                'layers': wms_mapping[id][k].layer,
                'format': 'image/png',
                'transparent': true,
                'attribution': 'NGDS',
                'tileSize': 128,
                'opacity': 0.9999
            });

            layer_control.addOverlay(layer_to_add, label_prefix + wms_mapping[id][k].name);
            ngds.Map.map.addLayer(layer_to_add);
        }
        ckan.notify("The Web Map Services you requested have been added to the map.","","info");

    });

    (function doc_ready_section() {
        $(document).ready(function () {
            $(".clear-map-state").on("click", function () {
                ngds.util.clear_map_state();
                ngds.Map.get_layer('drawnItems').clearLayers();
                ngds.publish('Map.clear_rect', {});
            });
        });
    })();

    ngds.publish('Map.results_rendered', {

    });
}
;

ngds.subscribe('Map.results_received', ngds.render_search_results);
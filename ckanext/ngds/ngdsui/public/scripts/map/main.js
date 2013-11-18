/*
 *	@author - Vivek Sunder
 *	This is the top-level control module for the NGDS map.
 */


ngds.config = {
    'number_of_rows': 10
};

if (typeof ngds.Search !== 'undefined') {
//    ngds.pager = new ngds.Search();
}


ngds.feature_event_manager = { //A container for state information on event bindings for features.
    /*
     *	Scheme - id -> {
     *					'feature':feature,
     *					'type':'Marker'||'Feature'
     *					'seq_id':seq_id
     *					'mouseover':mouseover_handler,
     *					'mouseout':mouseout_handler,
     *					'add':add_handler
     *					'remove':remove_handler
     *					}
     */
};

ngds.layer_map = { // A mapping table to map ngds result ids(dom) to leaflet ids which we'll use with the feature_event_manager.
    /*
     *	Scheme - ngds_id -> leaflet_id
     *
     *
     */
};

/*
 * 	Publish module
 */


(function setup_control_styles() {
    ngds.subscribe("Map.loaded", function (topic, data) {
        // ngds.Map.top_level_search();
    });
})();

if (typeof ngds.Map !== 'undefined') {
    $(document).ready(function () {
        ngds.Map.initialize();
    });


    ngds.Map.top_level_search = function () {
        ngds.publish('Map.expander.toggle', {

        });
        ngds.pager = new ngds.Search();
        ngds.publish('Map.search_initiated', {

        });
        var geoj = ngds.Map.get_layer('drawnItems');
        var query = $("#map-query").val();
        ngds.util.clear_map_state();
        ngds.pager.go_to({
            'page': 1,
            'action': ngds.ckanlib.package_search,
            'rows': ngds.config['number_of_rows'],
            'q': query
        });

    };
}

(function publish_pager_advance() {
    $("#map-search").click(function () {
        ngds.Map.top_level_search();
    });

    $(".search-results-page-nums").on('click', null, function (ev) {
        var page = ev.target.firstChild.data;
        if (page === "<") {
            page = Number(ngds.Map.cur_page) - 1;
        }
        if (page === ">") {
            page = Number(ngds.Map.cur_page) + 1;
        }
        if (page === 0) {
            page = 1;
        }
        if (page >= ngds.Map.num_pages) {
            page = ngds.Map.num_pages;
        }
        if (typeof page === 'undefined') {
            return;
        }
        ngds.log("Going to page : " + page);
        ngds.publish('page.advance', { 'page': page });
    });
})();


/*
 *	Subscribe module
 */

(function subscribe_page_advance() {
    ngds.subscribe('page.advance', function (msg, data) {
        ngds.feature_ngds_id_mapping = {
            // Clearing the state table.
        };
        ngds.util.clear_map_state();
        ngds.Map.zoom_handler.clear_listeners();
        ngds.pager.go_to({
            'page': data['page'],
            'action': ngds.ckanlib.package_search,
            'rows': 10
        });
    });
})();


(function subscribe_data_loading() {
    ngds.subscribe('data-loading', function (msg, data) {
        ngds.publish('Map.results_hide', {});
        ngds.Map.map.fireEvent('dataloading');
    });
})();

(function subscribe_data_loaded() {
    ngds.subscribe('data-loaded', function (msg, data) {
        ngds.Map.map.fireEvent('dataload');
    })
})();


if (typeof ngds.Map !== 'undefined') {
    $(document).ready(function () {
        ngds.Map.map.on('draw:rectangle-created', function (e) {
            ngds.Map.clear_layer('drawnItems');
            ngds.Map.add_to_layer([e.rect], 'drawnItems');
            ngds.publish("Map.area_selected", {
                'type': 'rectangle',
                'feature': e
            });
        });

        ngds.Map.map.on('draw:poly-created', function (e) {
            ngds.Map.clear_layer('drawnItems');
            ngds.Map.add_to_layer([e.poly], 'drawnItems');

            ngds.publish("Map.area_selected", {
                'type': 'polygon',
                'feature': e
            });
        });
    });

}


(function subscribe_feature_received() {
    ngds.subscribe('Map.feature_received', function (topic, data) {
        var feature = ngds.Map.add_raw_result_to_geojson_layer(data['feature'], {'seq': data['seq'], 'alph_seq': data['alph_seq']});
        ngds.publish('Map.feature_processed', {'feature': feature, 'seq': data['seq']});
    });

    $('.map-search-results').on('mouseover', null, function (ev) {
        var node = '';
        if (typeof ev.srcElement === 'undefined') {
            node = ev.target;
        }
        else {
            node = ev.srcElement;
        }
        var tag_index = ngds.util.node_matcher(node, /result-\d.*/);
        if (tag_index === null) {
            return;
        }

        var feature = { 'layer': ngds.layer_map[tag_index] };
        ngds.publish('Layer.mouseover', {
            'Layer': feature,
            'tag_index': tag_index
        });

    });

    $('.map-search-results').on('mouseout', null, function (ev) {
        var node = '';
        if (typeof ev.srcElement === 'undefined') {
            node = ev.target;
        }
        else {
            node = ev.srcElement;
        }
        var tag_index = ngds.util.node_matcher(node, /result-\d.*/);

        if (tag_index === null) {
            return;
        }

        var feature = { 'layer': ngds.layer_map[tag_index] };

        ngds.publish('Layer.mouseout', {
            'Layer': feature,
            'tag_index': tag_index
        });

    });

    $('.map-search-results').on('click', ".result", function (ev) {
        console.log($(this).attr("class"));
        var node = '';
        console.log("here");
        if (typeof ev.srcElement === 'undefined') {
            node = ev.target;
        }
        else {
            node = ev.srcElement;
        }
        var tag_index = ngds.util.node_matcher(node, /result-\d.*/);

        if (tag_index === null || typeof tag_index === 'undefined') {
            return;
        }

        ngds.util.reset_result_styles();
        var feature = { 'layer': ngds.layer_map[tag_index] };
        ngds.publish('Layer.click', {
            'Layer': feature,
            'tag_index': tag_index
        });

    });

    $('.map-search-results').on('click', ".visibility-toggler button", function (ev) {
        ev.stopPropagation();
        var id = Number($(ev.target).attr('data-seq'));
        ngds.Map.visibility_mgr.process(id);
    });


    ngds.Map.visibility_mgr = {
        'init': function () {
            var me = this;

            ngds.subscribe('Map.feature_processed', function (topic, data) {
                var show_op = function (feature) {
                    ngds.Map.map.addLayer(feature);
                };

                var hide_op = function (feature) {
                    ngds.Map.map.removeLayer(feature);
                }

                me.features[data['seq']] = me.construct_individual_mgr(data['feature'], data['seq'], show_op, hide_op);
            });

            var fshow = function (feature) {
                for (var i in me.features) {
                    if (Number(i) !== 0) {
                        me.features[i].show();
                    }
                }
                $("button[data-seq='0']").removeClass("toggled");

            };

            var fhide = function (feature) {
                for (var i in me.features) {
                    if (Number(i) !== 0) {
                        me.features[i].hide();
                    }
                }
                $("button[data-seq='0']").addClass("toggled");
            };

            var family_mgr = me.construct_individual_mgr(null, 0, fshow, fhide);
            me.features[0] = family_mgr;
        },
        'process': function (id) {
            var me = this;
            if (me.features[id].is_hidden()) {
                me.features[id].show();
            }
            else {
                me.features[id].hide()
            }
        },
        'clearMgrs': function () {
            var family_mgr = this.features[0];
            this.features = [family_mgr];
        },
        'features': {},
        'construct_individual_mgr': function (feature, id, show_op, hide_op) {
            var button = $("button[data-seq=" + id + "]");
            var feature = feature;
            var hidden = false;

            var ob = {
                'show': function () {
                    show_op(feature);
                    button.removeClass("toggled");
                    hidden = false;
                },
                'hide': function () {
                    hide_op(feature);
                    button.addClass("toggled");
                    hidden = true;
                },
                'is_hidden': function () {
                    return hidden;
                }
            };

            return ob;
        }
    };

    ngds.Map.visibility_mgr.init();


})();

(function setup_styler_for_features() {
    /*
     *	This is really where all the events on features are bound regardless of how they are initiated. No event listeners should
     *	directly be bound on features except through
     *	here. This lets us use our own events as a forwarding mechanism that lead to these functions below.
     *
     *
     */
    ngds.subscribe('Layer.mouseover', function (topic, data) {
        if (typeof data['Layer'] === 'undefined' || typeof data['Layer'].layer === 'undefined') {
            return;
        }
        var is_active = data['Layer'].layer.is_active || null;
        if (is_active === null || is_active === false) {
            ngds.util.apply_feature_hover_styles(data['Layer'].layer, data['tag_index'])
        }
    });

    ngds.subscribe('Layer.mouseout', function (topic, data) {
        if (typeof data['Layer'] === 'undefined' || typeof data['Layer'].layer === 'undefined') {
            return;
        }
        var is_active = data['Layer'].layer.is_active || null;
        if (is_active === null || is_active === false) {
            ngds.util.apply_feature_default_styles(data['Layer'].layer, data['tag_index']);
        }
    });

    ngds.subscribe('Layer.click', function (topic, data) {
        if (typeof data['Layer'] === 'undefined' || typeof data['Layer'].layer === 'undefined') {
            return;
        }
        ngds.util.reset_result_styles();
        for (var l in ngds.layer_map) {
            ngds.util.apply_feature_default_styles(ngds.layer_map[l], l);
            if (ngds.layer_map[l]._leaflet_id === data['Layer'].layer._leaflet_id) {
                ngds.layer_map[l].is_active = true;
            }
            else {
                ngds.layer_map[l].is_active = false;
            }
        }
        var latlngs = data['Layer'].layer._latlng || data['Layer'].layer._latlngs;

        var approximate_center = (function (latlngs) {
            if (typeof latlngs === 'object' && typeof latlngs[0] === 'undefined') { // Then it's a point
                return latlngs;
            }
            var minx = ngds.Map.utils.get_bound(latlngs, 'lat', 'min');
            var maxx = ngds.Map.utils.get_bound(latlngs, 'lat', 'max');
            var miny = ngds.Map.utils.get_bound(latlngs, 'lng', 'min');
            var maxy = ngds.Map.utils.get_bound(latlngs, 'lng', 'max');

            return {
                'lat': (minx + maxx) / 2,
                'lng': (miny + maxy) / 2
            }

        })(latlngs);

        ngds.Map.map.panTo(approximate_center);
        try {
            data['Layer'].layer.openPopup();
        }
        catch (e) {

        }
        ngds.util.apply_feature_active_styles(data['Layer'], data['tag_index']);
    });

    ngds.subscribe('Layer.add', function (topic, data) {

    });

    ngds.subscribe('Layer.remove', function (topic, data) {

    });
})();

(function setup_events_for_map_features() {
    // Ref : ngds.feature_event_manager
    // Ref : ngds.feature_ngds_id_mapping

    ngds.subscribe('Map.add_feature', function (topic, data) {
        var feature = data['feature'];
        ngds.layer_map[data['seq_id']] = feature;

        ngds.util.apply_feature_default_styles(feature, data['seq_id']);
        ngds.feature_event_manager[feature._leaflet_id] = {
            'Layer': feature,
            'seq_id': data['seq_id']
        };

        ngds.publish('Map.layer_added', {});

        feature.on('mouseover', function (feature) {

            ngds.publish('Layer.mouseover', {
                'Layer': feature,
                'tag_index': data['seq_id']
            });
        });

        feature.on('mouseout', function (feature) {
            ngds.publish('Layer.mouseout', {
                'Layer': feature,
                'tag_index': data['seq_id']
            });
        });

        feature.on('click', function (feature) {
            ngds.publish('Layer.click', {
                'Layer': feature,
                'tag_index': data['seq_id']
            });
        });

    });
})();


ngds.subscribe('Map.results_rendered', function (topic, data) {
//    TODO - This is a good place to put in layer sorting.
    var bounds = ngds.util.state['map_features'].map(function (item) {
        var b = item.getBounds();
        var sw = b.getSouthWest();
        var ne = b.getNorthEast();
        return new L.LatLngBounds(sw, ne);
    });

    for (var i = 0; i < bounds.length; i++) {
        bounds[i].extend(bounds[i - 1]);
    }

    ngds.Map.map.fitBounds(bounds[bounds.length - 1]);
    $(".visibility-managed").show();
    $(".results").jScrollPane({contentWidth: '0px', hideFocus: true});
});

ngds.subscribe('Map.results_hide', function (topic, data) {
    $(".visibility-managed").hide();
});

$(document).ready(function () {
    var state = false;
    $(".map-expander").on("click", function () {

        if (state === false) {
            $(".visibility-managed").hide();
            state = true;
        }
        else {
            $(".visibility-managed").show();
            state = false;
        }

    });
});

(function () {
    ngds.subscribe('Map.size_changed', function (topic, data) {
        if (data['fullscreen'] === true) {
            ngds.Map.state['map-search-results-left'] = $(".map-search-results").css('left');
            ngds.Map.state['map-search-results-top'] = $(".map-search-results").css('top');
            ngds.Map.state['map-search-left'] = $(".map-search").css('left');
            ngds.Map.state['map-search-top'] = $(".map-search").css('top');

            $(".map-search").css({'left': '10px', 'position': 'fixed'});
            $(".map-search-results").css({'left': '10px', 'position': 'fixed'});
        }
        else {
            $(".map-search").css({'left': ngds.Map.state['map-search-left'], 'top': ngds.Map.state['map-search-top'], 'position': 'absolute'});
            $(".map-search-results").css({'left': ngds.Map.state['map-search-results-left'], 'top': ngds.Map.state['map-search-results-top'], 'position': 'absolute'});
        }
    });
})();

$(document).ready(function () {
    ngds.Map.map.on('zoomend', ngds.util.make_prominent);

    $(".map-search").on("click", ".wms", function (ev) {
        ev.preventDefault();
        ckan.notify("Please wait while the Web Map Services you requested are fetched", "", "info");
        var package_id = $(this).attr("data-package-id");
        ngds.ckanlib.get_wms_urls(package_id, function (wms_mappings) {
            for (var i = 0; i < wms_mappings.length; i++) {
                var mapping = wms_mappings[i];
                var wms_params = {
                    'layers': mapping['layer'],
                    'format': 'image/png',
                    'transparent': true,
                    'attribution': 'NGDS',
                    'tileSize': 128,
                    'opacity': 0.9999,
                    'version': '1.1.1'
                };

                var layer = L.tileLayer.wms(mapping['url'], wms_params);

                ngds.Map.layer_control.addOverlay(layer, mapping['layer']);
                ngds.Map.map.addLayer(layer);
            }
            ckan.notify("The Web Map Services you requested have been added to the map.", "", "success");

        });
        return false;
    });

});

ngds.subscribe('Map.layer_added', function () {
    ngds.util.make_prominent();
});

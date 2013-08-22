/*
 *	@author - Vivek Sunder
 *	This is the top-level control module for the NGDS map.
 */


ngds.config = {
    'number_of_rows': 10
};

if (typeof ngds.Search !== 'undefined') {
    ngds.pager = new ngds.Search();
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
    ngds.Map.initialize();

    ngds.Map.top_level_search = function () {
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
        ngds.publish('Map.expander.toggle', {
            'no_toggle': true
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


if (typeof ngds.Map !== 'undefined') {

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
}


(function subscribe_feature_received() {
    ngds.subscribe('Map.feature_received', function (topic, data) {
        ngds.Map.add_raw_result_to_geojson_layer(data['feature'], {'seq': data['seq'], 'alph_seq': data['alph_seq']});
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

    $('.map-search-results').on('click', null, function (ev) {
        var node = '';
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
})();

(function setup_styler_for_features() {
    /*
     *	This is really where all the events on features are bound regardless of how they are initiated. No events should directly be bound on features except through
     *	here. This lets us use our own events as a forwarding mechanism that lead to these functions below.
     *
     *
     */
    ngds.subscribe('Layer.mouseover', function (topic, data) {
        var is_active = data['Layer'].layer.is_active || null;
        if (is_active === null || is_active === false) {
            ngds.util.apply_feature_hover_styles(data['Layer'].layer, data['tag_index'])
        }
    });

    ngds.subscribe('Layer.mouseout', function (topic, data) {
        var is_active = data['Layer'].layer.is_active || null;
        if (is_active === null || is_active === false) {
            ngds.util.apply_feature_default_styles(data['Layer'].layer, data['tag_index']);
        }
    });

    ngds.subscribe('Layer.click', function (topic, data) {
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
        data['Layer'].layer.openPopup();
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


(function publish_map_search_results_expanded() {
    $(".map-expander").on('click', null, function () {
        ngds.publish("Map.expander.toggle", {
            // Empty payload
        });
    });
})();

(function subscribe_map_search_results_expanded() {
    var operation = 'contract';
    ngds.subscribe('Map.expander.toggle', function (topic, data) {
        var no_toggle = data['no_toggle'] || false;

        if (operation === 'contract' && no_toggle === false) {
            operation = 'expand';
            $(".results").hide();
            $(".search-results-pagination").hide();
            $(".search-results-pagination").addClass("no-padding");
            $(".results-text").hide();
            $(".map-expander").css("top", "80px");
        }
        else {
            operation = 'contract';
            $(".results").show();
            $(".results-text").show();
            $(".search-results-pagination").show();
            $(".search-results-pagination").removeClass("no-padding");
            $(".map-expander").css("top", "0px");
        }
    });
})();

ngds.publish('Map.expander.toggle', {
    // Empty payload
});


(function () {
    if (typeof ngds.Map !== 'undefined') {
        ngds.Map.map.on('enterFullscreen', function () {
            ngds.publish("Map.size_changed", {
                'fullscreen': true
            });
        });

        ngds.Map.map.on('exitFullscreen', function () {
            ngds.publish("Map.size_changed", {
                'fullscreen': false
            });
        });
    }

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

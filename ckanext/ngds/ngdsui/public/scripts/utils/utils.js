ngds.util = { };

ngds.util.dom_element_constructor = function (payload) {
    var parent = $('<' + payload['tag'] + '/>', payload['attributes']);
    if (typeof payload['children'] !== 'undefined') {
        for (var i = 0; i < payload['children'].length; i++) {
            if (typeof payload['children'][i] === 'undefined') {
                continue;
            }
            if (payload['children'][i]['priority'] === 1) {
                parent.prepend(ngds.util.dom_element_constructor(payload['children'][i]));
            }
            else {
                parent.append(ngds.util.dom_element_constructor(payload['children'][i]));
            }
        }
    }
    return parent;
};

ngds.util.sequence_generator = function () {
    var begin = 0;
    var begin_alph = 97;
    return {
        'next': function () {
            return begin = begin + 1;
        },
        'current': function (alph_switch) {
            if (typeof alph_switch !== 'undefined' && alph_switch === 'alph') {
                var marker_ch = String.fromCharCode(begin_alph).toUpperCase();
                begin_alph = begin_alph + 1;
                return marker_ch;
            }
            return begin;
        }
    }
};

ngds.util.tick = function () {
    var hand = 0;

    var next = function () {
        return ++hand;
    };

    var current = function () {
        return hand;
    };
    return {
        'next': next,
        'current': current
    };
};

ngds.util.node_matcher = function (node, match_exp) {
    if (node.className.match(match_exp) !== null) {
        return node.className.substring(node.className.indexOf("-") + 1, node.length);
    }

    var parents = $(node).parents();
    for (var i = 0; i < parents.length; i++) {
        if (parents[i].className.match(match_exp) !== null) {
            var clazz = parents[i].className;
            return clazz.substring(clazz.indexOf("-") + 1, clazz.length);
        }
    }
    return null;
};

ngds.util.apply_feature_hover_styles = function (feature, tag_index) {
    var type = feature.feature.geometry.type;
    if (type === 'Point') {
        var marker_tag = $('.lmarker-' + tag_index);
        if (marker_tag.length > 0) {
            marker_tag.css("width", "30px");
            marker_tag.css("height", "45px");
            var span_elem = $('.lmarker-' + tag_index).next();
            span_elem.css("font-size", "14pt");
            span_elem.css("margin-left", "2px");
        }
    }
    else {
        feature.setStyle({weight: 2, color: "#d54799", fillColor: ngds.util.state['colorify'][tag_index]});
//        ngds.util.svg_crispify_post_process();
    }
};


ngds.util.apply_feature_default_styles = function (feature, tag_index) {
    var type = feature.feature.geometry.type;
    if (type === 'Point') {
        var marker_tag = $('.lmarker-' + tag_index);
        marker_tag.attr("src", "/images/marker.png")
        marker_tag.css("width", "25px");
        marker_tag.css("height", "41px");
        var span_elem = $('.lmarker-' + tag_index).next();
        span_elem.css("font-size", "12.5pt");
        span_elem.css("margin-left", "0px");
    }
    else {
        feature.setStyle({weight: 1, color: ngds.util.state['colorify'][tag_index], fillColor: ngds.util.state['colorify'][tag_index], dashArray: "", opacity: 0.7, fillOpacity: 0.5});
//        ngds.util.svg_crispify_post_process();
    }
};

ngds.util.apply_feature_active_styles = function (feature, tag_index) {
    var type = feature.layer.feature.geometry.type;
//    $('.result-' + tag_index).css('background-color', '#DDE9ED');
    $(".result-" + tag_index).addClass("selected");
    if (type === 'Point') {
        $('.lmarker-' + tag_index).attr("src", "/images/marker-red.png");
    }
    else {
        feature.layer.setStyle({weight: 3, color: "red", fillColor: "red", fillOpacity: 0.2, opacity: 1, dashArray: ""});
//        ngds.util.svg_crispify_post_process();
    }
};

ngds.util.reset_result_styles = function () {
//    $('.result').css('background-color', '#efefef');
    $(".result").removeClass("selected");
};

ngds.util.svg_crispify_post_process = function () {
    $("#map-container g").attr("shape-rendering", "crispEdges");
};

ngds.util.clear_map_state = function () {
    $("#jspContainer").remove();
    $(".result").remove();
    $(".reader").remove();
    $(".search-results-page-nums").empty();
    $(".results-text").remove();
    ngds.Map.zoom_handler.clear_listeners();
    ngds.layer_map = {};
    ngds.Map.clear_layer('geojson');
    ngds.util.state['map_features'] = []
    for (var prom_index in ngds.util.state['prominence']) {
        ngds.Map.map.removeLayer(ngds.util.state['prominence'][prom_index]);
    }
    ngds.util.state['prominence'] = {};

};

ngds.util.get_n_chars = function (words_str, num_chars) {
    if (typeof words_str === "undefined" || words_str === "") {
        return "";
    }
    if (words_str.length <= num_chars) {
        return words_str;
    }
    var spliced = words_str.slice(0, num_chars - 4);
    while (spliced[spliced.length - 1] === '.' || spliced[spliced.length - 1] === ' ') {
        spliced = spliced.slice(0, spliced.length - 1);
    }
    return spliced + " ...";
};

ngds.util.deep_joiner = function (data, property, separator) {
    var final_list = [ ];
    for (var i = 0; i < data.length; i++) {
        final_list.push(data[i][property]);
    }

    return final_list.join(separator) || "None";
};

ngds.util.replace_content = function (container, content) {
    $(container).empty();
    container.append(content);
};

ngds.util.parse_raw_json = function (raw) {
    var parsed_json = raw.replace(/&#34;/g, "\"").replace(/&#39;/g, "\"").replace(/u\"/g, "\"").replace(/null/g, "\"\"");
    x = JSON.parse(parsed_json);
    return x;
};

ngds.util.state = {

};

ngds.util.rotate_color = function () {
    var colors = ["#f26a50", "#99ca57", "#a299c8", "#b74692", "#fcd53c", "#414686", "#0090A8", "#f6879f", "#177abe", "#4a3134", "#bd0331"];

    if (typeof ngds.util.state['rotate_color'] === "undefined" || ngds.util.state === null) {
        ngds.util.state['rotate_color'] = {};
        ngds.util.state['rotate_color']['index'] = -1;
    }

    if (ngds.util.state['rotate_color']['index'] === colors.length - 1) {
        ngds.util.state['rotate_color']['index'] = -1;
    }

    ngds.util.state['rotate_color']['index'] = ngds.util.state['rotate_color']['index'] + 1;

    return colors[ngds.util.state['rotate_color']['index']];
};

ngds.util.make_prominent = function () {

    if (typeof ngds.util.state['prominence'] === 'undefined') {
        ngds.util.state['prominence'] = {};
    }
    var prominence_state = ngds.util.state['prominence'];

    for (var layer_index in ngds.layer_map) {
        if (typeof prominence_state[layer_index] === 'undefined') {
            var layer = ngds.layer_map[layer_index];
            var layer_bounds = layer.getBounds();
            var prominence = ngds.util.compute_prominence(layer);

            if (prominence > 24000) {
                var center = new L.LatLng((layer_bounds._northEast.lat + layer_bounds._southWest.lat) / 2, (layer_bounds._northEast.lng + layer_bounds._southWest.lng) / 2);
                var circleMarker = new L.CircleMarker(center, {weight: 3, color: "green", fillColor: "green", fillOpacity: 0, opacity: 1, dashArray: "5,5"});
                circleMarker.setRadius(20);
                ngds.Map.map.addLayer(circleMarker);
                prominence_state[layer_index] = circleMarker;
            }

        }
        else {
            var layer = ngds.layer_map[layer_index];
            if (ngds.util.compute_prominence(layer) < 24000) {
                ngds.Map.map.removeLayer(prominence_state[layer_index]);
                delete prominence_state[layer_index];
            }

        }

    }
};

ngds.util.compute_prominence = function (layer) {
    var map_bounds = ngds.Map.map.getBounds();
    var map_area = (map_bounds._northEast.lat - map_bounds._southWest.lat) * (map_bounds._northEast.lng - map_bounds._southWest.lng );
    var layer_bounds = layer.getBounds();
    var layer_area = (layer_bounds._northEast.lat - layer_bounds._southWest.lat) * (layer_bounds._northEast.lng - layer_bounds._southWest.lng );
    return (map_area / layer_area);

};
ngds.util = { };

ngds.util.dom_element_constructor = function (payload) {
    var parent = $('<' + payload['tag'] + '/>', payload['attributes']);
    if (typeof payload['children'] !== 'undefined') {
        for (var i = 0; i < payload['children'].length; i++) {
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
        feature.setStyle({weight: 2, color: "#d54799"});
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
        feature.setStyle({weight: 1, color: "black", fillColor:"grey", dashArray:"", opacity:1, fillOpacity:0.2});
    }
};

ngds.util.apply_feature_active_styles = function (feature, tag_index) {
    var type = feature.layer.feature.geometry.type;
    $('.result-' + tag_index).css('background-color', '#dadada');
    if (type === 'Point') {
        $('.lmarker-' + tag_index).attr("src", "/images/marker-red.png");
    }
    else {
        feature.layer.setStyle({weight: 3, color: "red", fillColor:"red", fillOpacity:0.2, opacity:1, dashArray:"5, 10"});
    }
};

ngds.util.reset_result_styles = function () {
    $('.result').css('background-color', '#fff');
};

ngds.util.clear_map_state = function () {
    $("#jspContainer").remove();
    $(".result").remove();
    $(".reader").remove();
    $(".search-results-page-nums").empty();
    $(".results-text").remove();
    ngds.Map.zoom_handler.clear_listeners();
    ngds.Map.clear_layer('geojson');
};

ngds.util.get_n_chars = function (words_str, num_chars) {
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
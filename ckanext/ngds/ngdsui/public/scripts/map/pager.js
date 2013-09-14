ngds.util.state['drawn_rectangle'] = (function () {
    var bbox = null;
    var southWest = new L.LatLng(-90, -180),
        northEast = new L.LatLng(90, 180),
        bounds = new L.LatLngBounds(southWest, northEast);
    var default_bbox = new ngds.Map.BoundingBox();
    default_bbox.store_raw(bounds);

    ngds.subscribe('Map.area_selected', function (msg, data) {
        if (data['type'] === 'rectangle') {
            bbox = new ngds.Map.BoundingBox();
            bbox.construct_from_leaflet_shape(data['feature']['rect']);
            package_extras = {
                'ext_bbox': bbox.get_bbox_array().join(',')
            };
        }
    });

    ngds.subscribe('Map.clear_rect', function (msg, data) {
        bbox = null;
    });

    var get_default_rectangle = function () {
        return default_bbox.get_bbox_array().join(',');
    };

    var get_rectangle = function () {
        if (bbox === null) {
            return get_default_rectangle();
        }
        var val = bbox.get_bbox_array().join(',');
        return val;
    };

    return {
        'get': get_rectangle
    }
})();


ngds.Search = function () {
    var package_extras = '';
    var me = this;
    var pager_div = $(".search-results-page-nums");

    var go_to = function (params, callback) {
        var q = '';
        var rows = params['rows'];
        var action = params['action'];
        var page = params['page'];
        ngds.Map.cur_page = page;
        var start = (page - 1) * rows;

        if (typeof params['q'] === 'undefined') {
            q = me._q;
        }
        else {
            me._q = params['q'];
            q = me._q;
        }
        ngds.Map.current_query = me._q;
        ngds.log("Searching for term : " + q + ", rows : " + rows + ", page : " + page + " start : " + start);
        console.log(package_extras);

        var package_extras = {
            'ext_bbox': ngds.util.state['drawn_rectangle'].get()
        };

//        if (package_extras === "") {
//            var southWest = new L.LatLng(-90, -180),
//                northEast = new L.LatLng(90, 180),
//                bounds = new L.LatLngBounds(southWest, northEast);
//            bbox = new ngds.Map.BoundingBox();
//            bbox.store_raw(bounds);
//            package_extras = {
//                'ext_bbox': bbox.get_bbox_array().join(',')
//            };
//        }

//        console.log(action);
//        console.log(package_extras);

        action({
            'rows': rows,
            'q': q,
            'start': start,
            'extras': package_extras
        }, function (response) {
            ngds.publish('Map.results_received', {
                'results': response.result.results,
                'query': ngds.Map.current_query,
                'count': response.result.count
            });
            var num_pages = ngds.Map.num_pages = Math.ceil(response.result.count / rows);
            var pager_div = $(".search-results-page-nums");
            var cur_page = Number(ngds.Map.cur_page);
            var dots_added = false;

            pager_div.append(ngds.util.dom_element_constructor({
                'tag': 'a',
                'attributes': {
                    'class': 'page-num',
                    'text': '<'
                }
            }));

            for (var i = 1; i < num_pages + 1; i++) {
                if ((i !== cur_page && i !== 1 && i !== num_pages) && (i < cur_page - 1 || i > cur_page + 1)) {
                    if (dots_added === false)
                        pager_div.append(ngds.util.dom_element_constructor({
                            'tag': 'a',
                            'attributes': {
                                'class': 'page-num',
                                'text': '...'
                            }
                        }));
                    dots_added = true;
                    continue;
                }
                var a_to_append = ngds.util.dom_element_constructor({
                    'tag': 'a',
                    'attributes': {
                        'class': 'page-num',
                        'text': i
                    }
                });

                pager_div.append(a_to_append);

                if (parseInt(ngds.Map.cur_page) === i) {
                    var a = a_to_append;
                    a.addClass("page-active");
                }
            }
            pager_div.append(ngds.util.dom_element_constructor({
                'tag': 'a',
                'attributes': {
                    'class': 'page-num',
                    'text': '>'
                }
            }));
        });
    };

    return {
        'go_to': go_to
    }
};
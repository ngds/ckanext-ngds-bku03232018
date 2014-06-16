/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/*
 *	@author - Vivek
 *	A set of functions to make ajax calls to the CKAN API.
 */

ngds.ckanlib = {
    /*
     *	Perform a POST to get the list of packages that are contained in a bounding rectangle.
     *	Inputs : minx, miny, maxx, maxy and a callback function.
     */
    dataset_geo: function (bbox, callback) {
        var url_pre = '/api/2/search/dataset/geo?bbox=';

        // Validate inputs.
        if (!typeof bbox === 'object') {
            throw "Parameter bbox : Expected a BoundingBox Object.";
        }

        $.each(bbox.get_bbox_array(), function (index, v) {
            (function (v) { // Throw an error if we didn't receive all the required parameters.
                if (v === null || typeof v === 'undefined') {
                    throw "Missing parameter : Expected minx,miny,maxx,maxy.";
                }
            })(v);
        });

        (function () {
            if (typeof callback !== 'function') {
                throw "Missing parameter : Expected callback function.";
            }
        })();

        // Construct the url for the GET call.
        var url = url_pre + bbox.get_bbox_array().join(',');

        // Make the GET call and perform the callback.
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'JSON',
            success: function (response) {
                return callback(response);
            }
        });

    },
    /*
     *	Perform a call to get the list of packages that are within a polygonal region.
     *	Inputs : An array of coordinate pairs that correspond to the polygonal region and a callback function.
     */
    dataset_poly_geo: function (poly_params, callback) {

        (function () {
            if (poly_params === null || typeof poly_params === 'undefined') {
                throw "Missing parameter : Expected an array of coordinates representing a polygon.";
            }
            if (typeof callback !== 'function') {
                throw "Missing parameter : Expected callback function.";
            }
        })();

        if (poly_params.length === 0) {
            return;
        }

        var url = '/poly';
        var data = {
            'data': JSON.stringify({
                'poly': poly_params
            })
        };
        var type = 'POST';

        $.ajax({
            url: url,
            data: data,
            success: function (response) {
                return callback(response);
            }
        });
    },
    /*
     *	Query a package by its id.
     *	Input : A package id and a callback.
     */
    package_show: function (package_id, callback) {
//        ngds.publish("data-loading", {});

        // Validate input.
        (function () {
            if (package_id === null || typeof package_id === 'undefined') {
                throw "Missing parameter : Expected package_id.";
            }
            if (typeof callback !== 'function') {
                throw "Missing parameter : Expected callback function.";
            }
        })();

        // URl and data required for the POST call.
        var url = '/api/action/package_show';
        var data = JSON.stringify({
            id: package_id
        });

        // Make the POST call and perform the callback.
        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'JSON',
            data: data,
            success: function (response) {
//                ngds.publish("data-loaded", {});
                return callback(response);
            }
        });
    },
    /*
     *	Do a package search query.
     *	Input : Parameter object with keys that make sense. Currently the only one that makes sense is 'extras'. And a callback.
     */
    package_search: function (parameter_obj, callback) {
        // Validate inputs.
        (function () {
            if (parameter_obj !== null && typeof parameter_obj !== 'undefined') {
                // The parameter object is optional, but if supplied, must be an object.
                if (typeof parameter_obj === 'undefined') {
                    throw "Expected an object as the second parameter.";
                }
            }

            if (typeof callback !== 'function') {
                throw "Expected a callback function.";
            }
        })();

        var location = null;

        var proximity_matched = false;
        var tokens = parameter_obj['q'].split(" ");
        for (var i = 0; i < tokens.length; i++) {
            var space_stripped = tokens[i].replace(" ", "").replace(" ", "");
            if (space_stripped === "near" || space_stripped === "in") {
                proximity_matched = true;
                break;
            }
        }

        if (proximity_matched === true) {
            location = tokens.splice(i + 1, tokens.length);
            var query = tokens.splice(0, i).join(" ");
            parameter_obj['q'] = query;
            var osm_provider = new L.GeoSearch.Provider.OpenStreetMap();
            var g_url = osm_provider.GetServiceUrl(location);
            ngds.publish("data-loading", {});
            $.getJSON(g_url, function (data) {
                    var transform_neg = ngds.ckanlib.transform_neg;
                    var transform_pos = ngds.ckanlib.transform_pos;

                    var t0 = Math.min(transform_neg(data[0]['boundingbox'][0]), transform_pos(data[0]['boundingbox'][1]));
                    var t1 = Math.max(transform_neg(data[0]['boundingbox'][0]), transform_pos(data[0]['boundingbox'][1]));
                    var t2 = Math.min(transform_neg(data[0]['boundingbox'][2]), transform_pos(data[0]['boundingbox'][3]));
                    var t3 = Math.max(transform_neg(data[0]['boundingbox'][2]), transform_pos(data[0]['boundingbox'][3]));

                    var transformed_bbox = t2 + "," +
                        t0 + "," +
                        t3 + "," +
                        t1;

                    new L.rectangle([
                        [t0, t2],
                        [t1, t3]
                    ], {color: 'green', dashArray: "5,5", weight: "3", opacity: 1, fillOpacity: 0}).addTo(ngds.Map.geoJSONLayer);
                    parameter_obj['extras']['ext_bbox'] = transformed_bbox;
                    ngds.ckanlib.package_search(parameter_obj, function (response) {
                            ngds.publish("data-loaded", {});
                            return callback(response);
                        }

                    )
                    ;
                }
            )
            ;
            return;
        }
        ngds.publish("data-loading", {});
        var url = '/api/action/get_better_package_info';
        var type = 'POST';

        var data = { 'sort': '' };

        for (key in parameter_obj) {
            if (parameter_obj[key] !== null && typeof parameter_obj[key] !== 'undefined') {
                data[key] = parameter_obj[key];
            }
        }

        $.ajax({
            url: url,
            type: type,
            dataType: 'JSON',
            data: JSON.stringify(data),
            success: function (response) {
                ngds.publish("data-loaded", {});
                return callback(response);
            }
        });

    },
    transform_neg: function (coordinate) {
        var c = Number(coordinate);
        var t = 0;
        if (c < 0) {
            t = -(Math.abs(c) + 2);
        }
        else {
            t = c - 2;
        }
        return t;
    },
    transform_pos: function (coordinate) {
        var c = Number(coordinate);
        var t = 0;
        if (c < 0) {
            t = -(Math.abs(c) - 2);
        }
        else {
            t = c + 2;
        }
        return t;
    },
    get_responsible_party: function (id, callback) {
        (function () {
            if (id === null || typeof id === 'undefined') {
                throw "Expected valid id";
            }
            if (typeof callback !== 'function') {
                throw "Expected callback function";
            }
        })();

        var url = '/api/action/additional_metadata';
        var model = "ResponsibleParty";
        var process = "read";
        var data = {
            "model": model,
            "process": process,
            "data": {
                "id": id
            }
        };
        $.ajax({
            url: url,
            data: data,
            success: function (response) {
                return callback(response);
            }
        });
    },
    datastore_search: function (resource_id, callback) {
        if (typeof resource_id === 'undefined' || resource_id === null) {
            throw "Expected resource id. Got nothing.";
        }
        if (typeof callback !== 'function' || callback === null) {
            throw "Expected callback function. Got nothing.";
        }

        $.ajax({
            'url': '/api/3/action/datastore_search',
            // Is there any particular reason why we would assume that this url should not be local?
            'data': {
                'resource_id': resource_id
            },
            'dataType': 'jsonp',
            'success': function (response) {
                return callback(response);
            }
        })
    },
    'publish_to_geoserver': function (params) {
        $.ajax({
            'url': params['action'],
            'type': 'POST',
            'data': JSON.stringify({
                gs_lyr_name: params['layer_name'],
                resource_id: params['resource_id'],
                package_id: params['package_id'],
                col_geography: params['col_geo'],
                col_latitude: params['col_lat'],
                col_longitude: params['col_lng']
            }),
            'success': function (response) {
                params['callback']({'response': response, 'status': 'success'});
            },
            'error': function () {
                params['callback']({'status': 'failure'});
            }
        });
    },
    'unpublish_layer': function (params) {
        $.ajax({
            'url': '/api/action/geoserver_unpublish_layer',
            'type': 'POST',
            'data': JSON.stringify({
                'resource_id': params['resource_id'],
                'gs_lyr_name': params['layer_name']
            }),
            'success': function (response) {
                params['callback']({'response': response, 'status': 'success'});
            },
            'error': function () {
                params['callback']({'status': 'failure'});
            }
        });
    },
    'get_wms_urls': function (package_id, callback) {
        $.ajax({
            'url': '/api/action/get_wms',
            'type': 'POST',
            'data': JSON.stringify({
                'pkg_id': package_id
            }),
            'success': function (response) {
                return callback(response.result);
            },
            'error': function () {

            }
        })
    }
};

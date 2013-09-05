/*
 *	@author - Vivek
 *	@revised by Adrian 7/2013
 *	This object exposes an API to interact with the NGDS map.
 *
 */

ngds.Map = {
    /*	Initialize the map and display it on the UI.
     *	Inputs : None.
     */
    initialize: function () {

        var nerc_url = "https://eia-ms.esri.com/arcgis/rest/services/20130301StateEnergyProfilesMap/MapServer/export"; //layer 42
        var geothermal_potential_url = "https://eia-ms.esri.com/arcgis/rest/services/20130301StateEnergyProfilesMap/MapServer/export"; //layer 36
        var counties_url = "https://eia-ms.esri.com/arcgis/rest/services/20130301StateEnergyProfilesMap/MapServer/export"; //layer 1
        var powergrid_url = "https://eia-ms.esri.com/arcgis/rest/services/20130301StateEnergyProfilesMap/MapServer/export"; //layers 21,22,26
        var weather_url = "https://gis.srh.noaa.gov/ArcGIS/rest/services/RIDGERadar/MapServer/export"; //layer 0
        var soil_url = "http://services.arcgisonline.com/ArcGIS/rest/services/Specialty/Soil_Survey_Map/MapServer/"; //layer ?
        var water_url = "http://basemap.nationalmap.gov/ArcGIS/rest/services/USGSTopo/MapServer/";

        var base = new L.TileLayer('http://{s}.maptile.maps.svc.ovi.com/maptiler/v2/maptile/newest/terrain.day/{z}/{x}/{y}/256/png8');

        var map = this.map = new L.Map('map-container', {
            layers: [base],
            center: new L.LatLng(34.1618, -100.53332),
            zoom: 3,
            zoomControl: false
        });

        var loadingControl = L.Control.loading({
            separate: true,
            position: 'topleft'
        });

        var nerc_wms = new L.TileLayer.EsriImageExports(nerc_url, {
            layers: "42"
        });
        var geothermal_potential_wms = new L.TileLayer.EsriImageExports(geothermal_potential_url, {
            layers: "36"
        });
        var counties_wms = new L.TileLayer.EsriImageExports(counties_url, {
            layers: "1"
        });
        var powergrid_wms = new L.TileLayer.EsriImageExports(powergrid_url, {
            layers: ["21,22,26"]
        });
        var weather_wms = new L.TileLayer.EsriImageExports(weather_url, {
            layers: "0"
        });

        var soil = new L.tileLayer.wms('http://geo.cei.psu.edu:8080/geoserver/wms', {
            format: 'image/png',
            transparent: true,
            attribution: 'US Soil Survey',
            layers: 'cei:canada,cei:mexicarib,cei:mlra_48,cei:lower48',
            styles: 'other_polygons,other_polygons,llrShadeTest_opaque,state_noFill',
            srs: 'srs:EPSG:102003'
        });

        var wells = L.tileLayer.wms("http://geothermal.smu.edu/geoserver/wms", {
            layers: 'wells',
            format: 'image/png',
            transparent: true,
            attribution: "SMU Well Data"
        });

        var land = L.tileLayer.wms('http://www.geocommunicator.gov/arcgis/services/Basemaps/MapServer/WMSServer', {
            layers: '0,1,3,4,5,6,7,8,9,10,11,12,13,14,15',
            format: 'image/png',
            transparent: true
        });

        var topography = new L.TileLayer('http://basemap.nationalmap.gov/ArcGIS/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}');

        var _geoJSONLayer = this.geoJSONLayer = new L.geoJson(null, {onEachFeature: function (a, b) {

        }}); // Geo JSON Layer where we'll display all our features.

        var _drawControl = new L.Control.Draw({
            position: 'topleft',
            polyline: false,
            circle: false,
            marker: false,
            polygon: true
        });

        map.addControl(_drawControl);
        var _drawnItems = ngds.Map.drawnItems = new L.LayerGroup();
        map.addLayer(_drawnItems);


        var zoom = new L.Control.Zoom({
            'position': 'topright'
        });

        map.addControl(zoom);
        map.addControl(loadingControl);

        L.control.fullscreen({
            position: 'topright',
            title: 'Show me the fullscreen !'
        }).addTo(map);


        this.layers = {
            'geojson': _geoJSONLayer,
            'drawnItems': _drawnItems,
            'powergrid': powergrid_wms,
            'soil': soil,
            //	'water':water_wms,
            'land': land,
            'topography': topography,
            'nerc': nerc_wms,
            'geothermal_potential': geothermal_potential_wms,
            'counties': counties_wms,
            'weather': weather_wms
        };
        // this.initialize_controls();

        var baseMaps = {
            "Terrain": base,
            "US Topographic Map": topography,
            'Soil Extent Map': soil
        };

        overlayMaps = {
            "Power Grid": powergrid_wms,
            "Search Results": _geoJSONLayer,
            "SMU Wells": wells,
            'USBLM Urban Areas, Counties': land,
            'NERC Regions': nerc_wms,
            'Geothermal Potential': geothermal_potential_wms,
            'US County Boundaries': counties_wms,
            'NEXRAD Weather': weather_wms
            // "ngds":ngds_layer
        };

        layer_control = new L.control.layers(baseMaps, overlayMaps, {autoZIndex: true});
        layer_control.addTo(map);

        map.on('layeradd', function (lev) { // Every time a layer is added or removed, make sure our geojson layer is the top-most one.
            try {
                _geoJSONLayer.bringToFront();
            }
            catch (e) {
                // Do nothing because we know that there will be an error when this layer is hidden on the map.
            }
        });
        copy = [];
        map.addLayer(_geoJSONLayer);

        var placeMarker_single = L.Icon.Label.extend({
            options: {
                iconUrl: '',
                shadowUrl: null,
                iconSize: new L.Point(36, 36),
                iconAnchor: new L.Point(0, 1),
                labelAnchor: new L.Point(0, 0),
                wrapperAnchor: new L.Point(0, 13),
                labelClassName: 'placeMarks-label'
            }
        });
        var placeMarker_double = L.Icon.Label.extend({
            options: {
                iconUrl: '',
                shadowUrl: null,
                iconSize: new L.Point(36, 36),
                iconAnchor: new L.Point(0, 1),
                labelAnchor: new L.Point(5, 5),
                wrapperAnchor: new L.Point(12, 13),
                labelClassName: 'placeMarks-label'
            }
        });
        placeMarker_triple = L.Icon.Label.extend({
            options: {
                iconUrl: '',
                shadowUrl: null,
                iconSize: new L.Point(25, 41),
                iconAnchor: new L.Point(0, 0),
                labelAnchor: new L.Point(0, 0),
                wrapperAnchor: new L.Point(13, 41),
                labelClassName: 'placeMarks-label',
                popupAnchor: new L.Point(0, -33)
            }
        });
        new L.Control.GeoSearch({
            provider: new L.GeoSearch.Provider.OpenStreetMap(),
            position: 'topright'
        }).addTo(map);

        ngds.publish("Map.loaded", { });
    },
    initialize_controls: function () {
        var html = '';
        html += '<div id="map-expander">';
        html += '<p>&lt;&lt;</p>';
        html += '</div>'; //
        var expanded_flag = false;
        var original_map_container_size = $("#map-container").css("width");
        var expander_handle_unexpanded = '<p>&lt;&lt;</p>';
        var expander_handle_expanded = '<p>&gt;&gt;</p>';
        $("#map-container").append(html);

        $("#map-expander").click(function () {

            if (expanded_flag === false) {	// If the resize handle is clicked, expand if not already expanded.
                expanded_flag = true;
                $(".map-search").hide();
                $("#map-container").css("width", 1024);
                $("#map-expander").empty();
                $("#map-expander").append(expander_handle_expanded);
                ngds.Map.map.invalidateSize();
            }
            else {
                expanded_flag = false;
                $("#map-container").css("width", original_map_container_size);
                ngds.Map.map.invalidateSize();
                $(".map-search").show();
                $("#map-expander").empty();
                $("#map-expander").append(expander_handle_unexpanded);
            }
            return false;
        });
    },
    zoom_managed_list: {

    },
    zoom_listeners: [

    ],
    map_search: function () {
        var me = this;
        geoj = me.get_layer('drawnItems');

        var query = $("#map-query").val();
        var pager = ngds.Pager(5);

        pager.set_action(ngds.ckanlib.package_search, { 'q': query });
        if (ngds.Map.shape.str == 'rect') {
            // ngds.Map.manage_zoom(ngds.Map.bounding_box,ngds.Map.shape.e.rect,ngds.Map.get_layer('drawnItems'));
        }
        else {
            // ngds.Map.manage_zoom(bounding_box,ngds.Map.shape.e.poly,ngds.Map.get_layer('drawnItems'));
        }
        me.clear_layer('geojson');
        pager.move(1, function (each_result, marker_or_shape) {
            var label = ngds.Map.labeller.get_cur_label();
            ngds.Map.add_raw_result_to_geojson_layer(each_result, {iconimg_id: 'lmarker-' + label});
            var span_margin = "0px";

            if (marker_or_shape === 'marker') {
                $('.result-' + label).hover(function () { //fadein
                    $('.lmarker-' + label).css("width", "30px");
                    $('.lmarker-' + label).css("height", "45px");
                    var span_elem = $('.lmarker-' + label).next();
                    span_elem.css("font-size", "14pt");
                    span_elem.css("margin-left", "2px");
                }, function () { // fadeout
                    $('.lmarker-' + label).css("width", "25px");
                    $('.lmarker-' + label).css("height", "41px");
                    var span_elem = $('.lmarker-' + label).next();
                    span_elem.css("font-size", "12.5pt");
                    span_elem.css("margin-left", span_margin);
                });

                $('.result-' + label).click(function () {					 		// Reset steps
                    $('.result').css('background-color', '#fff'); // This is really a reset step. Do we need to move this into a .reset_background() ?
                    var labels_colored = ngds.Map.state.colored_labels || (ngds.Map.state.colored_labels = []);
                    for (var i = 0; i < labels_colored.length; i++) {
                        labels_colored[i].attr("src", "/images/marker.png");
                    }

                    for (var shape_index in ngds.Map.state.shapes_map) {
                        if (ngds.Map.state.shapes_map[shape_index] !== null && typeof ngds.Map.state.shapes_map[shape_index] !== 'undefined') {
                            ngds.Map.state.shapes_map[shape_index].setStyle({weight: ngds.Map.state.shapes_map[shape_index].orig_weight, color: ngds.Map.state.shapes_map[shape_index].orig_color});
                        }
                    }

                    labels_colored = ngds.Map.state.colored_labels = [];
                    // End reset steps

                    // Now do the actual transitions
                    $('.result-' + label).css('background-color', '#dadada');
                    $('.lmarker-' + label).attr("src", "/images/marker-red.png");
                    labels_colored.push($('.lmarker-' + label));
                    // End actual transitions
                });
            }
            else {
                $('.result-' + label).hover(function () { //fadein
                    var shape = ngds.Map.state.shapes_map[label];

                    ngds.Map.state.shapes_map[label].prev_weight = ngds.Map.state.shapes_map[label].options.weight;
                    ngds.Map.state.shapes_map[label].prev_color = ngds.Map.state.shapes_map[label].options.color;
                    shape.setStyle({weight: 2, color: "#d54799"});

                }, function () { //fadeout
                    var shape = ngds.Map.state.shapes_map[label];
                    shape.setStyle({weight: ngds.Map.state.shapes_map[label].prev_weight, color: ngds.Map.state.shapes_map[label].prev_color});
                });

                $('.result-' + label).click(function () {
                    // Reset steps
                    $('.result').css('background-color', '#fff'); // This is really a reset step. Do we need to move this into a .reset_background() ?
                    var labels_colored = ngds.Map.state.colored_labels || (ngds.Map.state.colored_labels = []);
                    for (var i = 0; i < labels_colored.length; i++) {
                        labels_colored[i].attr("src", "/images/marker.png");
                    }
                    // shapes

                    for (var shape_index in ngds.Map.state.shapes_map) {
                        if (ngds.Map.state.shapes_map[shape_index] !== null && typeof ngds.Map.state.shapes_map[shape_index] !== 'undefined' && shape_index !== label) {
                            ngds.Map.state.shapes_map[shape_index].setStyle({weight: ngds.Map.state.shapes_map[shape_index].orig_weight, color: ngds.Map.state.shapes_map[shape_index].orig_color});
                        }
                    }

                    // End of Reset steps
                    $('.result-' + label).css('background-color', '#dadada');
                    var shape = ngds.Map.state.shapes_map[label];
                    if (shape !== null && typeof shape !== 'undefined') {
                        shape.setStyle({weight: 3, color: "red"});
                        ngds.Map.state.shapes_map[label].prev_weight = 3;
                        ngds.Map.state.shapes_map[label].prev_color = "red";

                    }
                });
            }

        }, function (count) {
            pager.set_state(count, query);
        });
    },
    get_layer: function (key) {
        if (key in this.layers) {
            return this.layers[key];
        }
        throw "No layer exists with the key : " + key;
    },
    /*	Add a list of features to a particular layer on the map.
     *	Inputs : A list of features and a key that identifies the layer.
     */
    add_to_layer: function (features, layer_str) {
        var me = this;
        if (layer_str in this.layers && features.length > 0) {
            $.each(features, function (index, feature) {
                feature.addTo(me.layers[layer_str]);
            });
        }
    },
    /*	Clear a layer using it's key.
     *	Inputs : A key that identifies the layer that is to be cleared.
     */
    clear_layer: function (layer_str) {
        this.layers[layer_str].clearLayers();
    },
    /*	Add a list of ckan packages to the map.
     *	Inputs : A list of package ids.
     */
    add_packages_to_geojson_layer: function (package_ids) {
        var me = this;
        $.each(package_ids, function (index, package_id) {
            ngds.ckanlib.package_show(package_id, function (response) {
                me.add_raw_result_to_geojson_layer(response.result);
            });
        });
    },
    add_raw_result_to_geojson_layer: function (result, options) { // Expects response.result, not response. Seq id passed in.
        try {
            var dataset = ngds.ckandataset(result);
            var feature = dataset.getGeoJSON();
            var popup = dataset.map.getPopupHTML();
        }
        catch (e) {
            return;
        }
        var geoJSONRepresentation = L.geoJson(feature, {
            style: {
                color: "black",
                weight: 1,
                opacity: 1,
                fillColor: "grey",
                fillOpacity: 0.2
            },
            onEachFeature: function (feature_data, layer) {
                var type = (function (layer) {
                    if (layer.feature.type == 'Point') {
                        return 'Marker';
                    }
                    else {
                        return 'Feature';
                    }
                })(layer);
                ngds.Map.add_to_layer([layer], 'geojson');
                ngds.publish('Map.add_feature', {
                    'feature': layer,
                    'seq_id': options['seq'],
                    'type': type

                });

                if (layer.feature.geometry.type === 'Polygon') {
                    ngds.Map.zoom_handler(layer);
                    var label = options['seq'];
                    var shapes_map = ngds.Map.state.shapes_map || (ngds.Map.state.shapes_map = {});
                    shapes_map[label] = layer;
                    shapes_map[label].orig_color = "blue";
                    shapes_map[label].orig_weight = 2;
                }
            },
            pointToLayer: function (feature, latlng) {
                var marker = L.marker(latlng, {icon: new placeMarker_triple({ iconUrl: '/images/marker.png', labelText: options['alph_seq'], className: 'lmarker-' + options['seq']})});
                return marker;
            }
        });

        geoJSONRepresentation.bindPopup(popup);
        this.add_to_layer([geoJSONRepresentation], 'geojson');
        this.sort_geojson_layers(geoJSONRepresentation);
    },
    sort_geojson_layers: function (layer) {
        var perimeter = new ngds.Map.BoundingBox().store_raw(layer.getBounds()).get_perimeter();

        var map_features = ngds.util.state['map_features'];
        var i = 0;
        for (i = 0; i <= map_features.length; i++) {
            if (i === map_features.length) {
                break;
            }
            if (perimeter < new ngds.Map.BoundingBox().store_raw(map_features[i].getBounds()).get_perimeter()) {
                break;
            }
        }
        map_features.splice(i, 0, layer);
        for (var i = map_features.length - 1; i > -1; i--) {
            map_features[i].bringToFront();
        }
    },
    // Exposes a set of utility functions to work with the map.
    utils: {
        /*
         *	Takes a list of coordinate pairs and returns a specific upper or lower bound of the bounding box for this shape.
         *	Inputs : A list of coordinate pairs, a string that is either 'lat' or 'lng', a string that is either 'min' or 'max'
         *	For ex : To get the lower bound for a bounding box, pass in the coordinates, 'lat','min' and coordinates, 'lng','min'.
         */
        get_bound: function (coords, lat_or_lng, min_or_max) {
            (function () {
                if (lat_or_lng !== 'lat' && lat_or_lng !== 'lng' || min_or_max !== 'min' && min_or_max !== 'max') {
                    throw "Expected 'lat' or 'lng' for lat_or_lng and 'min' or 'max' for min_or_max"
                }
            })();

            var func = eval("Math." + min_or_max);
            var operands = [];
            $.each(coords, function (index, item) {
                operands.push(item[lat_or_lng]);
            });
            return func.apply(this, operands);
        }
    },
    register_map_query_provider: function (id_provider) {
        // Validate inputs.
        (function () {
            if (id_provider === null || typeof id_provider === 'undefined') {
                throw "Expected a string for id_provider.";
            }
        })();

        this.query_provider = "#" + id_provider;
    },
    state: { // Maintain state of various components in here ... make sure your keys are unique

    },
    is_fullscreen: function () {
        if (typeof ngds.Map.state['fullscreen'] === 'undefined') {
            return false;
        }
        return ngds.Map.state['fullscreen'];
    }
};
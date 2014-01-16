/**
 * Created by Adrian Sonnenschein on 12/23/13.
 */
(function () {

var drawings = new L.FeatureGroup();

ngds.Map = {
    map: L.map('map-container', {center: [39.977, -97.646], zoom: 4,
        maxBounds: [[-84, -179], [84, 179]], attributionControl: true, minZoom: 2}),
    layers: {
        baseLayer: L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg', {
            subdomains: '1234',
            attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; ' +
                '<a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.' +
                'org/licenses/by-sa/2.0/">CC-BY-SA</a>',
            detectRetina: true
        }),
        searchResultsGroup: {"Search Results": L.layerGroup()},
        dataExtentsGroup: {"Data Extents": new Array()}
    },
    controls: {
        loading: L.Control.loading({separate: true, position: 'topleft'}),
        doodle: new L.Control.Draw({position: 'topleft',
            draw:{polyline: false, circle: false, marker: false, polygon: false},
            edit: {featureGroup: drawings, remove: false, edit: false}
        }),
        search: L.Control.extend({options: {position: 'topleft'}, onAdd: function () {
            var container = L.DomUtil.create('div', 'ngds-custom-control search-control');
            L.DomEvent.on(container, 'click', L.DomEvent.stopPropagation)
                .on(container, 'dblclick', L.DomEvent.stopPropagation)
                .on(container, 'mousedown', L.DomEvent.stopPropagation)
                .addListener(container, 'click', function () {
                    var layers = ngds.Map.layers.searchResultsGroup["Search Results"];
                    if ($(container).hasClass('off')) {
                        $(container).removeClass('off');
                        $(container).addClass('on');
                        ngds.Map.map.addLayer(layers);
                    } else if ($(container).hasClass('on')) {
                        $(container).removeClass('on');
                        $(container).addClass('off');
                        ngds.Map.map.removeLayer(layers);
                    } else {
                        $(container).addClass('off');
                        ngds.Map.map.removeLayer(layers);
                    }
                });
            $(container).append('<a class="glyphicon icon-search" href="#" title="Toggle search results"></a>');
            return container;
        }}),
        reset: L.Control.extend({options: {position: 'topleft'}, onAdd: function (){
            var container = L.DomUtil.create('div', 'ngds-custom-control reset-control');
            L.DomEvent.on(container, 'click', L.DomEvent.stopPropagation)
                .on(container, 'dblclick', L.DomEvent.stopPropagation)
                .on(container, 'mousedown', L.DomEvent.stopPropagation)
                .addListener(container, 'click', function () {
                    ngds.Map.map.setView([39.977, -97.46], 4);
                });
            $(container).append('<a class="glyphicon icon-home" href="#" title="Reset extent"></a>')
            return container;
        }})
    }
};

ngds.Map.topLevelSearch = function (bbox) {
    var theseLayers = ngds.Map.layers.searchResultsGroup["Search Results"];
    if (theseLayers.getLayers().length > 1) {theseLayers.clearLayers();}
    $('#query-results').empty();
    var extras = bbox || {'ext:bbox': "-180,-90,180,90"},
        searchQuery = $('#map-search-query').val();
    ngds.Map.makeSearch({
        'q': searchQuery,
        'extras': extras
    })
    $('#content-legend-menu').addClass('shown');
};

ngds.Map.makeSearch = function (parameters) {
    var action = ngds.ckanlib.package_search,
        rows = 10000000,
        start = 0,
        query = parameters['q'],
        extras = parameters['extras'];

    action({'q': query, 'rows': rows, 'start': start, 'extras': extras}, function (response) {
        _.each(response.result, function (rec) {
            var randomNumber = Math.floor(Math.random()*1000000000000000000000),
                coords = JSON.parse(rec.bbox[0]),
                geoData = {'sw_lat': coords.coordinates[0][0][1], 'sw_lon': coords.coordinates[0][0][0],
                    'ne_lat': coords.coordinates[0][2][1], 'ne_lon': coords.coordinates[0][2][0]},
                geoString = geoData['sw_lat'] + ',' + geoData['sw_lon'] + ',' + geoData['ne_lat'] + ',' + geoData['ne_lon'];
                bounds = L.latLngBounds([[geoData.sw_lon, geoData.sw_lat],[geoData.ne_lon, geoData.ne_lat]]),
                center = bounds.getCenter(),
                geojson = {'type': 'Feature', 'properties': {'feature_id': randomNumber, 'title': rec.title},
                    'geometry': {'type': 'Point', 'coordinates': [center.lat, center.lng]}},
                reqData = {'title': rec.title, 'name': rec.name, 'notes': rec.notes, 'pkg_id': rec.id,
                    'resources': rec.resources, 'geoData': geoData, 'geojson': geojson, 'geoString': geoString};
            ngds.Map.returnSearchResult(reqData);
        })
    })
};

ngds.Map.returnSearchResult = function (result) {
    var thisResult = [result];
    var vanillaOptions = _.map(thisResult, function (data) {
        if (data.geoData) {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a id=bbox-handle' + data.pkg_id + ' class="extent-absent" value="' + result.geoString + '" href="javascript:void(0)" onclick="ngds.Map.addBbox(this)">Show Area on Map</a>';
            html += '</div></div>';
            return html;
        }
    }).join('');

    var resources = _.map(result.resources, function (data) {
        if (data.format) {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<table><tr><td><span class="label label-success">' + data.format + '</span></td><td>';
            html += '<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion-search-result" href=#collapse' + data.id + '>' + data.name + '</a></div>';
            html += '</td></tr></table>';
            html += '<div id=collapse' + data.id + ' class="accordion-body collapse">';
            html += '<p>' + data.description + '</p>';
            html += '</div></div></div>';
            return html;
        } else if (data.protocol === 'OGC:WMS') {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<table><tr><td><span class="label label-success">' + data.protocol + '</span></td><td>';
            html += '<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion-search-result" href=#collapse' + data.id + '>' + data.layer + '</a></div>';
            html += '</td></tr></table>';
            html += '<div id=collapse' + data.id + ' class="accordion-body collapse">';
            html += '<p>' + data.description + '</p>';
            html += '<table><tr><td><div class="glyphicon icon-globe"</td>';
            html += '<td><a id="' + result.pkg_id + '" class="wms-handle" href="javascript:void(0)" onclick="ngds.Map.addWmsLayer(this.id)">WMS Layer</a></td>';
            html += '</tr></table></div></div></div>';
            return html;
        } else if (data.protocol) {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<table><tr><td><span class="label label-success">' + data.protocol + '</span></td><td>';
            html += '<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion-search-result" href=#collapse' + data.id + '>' + data.layer + '</a></div>';
            html += '</td></tr></table>';
            html += '<div id=collapse' + data.id + ' class="accordion-body collapse">';
            html += '<p>' + data.description + '</p>';
            html += '</div></div></div>';
            return html;
        }
    }).join('');

    var getPackageDescription = function (data) {
        if (data.length > 200) {
            return {'preview': data.substr(0,200) + '...', 'full': data}
        } else if (data.length <= 200) {
            return data
        } else {
            return ''
        }
    };

    var feature_id = result.geojson.properties.feature_id,
        packageDescription = getPackageDescription(result.notes),
        html = '<li class="map-search-result result-' + feature_id + '" >';
        html += '<div class="accordion" id="accordion-search">';
        html += '<div class="accordion-group">';
        html += '<div class="accordion-heading">';
        html += '<table>';
        html += '<a class="accordion-toggle feature-id-' + feature_id + '" data-toggle="collapse" data-parent="#accordion-search" href=#collapse' + feature_id + '>' + result.title + '</td>';
        html += '</td></tr></table>';
        html += '<div class="package-description"><p>' + packageDescription['preview'] + '</p></div></div>';
        html += '<div id=collapse' + feature_id + ' class="accordion-body collapse">';
        html += '<div class="resource-content">' + vanillaOptions + '</div>';
        html += '<div class="resource-content">' + resources + '</div>';
        //html += '<div class="resource-content">' + resources + '<div class="btn-mini btn-info btn">Bounding Box</div></div>';
        html += '</div></div></div></li>';
    $('#query-results').append(html);

    var defaultStyle = {radius: 8, fillColor: '#ff00ff', color: '#ff00ff',
            weight: 2, opacity: 1, fillOpacity: 0.5},
         highlightStyle = {radius: 8, fillColor: 'blue', color: 'blue',
            weight: 2, opacity: 1, fillOpacity: 0.5};
    var circles = L.geoJson(result.geojson, {pointToLayer: function (f,ll) {
        return L.circleMarker(ll, defaultStyle)
        },
        onEachFeature: function (feature, layer) {
            var feature_id = layer.feature.properties.feature_id,
                popupText = layer.feature.properties.title,
                thisPopup = L.popup().setLatLng(feature).setContent(popupText),
                searchResult = $('.map-search-result.result-' + feature_id);
            layer.bindPopup(thisPopup);
            layer.on('click', function() {
                var toggleId = $('#collapse' + feature_id),
                    collapseId = $('.feature-id-' + feature_id);
                $('#query-results').prepend(searchResult);
                $('#query-results').animate({scrollTop:0}, 'fast');
                if (collapseId.hasClass('collapsed')) {
                    toggleId.addClass('in');
                    collapseId.removeClass('collapsed');
                } else if (toggleId.hasClass('in')) {
                    toggleId.removeClass('in');
                    collapseId.addClass('collapsed');
                } else {
                    toggleId.addClass('in');
                }
            }),
            layer.on('mouseover', function () {
                layer.setStyle(highlightStyle);
                var resultId = $('.result-' + feature_id);
                resultId.addClass('result-highlight');
            }),
            layer.on('mouseout', function () {
                layer.setStyle(defaultStyle);
                var resultId = $('.result-' + feature_id);
                resultId.removeClass('result-highlight');
            })

            searchResult.hover(function () {
                $(searchResult).addClass('result-highlight');
                layer.setStyle(highlightStyle);
            }, function () {
                $(searchResult).removeClass('result-highlight');
                layer.setStyle(defaultStyle);
            })
        }}
    );

    ngds.Map.layers.searchResultsGroup["Search Results"].addLayer(circles).addTo(ngds.Map.map);
};

ngds.Map.map.on('draw:created', function (e) {
    var layer = e.layer,
        theseBounds = layer.getBounds().toBBoxString(),
        ext_bbox = {'ext_bbox': theseBounds};
    ngds.Map.topLevelSearch(ext_bbox);
    ngds.Map.map.fitBounds(layer.getBounds());
});

ngds.Map.addWmsLayer = function (thisId) {
    ngds.ckanlib.get_wms_urls(thisId, function (wmsMapping) {
        _.each(wmsMapping, function (wms) {
            var params = {
                'layers': wms['layer'],
                'format': wms['format'],
                'transparent': true,
                'version': '1.1.1'
                },
                bbox = [[wms.bbox[1], wms.bbox[0]],[wms.bbox[3], wms.bbox[2]]],
                wmsLayer = L.tileLayer.wms(wms['service_url'], params);
            layersControl.addOverlay(wmsLayer, 'my_layer');
            ngds.Map.map.addLayer(wmsLayer);
            ngds.Map.map.fitBounds(bbox);
        })
    })
};

ngds.Map.addBbox = function (event) {
    var thisId = $('#' + event.getAttribute('id')),
        thisUID = thisId[0].id.split('bbox-handle')[1];
    if (thisId.hasClass('extent-absent')) {
        var theseValues = event.getAttribute('value').split(','),
            theseCoords = [];
        _.each(theseValues, function (value) {
            var coord = parseFloat(value);
            theseCoords.push(coord);
        });
        var theseBounds = [[theseCoords[0], theseCoords[1]], [theseCoords[2], theseCoords[3]]],
            boundingBox = L.rectangle(theseBounds, {color: 'blue', weight: 1});
            bboxGroup = ngds.Map.layers.dataExtentsGroup;
        bboxGroup['Data Extents'][thisUID] = boundingBox;
        bboxGroup['Data Extents'][thisUID].addTo(ngds.Map.map);
        thisId.removeClass('extent-absent').addClass('extent-present');
    } else if (thisId.hasClass('extent-present')) {
        var thisLayer = bboxGroup['Data Extents'][thisUID];
        ngds.Map.map.removeLayer(thisLayer);
        thisId.removeClass('extent-present').addClass('extent-absent');
    }
};

ngds.Map.toggleContentMenu = function () {
    if ($('#content-legend-menu').hasClass('shown')) {
        $('#content-legend-menu').removeClass('shown');
        $('#line-triangle').removeClass('left-triangle');
        $('#line-triangle').addClass('right-triangle');
    } else {
        $('#content-legend-menu').addClass('shown');
        $('#line-triangle').removeClass('right-triangle');
        $('#line-triangle').addClass('left-triangle');
    }
};

var overlayPane = ngds.Map.layers.searchResultsGroup,
    layersControl = L.control.layers(null, overlayPane, {position: 'topleft'});

drawings.addTo(ngds.Map.map);
ngds.Map.layers.baseLayer.addTo(ngds.Map.map);
ngds.Map.map.addControl(ngds.Map.controls.doodle);
ngds.Map.map.addControl(new ngds.Map.controls.search);
ngds.Map.map.addControl(new ngds.Map.controls.reset);
layersControl.addTo(ngds.Map.map);
ngds.Map.map.addControl(ngds.Map.controls.loading);

$('.leaflet-draw-toolbar-top').removeClass('leaflet-draw-toolbar');
$('.leaflet-draw-draw-rectangle').addClass('glyphicon icon-pencil');

$('.bbox-handle').click(function (e) {
    console.log(e.val());
});

}).call(this);
/**
 * Created by Adrian Sonnenschein on 12/23/13.
 */
(function () {

var drawings = new L.FeatureGroup();

ngds.Map = {
    map: L.map('map-container', {center: [39.977, -97.646], zoom: 4,
        maxBounds: [[-84, -179], [84, 179]], attributionControl: true}),
    layers: {
        baseLayer: L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg', {
            subdomains: '1234',
            attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; ' +
                '<a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.' +
                'org/licenses/by-sa/2.0/">CC-BY-SA</a>',
            detectRetina: true
        }),
        searchResultsGroup: L.layerGroup()
    },
    controls: {
        loading: L.Control.loading({separate: true, position: 'topleft'}),
        doodle: new L.Control.Draw({position: 'topleft',
            draw:{polyline: false, circle: false, marker: false, polygon: false},
            edit: {featureGroup: drawings, remove: false, edit: false}
        }),
        search: L.Control.extend({options: {position: 'topleft'}, onAdd: function (map) {
            var container = L.DomUtil.create('div', 'search-control');
            L.DomEvent.on(container, 'click', L.DomEvent.stopPropagation)
                .on(container, 'dblclick', L.DomEvent.stopPropagation)
                .on(container, 'mousedown', L.DomEvent.stopPropagation)
                .addListener(container, 'click', function () {
                    var layers = ngds.Map.layers.searchResultsGroup;
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
        }})
    }
};

ngds.Map.topLevelSearch = function (bbox) {
    $('#query-tab .results').empty();
    var extras = bbox || {'ext:bbox': "-180,-90,180,90"},
        searchQuery = $('#map-search-query').val();
    ngds.Map.makeSearch({
        'q': searchQuery,
        'extras': extras
    })
};

ngds.Map.makeSearch = function (parameters) {
    var action = ngds.ckanlib.package_search,
        rows = 10,
        page = 1,
        start = (page - 1) * rows,
        query = parameters['q'],
        extras = parameters['extras'];

    action({'q': query, 'rows': rows, 'start': start, 'extras': extras}, function (response) {
        _.each(response.result.results, function (rec) {
            _.each(rec.resources, function (single_resource) {
                var randomNumber = Math.floor(Math.random()*1000000000000000000000),
                    coords = JSON.parse(rec.extras[8].value),
                    geoData = {'sw_lat': coords.coordinates[0][0][1], 'sw_lon': coords.coordinates[0][0][0],
                        'ne_lat': coords.coordinates[0][2][1], 'ne_lon': coords.coordinates[0][2][0]},
                    bounds = L.latLngBounds([[geoData.sw_lon, geoData.sw_lat],[geoData.ne_lon, geoData.ne_lat]]),
                    center = bounds.getCenter(),
                    geojson = {'type': 'Feature', 'properties': {'feature_id': randomNumber},
                        'geometry': {'type': 'Point', 'coordinates': [center.lat, center.lng]}},

                reqData = {'title': rec.title, 'pkg_id': rec.id, 'resources': single_resource, 'geojson': geojson};
                ngds.Map.returnSearchResult(reqData);
            })
        })
    })
};

ngds.Map.returnSearchResult = function (result) {
    // '/dataset/' + results[i]['name'],
    var feature_id = result.geojson.properties.feature_id,
        html = '<li class="map-search-result result-' + feature_id + '" >';
        html += '<div class="accordion" id="accordion-search">';
        html += '<div class="accordion-group">';
        html += '<div class="accordion-heading">';
        html += '<table><tr><td>';
        html += '<a class="accordion-toggle glyphicon icon-align-justify feature-id-' + feature_id + '" data-toggle="collapse" data-parent="#accordion-search" href=#collapse' + feature_id + '></a></td>';
        html += '<td>' + result.resources.name + '</td>';
        html += '</tr></table></div>';
        html += '<div id=collapse' + feature_id + ' class="accordion-body collapse">';
        html += '<p>' + result.title + '</p>';
        html += '<p>' + result.resources.layer + '</p>';
        html += '<p>' + result.resources.distributor + '</p>';
        html += '<p>' + result.resources.description + '</p>';
        html += '<p>' + result.resources.protocol + '</p>';
        html += '<p>' + result.resources.format + '</p>';
        html += '<a id="' + result.pkg_id + '" class="wms-handle" href="javascript:void(0)" onclick="ngds.Map.addWmsLayer(this.id)">';
        html += 'WMS</a></div></div></div></li>';
    $('#query-results').append(html);

    var defaultStyle = {radius: 8, fillColor: '#ff0000', color: '#ff0000',
            weight: 2, opacity: 1, fillOpacity: 0.5};
    var circles = L.geoJson(result.geojson, {pointToLayer: function (f,ll) {
        return L.circleMarker(ll, defaultStyle)
        },
        onEachFeature: function (feature, layer) {
            var feature_id = layer.feature.properties.feature_id;
            layer.on('click', function() {
                var toggleId = $('#collapse' + feature_id),
                    collapseId = $('.feature-id-' + feature_id);

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
                layer.setStyle({fillColor: 'yellow'});
                var resultId = $('.result-' + feature_id);
                resultId.addClass('result-highlight');
            }),
            layer.on('mouseout', function () {
                layer.setStyle(defaultStyle);
                var resultId = $('.result-' + feature_id);
                resultId.removeClass('result-highlight');
            })
            var searchResult = $('.map-search-result.result-' + feature_id),
                domSelector = searchResult.selector.split('.')[2],
                dataSelector = 'result-' + layer.feature.properties.feature_id;

            searchResult.hover(function () {
                $(searchResult).addClass('result-highlight');
                layer.setStyle({fillColor: 'yellow'});
            }, function () {
                $(searchResult).removeClass('result-highlight');
                layer.setStyle(defaultStyle);
            })
        }}
    );
    ngds.Map.layers.searchResultsGroup.addLayer(circles).addTo(ngds.Map.map);
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
                'attribution': 'NGDS',
                'version': '1.1.1'
                },
                wmsLayer = L.tileLayer.wms(wms['service_url'], params);
            ngds.Map.map.addLayer(wmsLayer);
        })
    })
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

drawings.addTo(ngds.Map.map);
ngds.Map.layers.baseLayer.addTo(ngds.Map.map);
ngds.Map.map.addControl(ngds.Map.controls.doodle);
ngds.Map.map.addControl(ngds.Map.controls.loading);
ngds.Map.map.addControl(new ngds.Map.controls.search);

}).call(this);
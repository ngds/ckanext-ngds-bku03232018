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
        })
    },
    controls: {
        loading: L.Control.loading({separate: true, position: 'topleft'}),
        doodle: new L.Control.Draw({position: 'topleft',
            draw:{polyline: false, circle: false, marker: false, polygon: false},
            edit: {featureGroup: drawings, remove: false, edit: false}
        })
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

                reqData = {'title': rec.title, 'resources': single_resource, 'geojson': geojson};
                ngds.Map.returnSearchResult(reqData);
            })
        })
    })
};


ngds.Map.returnSearchResult = function (result) {
    var circlesLayer = L.geoJson(result.geojson, {pointToLayer: function (f,ll) {
        return L.circleMarker(ll, {radius: 8, fillColor: '#ff0000', color: '#ff0000',
            weight: 2, opacity: 1, fillOpacity: 0.5})
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
            })
        }}
    ).addTo(ngds.Map.map);

    console.log(circlesLayer.getBounds().toBBoxString());

    // '/dataset/' + results[i]['name'],
    var feature_id = result.geojson.properties.feature_id,
        html = '<li class="map-search-result">';
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
        html += '<p>' + result.geo + '</p>';
        html += '</div></div></div></li>';
    $('#query-tab .results').append(html);
};

ngds.Map.map.on('draw:created', function (e) {
    var layer = e.layer,
        theseBounds = layer.getBounds().toBBoxString(),
        ext_bbox = {'ext_bbox': theseBounds};
    ngds.Map.topLevelSearch(ext_bbox);
    ngds.Map.map.fitBounds(layer.getBounds());
});

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

}).call(this);
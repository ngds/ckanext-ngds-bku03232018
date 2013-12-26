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
                reqData = {'title': rec.title, 'resources': single_resource, 'geo': rec.extras[8].value};
                ngds.Map.returnSearchResult(reqData);
            })
        })
    })
};

ngds.Map.returnSearchResult = function (result) {
    // '/dataset/' + results[i]['name'],
    var randomNumber = Math.floor(Math.random()*1000000000000000000000),
        html = '<li class="map-search-result">';
        html += '<div class="accordion" id="accordion-search">';
        html += '<div class="accordion-group">';
        html += '<div class="accordion-heading">';
        html += '<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion-search" href=#collapse' + randomNumber + '>';
        html += result.title;
        html += result.resources.name + '</a>';
        html += '</div>'
        html += '<div id=collapse' + randomNumber + ' class="accordion-body collapse">';
        html += '<p>' + result.resources.layer + '</p>';
        html += '<p>' + result.resources.distributor + '</p>';
        html += '<p>' + result.resources.description + '</p>';
        html += '<p>' + result.resources.created + '</p>';
        html += '</div></div></div></li>';
    $('#query-tab .results').append(html);
};

ngds.Map.map.on('draw:created', function (e) {
    var layer = e.layer,
        theseBounds = layer.getBounds().toBBoxString(),
        ext_bbox = {'ext_bbox': theseBounds};
    ngds.Map.topLevelSearch(ext_bbox);
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
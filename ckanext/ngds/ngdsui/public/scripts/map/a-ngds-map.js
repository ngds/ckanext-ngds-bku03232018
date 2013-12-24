/**
 * Created by adrian on 12/23/13.
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

ngds.Map.map.on('draw:created', function (e) {
    var layer = e.layer;
    console.log(layer.getLatLngs());
})

ngds.Map.makeSearch = function (parameters) {
    var query = parameters['query'],
        rows = parameters['rows'],
        action = parameters['action'],
        page = parameters['page'],
        start = (page - 1) * rows,
        extras = {"ext_bbox":"-180,-90,180,90"};

    action({'query': query, 'rows': rows, 'start': start, 'extras': extras}, function (response) {
        console.log(response);
    })
};

ngds.Map.topLevelSearch = function () {
    var searchQuery = $('#map-search-query').val();
    ngds.Map.makeSearch({
        'page': 1,
        'action': ngds.ckanlib.package_search,
        'rows': 10,
        'query': searchQuery
    })
};

drawings.addTo(ngds.Map.map);
ngds.Map.layers.baseLayer.addTo(ngds.Map.map);
ngds.Map.map.addControl(ngds.Map.controls.doodle);
ngds.Map.map.addControl(ngds.Map.controls.loading);

}).call(this);
$(document).ready(function () {
    if ($("#bbox-map").length < 1) {
        return;
    }
    var base = new L.TileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg', {
        subdomains: '1234',
        attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; ' +
            '<a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.' +
            'org/licenses/by-sa/2.0/">CC-BY-SA</a>',
        detectRetina: true
    });
    var map = new L.Map('bbox-map', {layers: [base], center: new L.LatLng(34.1618, -111.53332), zoom: 5});

    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    var drawControl = new L.Control.Draw({
        position: 'topright',
        draw: {polyline: false, circle: false, marker: false, polygon: false},
        edit: {featureGroup: drawnItems, remove: true, edit: false}
    });

    map.addControl(drawControl);

    map.on('draw:created', function (e) {
        var layer = e.layer;
        drawnItems.clearLayers();
        drawnItems.addLayer(layer);
        var geojson = JSON.stringify(layer.toGeoJSON().geometry);
        $('#field-extras-10-value').val(geojson);
    });
});
var base = new L.TileLayer('http://{s}.maptile.maps.svc.ovi.com/maptiler/v2/maptile/newest/normal.day/{z}/{x}/{y}/256/png8');
var map = new L.Map('bbox-map', {layers:[base], center: new L.LatLng(34.1618, -111.53332), zoom: 5});

// Drawing bits from example:
//    https://github.com/jacobtoye/Leaflet.draw/blob/master/example/drawing.html

// Add the control panel
var drawControl = new L.Control.Draw({
	position: 'topright',
	polyline: false,
	circle: false
});
map.addControl(drawControl);

// Add callbacks for when drawing is completed
var drawnItems = new L.LayerGroup();
map.on('draw:poly-created', function(e) {
	drawnItems.clearLayers();
	drawnItems.addLayer(e.poly);
	geojson = getGeoJSON("Polygon", e.poly._latlngs);
	writeGeoJson(geojson);
});
map.on('draw:rectangle-created', function (e) {
	drawnItems.clearLayers();
	drawnItems.addLayer(e.rect);
	geojson = getGeoJSON("Polygon", e.rect._latlngs);
	writeGeoJson(geojson);
});
map.on('draw:marker-created', function (e) {
	drawnItems.clearLayers();
	drawnItems.addLayer(e.marker);
	geojson = getGeoJSON("Point", e.marker._latlng);
	writeGeoJson(geojson);
});
map.addLayer(drawnItems);

// Custom function to write GeoJSON from LatLngs
//  I have a hunch there's a better way to do this lurking in Leaflet somewhere
function getGeoJSON(geometryType, latLngs) {
	var coords = [];
	if (geometryType === 'Point') {
		coords = [ latLngs.lng, latLngs.lat ]
	} else {
		coords.push([]);
		for (var i = 0; i < latLngs.length; i++) {
			coords[0].push([latLngs[i].lng, latLngs[i].lat]);
		}
	}
	return JSON.stringify({type: geometryType, coordinates: coords});
}

// Stupid function to put the value into the first "extra" field
function writeGeoJson(geojson) {
	console.log(geojson);
	$('#field-extras-0-key').val('spatial');
	$('#field-extras-0-value').val(geojson);
}

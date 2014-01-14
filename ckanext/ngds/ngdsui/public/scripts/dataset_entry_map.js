$(document).ready(function () {
    if ($("#bbox-map").length < 1) {
        return;
    }
    var base = new L.TileLayer('http://{s}.maptile.maps.svc.ovi.com/maptiler/v2/maptile/newest/normal.day/{z}/{x}/{y}/256/png8');
    map = new L.Map('bbox-map', {layers: [base], center: new L.LatLng(34.1618, -111.53332), zoom: 5});

// Drawing bits from example:
//    https://github.com/jacobtoye/Leaflet.draw/blob/master/example/drawing.html

   L.Clear = L.Control.extend({
       options: {
           position: 'topleft',
           title: 'Clear Rectangle',
           forceSeparateButton: false
       },

       onAdd: function (map) {
           var container = L.DomUtil.create('div', 'leaflet-control-rectangle-clear-container');
           this._createButton(this.options.title, 'leaflet-control-rectangle-clear', container, this.clearRectangle, map);
           return container;
       },

       _createButton: function (title, className, container, fn, context) {
           var link = L.DomUtil.create('a', className, container);
           link.href = '#';
           link.title = title;
           L.DomEvent
               .addListener(link, 'click', L.DomEvent.stopPropagation)
               .addListener(link, 'click', L.DomEvent.preventDefault)
               .addListener(link, 'click', fn, context);
           return link;
       },
       clearRectangle: function () {
           try {
               if (map.hasLayer(map.originalExtent)) {
                   map.removeLayer(map.originalExtent);
               }
           } catch(err) {
               console.log("No original dataset extent layer.  Error: " + err);
           }
       }
   });


// Add the control panel
    var drawControl = new L.Control.Draw({
        position: 'topright',
        polyline: false,
        circle: false,
        polygon: false,
        marker: false
    });
    map.addControl(drawControl);

    var clearControl = new L.Clear({
        position: 'topright'
    });
    map.addControl(clearControl);

// Add callbacks for when drawing is completed
    var drawnItems = new L.LayerGroup();
    map.addLayer(drawnItems);

    map.on('draw:rectangle-created', function (e) {
        drawnItems.clearLayers();
        drawnItems.addLayer(e.rect);
        var geojson = JSON.stringify(e.rect.toGeoJSON().geometry);
        $('#field-extras-10-value').val(geojson);
    });
});
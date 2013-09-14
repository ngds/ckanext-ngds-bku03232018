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
        ngds.Map.get_layer('drawnItems').clearLayers();
        ngds.publish('Map.clear_rect', {});
        $("#content-container")[0].webkitRequestFullScreen();
    }
});
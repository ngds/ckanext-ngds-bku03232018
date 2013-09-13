ngds.Zoom = L.Control.Zoom.extend({
    onAdd: function (map) {
        var zoomName = 'leaflet-control-zoom',
            container = L.DomUtil.create('div', zoomName + ' leaflet-bar');

        this._map = map;

        this._zoomInButton = this._createButton(
            '', 'Zoom in', zoomName + '-in', container, this._zoomIn, this);
        this._zoomOutButton = this._createButton(
            '', 'Zoom out', zoomName + '-out', container, this._zoomOut, this);

        map.on('zoomend zoomlevelschange', this._updateDisabled, this);

        return container;
    }
});
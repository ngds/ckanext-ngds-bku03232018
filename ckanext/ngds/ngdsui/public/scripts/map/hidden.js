L.Control.Hidden = L.Control.extend({
    options: {
        position: 'bottomright'
    },

    onAdd: function (map) {
        var className = 'leaflet-control-hidden',
            container = L.DomUtil.create('div', className),
            off = this.options.panOffset;
        this.container = container;
//        var c = L.DomUtil.create('div', 'wrapper', container);
//        var link = L.DomUtil.create('a', className, c);
//        link.href = "/ngds/map";
        return container;
    },
    hide: function (layer) {
        console.log(layer);
        var c = L.DomUtil.create('div', 'wrapper', this.container);
        var link = L.DomUtil.create('a', "", c);
        link.href = "#";
        L.DomEvent
            .on(link, 'click', L.DomEvent.stopPropagation)
            .on(link, 'click', L.DomEvent.preventDefault)
            .on(link, 'mouseover', function () {
                console.log(layer);
                x=layer;
            });
    },
    unhide: function (layer) {
        console.log(layer);
    }
});


L.Map.addInitHook(function () {
    if (this.options.hidden) {
        this.hidden = new L.Control.Hidden();
        this.addControl(this.hidden);
    }
});

L.control.Hidden = function (options) {
    return new L.Control.Hidden(options);
};
L.FullScreen = L.Control.extend({
    options: {
        position: 'topright',
        title: 'FullScreen',
        forceSeparateButton: false
    },

    onAdd: function (map) {
        var container = L.DomUtil.create('div', 'leaflet-control-fullscreen-container');
        this._createButton(this.options.title, 'leaflet-control-fullscreen', container, this.fullscreen, this);
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
    get_state: function () {
        if (typeof this.fs_state === 'undefined') {
            this.fs_state = false;
        }

        return this.fs_state;
    },
    set_state: function (val) {
        this.fs_state = val;
    },
    fullscreen: function () {
        this.fs = this.get_state();
        if (this.fs === true) {
            document.webkitCancelFullScreen();
            $("#map-container").removeClass("fullscreen");
            ngds.Map.map.invalidateSize();
            this.set_state(false);
        }
        else {
            $("#content-container")[0].webkitRequestFullScreen();
            $("#map-container").addClass("fullscreen");
            ngds.Map.map.invalidateSize();
            this.set_state(true);
        }
    }
});
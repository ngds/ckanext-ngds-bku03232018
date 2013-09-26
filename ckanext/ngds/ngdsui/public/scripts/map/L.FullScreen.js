L.FullScreen = L.Control.extend({
    options: {
        position: 'topright',
        title: 'FullScreen',
        forceSeparateButton: false
    },

    onAdd: function (map) {
        var container = L.DomUtil.create('div', 'leaflet-control-fullscreen-container');
        this._createButton(this.options.title, 'leaflet-control-fullscreen', container, this.full_screen, this);
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
    request_fs: function (el) {
        if (typeof el.webkitRequestFullScreen !== 'undefined') {
            el.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
            return;
        }
        if (typeof el.mozRequestFullScreen !== 'undefined') {
            el.mozRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
            return;
        }
    },
    cancel_fs: function () {
        if (typeof document.webkitCancelFullScreen !== 'undefined') {
            document.webkitCancelFullScreen();
            return;
        }
        if (typeof document.mozCancelFullScreen !== 'undefined') {
            document.mozCancelFullScreen();
            return;
        }
    },
    is_full_screen: function () {
        if (typeof el.webkitRequestFullScreen !== 'undefined') {
            return document.webkitIsFullScreen;
        }
        if (typeof el.mozRequestFullScreen !== 'undefined') {
            return document.mozIsFullScreen;
        }
    },
    is_fs_supported: function () {
        if (typeof document.webkitIsFullScreen === 'undefined' && typeof document.mozCancelFullScreen === 'undefined') {
            return false;
        }
        return true;
    },
    full_screen: function () {
        if (this.is_fs_supported() === false) {
            return;
        }
        this.fs = this.get_state();
        if (this.fs === true) {
            this.cancel_fs();
            $("#map-container").removeClass("fullscreen");
            ngds.Map.map.invalidateSize();
            this.set_state(false);
        }
        else {
            this.request_fs($("#content-container")[0]);
            $("#map-container").addClass("fullscreen");
            ngds.Map.map.invalidateSize();
            this.set_state(true);
            var me = this;
            var key = setInterval(function () {
                if (document.webkitIsFullScreen === false) {
                    me.set_state(false);
                    $("#map-container").removeClass("fullscreen");
                    ngds.Map.map.invalidateSize();
                    clearInterval(key);
                }
            }, 500);
        }
    }
});
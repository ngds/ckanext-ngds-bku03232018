ngds.Zoom=L.Control.Zoom.extend({onAdd:function(b){var c="leaflet-control-zoom",a=L.DomUtil.create("div",c+" leaflet-bar");this._map=b;this._zoomInButton=this._createButton("","Zoom in",c+"-in",a,this._zoomIn,this);this._zoomOutButton=this._createButton("","Zoom out",c+"-out",a,this._zoomOut,this);b.on("zoomend zoomlevelschange",this._updateDisabled,this);return a}});
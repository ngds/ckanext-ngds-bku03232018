/*

var ngds = ngds || (ngds = { } );
/*
*	@author - Vivek Sunder
*	Hide a feature on the map if the zoom level is such that the layer's bounds exceed that of the map's. This is useful
*	when there are features that overlap and the user is unable to get to a feature that is below another.
*/

var zoom_handler = ngds.Map.zoom_handler = function(layer) {
	(function() { // Sanity Checks
		if(layer===null || typeof layer==='undefined') {
			throw "Invalid layer";
		}
	})();
	var layer = layer;
	var bounding_box_c = new ngds.Map.BoundingBox();
	bounding_box_c.construct_from_leaflet_shape(layer);
	var bbox = bounding_box_c.get_leaflet_bbox();

	layer._shown = true;
	var handlers = ngds.Map.handlers || ( ngds.Map.handlers = [ ] );
	var handler = function () {
		var map_bounds = ngds.Map.map.getBounds();				
		var map_miny = map_bounds._southWest.lat;
		var map_minx = map_bounds._southWest.lng;
		var map_maxy = map_bounds._northEast.lat;
		var map_maxx = map_bounds._northEast.lng;
		var bbox_miny = bbox._southWest.lat;
		var bbox_minx = bbox._southWest.lng;
		var bbox_maxy = bbox._northEast.lat;
		var bbox_maxx = bbox._northEast.lng;
		if((bbox_minx<map_minx) && (bbox_maxx>map_maxx) && (bbox_miny<map_miny) && (bbox_maxy>map_maxy) && layer._shown===true) {
			layer._shown = false;
			ngds.log("Hiding layer : "+layer,layer);
			ngds.Map.get_layer('geojson').removeLayer(layer);
		}
		else if((bbox_minx>map_minx) || (bbox_maxx<map_maxx) || (bbox_miny>map_miny) || (bbox_maxy<map_maxy) && layer._shown===false){
			ngds.log("Showing layer : "+layer,layer);
			ngds.Map.get_layer('geojson').addLayer(layer);	
			layer._shown = true;
		}
	}
	ngds.Map.map.on('zoomend',handler);
	ngds.Map.handlers.push(handler);
	ngds.log("Pushing zoom handler to : "+ngds.Map.handlers);
};

zoom_handler.clear_listeners = function() { // Unregister the zoom event handlers from the previous page.
	if(typeof ngds.Map.handlers!=='undefined') {
		for(var i=0;i<ngds.Map.handlers.length;i++) {
			ngds.Map.map.off('zoomend',ngds.Map.handlers[i]);
			ngds.log("Removing zoom handler");
		}
	}
	ngds.Map.handlers = [];
}
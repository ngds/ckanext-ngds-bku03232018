/*
*	@author - Vivek
*	Map functionality for the map page.
*/

$(document).ready(function() {
	ngds.Map.initialize();
	var southWest = new L.LatLng(-90, -180),
    northEast = new L.LatLng(90, 180),
    bounds = new L.LatLngBounds(southWest, northEast);
	ngds.Map.bounding_box = new ngds.Map.BoundingBox();
	ngds.Map.bounding_box.store_raw(bounds);
	ngds.Map.shape= {};
	ngds.Map.shape.str = 'rect';
	
	ngds.Map.map.on('draw:poly-created',function(e){
		// Clear the drawn items layers to get rid of rectangles drawn previously.
		
		if(ngds.Map.map.lock===true) {
			ngds.Map.removeZoomEventListeners();
		}
		else {
			ngds.Map.map.lock=true;
		}
		ngds.Map.clear_layer('drawnItems');
		// Add this layer to the map.
		ngds.Map.add_to_layer([e.poly],'drawnItems');
	
		var param_arr = [];
		// Get an array of coordinate pairs from this object.
		$.each(e.poly._latlngs,function(index,item){
				param_arr.push([item.lat,item.lng]);
		});
		// Get the packages that are within this polygon and display them all on the map.
		// TODO - Limit this to '8' results.
		ngds.Map.params = param_arr;
		// ngds.Map.map_search();
		ngds.Map.bounding_box = new ngds.Map.BoundingBox();
		ngds.Map.bounding_box.construct_from_leaflet_shape(e.poly);
		ngds.Map.shape.e = e;
		ngds.Map.shape.str='poly';
	});

	ngds.Map.map.on('draw:rectangle-created',function(e) {
		// Clear the drawn items layers to get rid of rectangles drawn previously.
		if(ngds.Map.lock===true) {
			ngds.Map.removeZoomEventListeners();
		}
		else {
			ngds.Map.map.lock=true;
		}
		ngds.Map.clear_layer('drawnItems');
		// Add this layer to the map.
		ngds.Map.add_to_layer([e.rect],'drawnItems');
		ngds.Map.bounding_box = new ngds.Map.BoundingBox();
		ngds.Map.shape.str = 'rect';
		ngds.Map.bounding_box.construct_from_leaflet_shape(e.rect);
		// ngds.Map.map_search();
		ngds.Map.shape.e = e;

	});

	
	
});
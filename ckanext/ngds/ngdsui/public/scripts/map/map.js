/*
*	@author - Vivek
*	Map functionality for the map page.
*/

$(document).ready(function() {
	ngds.Map.initialize();
	ngds.Map.map.on('draw:poly-created',function(e){
		// Clear the drawn items layers to get rid of rectangles drawn previously.
		ngds.Map.drawnItems.clearLayers();
		// Add this layer to the map.
		ngds.Map.add_to_layer([e.poly],'drawnItems');
		x = e.poly;
		// Clear the geojson layer to get rid of previous results.
		ngds.Map.clear_layer('geojson');

		var param_arr = [];
		// Get an array of coordinate pairs from this object.
		$.each(e.poly._latlngs,function(index,item){
				param_arr.push([item.lat,item.lng]);
		});
		// Get the packages that are within this polygon and display them all on the map.
		// TODO - Limit this to '8' results.
		ngds.ckanlib.dataset_poly_geo(param_arr,function(response){
			ngds.Map.add_packages_to_geojson_layer(response.results);
		});

	});

	ngds.Map.map.on('draw:rectangle-created',function(e) {
		// Clear the drawn items layers to get rid of rectangles drawn previously.
		ngds.Map.clear_layer('drawnItems');
		// Add this layer to the map.
		ngds.Map.add_to_layer([e.rect],'drawnItems');
		bounding_box = new ngds.Map.BoundingBox();
		bounding_box.construct_from_leaflet_rect(e.rect);
		// Find the packages that are within this rectangle and display them on the map.
		// TODO - Limit this to 8 resuls.
		ngds.ckanlib.dataset_geo(bounding_box,function(response){
			ngds.Map.add_packages_to_geojson_layer(response.results);

		});
		var bbox_bounds = bounding_box.get_leaflet_bbox();
		var _hidden = false;
		ngds.Map.map.on('zoomend',function(ev){
			var map_bounds = ngds.Map.map.getBounds();
			if(map_bounds.contains(bbox_bounds)) {
				if(!_hidden) {
					ngds.Map.drawnItems.addLayer(e.rect);
					_hidden=true;
				}
			}
			else {
				if(_hidden) {
					ngds.Map.drawnItems.removeLayer(e.rect);
					_hidden=false;
				}
				
			}
		});

	});
});
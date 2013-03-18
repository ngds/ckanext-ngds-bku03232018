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
		ngds.Map.drawnItems.addLayer(e.poly);
		// Clear the geojson layer to get rid of previous results.
		ngds.Map.geoJSONLayer.clearLayers();

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
		ngds.Map.drawnItems.clearLayers();
		// Add this layer to the map.
		ngds.Map.drawnItems.addLayer(e.rect);

		// Get the bounds.
		var minx = ngds.Map.utils.get_bound(e.rect._latlngs,'lng','min');
		var miny = ngds.Map.utils.get_bound(e.rect._latlngs,'lat','min');
		var maxx = ngds.Map.utils.get_bound(e.rect._latlngs,'lng','max');
		var maxy = ngds.Map.utils.get_bound(e.rect._latlngs,'lat','max');
		// Find the packages that are within this rectangle and display them on the map.
		// TODO - Limit this to 8 resuls.
		ngds.ckanlib.dataset_geo(minx,miny,maxx,maxy,function(response){
			ngds.Map.add_packages_to_geojson_layer(response.results);
		});
	});
});
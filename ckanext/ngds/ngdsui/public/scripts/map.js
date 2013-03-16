/*
*	@author - Vivek
*	Map functionality for the map page.
*/

$(document).ready(function() {
	var ngds = window.ngds || {};

	initialize_map();
	initialize_controls();

	/*
	*	Initialize the map, addition of controls and event handling for area selection.
	*/
	function initialize_map() {
		var base = new L.TileLayer('http://{s}.maptile.maps.svc.ovi.com/maptiler/v2/maptile/newest/normal.day/{z}/{x}/{y}/256/png8');
		var map = ngds.map = new L.Map('map-container', {layers:[base], center: new L.LatLng(34.1618, -111.53332), zoom: 3});
		var drawControl = new L.Control.Draw({
			position: 'topright',
			polyline: false,
			circle: false,
			marker:false,
			polygon:false
		});	
		
		// When a rectangle is drawn on the map, find packages that intersect with the rectangle and display them on the geoJSON layer.
		map.on('draw:rectangle-created', function (e) {
			
			drawnItems.clearLayers();
			drawnItems.addLayer(e.rect);
			
			var minx = get_bound(e.rect._latlngs,'lng','min');
			var miny = get_bound(e.rect._latlngs,'lat','min');
			var maxx = get_bound(e.rect._latlngs,'lng','max');
			var maxy = get_bound(e.rect._latlngs,'lat','max');
			
			ngds.geoJSONLayer.clearLayers();
			
			var package_ids = ngds.ckanlib.dataset_geo(minx,miny,maxx,maxy,function(response){
					$.each(response.results,function(index,package_id){
						ngds.ckanlib.package_show(package_id,function(response){
							try {
								var dataset = ngds.ckandataset(response.result);	
								var feature = dataset.getGeoJSON();
								var popup = dataset.map.getPopupHTML();
								}
								catch(e) {
									console.log(e);
									return;
								}																
								var geoJSONRepresentation = L.geoJson(feature);								
								geoJSONRepresentation.bindPopup(popup);
								geoJSONRepresentation.addTo(ngds.geoJSONLayer); 
						});
					});
			});

		
		});

		map.addControl(drawControl);
		var drawnItems = new L.LayerGroup();
		map.addLayer(drawnItems);
		ngds.geoJSONLayer = L.geoJson().addTo(map); // Geo JSON Layer where we'll display all our features.
		// map.addLayer(layer);
	}

	/*
	*	Get a specific bound - minx, miny, maxx, maxy.
	*	Input - coords 		- 	An array of coordinate pairs.
	*	Input - lat_or_lng 	- 	A string, either 'lat' or 'lng'
	*	Input - min_or_max	-	A string, either 'min' or 'max'
	*	Output - Either Math.min or Math.max applied to the coords(lat) or coords(lng)
	*/

	function get_bound(coords,lat_or_lng,min_or_max) {
		(function() {
			if(lat_or_lng!=='lat' && lat_or_lng!=='lng' || min_or_max!=='min' && min_or_max!=='max') {
				throw "Expected 'lat' or 'lng' for lat_or_lng and 'min' or 'max' for min_or_max"
			}
		})();

		var func = eval("Math."+min_or_max);
		var operands=[];
		$.each(coords,function(index,item){
			operands.push(item[lat_or_lng]);
		});
		return func.apply(this,operands);
	}

	
	/*
	*	Initialze custom controls for the map widget.
	*/

	function initialize_controls() {
		var html;
		// var html = '<div id="map-widget-control-menu">';
		// html+='<div id="layer-combo">';
		// html+='<p>Placeholder</p>';

		// html+='</div>'; //End of layer combo
		// // html+='<div id="layer-selector" class="not-implemented" style="display:none;">';
		// // html+='<p id="satellite-layer">Satellite</p>';
		// // html+='<p>Watercolor</p>';
		// // html+='</div>';
		
		// html+='<div id="basemap-combo">';
		// html+='<p>Placeholder</p>';
		// html+='</div>'; // End of basemap-combo
		
		// html+='</div>'; // End of map-widget-control-menu

		html+='<div id="map-expander">';
		html+='<p>&lt;&lt;</p>';
		html+='</div>'; // End of map-expander

		$("#map-container").append(html);
		var layer_combo_active = false;
		$("#layer-combo").click(function() {
			if(layer_combo_active===false) {
				$("#layer-selector").css('display','table');
				layer_combo_active = true;
			}
			else {
				$("#layer-selector").css('display','none');
				layer_combo_active = false;
			}
			
		});

		var expanded_flag = false;
		var original_map_container_size = $("#map-container").css("width");
		var expander_handle_unexpanded = '<p>&lt;&lt;</p>';
		var expander_handle_expanded='<p>&gt;&gt;</p>';
				
				$("#map-expander").click(function(){
					
					if(expanded_flag===false){	// If the resize handle is clicked, expand if not already expanded.
							expanded_flag=true;
							$(".map-search").hide();
							$("#map-container").css("width",1024);
							$("#map-expander").empty();
							$("#map-expander").append(expander_handle_expanded);
							ngds.map.invalidateSize();
					}
					else {
						expanded_flag=false;
						$("#map-container").css("width",original_map_container_size);
						ngds.map.invalidateSize();	
						$(".map-search").show();
						$("#map-expander").empty();
						$("#map-expander").append(expander_handle_unexpanded);
					}
					return false;
				});
	}


});
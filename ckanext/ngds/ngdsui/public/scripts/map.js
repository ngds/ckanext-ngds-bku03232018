$(document).ready(function() {
	var map = new L.Map("map-container", {
		center: new L.LatLng(40, -100),
		zoom: 4
	});			
	var layer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
					maxZoom: 18
	});

	map.addLayer(layer);

	var geoJSONLayer = L.geoJson().addTo(map); // Geo JSON Layer where we'll display all our features.
	window.geojsonlayer = geoJSONLayer;


	var html = '<div id="map-widget-control-menu">';
	html+='<div id="layer-combo">';
	html+='<p>Placeholder</p>';

	html+='</div>'; //End of layer combo
	// html+='<div id="layer-selector" class="not-implemented" style="display:none;">';
	// html+='<p id="satellite-layer">Satellite</p>';
	// html+='<p>Watercolor</p>';
	// html+='</div>';
	
	html+='<div id="basemap-combo">';
	html+='<p>Placeholder</p>';
	html+='</div>'; // End of basemap-combo
	
	html+='</div>'; // End of map-widget-control-menu

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

	// $("#satellite-layer").click(function() {
	// 	map.removeLayer(layer);
	// 	console.log("Removing layer");
	// });

		//  We don't have any programmatic control over the select tag even though there's a great deal of control over event-bubbling and handling. We'll
		//  need a custom element that looks and works like the selects here. 

	(function(){
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
							map.invalidateSize();
					}
					else {
						expanded_flag=false;
						$("#map-container").css("width",original_map_container_size);
						map.invalidateSize();	
						$(".map-search").show();
						$("#map-expander").empty();
						$("#map-expander").append(expander_handle_unexpanded);
					}
					return false;
				});

		var package_id_1, package_id_2, demo_feature_1, demo_feature_2;


		$.ajax({
				url:'/api/2/search/dataset/geo?bbox=-360,-360,360,360',
				type:"GET",
				dataType:"JSON",
				success:function(response){ // Get everything we have in the database with geocoded information
						
						$.each(response.results,function(index,eachPackageId){
							var ajax = $.ajax({
								type:"POST",
								data:"{\"id\":\""+eachPackageId+"\"}",
								url:'/api/action/package_show',
								dataType:'JSON',
								success:function(response){
									if(response.result===null || typeof response.result==='undefined'){
										return;
									}
									try {
										var dataset = ngds.CKANDataset(response.result);
										var feature = dataset.getGeoJSON();
										var popup = dataset.map.getPopupHTML();
									}
									catch(e) {
										console.log(e);
										return;
									}																
									var geoJSONRepresentation = L.geoJson(feature);								
									geoJSONRepresentation.bindPopup(popup);
									geoJSONRepresentation.addTo(map);
								}
							});
						});
				}
			});
	})();
});
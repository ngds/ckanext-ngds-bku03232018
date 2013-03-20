/*
*	@author - Vivek
*	This object exposes an API to interact with the NGDS map.
*
*/

ngds.Map = {
		/*	Initialize the map and display it on the UI.
		*	Inputs : None.
		*/
		initialize:function() {
			
			var base = new L.TileLayer('http://{s}.maptile.maps.svc.ovi.com/maptiler/v2/maptile/newest/terrain.day/{z}/{x}/{y}/256/png8');


			var powergrid = new L.AgsDynamicLayer();
			powergrid.initialize('https://eia-ms.esri.com/arcgis/rest/services/20130301StateEnergyProfilesMap/MapServer//export',
				{ 'layers':'show:21,22,26'});
			
			var map = this.map = new L.Map('map-container', {layers:[base], center: new L.LatLng(34.1618, -111.53332), zoom: 4});

			var _drawControl = new L.Control.Draw({
				position: 'topright',
				polyline: false,
				circle: false,
				marker:false,
				polygon:true
			});	
			map.addControl(_drawControl);
			var _drawnItems = ngds.Map.drawnItems = new L.LayerGroup();
			map.addLayer(_drawnItems);
			var _geoJSONLayer = this.geoJSONLayer = L.geoJson(); // Geo JSON Layer where we'll display all our features.


			this.layers = {
				'geojson':_geoJSONLayer,
				'drawnItems': _drawnItems
			};
			this.initialize_controls();

			var baseMaps = {
				"Terrain":base,
			};

			var overlayMaps = {				
				"Power Grid":powergrid,
				"Geo JSON":_geoJSONLayer
			};

			var layer_control = new L.control.layers(baseMaps, overlayMaps);
			layer_control.addTo(map);
		},
		/*	Initialize our NGDS specific custom controls. 
		*	Inputs : None.
		*/
		initialize_controls:function() {
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
									ngds.Map.map.invalidateSize();
							}
							else {
								expanded_flag=false;
								$("#map-container").css("width",original_map_container_size);
								ngds.Map.map.invalidateSize();	
								$(".map-search").show();
								$("#map-expander").empty();
								$("#map-expander").append(expander_handle_unexpanded);
							}
							return false;
						});
			},
		/*	Add a list of features to a particular layer on the map.
		*	Inputs : A list of features and a key that identifies the layer.
		*/
		add_to_layer:function(features,layer_str) {
			var me = this;
			if(layer_str in this.layers && features.length>0) {
				$.each(features,function(index,feature){
					feature.addTo(me.layers[layer_str]);
				});
			}
		},
		/*	Clear a layer using it's key.
		*	Inputs : A key that identifies the layer that is to be cleared.
		*/
		clear_layer:function(layer_str){
			this.layers[layer_str].clearLayers();
		},
		/*	Add a list of ckan packages to the map. 
		*	Inputs : A list of package ids.
		*/
		add_packages_to_geojson_layer:function(package_ids) {
			var me = this;
			$.each(package_ids,function(index,package_id){
				var geojson = ngds.ckanlib.package_show(package_id,function(response){
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
							me.add_to_layer([geoJSONRepresentation],'geojson');
					});
			});
		},
		manage_zoom:function(bounding_box,layer) {
			var bbox_bounds = bounding_box.get_leaflet_bbox();
			var _hidden = false;
			var _ev = function(ev) {
				var map_bounds = ngds.Map.map.getBounds();
				if(map_bounds.contains(bbox_bounds)) {
					if(!_hidden) {
						ngds.Map.drawnItems.addLayer(layer);
						_hidden=true;
					}
				}
				else {
					if(_hidden) {
						ngds.Map.drawnItems.removeLayer(layer);
						_hidden=false;
					}
				}
			};
			ngds.Map.zoom_listener = _ev;
			ngds.Map.map.on('zoomend',_ev);
		},
		removeZoomEventListener:function() {
			ngds.Map.map.removeEventListener('zoomend',ngds.Map.zoom_listener);
		},
		// Exposes a set of utility functions to work with the map.
		utils:{
			/*
			*	Takes a list of coordinate pairs and returns a specific upper or lower bound of the bounding box for this shape.
			*	Inputs : A list of coordinate pairs, a string that is either 'lat' or 'lng', a string that is either 'min' or 'max'
			*	For ex : To get the lower bound for a bounding box, pass in the coordinates, 'lat','min' and coordinates, 'lng','min'.
			*/
			get_bound:function (coords,lat_or_lng,min_or_max) {
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
		},
		register_map_query_provider:function(id_provider) {
			// Validate inputs.
			(function(){
				if(id_provider===null || typeof id_provider === 'undefined') {
					throw "Expected a string for id_provider.";
				}
			})();
			
			this.query_provider = "#"+id_provider;
		},
		set_search_mode:function(mode) {

			(function() {
				if(mode === null || typeof mode === 'undefined') {
					throw "Allowed modes are 'search' and 'filter'";
				}
			})();

			this.mode = mode;
		},
		get_search_mode:function() {
			return this.mode;
		},




	};
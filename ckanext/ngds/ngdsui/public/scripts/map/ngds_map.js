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

			var wells = L.tileLayer.wms("http://geothermal.smu.edu/geoserver/wms", {
			    layers: 'wells',
			    format: 'image/png',
			    transparent: true,
			    attribution: "SMU Well Data"
			});

			// ngds_layer = L.tileLayer.wms("http://localhost:8080/geoserver/NGDS/wms",{
			// 	layers:"NGDS:45276b7a-4335-4548-aa92-e82ffbbde56f",
			// 	format: 'image/png',
			//     transparent: true,
			//     attribution: "NGDS",
			//     opacity:'0.9999'
			// });
			var _geoJSONLayer = this.geoJSONLayer = L.geoJson(); // Geo JSON Layer where we'll display all our features.
			var map = this.map = new L.Map('map-container', {layers:[base,_geoJSONLayer], center: new L.LatLng(34.1618, -100.53332), zoom: 3});

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
		
			this.layers = {
				'geojson':_geoJSONLayer,
				'drawnItems': _drawnItems,
				'powergrid':powergrid
			};
			this.initialize_controls();

			var baseMaps = {
				"Terrain":base,
			};

			overlayMaps = {				
				"Power Grid":powergrid,
				"Geo JSON":_geoJSONLayer,
				"Wells":wells,
				// "ngds":ngds_layer
			};

			layer_control = new L.control.layers(baseMaps, overlayMaps,{autoZIndex:true});
			layer_control.addTo(map);

			map.on('layeradd',function(lev) { // Every time a layer is added or removed, make sure our geojson layer is the top-most one.
				try {
					_geoJSONLayer.bringToFront();
				}
				catch(e){
					// Do nothing because we know that there will be an error when this layer is hidden on the map.
				}
			});
			copy = [];


			// this.initialize_map_search();
		},
		zoom_managed_list:{
		
		},
		zoom_listeners:[

		],
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
		map_search:function() {
			var me = this;
			// this.removeZoomEventListeners();0
			// this.bind_zoom_listeners();

			// this.clear_layer('geojson');
			geoj = me.get_layer('drawnItems');

			var query = $("#map-query").val();
			var pager = ngds.Pager(5);

			pager.set_action(ngds.ckanlib.package_search,{ 'q':query });
			if(ngds.Map.shape.str=='rect') {
				// ngds.Map.manage_zoom(ngds.Map.bounding_box,ngds.Map.shape.e.rect,ngds.Map.get_layer('drawnItems'));
			}
			else {
				// ngds.Map.manage_zoom(bounding_box,ngds.Map.shape.e.poly,ngds.Map.get_layer('drawnItems'));
			}
			pager.move(1,function(search_result) {
				var count = search_result.get('count');				
				var raw_result = search_result.raw();
				me.clear_layer('geojson');
				pager.set_state(count,query);

				for(index in raw_result.results) {
				 	ngds.Map.add_raw_result_to_geojson_layer(raw_result.results[index]);
				 }

			});
			
			// ngds.ckanlib.package_search({ "q":query },function(response) {
			// 	console.info(response.result);
			// 	var search_result = x = ngds.SearchResult(response.result);
			// 	ngds.Map.SearchContext.set_preamble_count(search_result.get('count'));
			// 	ngds.Map.SearchContext.set_results(response.result.results);
			// });
		},
		get_layer:function(key) {
			if(key in this.layers) {
				return this.layers[key];
			}
			throw "No layer exists with the key : "+key;
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
				ngds.ckanlib.package_show(package_id,function(response){
						me.add_raw_result_to_geojson_layer(response.result);
				});
			});
		},
		add_raw_result_to_geojson_layer:function(result) { // Expects response.result, not response.
			try {				
				var dataset = ngds.ckandataset(result);	
				x=dataset;
				var feature = dataset.getGeoJSON();				
				var popup = dataset.map.getPopupHTML();
			}
			catch(e) {
				return;
			}															
			var geoJSONRepresentation = L.geoJson(feature);		
			geoJSONRepresentation.bindPopup(popup);
			this.add_to_layer([geoJSONRepresentation],'geojson');
		},
		bind_zoom_listeners:function() {
			var _ev = function(ev) {	
				var map_bounds = ngds.Map.map.getBounds();				
				var map_sw_lat = map_bounds._southWest.lat;
				var map_sw_lng = map_bounds._southWest.lng;
				var map_ne_lat = map_bounds._northEast.lat;
				var map_ne_lng = map_bounds._northEast.lng;
				var layers = ngds.Map.zoom_managed_list;
				console.log(layers);
				for(var i in ngds.Map.zoom_managed_list) {
					var lid=layers[i]._leaflet_id;
						var bbox_sw_lat = layers[i].bbox_bounds._southWest.lat;
						var bbox_sw_lng = layers[i].bbox_bounds._southWest.lng;
						var bbox_ne_lat = layers[i].bbox_bounds._northEast.lat;
						var bbox_ne_lng = layers[i].bbox_bounds._northEast.lng;
						console.log(layers[i]);

						if((map_sw_lat>bbox_sw_lat) && (map_sw_lng>bbox_sw_lng) && (map_ne_lat<bbox_ne_lat) && (map_ne_lng<bbox_ne_lng)) {
							if(layers[i]._shown) {
								layers[i].parent.removeLayer(layers[i].layer);
								layers[i]._shown=false;
							}
						}
						else {
							if(!layers[i]._shown) {
								layers[i].parent.addLayer(layers[i].layer);
								layers[i]._shown=true;
							}
						}
					}
			};
			ngds.Map.map.on('zoomend',_ev);
			ngds.Map.zoom_listeners.push(_ev);
		},
		manage_zoom:function(bounding_box,layer,parent) {
			var bbox_bounds = bounding_box.get_leaflet_bbox();
			ngds.Map.zoom_managed_list[layer._leaflet_id] = { };
			ngds.Map.zoom_managed_list[layer._leaflet_id].bbox_bounds = bbox_bounds;
			ngds.Map.zoom_managed_list[layer._leaflet_id].parent = parent;
			ngds.Map.zoom_managed_list[layer._leaflet_id]._shown = false;
			ngds.Map.zoom_managed_list[layer._leaflet_id].layer = layer;
		},
		removeZoomEventListeners:function() {
			$.each(ngds.Map.zoom_listeners,function(index,item) {
				ngds.Map.map.removeEventListener('zoomend',item);				
			});
			ngds.Map.zoom_listeners = [];
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
/*
*	@author - Vivek
*	@revised by Adrian 7/2013
*	This object exposes an API to interact with the NGDS map.
*
*/

ngds.Map = {
		/*	Initialize the map and display it on the UI.
		*	Inputs : None.
		*/
		initialize:function() {

			var nerc_url = "https://eia-ms.esri.com/arcgis/rest/services/20130301StateEnergyProfilesMap/MapServer/"; //layer 42
			var geothermal_potential_url = "https://eia-ms.esri.com/arcgis/rest/services/20130301StateEnergyProfilesMap/MapServer/"; //layer 36
			var counties_url = "https://eia-ms.esri.com/arcgis/rest/services/20130301StateEnergyProfilesMap/MapServer/"; //layer 1
			var powergrid_url = "https://eia-ms.esri.com/arcgis/rest/services/20130301StateEnergyProfilesMap/MapServer/"; //layers 21,22,26
			var weather_url = "https://gis.srh.noaa.gov/ArcGIS/rest/services/RIDGERadar/MapServer/"; //layer 0
			var soil_url = "http://services.arcgisonline.com/ArcGIS/rest/services/Specialty/Soil_Survey_Map/MapServer/"; //layer ?
			var water_url = "http://basemap.nationalmap.gov/ArcGIS/rest/services/USGSTopo/MapServer/";

			var base = new L.TileLayer('http://{s}.maptile.maps.svc.ovi.com/maptiler/v2/maptile/newest/terrain.day/{z}/{x}/{y}/256/png8');

			var map = this.map = new L.Map('map-container', {
				layers:[base],
				center: new L.LatLng(34.1618, -100.53332),
				zoom: 3,
				zoomControl:false
			});
			var nerc_wms = new L.tileLayer.wms(nerc_url, {
				layers:42,
				format:"image/png",
				transparent:true
			});
			var geothermal_potential_wms = new L.tilelayer.wms(geothermal_potential_url, {
				layers:36,
				format:"image/png"
			});
			var counties_wms = new L.tilelayer.wms(counties_url, {
				layers:1,
				format:"image/png"
			});
			var powergrid_wms = new L.tilelayer.wms(powergrid_url, {
				layers:[21,22,26],
				format:"image/png"
			});
			var weather_wms = new L.tilelayer.wms(weather_url, {
				layers:0,
				format:"image/png"
			});
/*
			var nerc_wms = new L.esri.dynamicMapLayer(nerc_url, {
				opacity:1,
				layers:42
			});

			var geothermal_potential_wms = new L.esri.dynamicMapLayer(geothermal_potential_url, {
				opacity:1,
				layers:36
			});

			var counties_wms = new L.esri.dynamicMapLayer(counties_url, {
				opacity:1,
				layers:1
			});

			var powergrid_wms = new L.esri.dynamicMapLayer(powergrid_url, {
				opacity:1,
				layers:[21,22,26]
			});

			var weather_wms = new L.esri.dynamicMapLayer(weather_url, {
				opacity:1,
				layers:0
			});

			var soil_wms = new L.esri.dynamicMapLayer(soil_url, {
				opacity:0,
				layers:?
			});

			var water_wms = new L.esri.dynamicMapLayer(water_url, {
				opacity:0,
				layers:?
			});
			*/

			var soil = new L.tileLayer.wms('http://geo.cei.psu.edu:8080/geoserver/wms',{
				format:'image/png',
				transparent:true,
				attribution:'US Soil Survey',
				layers:'cei:canada,cei:mexicarib,cei:mlra_48,cei:lower48',
				styles:'other_polygons,other_polygons,llrShadeTest_opaque,state_noFill',
				srs:'srs:EPSG:102003'
			});

			var wells = L.tileLayer.wms("http://geothermal.smu.edu/geoserver/wms", {
				layers: 'wells',
				format: 'image/png',
				transparent: true,
				attribution: "SMU Well Data"
			});

			var land = L.tileLayer.wms('http://www.geocommunicator.gov/arcgis/services/Basemaps/MapServer/WMSServer',{
				layers:'0,1,3,4,5,6,7,8,9,10,11,12,13,14,15',
				format:'image/png',
				transparent:true
			});

			var topography = new L.TileLayer('http://basemap.nationalmap.gov/ArcGIS/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}');

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

			new L.Control.GeoSearch({
				provider: new L.GeoSearch.Provider.OpenStreetMap()
			}).addTo(map);

			this.layers = {
//				'geojson':_geoJSONLayer,
				'drawnItems': _drawnItems,
				'powergrid':powergrid_wms,
				'soil':soil,
//				'water':water_wms,
				'land':land,
				'topography':topography,
				'nerc':nerc_wms,
				'geothermal_potential':geothermal_potential_wms,
				'counties':counties_wms,
				'weather':weather_wms
			};
			// this.initialize_controls();

			var baseMaps = {
				"Terrain":base,
				"US Topographic Map":topography,
				'Soil Extent Map':soil
			};

			overlayMaps = {				
				"Power Grid":powergrid_wms,
//				"Search Results":_geoJSONLayer,
				"SMU Wells":wells,
				'USBLM Urban Areas, Counties':land,
				'NERC Regions':nerc_wms,
				'Geothermal Potential':geothermal_potential_wms,
				'US County Boundaries':counties_wms,
				'NEXRAD Weather':weather_wms
				// "ngds":ngds_layer
			};
			var zoomFS = new L.Control.ZoomFS({
				'position':'topright'
			});
			map.addControl(zoomFS);

			layer_control = new L.control.layers(baseMaps, overlayMaps,{autoZIndex:true});
			layer_control.addTo(map);
		}
   };
/*
ngds.Map.BoundingBox = function() {
	this.construct_from_leaflet_shape = function(leaflet_shape) {
		this.minx = ngds.Map.utils.get_bound(leaflet_shape._latlngs,'lng','min');
		this.miny = ngds.Map.utils.get_bound(leaflet_shape._latlngs,'lat','min');
		this.maxx = ngds.Map.utils.get_bound(leaflet_shape._latlngs,'lng','max');
		this.maxy = ngds.Map.utils.get_bound(leaflet_shape._latlngs,'lat','max');
		this.type='custom';
	};

	this.store_raw=function(raw_bbox) {
		this.minx = raw_bbox._southWest.lng;
		this.miny = raw_bbox._southWest.lat;
		this.maxx = raw_bbox._northEast.lng;
		this.maxy = raw_bbox._northEast.lat;
		this.raw = raw_bbox;
	};

	this.get_leaflet_bbox=function() {
		if(this.type==='custom') {
			var south_west = new L.LatLng(this.miny,this.minx);
			var north_east = new L.LatLng(this.maxy,this.maxx);
			return new L.LatLngBounds(south_west,north_east);
		}
		else {
			return this.raw;
		}
	};

	this.get_bbox_array=function() {
		return [this.minx,this.miny,this.maxx,this.maxy];
	};

	this.get_minx=function() {
		return this.minx;
	};

	this.get_miny=function() {
		return this.miny;
	};

	this.get_maxx=function() {
		return this.maxx;
	};

	this.get_maxy=function() {
		return this.maxy;
	};

	this.get_min_lat=function() {
		return this.miny;
	};

	this.get_min_lng=function() {
		return this.minx;
	};

	this.get_max_lat=function() {
		return this.maxy;
	};

	this.get_max_lng=function() {
		return this.maxx;
	}
};
*/
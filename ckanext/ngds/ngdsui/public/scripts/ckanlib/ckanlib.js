/*
*	@author - Vivek
*	A set of functions to make ajax calls to the CKAN API.
*/

ngds.ckanlib = {
	/*
	*	Perform a POST to get the list of packages that are contained in a bounding rectangle.
	*	Inputs : minx, miny, maxx, maxy and a callback function.
	*/
	dataset_geo:function(bbox,callback) {
		var url_pre = '/api/2/search/dataset/geo?bbox=';
		
		// Validate inputs.
		if(!typeof bbox === 'object') {
			throw "Parameter bbox : Expected a BoundingBox Object.";
		}

		$.each(bbox.get_bbox_array(),function(index,v) {
			(function(v){ // Throw an error if we didn't receive all the required parameters.
				if(v === null || typeof v === 'undefined') {
					throw "Missing parameter : Expected minx,miny,maxx,maxy.";
				}
			})(v);
		});

		(function(){
			if(typeof callback !== 'function') {
				throw "Missing parameter : Expected callback function.";
			}
		})();

		// Construct the url for the GET call.
		var url = url_pre+bbox.get_bbox_array().join(',');

		// Make the GET call and perform the callback.
		$.ajax({
			url:url,
			type:'GET',
			dataType:'JSON',
			success:function(response){
				return callback(response);
			}
		});

	},
	/*
	*	Perform a call to get the list of packages that are within a polygonal region.
	*	Inputs : An array of coordinate pairs that correspond to the polygonal region and a callback function.
	*/
	dataset_poly_geo:function(poly_params,callback) {
		
		(function() {
			if(poly_params===null || typeof poly_params === 'undefined') {
				throw "Missing parameter : Expected an array of coordinates representing a polygon.";
			}
			if(typeof callback !== 'function') {
				throw "Missing parameter : Expected callback function.";
			}
		})();

		if(poly_params.length===0) {
			return;
		}

		var url = '/poly';
		var data = {
			'data':JSON.stringify({
				'poly':poly_params
			})
		};
		var type = 'POST';

		$.ajax({
			url:url,
			data:data,
			success:function(response){
				return callback(response);
			}
		});
	},
	/*
	*	Query a package by its id.
	*	Input : A package id and a callback.
	*/
	package_show:function(package_id,callback) {
		
		// Validate input.
		(function(){	
			if(package_id===null || typeof package_id === 'undefined') {
				throw "Missing parameter : Expected package_id.";
			}
			if(typeof callback !== 'function') {
				throw "Missing parameter : Expected callback function.";
			}
		})();

		// URl and data required for the POST call.
		var url = '/api/action/package_show';
		var data = JSON.stringify({
			id:package_id
		});

		// Make the POST call and perform the callback.
		$.ajax({
			url:url,
			type:'POST',
			dataType:'JSON',
			data:data,
			success:function(response) {
				return callback(response);
			}
		});
	},
	/*
	*	Do a package search query. 
	*	Input : Parameter object with keys that make sense. Currently the only one that makes sense is 'extras'. And a callback.
	*/
	package_search:function(parameter_obj,callback) {
		// Validate inputs.
		(function() {
			if(parameter_obj!==null && typeof parameter_obj!=='undefined') {
				// The parameter object is optional, but if supplied, must be an object.
				if(typeof parameter_obj==='undefined') { 
					throw "Expected an object as the second parameter.";
				}
			}

			if(typeof callback !== 'function') {
				throw "Expected a callback function.";
			}
		})();

		var url = '/api/action/package_search';
		var type = 'POST';
	
		var data = { 'sort':'' };
		
		for(key in parameter_obj) {
			if(parameter_obj[key]!==null && typeof parameter_obj[key]!== 'undefined') {
				data[key] = parameter_obj[key];
			}
		}

		$.ajax({
			url:url,
			type:type,
			dataType:'JSON',
			data:JSON.stringify(data),
			success:function(response) {
				return callback(response);
			}
		});

	},
	get_responsible_party:function(id,callback) {
		(function() {
			if(id===null || typeof id==='undefined') {
				throw "Expected valid id";
			}
			if(typeof callback!=='function') {
				throw "Expected callback function";
			}
		})();

		var url = '/api/action/additional_metadata';
		var model = "ResponsibleParty";
		var process = "read";
		var data = {
			"model":model,
			"process":process,
			"data":{
				"id":id
			}
		};
		$.ajax({
			url:url,
			data:data,
			success:function(response) {
				return callback(response);
			}
		});
	}
}
/*
*	@author - Vivek
*	A set of functions to make ajax calls to the CKAN API.
*/

ngds.ckanlib = {
	dataset_geo:function(minx,miny,maxx,maxy,callback) {
		var url_pre = '/api/2/search/dataset/geo?bbox=';
		
		// Validate inputs.
		$.each([minx,miny,maxx,maxy],function(index,v) {
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
		var url = url_pre+[minx,miny,maxx,maxy].join(',');

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
	}
}
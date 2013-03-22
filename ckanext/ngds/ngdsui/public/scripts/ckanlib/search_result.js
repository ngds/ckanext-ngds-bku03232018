ngds.SearchResult = function(raw_result) {
	(function() {
		if(raw_result===null || typeof raw_result==='undefined') {
			throw "Expected raw_result to not be null or undefined.";
		}
	})();

	var from_ckanlib;

	if(this.ckanlib!==null && typeof this.ckanlib !== 'undefined') {
		from_ckanlib=function(params) {
			var response_container = function(response) {
				return response;
			};

			var func_dict = {
				'author':this.ckanlib.get_responsible_party,
				'maintainer':this.ckanlib.get_responsible_party
			};

			return func_dict[params['type']](params['id'],response_container);
		}		
	}
	else {
		from_ckanlib=function(param,key) {
			return null;
		}
	}

	var func_map = {
		'count':raw_result.count,
		'author_email':raw_result.author_email,
		'id':raw_result.id,
		'maintainer':from_ckanlib
	}

	return {
		get:function() {
			var params_set = false;
			var params = { }, key;
			for(argument in arguments) {
				if(typeof arguments[argument]==="object") {
					params_set = true;
					params = arguments[argument];
				}
				else {
					key = arguments[argument];
				}
			}
			if(params_set === false) {
				console.info("search_result > get : ","Got : ",key);
				return func_map[key];
			}
			return func_map[key](params)
		},
		raw:function() {
			return raw_result;
		}
	};
};

(function(ckanlib) {
	ngds.SearchResult.ckanlib = ckanlib;
})(ngds.ckanlib);
/**
*	@author - Vivek
*	Pager to page search results for the map.
*/
ngds.Pager = function(rows) {
	// Must keep in mind to clear the dom each time.

	var start = 0;
	var rows = rows;
	var num_pages = 0;
	var pager_div = $(".search-results-page-nums");
	pager_div.empty();
	var me = this;
	var handler = null;
	var cur_page = 0;

	var preamble = $(".preamble");
	this.set_state = function(count,query) {

		preamble.empty();
		preamble.text("Found $1 results for \"$2\"".replace("$1",count).replace("$2",query));
	};

	this.set_action = function(action, params) {
		(function() {
			if(typeof action !== 'function') {
				throw "Expected a function";
			}
		})();

		me._action = action;
		me._params = params;
	};

	var construct_anchor = function(i) {
		var anchor = $("<a/>",{class:"page-num"});
		anchor.text(i);
		return anchor;
	};

	var initialize_pages_ui = function(n) {
		for(var i=1;i<n+1;i++) {
			pager_div.append(construct_anchor(i));
		}
		$(".page-num").click(function(ev){
			var page_number = ev.target.firstChild.data;
			me.move(page_number,handler);
		});
	};

	var clear_results_div = function() {
		$(".results").empty();
	};

	this.move = function(page_number,fn) {
		handler = fn;
		start = (page_number - 1) * rows;

		if(start>(num_pages*rows+1)) {
			return;
		}

		var params = me._params;
		params['rows'] = rows;
		params['start'] = start;
		if(ngds.Map.shape!==null && typeof ngds.Map.shape !== 'undefined') {
			if(ngds.Map.shape==='rect') {
				params['extras'] = { "ext_bbox":ngds.Map.bounding_box.get_bbox_array().join(',')};		
			}
			else {
				params['extras'] = { 'poly':ngds.Map.params }
			}
			
		}
		
		me._action(params,function(response){
			var result = ngds.SearchResult(response.result);
			if(response.result.results.length<rows) {
				rows = response.result.results.length;	
			}
			num_pages = Math.ceil(result.get('count')/rows);
			
			clear_results_div();
			var results_div = $(".results");

			var results = response.result.results;

			for(var i=0;i<results.length;i++){
				var each_result = $("<div/>",{class:"result"});
				var title = $('<p/>',{class:'description'});
				var notes = $('<p/>',{class:'notes'});
				var type = $('<p/>',{class:'type'});
				var published = $('<p/>',{class:'published'});
				published.attr('id','ngds'+i);

				notes.text(results[i]['notes']);
				title.text(results[i]['title']);
				type.text(results[i]['type']);
				published.text(new Date(results[i]['metadata_created']).toLocaleDateString());
				
				each_result.append(title);
				each_result.append(notes);
				each_result.append(type);
				each_result.append(published);
				results_div.append(each_result);
			}

			if($('.page-num').length==0) {
				initialize_pages_ui(num_pages);
			}
			return fn(result);
		});

		start = start + rows;
	};


	return {
		'set_state':this.set_state,
		'set_action':this.set_action,
		'move':this.move,
		'is_defined':this.is_defined
	};
};
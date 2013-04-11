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

	this.move = function(page_number,fn,finish_fn) {
		handler = fn;
		ngds.Map.labeller.reset();
		start = (page_number - 1) * rows;
		// ngds.Map.removeZoomEventListeners();
		if(start>(num_pages*rows+1)) {
			return;
		}

		var params = me._params;
		params['rows'] = rows;
		params['start'] = start;
		if(ngds.Map.shape.str!==null && typeof ngds.Map.shape.str !== 'undefined') {
			if(ngds.Map.shape.str==='rect') {
				params['extras'] = { "ext_bbox":ngds.Map.bounding_box.get_bbox_array().join(',')};		
			}
			else {
				params['extras'] = { 'poly':ngds.Map.params }
			}
			
		}
		
		me._action(params,function(response){
			var result = ngds.SearchResult(response.result);
			var rows_to_req = 0;
			if(response.result.results.length<rows) {
				rows_to_req = response.result.results.length;	
			}
			else {
				rows_to_req = rows;
			}
			num_pages = Math.ceil(result.get('count')/rows_to_req);
			
			clear_results_div();
			var results_div = $(".results");

			var results = response.result.results;
			for(var i=0;i<results.length;i++){
				var each_result = $("<div/>",{class:"result"});
				var title = $('<a/>',{class:'description',href:['/dataset',results[i].name].join('/'),target:"_blank"});
				
				var notes = $('<p/>',{class:'notes'});
				var type = $('<p/>',{class:'type'});
				var wms = $('<button/>',{class:'wms',id:results[i]['resources'][0].id});
				var published = $('<p/>',{class:'published'});
				
				var marker_or_shape='';
				if(ngds.ckandataset(results[i]).get_feature_type().type==='Point'){
					var label = ngds.Map.labeller.get_label();
					each_result.addClass('result-'+label);
					var marker_container = $("<div/>",{class:'result-marker-container marker-'+label});
					var marker_image = $("<img/>",{src:"/images/marker.png",class:'result-marker'});
					var marker_label = $("<span/>",{class:'result-marker-label marker-label-'+label});
					marker_label.text(label);
					marker_container.append(marker_image);
					marker_container.append(marker_label);
					each_result.append(marker_container);
					marker_or_shape='marker'
				}
				else if (ngds.ckandataset(results[i]).get_feature_type().type==='Polygon'){
					var label = ngds.Map.labeller.get_label();
					each_result.addClass('result-'+label);
					marker_or_shape='shape'
				}
				published.attr('id','ngds'+i);
				notes.text(results[i]['notes']);
				title.text(results[i]['title']);
				type.text(results[i]['type']);
				wms.text("WMS");
				published.text(new Date(results[i]['metadata_created']).toLocaleDateString());
			
				each_result.append(title);
				each_result.append(notes);
				each_result.append(type);
				each_result.append(wms);
				each_result.append(published);
				results_div.append(each_result);
				fn(results[i],marker_or_shape);
			}
			inc = 1;
			$(".wms").click(function(ev){
				var id=ev.currentTarget.id;
						var ngds_layer = L.tileLayer.wms("http://ec2-184-72-146-8.compute-1.amazonaws.com:8080/geoserver/NGDS/wms",{
						layers:"NGDS:"+id,
						format: 'image/png',
					    transparent: true,
					    attribution: "NGDS",
					    opacity:'0.9999'
					});

				layer_control.addOverlay(ngds_layer,"WMS"+inc);
				inc++;
			});

			if($('.page-num').length==0) {
				initialize_pages_ui(num_pages);
			}
			return finish_fn(response.result.count);
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
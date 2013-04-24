/*
*	@author - Vivek Sunder
*	This is the top-level control module for the NGDS map.
*/

var ngds = ngds || ( ngds= { } );

(function setup_debugging(){
	if(window.document.location.hash==="#!debug") {
		
		ngds.log = function(msg,last_log) {
			ngds.last_log = last_log;
			console.log(msg);
		};

		ngds.error = function(msg,last_error) {
			ngds.last_error = last_error;
			console.error(msg);
		};

	}
	else {
		
		ngds.log = function(msg,last_log) {
			ngds.last_log = last_log;
			// swallow it.
		};

		ngds.error = function(msg,last_error) {
			ngds.last_error = last_error;
			// swallow it.
		}

	}
})();

ngds.publish = function(topic,msg) {
	ngds.log("Published message : "+msg+" to topic : "+topic,msg);
	PubSub.publish(topic,msg);
};

ngds.subscribe = function(topic,handler) {
	ngds.log("Subscribed to topic : "+topic+" with handler : "+handler,handler);
	PubSub.subscribe(topic,handler);
}

ngds.feature_event_manager = { //A container for state information on event bindings for features.
		/*
		*	Scheme - id -> { 
		*					'feature':feature,
		*					'type':'Marker'||'Feature'
		*					'seq_id':seq_id
		*					'mouseover':mouseover_handler,
		*					'mouseout':mouseout_handler,
		*					'add':add_handler
		*					'remove':remove_handler
		*					}
		*/
}; 

ngds.layer_map = { // A mapping table to map ngds result ids(dom) to leaflet ids which we'll use with the feature_event_manager.
	/*
	*	Scheme - ngds_id -> leaflet_id
	*
	*
	*/
};

/*
* 	Publish module
*/ 	

ngds.Map.initialize();


(function publish_pager_advance() {
	$("#map-search").click(function(){
		ngds.publish('Map.search_initiated',{

		});
		var geoj = ngds.Map.get_layer('drawnItems');
		var query = $("#map-query").val();
		ngds.pager.go_to({
			'page':1,
			'action':ngds.ckanlib.package_search,
			'rows':5,
			'q':query
		});
	});

	$(".page-num").click(function(ev){
			var page = ev.target.firstChild.data;
			ngds.publish('page.advance',{ 'page':page });
		});
})();


/*
*	Subscribe module
*/ 

(function subscribe_page_advance() {
	ngds.pager = new ngds.Search();

	ngds.subscribe('page.advance',function(msg,data) {
		ngds.feature_ngds_id_mapping = {
			// Clearing the state table.
		};
		ngds.Map.clear_layer('geojson');
		ngds.Map.zoom_handler.clear_listeners();
		pager.go_to({
			'page':data['page'],
			'action':ngds.ckanlib.package_search,
			'rows':5
		});
	});
})();


ngds.Map.map.on('draw:rectangle-created',function(e) {
	ngds.Map.clear_layer('drawnItems');
	ngds.Map.add_to_layer([e.rect],'drawnItems');

	ngds.publish("Map.area_selected",{ 
		'type':'rectangle',
		'feature':e
	});
});

ngds.Map.map.on('draw:poly-created',function(e){
	ngds.Map.clear_layer('drawnItems');
	ngds.Map.add_to_layer([e.poly],'drawnItems');

	ngds.publish("Map.area_selected",{
		'type':'polygon',
		'feature':e
	});
});


(function subscribe_feature_received(){
	ngds.subscribe('Map.feature_received',function(topic,data){
		ngds.Map.add_raw_result_to_geojson_layer(data['feature'],{'seq':data['seq']});
	});

	$('.results').on('mouseover',null,function(ev){
		var tag_index = ngds.util.node_matcher(ev.srcElement,/result-\d.*/);
		if(tag_index===null) {
			ngds.error("Got null tag for mouseover");
			return;
		}

		var feature = ngds.layer_map[tag_index];
		ngds.publish('Layer.mouseover',{
			'Layer':feature,
			'tag_index':tag_index
		});

	});

	$('.results').on('mouseout',null,function(ev){
		var tag_index = ngds.util.node_matcher(ev.srcElement,/result-\d.*/);
		
		if(tag_index===null) {
			ngds.error("Got null tag for mouseout");
			return;
		}

	 	var feature = ngds.layer_map[tag_index];
	 	
	 	ngds.publish('Layer.mouseout',{
	 		'Layer':feature,
	 		'tag_index':tag_index
	 	});
		
	});

	$('.results').on('click',null,function(ev){
		var tag_index = ngds.util.node_matcher(ev.srcElement,/result-\d.*/);
		
		if(tag_index===null) {
			return;
		}
		
		ngds.Map.reset_styles(tag_index);
		var feature = ngds.layer_map[tag_index];
	 	ngds.publish('Layer.click',{
	 		'Layer':feature,
	 		'tag_index':tag_index
	 	});

	});
})();

(function setup_styler_for_features(){
	/*
	*	This is really where all the events on features are bound regardless of how they are initiated. No events should directly be bound on features except through
	*	here. This lets us use our own events as a forwarding mechanism that lead to these functions below.
	*
	*
	*/
	ngds.subscribe('Layer.mouseover',function(topic,data){
		var is_active = data['Layer'].is_active || null;
		if(is_active === null || is_active===false) {
			ngds.util.apply_feature_hover_styles(data['Layer'],data['tag_index'])
		}
	});

	ngds.subscribe('Layer.mouseout',function(topic,data){
		var is_active = data['Layer'].is_active || null;
		if(is_active === null || is_active===false) {
			ngds.util.apply_feature_default_styles(data['Layer'],data['tag_index']);
		}
	});

	ngds.subscribe('Layer.click',function(topic,data){
		ngds.Map.reset_styles(data['tag_index']);
		for(var l in ngds.layer_map) {
			ngds.util.apply_feature_default_styles(ngds.layer_map[l],l);
			if(ngds.layer_map[l]._leaflet_id===data['Layer']._leaflet_id) {
				ngds.layer_map[l].is_active=true;
			}
			else{
				ngds.layer_map[l].is_active=false;
			}
		}
		ngds.util.apply_feature_active_styles(data['Layer'],data['tag_index']);
	});

	ngds.subscribe('Layer.add',function(topic,data){

	});

	ngds.subscribe('Layer.remove',function(topic,data){

	});
})();

(function setup_events_for_map_features() {
	// Ref : ngds.feature_event_manager
	// Ref : ngds.feature_ngds_id_mapping

	ngds.subscribe('Map.add_feature',function(topic,data){
		var feature = data['feature'];
		ngds.layer_map[data['seq_id']] = feature;
		
		ngds.feature_event_manager[feature._leaflet_id] = {
			'Layer':feature,
			'seq_id':data['seq_id']
		};
		
		feature.on('mouseover',function(feature){

			ngds.publish('Layer.mouseover',{
				'Layer':feature.layer,
				'tag_index':data['seq_id']
			});
		});

		feature.on('mouseout',function(feature){
			ngds.publish('Layer.mouseout',{
				'Layer':feature.layer,
				'tag_index':data['seq_id']
			});
		});

		feature.on('click',function(feature){
			ngds.publish('Layer.click',{
				'Layer':feature.layer,
				'tag_index':data['seq_id']
			});
		});

	});
})();



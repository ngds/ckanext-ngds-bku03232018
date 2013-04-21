/*
*	@author - Vivek Sunder
*	This is the top-level control module for the NGDS map.
*/

var ngds = ngds || ( ngds= { } );

/*
* 	Publish module
*/ 	

ngds.Map.initialize();


(function publish_pager_advance() {
	$("#map-search").click(function(){
		PubSub.publish('Map.search_initiated',{

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
			PubSub.publish('page.advance',{ 'page':page });
		});
})();


/*
*	Subscribe module
*/ 

(function subscribe_page_advance() {
	ngds.pager = new ngds.Search();

	PubSub.subscribe('page.advance',function(msg,data) {
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

	PubSub.publish("Map.area_selected",{ 
		'type':'rectangle',
		'feature':e
	});
});

ngds.Map.map.on('draw:poly-created',function(e){
	ngds.Map.clear_layer('drawnItems');
	ngds.Map.add_to_layer([e.poly],'drawnItems');

	PubSub.publish("Map.area_selected",{
		'type':'polygon',
		'feature':e
	});
});


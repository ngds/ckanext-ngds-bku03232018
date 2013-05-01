ngds.util = { };

ngds.util.dom_element_constructor = function(payload) {	
	var parent = $('<'+payload['tag']+'/>',payload['attributes']);
	if(typeof payload['children']!=='undefined') {
		for(var i=0;i<payload['children'].length;i++) {
			if(payload['children'][i]['priority']===1) {
				parent.prepend(ngds.util.dom_element_constructor(payload['children'][i]));
			}
			else {
				parent.append(ngds.util.dom_element_constructor(payload['children'][i]));
			}
		}
	}
	return parent;
};

ngds.util.sequence_generator = function() {
	var begin = 0;
	return {
		'next':function() {
			return begin=begin+1;
		},
		'current':function() {
			return begin;
		}
	}
};

// Fix this !!!
ngds.util.node_matcher = function(node,match_exp) { 
	if(node.className.match(match_exp)!==null) {
		return node.className.substring(node.className.indexOf("-")+1,node.length);
	}
	
	var parents = $(node).parents();
	for(var i=0;i<parents.length;i++) {
		if(parents[i].className.match(match_exp)!==null) {
			var clazz = parents[i].className;
			return clazz.substring(clazz.indexOf("-")+1,clazz.length);
		}
	}
	return null;		
};

ngds.util.apply_feature_hover_styles = function(feature,tag_index) {
	if(feature.feature.type==='Point') {
		var marker_tag = $('.lmarker-'+tag_index);
			if(marker_tag.length>0) {
				marker_tag.css("width","30px");
		 		marker_tag.css("height","45px");
		 		var span_elem = $('.lmarker-'+tag_index).next();
		 		span_elem.css("font-size","14pt");
		 		span_elem.css("margin-left","2px");	
		 	}
	}
	else {
		feature.setStyle({weight:2,color:"#d54799"});
	}
};


ngds.util.apply_feature_default_styles = function(feature,tag_index) {
	if(feature.feature.type==='Point') {
		var marker_tag = $('.lmarker-'+tag_index);
		marker_tag.attr("src","/images/marker.png")
		marker_tag.css("width","25px");
 		marker_tag.css("height","41px");
 		var span_elem = $('.lmarker-'+tag_index).next();
 		span_elem.css("font-size","12.5pt");
 		span_elem.css("margin-left","0px");	
	}
	else {
		feature.setStyle({weight:2,color:"blue"});
	}
};

ngds.util.apply_feature_active_styles = function(feature,tag_index) {
	$('.result-'+tag_index).css('background-color','#dadada');
	if(feature.feature.type==='Point') {
 		$('.lmarker-'+tag_index).attr("src","/images/marker-red.png");
	}
	else {
		feature.setStyle({weight:3,color:"red"});
	}
};

ngds.util.reset_result_styles = function() {
	$('.result').css('background-color','#fff');
};

ngds.util.clear_map_state = function() {
	$("#jspContainer").remove();
	$(".result").remove();
	$(".reader").remove();
	$(".search-results-page-nums").empty();
	ngds.Map.zoom_handler.clear_listeners();
	ngds.Map.clear_layer('geojson');
};

ngds.util.get_n_chars = function(words_str,num_chars) {
	var spliced = words_str.slice(0,num_chars-4);
	while(spliced[spliced.length-1]==='.' || spliced[spliced.length-1]===' ') {
		spliced=spliced.slice(0,spliced.length-1);
	}
	return spliced+" ...";
};
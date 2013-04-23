ngds.util = { };

console.log("Fix node matcher");

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
	if(node.match(match_exp)) {
		return node;
	}
	
	else return null;
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
	if(feature.feature.type==='Point') {
		$('.result-'+tag_index).css('background-color','#dadada');
 		$('.lmarker-'+tag_index).attr("src","/images/marker-red.png");
	}
	else {
		feature.setStyle({weight:3,color:"red"});
	}
};
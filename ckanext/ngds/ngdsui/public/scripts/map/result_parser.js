function result_parser(msg,results) {
	var results = results['results'];
	for(var i=0;i<results.length;i++){
			var each_result = $("<div/>",{class:"result"});
			var title = $('<a/>',{class:'description',href:['/dataset',results[i].name].join('/'),target:"_blank"});
			
			var notes = $('<p/>',{class:'notes'});
			var type = $('<p/>',{class:'type'});
			var wms = $('<button/>',{class:'wms',id:results[i]['resources'][0].id});
			var published = $('<p/>',{class:'published'});
			
			var marker_or_shape='';
			// console.log(ngds.ckandataset(results[i]).get_feature_type());
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
			$(".results").append(each_result);
			PubSub.publish('Map.result_rendered',{
				'each_result':results[i],
				'marker_or_shape':marker_or_shape
			});
		}
}



function render_marker(msg,data) {
	var each_result = data['each_result'];
	var marker_or_shape = data['marker_or_shape'];
	console.log(marker_or_shape);
 	var label = ngds.Map.labeller.get_cur_label();
 	ngds.Map.add_raw_result_to_geojson_layer(each_result,{iconimg_id:'lmarker-'+label});
 	var span_margin = "0px";
 	
 	if(marker_or_shape==='marker') {
	 	$('.result-'+label).hover(function() { //fadein
		 		$('.lmarker-'+label).css("width","30px");
		 		$('.lmarker-'+label).css("height","45px");
		 		var span_elem = $('.lmarker-'+label).next();
		 		span_elem.css("font-size","14pt");
		 		// span_margin=span_elem.css("margin-left");
		 		span_elem.css("margin-left","2px");
		 	},function(){ // fadeout
		 		$('.lmarker-'+label).css("width","25px");
		 		$('.lmarker-'+label).css("height","41px");
		 		var span_elem = $('.lmarker-'+label).next();
		 		span_elem.css("font-size","12.5pt");
		 		span_elem.css("margin-left",span_margin);
	 	});

	 	$('.result-'+label).click(function(){					 		// Reset steps
	 		$('.result').css('background-color','#fff'); // This is really a reset step. Do we need to move this into a .reset_background() ?
	 		var labels_colored = ngds.Map.state.colored_labels || (ngds.Map.state.colored_labels=[]);
	 		for(var i=0;i<labels_colored.length;i++){
	 			labels_colored[i].attr("src","/images/marker.png");
	 		}

			for(var shape_index in ngds.Map.state.shapes_map){
				if(ngds.Map.state.shapes_map[shape_index]!==null && typeof ngds.Map.state.shapes_map[shape_index]!=='undefined') {
					ngds.Map.state.shapes_map[shape_index].setStyle({weight:ngds.Map.state.shapes_map[shape_index].orig_weight,color:ngds.Map.state.shapes_map[shape_index].orig_color});
				}
			}

	 		labels_colored = ngds.Map.state.colored_labels = [];
	 		// End reset steps

	 		// Now do the actual transitions
	 		$('.result-'+label).css('background-color','#dadada');
	 		$('.lmarker-'+label).attr("src","/images/marker-red.png");
	 		labels_colored.push($('.lmarker-'+label));
	 		// End actual transitions
	 	});
	}
	else {
		$('.result-'+label).hover(function(){ //fadein
				var shape=ngds.Map.state.shapes_map[label];
				
				ngds.Map.state.shapes_map[label].prev_weight=ngds.Map.state.shapes_map[label].options.weight;
				ngds.Map.state.shapes_map[label].prev_color=ngds.Map.state.shapes_map[label].options.color;
				shape.setStyle({weight:2,color:"#d54799"});
		},function(){ //fadeout
				var shape=ngds.Map.state.shapes_map[label];
				shape.setStyle({weight:ngds.Map.state.shapes_map[label].prev_weight,color:ngds.Map.state.shapes_map[label].prev_color});
		});

		$('.result-'+label).click(function(){
			// Reset steps
			$('.result').css('background-color','#fff'); // This is really a reset step. Do we need to move this into a .reset_background() ?
	 		var labels_colored = ngds.Map.state.colored_labels || (ngds.Map.state.colored_labels=[]);
	 		for(var i=0;i<labels_colored.length;i++){
	 			labels_colored[i].attr("src","/images/marker.png");
	 		}
			// shapes
	 		
			for(var shape_index in ngds.Map.state.shapes_map){
				if(ngds.Map.state.shapes_map[shape_index]!==null && typeof ngds.Map.state.shapes_map[shape_index]!=='undefined' && shape_index!==label) {
					ngds.Map.state.shapes_map[shape_index].setStyle({weight:ngds.Map.state.shapes_map[shape_index].orig_weight,color:ngds.Map.state.shapes_map[shape_index].orig_color});
				}
			}
			// ngds.Map.state.sha=[];
			// End of Reset steps
			$('.result-'+label).css('background-color','#dadada');
			var shape=ngds.Map.state.shapes_map[label];
			if(shape!==null && typeof shape!=='undefined') {
				shape.setStyle({weight:3,color:"red"});
				ngds.Map.state.shapes_map[label].prev_weight=3;
				ngds.Map.state.shapes_map[label].prev_color="red";
				
			}
		});
	}

			}


PubSub.subscribe('Map.result_rendered',render_marker);
PubSub.subscribe('Map.results_received',result_parser);
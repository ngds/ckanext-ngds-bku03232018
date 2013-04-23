
ngds.render_search_results = function(topic,results) { //Subscription - 'Map.result_received'
	var seq = new ngds.util.sequence_generator();
	var results = results['results'];
	for(var i=0;i<results.length;i++) {
		var skeleton = {
			'tag':'div',
			'attributes':{
				'class':'result result-'+seq.next()
			},
			'children':[
				{
					'tag':'anchor',
					'attributes':{
						'class':'description',
						'href':['/dataset',results[i]['name']].join('/'),
						'target':'_blank',
						'text':results[i]['title']
					}
					
				},
				{
					'tag':'p',
					'attributes':{
						'class':'notes',
						'text':results[i]['notes']
					}
				},
				{
					'tag':'p',
					'attributes':{
						'class':'type',
						'text':results[i]['type']
					}
				},
				{
					'tag':'button',
					'attributes':{
						'class':'wms',
						'id':results[i]['resources'][0]['id'],
						'text':"WMS"
					}
				},
				{
					'tag':'p',
					'attributes':{
						'class':'published',
						'text':new Date(results[i]['metadata_created']).toLocaleDateString()
					}
				}
			]
		};
		var shaped_loop_scope = ngds.ckandataset(results[i]).get_feature_type()['type'];
		var marker_container = { };
		
		PubSub.publish('Map.feature_received',{
				'feature':results[i],
				'seq':seq.current()
			});

		if(shaped_loop_scope==='Point') {	
			marker_container = {
				'tag':'div',
				'attributes':{
					'class':'result-marker-container marker-'+seq.current()
				},
				'priority':1,
				'children':[
					{
						'tag':'img',
						'attributes':{
							'src':'/images/marker.png',
							'class':'result-marker',
						}
					},
					{
						'tag':'span',
						'attributes':{
							'class':'result-marker-label marker-label-'+seq.current(),
							'text':seq.current()
						}
					}
				]
			};
			skeleton['children'].push(marker_container);
		}

		var dom_node = ngds.util.dom_element_constructor(skeleton);
		$('.results').append(dom_node);
	}
};

PubSub.subscribe('Map.results_received',ngds.render_search_results);
var populate_content_models = function(selector) {
	var content_model_combo = $(selector);
	if(typeof content_models==='undefined') {
		content_models = {

		};

		$.ajax({ // Fetch content models.
			      url:'/api/action/contentmodel_list_short',
			      type:'POST',
			      data: JSON.stringify({
			        dummy:'appendix' // Ckan needs something in the body or the request is not accepted.
			      }),
			      success:function(response) {
			        for(var i=0;i<response.result.length;i++) {
			        	content_models[response.result[i].uri]= response.result[i];
			        }
			         $('<option/>', {value: 'none', text: 'None'}).appendTo(content_model_combo);
			        for(var val in content_models) {
					    $('<option/>', {value: val, text: content_models[val].title}).appendTo(content_model_combo);
					}

			      }
		});

		return;
	}

  for(var val in content_models) {
	    $('<option/>', {value: val, text: content_models[val].title}).appendTo(content_model_combo);
	}
};

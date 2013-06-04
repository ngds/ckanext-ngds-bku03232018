var populate_content_models = function() {
	var content_model_combo = $("#content_model");
	if(typeof options==='undefined') {
		options = [];
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

			        options.push($('<option/>', {value: 'none', text: 'None'}).appendTo(content_model_combo));
			        for(var val in content_models) {
					    options.push($('<option/>', {value: val, text: content_models[val].title}).appendTo(content_model_combo));
					}
			      }
		});

		return;
	}

  for(var i=0;i<options.length;i++) {
	   options[i].appendTo(content_model_combo);
	}
};


var populate_content_model_versions = function() {
	var marker = $(".content_model_marker");
	var content_model_combo = $("#content_model");
	if(content_model_combo.val()==='none') { // If the value is 'none', then don't populate any versions.
		return;
	}

	$('.content_model_version_marker').remove();

	var content_model_version_struct = {
	'form':[{
		'label':'Version',
		'name':'content_model_version',
		'top_classes':function() {
			return 'content_model_version_marker';
		},
		'tag':'select',
		'id':function() {
			return 'id=content_model_version';
		}
	}]};

	content_model_combo.after(Mustache.render(structured_form_template,content_model_version_struct));
	
	var content_model_version_combo = $("#content_model_version");
	var content_model_selected = content_model_combo.val();

	for(var i=0;i<content_models[content_model_selected].versions.length;i++) {
    	$('<option/>',{value:content_models[content_model_selected].versions[i].uri,text:content_models[content_model_selected].versions[i].version}).appendTo(content_model_version_combo);
    }
};


$(".form-body").on("change","#content_model",function() { // When the content model combo's value changes, populate the content model versions into the content_model_version combo box.
	populate_content_model_versions();	
});
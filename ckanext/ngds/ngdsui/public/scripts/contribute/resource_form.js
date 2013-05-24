var upload_type_radios = $('input[name="upload-type"]');

var content_models = {

};

$("#upload-type-structured-label").css("color","#808080");
$("#upload-type-unstructured-label").css("color","#808080");

var content_model_combo = $("#content_model");

var populate_content_model_versions = function() {
	var content_model_selected = $("#content_model").val();
	var content_model = content_model_combo.val();
	var content_model_version_combo = $("#content_model_version");
    content_model_version_combo.empty();
    for(var i=0;i<content_models[content_model_selected].versions.length;i++) {
    	$('<option/>',{value:content_models[content_model_selected].versions[i].uri,text:content_models[content_model_selected].versions[i].version}).appendTo(content_model_version_combo);
    }
};

$.ajax({ // Fetch content models.
	      url:'/api/action/contentmodel_list_short',
	      type:'POST',
	      data: JSON.stringify({
	        something:'something' // Ckan needs something in the body or the request is not accepted.
	      }),
	      success:function(response) {
	        for(var i=0;i<response.result.length;i++) {
	        	content_models[response.result[i].uri]= response.result[i];
	        }
	        for(var val in content_models) {
			    $('<option/>', {value: val, text: content_models[val].title}).appendTo(content_model_combo);
			}

			populate_content_model_versions();

	      }
});

content_model_combo.on('change',function(){
	populate_content_model_versions();
});

var hide_all = function() {
	$(".structured-form").hide();
};

var show_structured_form = function() {
	$(".structured-form").show();
};

upload_type_radios.on('change',function(ev){
	var value = ev.target.value;
	var upload_type_selection = $("#upload-type-selection");
	var form_body = $(".form-body");
	var form = $(".dataset-form");

	hide_all();

	if(value==='structured' || value==='unstructured') {
		// Check the 'upload a file' radio
		upload_type_selection.prop('checked',true);
	}
	else {
		upload_type_selection.prop('checked',false);	
	}
	
	if(value==='structured') { // Display the structured upload form.
		$("#upload-type-structured-label").css("color","#545454");
		show_structured_form();
	}
	else {
		$("#upload-type-structured-label").css("color","#808080");
	}


	if(value==='unstructured') { // Display the unstructured upload form
		$("#upload-type-unstructured-label").css("color","#545454");
		form.append();
	}
	else {
		$("#upload-type-unstructured-label").css("color","#808080");
	}

	if(value==='data-service') { // Display the data service link form
		form.append();
	}

	if(value==='offline-resource') { // Display the offline resource upload form
		form.append();
	}
	
});

$("#file").on('change',function(ev){
	var timestamp = new Date().toISOString();
	$("#key").value = timestamp;
	$(".dataset-form").submit();
});


var populate_content_models = function() {
	var content_model_combo = $(".content_model");
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
	var content_model_combo = $(".content_model");
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
		'class':function() {
			return 'content_model_version';
		}
	}]};
	
	content_model_combo.after(Mustache.render(ngds.structured_form_template,content_model_version_struct));
	
	var content_model_version_combo = $(".content_model_version");
	var content_model_selected = content_model_combo.val();

	for(var i=0;i<content_models[content_model_selected].versions.length;i++) {
    	$('<option/>',{value:content_models[content_model_selected].versions[i].uri,text:content_models[content_model_selected].versions[i].version}).appendTo(content_model_version_combo);
    }
};


$(".form-body").on("change",".content_model",function() { // When the content model combo's value changes, populate the content model versions into the content_model_version combo box.
	populate_content_model_versions();	
});

$("#file").on('change',function(ev){
	var timestamp = new Date().toISOString();
	var file = $("#file").val();
	var filename = file.substring(file.lastIndexOf("\\")+1);
	$("#key1").val(timestamp+"/"+filename);
	$("#key2").val(timestamp+"/"+filename);
	$("#form_type").val($("[name=upload-type]:checked").val());
	$("#file-upload-form").submit();
});

var populate_form = function(data) {
	for(property in data) {
		if($("[name="+property+"]").length>0) {
			if(property==='url') {
				$("[name="+property+"]").val('http://'+window.location.host+'/storage/f/'+data[property]);
				continue;
			}
			$("[name="+property+"]").val(data[property]);
		}
	}
};

var activate_populate_form = function(data) {
	render_forms(data['form_type']);
	populate_form(data);
	var name = get_prop($("#url").val(),'name');
	var file_extension = get_prop($("#url").val(),'extension');
	$("[name=name]").val(name);
	$("[name=format]").val(file_extension);
};


var get_prop = function(url,what) {
	if(typeof url === 'undefined' || url.length===0) {
		return '';
	}
	var sp = url.substring(url.lastIndexOf('/')+1);
	if(what==='name') {
		return sp.split('.')[0];
	}
	if(what==='extension') {
		return sp.split('.')[1];
	}
};


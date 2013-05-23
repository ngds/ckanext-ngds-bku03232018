var upload_type_radios = $('input[name="upload-type"]');

upload_type_radios.on('change',function(ev){
	var value = ev.target.value;
	var upload_type_selection = $("#upload-type-selection");
	
	if(value==='structured' || value==='unstructured') {
		upload_type_selection.prop('checked',true);
	}
	else {
		upload_type_selection.prop('checked',false);	
	}
	
});
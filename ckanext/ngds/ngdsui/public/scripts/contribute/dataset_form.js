/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
$("[name=title]").on('input',function(ev){
	var title = $("[name=title]").val();
	title = title.trim(); // Remove leading and trailing spaces.
	title = title.replace(/^-/,'');
	title = title.replace(/-$/,'');
	title = title.replace(/[^a-zA-Z0-9]/g,'-');
	title = title.replace(/-{2,}/g,'-');
	$("[name=name]").val(title.toLowerCase());
});

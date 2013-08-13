/*
*	@author - Vivek
*	Exposes a set of functions and objects to work with datasets obtained from ckan.
*/

ngds.ckandataset = function(raw) { 

	var me = this;
	this.dataset = raw;

	(function(raw) {
		if(raw===null || typeof raw==='undefined') {
			throw "Passed in object was null or undefined.";
		}
	})(raw);

	_ckan_dataset = {
		construct:function() {
			var spatial_extra;
			$.each(raw.extras,function(index,val) {
				if(val.key==='spatial')	{
					spatial_extra = val.value;
				}
			});
			var geojson = $.parseJSON(spatial_extra);
			var description = raw.notes;

			var popup_skeleton = {
				'tag':'div',
				'children':[
					{
						'tag':'p',
						'attributes':{
							'style':'margin-bottom:3px; margin-top:3px;'
						},
						'children':[
							{
								'tag':'strong',
								'priority':1,
								'attributes':{
									'text':'Title : '
								}
							},
							{
								'tag':'a',
								'attributes':{
									'href':'/dataset/'+raw.name,
									'text':raw.title,
									'target':'_blank'
								}
							}
						]
					},
					{
						'tag':'p',
						'attributes':{							
							'style':'margin-bottom:3px; margin-top:3px;',
							'text':raw.type
						},
						'children':[
							{
								'tag':'strong',
								'priority':1,
								'attributes':{
									'text':'Type : '
								}
							}
						]
					},
					{
						'tag':'strong',
						'attributes':{							
							'style':'margin-bottom:3px; margin-top:3px;',
							'text':'Author : '
						},
						'children':[
							{
								'tag':'a',
								'attributes':{
									'href':'mailto:'+raw.author_email,
                                    'text':raw.author
								}
							}
						]
					},
					{
						'tag':'strong',
						'attributes':{							
							'style':'margin-bottom:3px; margin-top:3px;',
							'text':"Maintainer : "
						},
						'children':[
							{
								'tag':'a',
								'attributes':{
									'href':'mailto:'+raw.maintainer_email,
                                    'text':raw.maintainer
								}
							}
						]
					},
					{
						'tag':'p',
						'attributes':{							
							'style':'margin-bottom:3px; margin-top:3px;',
							'text':ngds.util.get_n_chars(description,150)
						},
						'children':[
							{
								'tag':'strong',
								'priority':1,
								'attributes':{
									'text':'Description : '
								}
							}
						]
					},
					{
						'tag':'p',
						'attributes':{							
							'style':'margin-bottom:3px; margin-top:3px;',
							'text':(new Date(raw.metadata_created)).toLocaleDateString()
						},
						'children':[
							{
								'tag':'strong',
								'priority':1,
								'attributes':{
									'text':'Created : '
								}
							}
						]
					},
					{
						'tag':'p',
						'attributes':{							
							'style':'margin-bottom:3px; margin-top:3px;',
							'text':(new Date(raw.metadata_modified)).toLocaleDateString()
						},
						'children':[
							{
								'tag':'strong',
								'priority':1,
								'attributes':{
									'text':'Last Modified : '
								}
							}
						]
					},
					{
						'tag':'p',
						'attributes':{							
							'style':'margin-bottom:3px; margin-top:3px;',
							'text':raw.num_resources
						},
						'children':[
							{
								'tag':'strong',
								'priority':1,
								'attributes':{
									'text':'Number of Resources : '
								}
							}
						]
					},
					{
						'tag':'p',
						'attributes':{							
							'style':'margin-bottom:3px; margin-top:3px; color:blue;',
							'text':ngds.util.deep_joiner(raw.tags,'display_name',', ')
						},
						'children':[
							{
								'tag':'strong',
								'priority':1,
								'attributes':{
									'text':'Tags : ',
									'style':'color:#000;'
								}
							}
						]
					}					
				]
			};

			var popupHTML = ngds.util.dom_element_constructor(popup_skeleton)[0].innerHTML;
			
			// var popupHTML = '<p>';
			// popupHTML+='<b> Title : '+raw.title+'</b><br>';
			// popupHTML+='Author : '+raw.author+'<br>';
			// popupHTML+='Description : '+description+'<br>';
			// popupHTML+='Published : '+(new Date()).toLocaleDateString()+'<br>';
			// popupHTML+='</p>';

			return {
						getGeoJSON:function() { // return the geojson feature associated with the dataset.
							return geojson;
						},
						map:{
							getPopupHTML:function() { // return a html popup of a dataset's metadata that is to be displayed when an icon or feature is clicked.
								return popupHTML;
								}
						},
						get_feature_type:function() {
							return geojson;
						}
			}
		}
	}
	return _ckan_dataset.construct();
};

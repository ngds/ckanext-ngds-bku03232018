ngds.ckandataset=function(a){var b=this;this.dataset=a;(function(c){if(c===null||typeof c==="undefined"){throw"Passed in object was null or undefined."}})(a);_ckan_dataset={construct:function(){var i;$.each(a.extras,function(k,l){if(l.key==="spatial"){i=l.value}});var e=$.parseJSON(i);var h=a.notes;var j={tag:"div",children:[{tag:"p",attributes:{"class":"title"},children:[{tag:"a",attributes:{href:"/dataset/"+a.name,text:a.title,target:"_blank","class":"title"}}]},{tag:"p",attributes:{style:"margin-bottom:3px; margin-top:3px;",text:(function(){var k=ngds.util.get_n_chars(h,150);if(k!==""){return k}else{return"No description."}})(),"class":"description"}},{tag:"p",attributes:{text:a.num_resources+(function(k){if(k===1){return" resource"}else{return" resources"}})(a.num_resources),"class":"resources"}}]};var f={tag:"div",attributes:{"class":"tags"},children:[]};j.children.push(f);var d=0;for(var c in a.tags){if(a.tags[c]["name"].length>25||c>=6){break}f.children.push({tag:"div",attributes:{"class":"ngds-tag",text:a.tags[c]["name"]}})}var g=ngds.util.dom_element_constructor(j)[0].innerHTML;return{getGeoJSON:function(){return e},map:{getPopupHTML:function(){return g}},get_feature_type:function(){return e}}}};return _ckan_dataset.construct()};
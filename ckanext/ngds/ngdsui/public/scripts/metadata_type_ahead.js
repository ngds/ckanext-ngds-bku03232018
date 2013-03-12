/*
  author : Vivek
  Autocomplete for textboxes on the edit and resource creation pages.

*/
$(document).ready(function() {
  var field_author = ngds.autocomplete("#field-author-fake","/responsible_parties",'q','name','name');  
  field_author.proxy("#field-author","id");
  
  var maintainer = ngds.autocomplete("#field-maintainer-fake","/responsible_parties",'q','name','name');
  maintainer.proxy("#field-maintainer","id");
  maintainer.proxy("#field-extras-1-value","id");

  var languages = ngds.autocomplete("#field-language-fake","/languages",'q','name','name');
  languages.proxy("#field-extras-8-value","id");
 
});



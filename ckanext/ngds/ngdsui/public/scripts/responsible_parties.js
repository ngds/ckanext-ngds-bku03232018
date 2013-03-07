/*
  author : Vivek
  Autocomplete for textboxes on the edit and resource creation pages.

*/
$(document).ready(function() {
  ngds.autocomplete("#field-author","/responsible_parties",'q','name','name');  
  // ngds.autocomplete("#field-maintainer","/api/2/util/user/autocomplete",'q','name','name');  
  ngds.autocomplete("#field-maintainer","/api/2/util/user/autocomplete",'q','name','name');
});



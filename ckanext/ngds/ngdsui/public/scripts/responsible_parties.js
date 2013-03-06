  // -- Get list of authors (responsible party) here.
  
  // var request_payload = { // This is our request payload to the additional_metadata api endpoint.
  //   "process":"read",
  //   "model":"ResponsibleParties"
  // }; // This is a placeholder call.

  // $.ajax({
  //   url:"/responsible_parties/",
  //   data:request_payload,
  //   success:function(data,status) {
  //     console.log(data);
  //     ngds.cache = {
  //       "ResponsibleParties": data
  //     };
  //   }
  // });

$(document).ready(function(){
    $( "#field-author" ).autocomplete({
  source: "/api/2/util/user/autocomplete"
  });
});
  

/*
  author : Vivek
*/

var ngds = ngds || { };
/*
    hash_id : The id of the text box element you wish to work with
    source_url : The URL where suggestions for autocompletion can be obtained
    query_param_key : The parameter to use to query the API endpoint. Ex : http://somewhere.com/some/api/endpoint/{q|x|term|a|b|whatever}?=vivek
    display_key : The key to the parameter in the response that gives us the display value of the suggestion drop down
    value_key : The key to the parameter in the response that gives us the value the text box should have
  */
ngds.autocomplete = function(hash_id_elem,source_url,query_param_key,display_key,value_key) {
  
  var textbox_component = $(hash_id_elem);
  var display_key = display_key;
  var value_key = value_key;
  
  if(textbox_component.length===0) {
    console.log("No such id "+hash_id_elem+" in the DOM. Make sure you're invoking the function with something like '#an_id' (one that is valid)");
    return;
  }

  var autocomplete = $(textbox_component).autocomplete({
      source: function(request, response) {
          var dict = { };
          dict[query_param_key]=request.term;
          $.getJSON(source_url, dict, response);
        },
      response:function(event,ui) {
        $.each(ui.content,function(index,val){ 
          
          var t1 = (val[display_key]!==null && typeof val[display_key]!=='undefined');
          var t2 = (val[value_key]!==null && typeof val[value_key]!=='undefined');
          
          if(t1 && t2) {  // scrub out values that are null or undefined since there's no point trying to display them.
            val.label=val[display_key];
            val.value=val[value_key];  
          }
          else { // console log it
            console.log("Got null/undefined value for call :",request);
          }
          
        });
      }
  });
  
  auto = autocomplete;
  
  var proxy_list = [];

  autocomplete.on('autocompleteselect',function(ev,ui) {
            $.each(proxy_list,function(index,proxy){
              $(proxy["proxy"]).val(ui.item[proxy["value_key"]]);
            });
        });

  return {
      autocomplete:autocomplete,
      proxy:function(proxy_id_elem,value_key){ // If the value of the autocomplete suggestion is something that doesn't make sense to the user, 
                                                // we can display the autocomplete value instead and use a proxy to carry the real value. 
                                                // Keep in mind that the proxy is really the text box that we care about, so id's et al have to make sense.
        proxy_list.push({ "proxy": proxy_id_elem,"value_key":value_key });
        
      }
  };
};
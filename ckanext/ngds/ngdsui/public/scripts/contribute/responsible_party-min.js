var ngds=ngds||(ngds={});ngds.responsible_party=function(){var b=this;var a=function(d,k){(function i(l){var m=typeof $(l.rs_name)==="undefined";var n=typeof $(l.rs_email)==="undefined";var o=typeof $(l.rs_fake)==="undefined";if(m||n||o){throw"Failed sanity check"}})(d);b.rs_name=d.rs_name;b.rs_email=d.rs_email;b.rs_fake=d.rs_fake;b.rs=d.rs;b.rs_slug="#"+b.rs.replace("#","")+"_slug";b.rs_token=b.rs.replace("#","");var j=ngds.autocomplete(b.rs_fake,"/responsible_parties","q",["name","email"],"name");var e=b.rs_name;var g=b.rs_email;b.slugify=this.slugify=function(s){var s=s||{};var o=ngds.util.state[b.rs_token]||(ngds.util.state[b.rs_token]={});var r={};r.name=s.name||$(b.rs_name).val();r.email=s.email||$(b.rs_email).val();var q=r.name;var p=r.email;if(q===""||p===""){return}var n=JSON.stringify(r);$(b.rs).val(n);if(typeof k!=="undefined"){k(s)}setTimeout(function(){$(b.rs_fake).val("")});ngds.util.state[b.rs_token]=n;$(d.slug_container).empty();var m=$("<span/>",{"class":"ngds-tag",text:r.name,title:"Name : "+q+", Email : "+p});$(d.slug_container).append(m);var l=$("<span/>",{text:"X","class":"close-button-transform",style:"cursor:pointer"});m.append(l);l.on("click",function(t){$(t.currentTarget.parentElement).fadeOut(500,function(){var u=t.currentTarget.parentElement;u.remove();$(b.rs).val("")})})};j.proxy(b.rs,b.slugify);if($(b.rs_fake).val()!==""){var h="";try{var h=JSON.parse($(b.rs_fake).val());$(b.rs_fake).val("");b.slugify(h)}catch(f){}}c()};var c=function(){var d=$(b.rs_fake);b.rs_create_anch=$("<a/>",{"class":"icon-plus "+b.rs.replace("#",""),style:"cursor:pointer;"});b.rs_create_anch.on("click",function(B){b.rs_create_anch.hide();$(b.rs_slug).hide();$(b.rs_fake).show();var q=b.rs.replace("#","");var z=q+"_c_name";var w=q+"_c_email";var m=q+"_c_org";var e=q+"_c_ph";var n=q+"_c_street";var k=q+"_c_state";var s=q+"_c_city";var h=q+"_c_zip";var g=q+"_c_country";var o=q+"_c_create_button";var x=q+"_c_cancel_button";var D=q+"_c_form";var u=[{label:"Name",label_class:D,input_name:z,input_class:D,input_id:z},{label:"Email",label_class:D,input_name:w,input_class:D,input_id:w},{label:"Organization",label_class:D,input_name:q+"org",input_class:D,input_id:m},{label:"Phone",label_class:D,input_name:q+"ph",input_class:D,input_id:e},{label:"Street",label_class:D,input_name:q+"street",input_class:D,input_id:n},{label:"City",label_class:D,input_name:q+"city",input_class:D,input_id:s},{label:"State",label_class:D,input_name:q+"state",input_class:D,input_id:k},{label:"Zip",label_class:D,input_name:q+"zip",input_class:D,input_id:h},{label:"Country",label_class:D,input_name:q+"-country",input_class:D,input_id:g},{button:"Create",id:o,"class":D},{button:"Cancel",id:x,"class":D}];b.rs_create_anch.after(ngds.rs_generator(u,D,q));var j=$("#"+z);var A=$("#"+w);var p=$("#"+m);var C=$("#"+e);var r=$("#"+n);var i=$("#"+s);var f=$("#"+k);var t=$("#"+h);var v=$("#"+g);var y=$("#"+o);var E=$("#"+x);y.on("click",function(){$.ajax({url:"/api/action/additional_metadata",type:"POST",data:JSON.stringify({process:"create",model:"ResponsibleParty",data:{name:j.val(),email:A.val(),organization:p.val(),phone:C.val(),street:r.val(),city:i.val(),state:f.val(),zip:t.val(),country:v.val()}}),success:function(F){console.log(F);b.slugify(F.result);b.rs_create_anch.show();l.remove()},error:function(){$(".add-responsible-party .tab").after($("<div/>",{"class":"error-block",text:"Invalid form entries"}))}})});var l=$("."+D);E.on("click",function(F){l.remove();b.rs_create_anch.show()})});d.after(b.rs_create_anch)};return{responsibilify:a}};
var ngds = ngds || ( ngds = { } );

ngds.responsible_party = function() {

	var me = this;

	var responsibilify = function(fields) {
		/*
		*	Fields - rs-fake, rs_name, rs_email.
		*/

		(function sanity_check(fields) {
			var rs_name_not_exists = typeof $(fields['rs_name']) === 'undefined';
			var rs_email_not_exists = typeof $(fields['rs_email']) === 'undefined';
			var rs_fake_not_exists = typeof $(fields['rs_fake']) === 'undefined';

			if(rs_name_not_exists || rs_email_not_exists || rs_fake_not_exists) {
				throw "Failed sanity check";
			}
		})(fields);

		
		me.rs_name = fields['rs_name'];
		me.rs_email = fields['rs_email'];
		me.rs_fake = fields['rs_fake'];
		me.rs = fields['rs'];
		me.rs_slug = "#"+me.rs.replace("#","")+'_slug';
		me.rs_token = me.rs.replace("#","");

		var rs_ac = ngds.autocomplete(me.rs_fake,"/responsible_parties",'q',['name','email'],'name'); 

	    rs_ac.proxy(me.rs_name,"name"); 
	    rs_ac.proxy(me.rs_email,"email");

	    var rs_name = me.rs_name;
	    var rs_email = me.rs_email;

        var slugify = function(dict){
            console.log("once");
            var rs_map = ngds.util.state[me.rs_token] || ( ngds.util.state[me.rs_token] = { });
            var payload = { };
            console.log(dict);
            payload["name"] = dict.name;
            payload["email"] = dict.email;
            var vdict = JSON.stringify(payload);
	        $(me.rs).val(vdict);

            setTimeout(function() {
                $(me.rs_fake).val("");
            });

	        ngds.util.state[me.rs_token] = vdict;
            $(fields['slug_container']).empty();
            var slug = $("<span/>",{ "class":"ngds-tag","text":dict.name });
            $(fields['slug_container']).append(slug);
            var anch = $("<span/>",{"text":"X","class":"close-button-transform","style":"cursor:pointer"});
            slug.append(anch);
            anch.on('click',function(ev) {
            $(ev.currentTarget.parentElement).fadeOut(500,function(){
                var parent = ev.currentTarget.parentElement;
                parent.remove();
                $(me.rs).val('');
               });
             });
        }

	    rs_ac.proxy(me.rs,slugify);

        if($(me.rs_fake).val()!=="") {
           var parsed_dict = '';
           try {
                 var parsed_dict = JSON.parse($(me.rs_fake).val());
                 $(me.rs_fake).val("");
                 slugify(parsed_dict);
           }
           catch(SyntaxError) {
                   //swallow
           }
        }

	   append_create_rs_anchor();
	};

	var append_create_rs_anchor = function() {
		var rs_fake = $(me.rs_fake);
		
		 me.rs_create_anch = $("<a/>",{
				'class':'icon-plus '+me.rs.replace("#",""),
				'style':'cursor:pointer;'
			});

		me.rs_create_anch.on('click',function(ev){
			me.rs_create_anch.hide();
			$(me.rs_slug).hide();
			$(me.rs_fake).show();
			var rs_token = me.rs.replace("#","");
			var rs_c_name = rs_token+"_c_name";
			var rs_c_email = rs_token+"_c_email";
			var rs_c_create_button = rs_token+"_c_create_button";
			var rs_c_cancel_button = rs_token+"_c_cancel_button";
			var rs_c_form = rs_token+"_c_form";

			 var responsible_parties = {
			 	'class':rs_c_form,
			    'responsible_parties':[
			      {
			        'label':'Name',				        
			        'type':'text',
			        'name':rs_c_name,
			        'id':rs_c_name,
			        'class':rs_c_form
			      },
			      {
			        'label':'Email',
			        'type':'text',
			        'name':rs_c_name,
			        'id':rs_c_email,
			        'class':rs_c_form
			      },
			      {
			        'button':'Create',
			        'id':rs_c_create_button,
			        'class':rs_c_form
			      },
			       {
			        'button':'Cancel',
			        'id':rs_c_cancel_button,
			        'class':rs_c_form
			      }
			    ]
			  };

			me.rs_create_anch.after(Mustache.render(ngds.add_responsible_party_template,responsible_parties));

			var rs_c_name_jq = $("#"+rs_c_name);
			var rs_c_email_jq = $("#"+rs_c_email);
			var rs_c_create_button_jq = $("#"+rs_c_create_button);
			var rs_c_cancel_button_jq = $("#"+rs_c_cancel_button);
			var rs_c_form_jq = $("."+rs_c_form);		

			rs_c_create_button_jq.on('click',function() {
				 $.ajax({
			        'url':'/api/action/additional_metadata',
			        'type':'POST',
			        'data':JSON.stringify({
			          "process":"create",
			          "model":"ResponsibleParty",
			          "data":{
			            "name":rs_c_name_jq.val(),
			            "email":rs_c_email_jq.val()
			          }
			        }),
			        'success':function(response) {
			          $(me.rs_name).val(response.result.name);
			          $(me.rs_email).val(response.result.email);
			          // $(rs_cre).html("Success");
			          rs_c_form_jq.fadeOut(1500,function() {
			             rs_c_form_jq.remove();

			             $(me.rs_fake).val(response.result.name);
			             rs_blur();
			          });
			        }
			  });
			});

			rs_c_cancel_button_jq.on('click',function(ev){
				rs_c_form_jq.remove();
				me.rs_create_anch.show();
			});
			

		});

		rs_fake.after(me.rs_create_anch);
	};

	return {
		'responsibilify':responsibilify
	}	
};
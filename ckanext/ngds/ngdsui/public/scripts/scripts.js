var ngds = ngds || { };

(function() {
	$(document).ready(function() { 


		/* This is for user management - Role changes (manage_users.html) - Start*/
		var prev_val;

		$('.dropdown').focus(function() {
		    prev_val = $(this).val();
		}).change(function() {
		     $(this).blur() // Firefox fix as suggested by AgDude
		    var success = confirm('Are you sure you want to change the role?');
		    if(success)
		    {		        
		        var formid = "#"+$(this)[0].id.substr(5);
		        $(formid).submit();
		        // Other changed code would be here...
		    }  
		    else
		    {
		        $(this).val(prev_val);
		        //alert('unchanged');
		        return false; 
		    }
		});
		/* This is for user management - Role changes (manage_users.html) - End*/

		$('#read-only-form :input').attr('readonly','readonly');
		$('#read-only-form :checkbox').attr('disabled', 'disabled');

		var $unique = $('input.unique');
		$unique.click(function() {
		    $unique.filter(':checked').not(this).removeAttr('checked');
		});


		$("#manage-nodes-table tr:odd").css("background-color", "#fff6f6");

		$(".not-implemented").click(function(event) { // Handle portions of the UI that haven't been implemented yet, display a div that says 'Not implemented Yet'.
				ngds.not_implemented_popup_active = true;
				$("#not-implemented-popup").show();
				return false;
			});

		$(document).click(function(){ // Handle clicks on the document level.
				
				if(ngds.not_implemented_popup_active ===true) { // If The not implemented yet popup is active, hide it.
					ngds.not_implemented_popup_active = false;
					$("#not-implemented-popup").hide();
				}

				if(isLoginPopupVisible()) { // If the login popup is active, hide it.
					$(".login-popup").hide();
				}				
			});

		$(document).keyup(function(e){ // On ESC hide the Not Implemented Yet popup, if it's visible.
			if(e.keyCode===27 && ngds.not_implemented_popup_active) {
				$("#not-implemented-popup").hide();
			}
		});

		(function(){ // Handle login popup events.

			$(".login-in").click(function(){ // When clicked, toggle between visible and hidden.
				if(isLoginPopupVisible()) {
					$(".login-popup").hide();
				}
				else {
					$(".login-popup").show();
				}
				return false;
			});

			$(document).keyup(function(e){ // On ESC toggle between visible and hidden.
				if(e.keyCode===27 && isLoginPopupVisible()) {
					$(".login-popup").hide();
				}
			});

			$("#login-popup").click(function(){ // Prevent the click event propagating upwards to document and resulting in the login popup being hidden
													// when a click occurs inside the div.
				return false;
			});

		})();


		// (function(){ // Handle username and password state transitions.
			
		// 	$("#username").click(function(e){
		// 		return false;
		// 	});

		// 	$("#password").click(function(e){ // Preventing the click event from firing on the document and resulting in the login popup from vanishing
		// 										// due to the focus event binding below.
		// 		return false;
		// 	});

		// 	$("#username").focus(function(e) {
		// 			if(this.value==="username") {
		// 				this.value = "";
		// 			}
		// 		});

		// 	$("#username").blur(function(e) {
		// 			if(this.value==="") {
		// 				this.value = "username";
		// 			}
		// 		});

		// 	$("#password").focus(function(e) {
		// 			if(this.value==="password") {
		// 				this.value = "";
		// 			}
		// 		});

		// 	$("#password").blur(function(e) {
		// 			if(this.value==="") {
		// 				this.value = "password";
		// 			}
		// 		});

		// })();


		$("#accordion").accordion({ // Create and configure the library search page's accordion menu.
		    	autoHeight:false,
		    	clearStyle: false,
		    	header:"h4",
		    	heightStyle:"content",
		    	active:false,
		    	collapsible:true
			});

		function isLoginPopupVisible(){
				return ($(".login-popup").css('display')!=='none');
			}
	
	    var dataset = ngds.autocomplete("#distributor-fake","/responsible_parties",'q','name','name');  
	    if(dataset!==null && typeof(dataset)!=='undefined') {
	    	dataset.proxy("#distributor","id");
	    }
	    var content_models = ngds.content_models = {
	   
	     };


	    $.ajax({
	      url:'/api/action/contentmodel_list_short',
	      type:'POST',
	      data: JSON.stringify({
	        something:'something' // Ckan needs something in the body or the request is not accepted.
	      }),
	      success:function(response) {
	        for(var i=0;i<response.result.length;i++) {
	        	content_models[response.result[i].uri]= response.result[i];
	        }
	      }
	    });

	    $("input:radio[name='type-of-data']").change(function(ev){
	      var structured_or_un = ev.currentTarget.value;
	      
	      if(structured_or_un==='structured') {
	      	var div = $("<div/>",{class:"control-group control-full content-model-div-marker"});
	        var content_model_label = $("<label/>",{for:'content-model',text:'Content Model : ',class:'control-label'});
	        var content_model_combo = $("<select/>",{ name:"content_model" });
	        var controls = $("<div/>",{class:"controls"});
	         $('<option/>', {value: "", text: "Select a Content Model"}).appendTo(content_model_combo);
	        for(var val in ngds.content_models) {
			    $('<option/>', {value: val, text: ngds.content_models[val].title}).appendTo(content_model_combo);
			}
			controls.append(content_model_combo);
			div.append(content_model_label);
			div.append(controls);
			$(".content-model-marker").after(div);	        
	      }
	      else{
	      	$(".content-model-div-marker").remove();
	      	if($(".content-model-version-marker")!==null && typeof $(".content-model-version-marker")!=='undefined') {
	      		$(".content-model-version-marker").remove();
	      	}
	      }
	      
	    });

	    $(".module-content").on('change','.content-model-div-marker',function() {
	    	
	    	if($(".content-model-version-marker")!==null && typeof $(".content-model-version-marker")!=='undefined') {
	      		$(".content-model-version-marker").remove();
	      	}
	    	var content_model_selected = $("select[name='content_model']").val();
	    	if(ngds.content_models[content_model_selected]===null || typeof ngds.content_models[content_model_selected]==='undefined') {
	    		return;
	    	}
	    	var div = $("<div/>",{class:"control-group control-full content-model-version-marker"});
	    	var content_model_version = $("<label/>",{for:'content-model_version',text:'Version: ',class:'control-label'});
	    	var content_model_version_combo = $("<select/>",{ name:"content_model_version" });
	        var controls = $("<div/>",{class:"controls"});

	        for(var i=0;i<ngds.content_models[content_model_selected].versions.length;i++) {
	        	$('<option/>',{value:ngds.content_models[content_model_selected].versions[i].uri,text:ngds.content_models[content_model_selected].versions[i].version}).appendTo(content_model_version_combo);
	        }
			controls.append(content_model_version_combo);
			div.append(content_model_version);
			div.append(controls);
			$(".content-model-marker+div").after(div);	       
	    });	

		if($("button[name='mine']").length!==0) {
			$("button[name='mine']").click(function() {
				var content_model_selected = $("select[name='content_model']").val();
				var content_model_version = $("select[name='content_model_version']").val();

				if(content_model_selected!==null && typeof content_model_selected!=='undefined' && content_model_version!==null && typeof content_model_version!=='undefined') {
					$.ajax({
						url:'/api/action/contentmodel_checkFile',
						type:'POST',
						data:JSON.stringify({
							cm_uri:content_model_selected,
							cm_version:content_model_version,
							csvfile:'/hardcoded'
						}),
						success:function(response) {
							console.log(response);
							$(".dataset-resource-form").submit();
						}
					});
				}
				$(".dataset-resource-form").submit();
				
			});
		}

	});

})();
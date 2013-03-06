var ngds = ngds || { };
(function() {
	$(document).ready(function() { 

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
					$("#login-popup").hide();
				}				
			});

		$(document).keyup(function(e){ // On ESC hide the Not Implemented Yet popup, if it's visible.
			if(e.keyCode===27 && ngds.not_implemented_popup_active) {
				$("#not-implemented-popup").hide();
			}
		});

		(function(){ // Handle login popup events.

			$("#login").click(function(){ // When clicked, toggle between visible and hidden.
				if(isLoginPopupVisible()) {
					$("#login-popup").hide();
				}
				else {
					$("#login-popup").show();
				}
				return false;
			});

			$(document).keyup(function(e){ // On ESC toggle between visible and hidden.
				if(e.keyCode===27 && isLoginPopupVisible()) {
					$("#login-popup").hide();
				}
			});

			$("#login-popup").click(function(){ // Prevent the click event propagating upwards to document and resulting in the login popup being hidden
													// when a click occurs inside the div.
				return false;
			})

		})();


		(function(){ // Handle username and password state transitions.
			
			$("#username").click(function(e){
				return false;
			});

			$("#password").click(function(e){ // Preventing the click event from firing on the document and resulting in the login popup from vanishing
												// due to the focus event binding below.
				return false;
			});

			$("#username").focus(function(e) {
					if(this.value==="username") {
						this.value = "";
					}
				});

			$("#username").blur(function(e) {
					if(this.value==="") {
						this.value = "username";
					}
				});

			$("#password").focus(function(e) {
					if(this.value==="password") {
						this.value = "";
					}
				});

			$("#password").blur(function(e) {
					if(this.value==="") {
						this.value = "password";
					}
				});

		})();


		$("#accordion").accordion({ // Create and configure the library search page's accordion menu.
		    	autoHeight:false,
		    	clearStyle: false,
		    	header:"h4",
		    	heightStyle:"content",
		    	active:false,
		    	collapsible:true
			});

		function isLoginPopupVisible(){
				return ($("#login-popup").css('display')!=='none');
			}

	});

})();
$(document).ready(function() {
	
	var cycler = function(initialState, possibleStates, setupInitialState, transitions) {
		// Cycle between a set of states.
		var stateIndex = $.inArray(initialState,possibleStates);
				if(stateIndex==-1) {
			throw "Initial State is not in the list of possible states."
		}
		// Execute initial transition
		setupInitialState();
		++stateIndex;
		return {
			cycle:function() {
				if(stateIndex==possibleStates.length-1) {
					stateIndex = 0;
				}
				else {
					++stateIndex;
				}
				transitions[stateIndex]();
			}
		}
	};

	// Run initial setup stuff for the home page. (Login dialog show/hide functionality, default text in username/password fields)
	(function() {
		
		// Beginning of event handling for the login form.

		var initialState = "hidden";
		var possibleStates = ["hidden","visible"];
		var initialStateSetup = function() {
			$("#login-popup").hide();
		};

		var transitions = [
			function() {
				$("#login-popup").show();
			},
			function() {
				$("#login-popup").hide();
			}
		];

		var loginPopupToggler = cycler(initialState,possibleStates,initialStateSetup,transitions);
		
		$("#login").click(function() {
			loginPopupToggler.cycle();
		});

		$(document).keyup(function(e) { // We might also want to hide that login div when the escape key is pressed while it's visible. 
 			if(e.keyCode===27 && $("#login-popup").css('display')==="block") {
				loginPopupToggler.cycle();
			}
		});

		var unamePasswdInitialState = "default";
		var unamePasswdPossibleStates = ["default","blank"];

		var unamePasswdSetInitialState = function() {
			$("#username").value = "username";
			$("#password").value = "password";
		}

		var unamePasswdTransitions = [
			function() {
				$("#username").value="";
				$("#password").value="";
			},
			function() {
				$("#username").value="username";
				$("#password").value="password";
			}
		];


		var usernameToggler = cycler(unamePasswdInitialState,unamePasswdPossibleStates,unamePasswdSetInitialState,unamePasswdTransitions);

		$("#username").focus(function() {
			console.log("Focus");
			usernameToggler.cycle();
		});


		// $("#username").focus(function() {
		// 	if(this.value==="username") {
		// 		this.value = "";
		// 	}
		// });

		// $("#username").blur(function() {
		// 	if(this.value==="") {
		// 		this.value = "username";
		// 	}
		// });

		// $("#password").focus(function() {
		// 	if(this.value==="password") {
		// 		this.value = "";
		// 	}
		// });

		// $("#password").blur(function() {
		// 	if(this.value==="") {
		// 		this.value = "password";
		// 	}
		// });

		// End of event handling for the login form.

	})();


});


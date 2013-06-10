var ngds = ngds || ( ngds= { } );

(function setup_debugging(){
	if(window.document.location.hash==="#!debug") {
		
		ngds.log = function(msg,last_log) {
			ngds.last_log = last_log;
			console.log(msg);
		};

		ngds.error = function(msg,last_error) {
			ngds.last_error = last_error;
			console.error(msg);
		};

	}
	else {
		
		ngds.log = function(msg,last_log) {
			ngds.last_log = last_log;
			// swallow it.
		};

		ngds.error = function(msg,last_error) {
			ngds.last_error = last_error;
			// swallow it.
		}

	}
})();

ngds.publish = function(topic,msg) {
	ngds.log("Published message : "+msg+" to topic : "+topic,msg);
	PubSub.publish(topic,msg);
};

ngds.subscribe = function(topic,handler) {
	ngds.log("Subscribed to topic : "+topic+" with handler : "+handler,handler);
	PubSub.subscribe(topic,handler);
}

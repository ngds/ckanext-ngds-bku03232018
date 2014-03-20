/* Copyright (c) 2014, Siemens Coporate Technology and Arizona Geological Survey */
var ngds = ngds || (ngds = { }); 

(function subscribe_notifications_received() {
	ngds.subscribe('Notifications.received',function(topic,data){
		var handler = ngds.notifications.handlers['resource_form_validation_error']; // Find a display handler for this type of error message.
		handler(data);
	});
})();

ngds.notifications = { };

$.ajax({
	'url':'/scripts/notifications/error_dialog.tmf',
	'success':function(response) {
		ngds.error_message_template = response;
	}
});

ngds.notifications.handlers = {
	'resource_form_validation_error':function(error){
		var error_msg = Mustache.render(ngds.error_message_template,error);
		$(document).append(error_msg);
		$(error_msg).dialog({
			'width':600,
			'height':300
		});
	}
};


/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
var ngds=ngds||(ngds={});(function setup_debugging(){if(window.document.location.hash==="#!debug"){ngds.log=function(b,a){ngds.last_log=a;console.log(b)};ngds.error=function(b,a){ngds.last_error=a;console.error(b)}}else{ngds.log=function(b,a){ngds.last_log=a};ngds.error=function(b,a){ngds.last_error=a}}})();ngds.publish=function(a,b){ngds.log("Published message : "+b+" to topic : "+a,b);PubSub.publish(a,b)};ngds.subscribe=function(a,b){ngds.log("Subscribed to topic : "+a+" with handler : "+b,b);PubSub.subscribe(a,b)};

L.Control.FullScreen = L.Control.extend({
	options: {
		position: 'topleft',
		title: 'Full Screen'
	},
	
	onAdd: function (map) {
		// Do nothing if we can't
		if (!fullScreenApi.supportsFullScreen)
			return map.zoomControl._container;
		
		var containerClass = 'leaflet-control-zoom', className, container;
		
		if(map.zoomControl) {
			container = map.zoomControl._container;
			className = '-fullscreen leaflet-bar-part leaflet-bar-part-bottom last';
			// Update class of the zoom out button (Leaflet v0.5)
			if (map.zoomControl._zoomOutButton) {
				L.DomUtil.removeClass(map.zoomControl._zoomOutButton, 'leaflet-bar-part-bottom');
			}
		} else {
			container = L.DomUtil.create('div', containerClass);
			className = '-fullscreen';
		}
		
		this._createButton(this.options.title, containerClass + className, container, this.toogleFullScreen, map);

		return container;
	},
	
	_createButton: function (title, className, container, fn, context) {
		var link = L.DomUtil.create('a', className, container);
		link.href = '#';
		link.title = title;

		L.DomEvent
			.addListener(link, 'click', L.DomEvent.stopPropagation)
			.addListener(link, 'click', L.DomEvent.preventDefault)
			.addListener(link, 'click', fn, context);
		
		L.DomEvent
			.addListener(container, fullScreenApi.fullScreenEventName, L.DomEvent.stopPropagation)
			.addListener(container, fullScreenApi.fullScreenEventName, L.DomEvent.preventDefault)
			.addListener(container, fullScreenApi.fullScreenEventName, this._handleEscKey, context);
		
		L.DomEvent
			.addListener(document, fullScreenApi.fullScreenEventName, L.DomEvent.stopPropagation)
			.addListener(document, fullScreenApi.fullScreenEventName, L.DomEvent.preventDefault)
			.addListener(document, fullScreenApi.fullScreenEventName, this._handleEscKey, context);

		return link;
	},
	
	toogleFullScreen: function () {
		this._exitFired = false;
		if (fullScreenApi.supportsFullScreen){
			var container = this._container;
			if(fullScreenApi.isFullScreen(container)){
				fullScreenApi.cancelFullScreen(container);
				this.invalidateSize();
				this.fire('exitFullscreen');
				this._exitFired = true;
			}
			else {
				fullScreenApi.requestFullScreen(container);
				this.invalidateSize();
				this.fire('enterFullscreen');
			}
		}
	},
	
	_handleEscKey: function () {
		
		if(!fullScreenApi.isFullScreen(this)){
			fullScreenApi.cancelFullScreen();			
		}
	}
});

L.Map.addInitHook(function () {
	if (this.options.fullscreenControl) {
		this.fullscreenControl = L.control.fullscreen();
		this.addControl(this.fullscreenControl);
	}
});

L.control.fullscreen = function (options) {
	return new L.Control.FullScreen(options);
};

/* 
Native FullScreen JavaScript API
-------------
Assumes Mozilla naming conventions instead of W3C for now

source : http://johndyer.name/native-fullscreen-javascript-api-plus-jquery-plugin/

*/

(function() {
	var 
		fullScreenApi = { 
			supportsFullScreen: false,
			isFullScreen: function() { return false; }, 
			requestFullScreen: function() {}, 
			cancelFullScreen: function() {},
			fullScreenEventName: '',
			prefix: ''
		},
		browserPrefixes = 'webkit moz o ms khtml'.split(' ');
	
	// check for native support
	if (typeof document.exitFullscreen != 'undefined') {
		fullScreenApi.supportsFullScreen = true;
	} else {	 
		// check for fullscreen support by vendor prefix
		for (var i = 0, il = browserPrefixes.length; i < il; i++ ) {
			fullScreenApi.prefix = browserPrefixes[i];
			
			if (typeof document[fullScreenApi.prefix + 'CancelFullScreen' ] != 'undefined' ) {
				fullScreenApi.supportsFullScreen = true;
				
				break;
			}
		}
	}
	
	// update methods to do something useful
	if (fullScreenApi.supportsFullScreen) {
		fullScreenApi.fullScreenEventName = fullScreenApi.prefix + 'fullscreenchange';
		
		fullScreenApi.isFullScreen = function() {
			switch (this.prefix) {	
				case '':
					return document.fullScreen;
				case 'webkit':
					return document.webkitIsFullScreen;
				default:
					return document[this.prefix + 'FullScreen'];
			}
		}
		fullScreenApi.requestFullScreen = function(el) {
			ngds.publish("Map.size_changed",{
				'fullscreen':true
			});

			ngds.Map.state['map-container-height']=$("#map-container").css("height");
			if(typeof $("#content-container")[0].webkitRequestFullScreen!=='undefined') {
				$("#content-container")[0].webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
			}
			if(typeof $("#content-container")[0].mozRequestFullScreen!=='undefined') {
				$("#content-container")[0].mozRequestFullScreen();
			}
			fullsc = '';
			setTimeout(function() {
				var ch = $("#content-container").css("height");
				$("#map-container").css("height","100%");
				// ngds.Map.state["orig_results_height"] = $(".results").css("height");
				// ngds.Map.state['orig_jspContainer_height'] = $(".jspContainer").css("height");
				// ngds.Map.state['orig_jspTrack_height'] = $(".jsptrack").css("height");
				// ngds.Map.state['orig_jspDrag_height'] = $(".jspDrag").css("height");
				
				// $(".results").addClass("large");
				
				// $(".jspContainer").css("height","700px");
				
				// $(".jspTrack").css("height","700px");
				
				// $(".jspDrag").css("height","500px");
				ngds.Map.map.invalidateSize();


				

				fullsc = true;

			},100);

			return true;
			// return (this.prefix === '') ? el.requestFullscreen() : el[this.prefix + 'RequestFullScreen']();
		}
		fullScreenApi.cancelFullScreen = function(el) {
			ngds.publish("Map.size_changed",{
				'fullscreen':false
			});
			(this.prefix === '') ? document.exitFullscreen() : document[this.prefix + 'CancelFullScreen']();
			setTimeout(function() {
						$("#map-container").css("height","700px");
			// $(".jspDrag").css("height",ngds.Map.state['orig_jspDrag_height']);
			// $(".jspTrack").css("height",ngds.Map.state['orig_jspTrack_height']);
			// $(".jspContainer").css("height",ngds.Map.state['orig_jspContainer_height']);
			// $(".results").removeClass("large");
			
			},100);
			return true;
		}		
	}

	// jQuery plugin
	if (typeof jQuery != 'undefined') {
		jQuery.fn.requestFullScreen = function() {
			i=0;
			return this.each(function() {
				var el = jQuery(this);
				if (fullScreenApi.supportsFullScreen) {
					i++;
					fullScreenApi.requestFullScreen(el);
					// fullScreenApi.requestFullScreen($(".map-search-results"));
				}

			});
		};
	}

	// export api
	window.fullScreenApi = fullScreenApi;	
})();

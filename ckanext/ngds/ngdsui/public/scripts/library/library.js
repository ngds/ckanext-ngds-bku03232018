var ngds = ngds || { };

(function() {
	$(document).ready(function() { 

		$(".accordion").accordion({ // Create and configure the library search page's accordion menu.
		    	autoHeight:false,
		    	clearStyle: false,
		    	header:"> li > h3",
		    	heightStyle:"content",
		    	active:false,
		    	collapsible:true
		});

		$(".facet").click(function() {
	      window.location = $(this).attr('href');
	      return false;
   		});      


	});

})();
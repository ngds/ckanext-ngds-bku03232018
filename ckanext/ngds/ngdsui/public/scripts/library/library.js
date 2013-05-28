var ngds = ngds || { };

(function() {
	$(document).ready(function() { 

		$(".accordion").accordion({ // Create and configure the library search page's accordion menu.
		    	autoHeight:false,
		    	clearStyle: false,
		    	header:"> li > h3",
		    	heightStyle:"content",
		    	active:false,
		    	collapsible:true,
		    	beforeActivate: function(event, ui) {
						         // The accordion believes a panel is being opened
						        if (ui.newHeader[0]) {
						            var currHeader  = ui.newHeader;
						            var currContent = currHeader.next('.ui-accordion-content');
						         // The accordion believes a panel is being closed
						        } else {
						            var currHeader  = ui.oldHeader;
						            var currContent = currHeader.next('.ui-accordion-content');
						        }
						         // Since we've changed the default behavior, this detects the actual status
						        var isPanelSelected = currHeader.attr('aria-selected') == 'true';

						         // Toggle the panel's header
						        currHeader.toggleClass('ui-corner-all',isPanelSelected).toggleClass('accordion-header-active ui-state-active ui-corner-top',!isPanelSelected).attr('aria-selected',((!isPanelSelected).toString()));

						        // Toggle the panel's icon
						        currHeader.children('.ui-icon').toggleClass('ui-icon-triangle-1-e',isPanelSelected).toggleClass('ui-icon-triangle-1-s',!isPanelSelected);

						         // Toggle the panel's content
						        currContent.toggleClass('accordion-content-active',!isPanelSelected)    
						        if (isPanelSelected) { currContent.slideUp(); }  else { currContent.slideDown(); }

						        return false; // Cancels the default action
						    }
		});

		$(".facet").click(function() {
	      window.location = $(this).attr('href');
	      return false;
   		});  

		$('#expander-image').click(function() {

			var sections = $('.accordion').find("> li > h3");

			if($(this).attr('src') == '/assets/plus_grey.png'){
			
		      sections.each(function(index, section){
							    if ($(section).hasClass('ui-state-default')) {
							      $(section).click();
							    }
							  });
		      $(this).attr('src','/assets/minus_grey.png');		    
		      $(this).attr('title','Collapse All');
			}
			else {

				  sections.each(function(index, section){
				    if ($(section).hasClass('ui-state-active')) {
				      $(section).click();
				    }
				  });

				$(this).attr('src','/assets/plus_grey.png');		    
				$(this).attr('title','Expand All');

			}

		    return false;
		}); 




		$('#field-order-by').change(function() {
		    // $('#hide-button').click();
		    var params = window.location.href.split('?')[1];
		    if(typeof params==='undefined'){
		    	$('#hide-button').click();
		    }
		    var split_params = params.split('&');
		    var acccumulator = [];

		    for(var i=0;i<split_params.length;i++) {		    	
		       	if(split_params[i].indexOf('sort=')===-1) {
		    		acccumulator.push(split_params[i]);
		    	}
		    }
		    acccumulator.push('sort='+$('#field-order-by').val());
		    var finished_string = acccumulator.join('&');
		    //acccumulator+='&sort='+$('#field-order-by').val();
		    console.log(finished_string);

		    window.location.href = window.location.href.split('?')[0]+"?"+finished_string;
		});  		    


	});

})();
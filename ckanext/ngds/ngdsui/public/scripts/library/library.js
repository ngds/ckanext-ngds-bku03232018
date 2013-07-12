var ngds = ngds || { };
ngds.state = ngds.state || ( ngds.state = { } );

	Date.prototype.getISOString = function(timeDecider) {
		hours = this.getUTCHours();
		mins = this.getUTCMinutes();
		secs = this.getUTCSeconds();

		if (timeDecider===-1){
			hours = 0;
			mins =0;
			secs=0;
		}else if(timeDecider===1){
			hours = 23;
			mins =59;
			secs=59;
		}

        function pad(n) { return n < 10 ? '0' + n : n }
        return this.getUTCFullYear() + '-'
            + pad(this.getUTCMonth() + 1) + '-'
            + pad(this.getUTCDate()) + 'T'
            + pad(hours) + ':'
            + pad(mins) + ':'
            + pad(secs) + 'Z';
    };


(function() {
	$(document).ready(function() { 

		$(".accordion").accordion({ // Create and configure the library search page's accordion menu.
		    	autoHeight:false,
		    	clearStyle: false,
		    	header:"> li > h3",
		    	heightStyle:"content",
		    	active:false,
		    	collapsible:true,
		    	navigation: true,
		    	icons:{   header: "expandIcon",activeHeader: "collapseIcon"},
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
						        currHeader.children('.ui-icon').toggleClass('expandIcon',isPanelSelected).toggleClass('collapseIcon',!isPanelSelected);

						         // Toggle the panel's content
						        currContent.toggleClass('accordion-content-active',!isPanelSelected)    
						        if (isPanelSelected) { currContent.slideUp(); }  else { currContent.slideDown(); }

						        return false; // Cancels the default action
						    }
		});

		$(".expanded").parents().filter("li").children().filter("h3").click();


/*		$(".facet").click(function() {
	      window.location = $(this).attr('href');
	      return false;
   		}); */ 

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


		previousElement = $(".pagination ul li a").filter(function(index){return $(this).text()==="«"; })[0];

		if ($(previousElement).length>0){
			    var newHTML = $(previousElement).html().replace('«','<img src = "/assets/previous.png" class="previous"/>');
      			$(previousElement).html(newHTML);
		}

		nextElement = $(".pagination ul li a").filter(function(index){return $(this).text()==="»"; })[0];

		if ($(nextElement).length>0){
			    var newHTML = $(nextElement).html().replace('»','<img src = "/assets/next.png" class="previous"/>');
      			$(nextElement).html(newHTML);
		}

        $('#save_search').click(function() {

		    var url= window.location.href;

            $( "#dialog-form" ).dialog( "open" );
		});

        $( "#dialog-form" ).dialog({
          autoOpen: false,
          height: 185,
          width: 300,
          modal: true,
          buttons: {
            "Save Search": function() {
                var url= window.location.href;
                ngds.state['search_name'] = $("#search_name").val();
                $.ajax({
                  url:'/ngds/save_search',
                  'type':'POST',
                  'data':{
                      url:url,
                      search_name:$( "#search_name" ).val()
                  },
                  success:function(response){
                        $( "#dialog-form" ).dialog("close");
                        var li = $("<li/>",{});
                        var a = $("<a/>",{text:ngds.state['search_name'], href:window.location.href });
                        li.append(a);
                        $( "#search_name" ).val('');
                        $("ul#saved-list").append(li);
                        $("ul#saved-list").menu("refresh");
                  }
                });
            },
            Cancel: function() {
              $( this ).dialog( "close" );
            }
          }
        });

       menu = $("ul#saved-list").menu().hide();

        $("#saved_searches_list_button").click(function() {
                menu.show().position({
                my: "left top",
                at: "left bottom",
                of: this
                });

                // Register a click outside the menu to close it
                $( document ).one( "click", function() {
                    menu.hide();
                });

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
		    //console.log(finished_string);

		    window.location.href = window.location.href.split('?')[0]+"?"+finished_string;
		}); 

		$('.facet').change(function(){
			//console.log($('.facet').val());
			window.location.href =$(this).val();

		});

		$('#filter-pub-date').click(function() {

			 from_date = $('#from-date').val();
			 to_date = $('#to-date').val();
			 console.log("Entered Here...");
			console.log(from_date);
			console.log(to_date);

			if(from_date==='' && to_date ===''){
				return false;
			}

		    var params = window.location.href.split('?')[1];
		    console.log(params);
	    
		    var acccumulator = [];

		    if(typeof params==='undefined'){
		    	//$('#hide-button').click();
		    }else{		    
			    var split_params = params.split('&');
			    for(var i=0;i<split_params.length;i++) {		    	
			       	if(split_params[i].indexOf('publication_date=')===-1) {
			    		acccumulator.push(split_params[i]);
			    	}
			    }
		    }

		    date_range = "[";

		    if(from_date===''){
		    	date_range+=" * TO ";
		    }else{
		    	from_str = (new Date(from_date)).getISOString(-1);
		    	date_range+=from_str+" TO ";
		    }

		    if(to_date===''){
		    	date_range+=" * ]";
		    }else{
		    	to_str = (new Date(to_date)).getISOString(1);
		    	date_range+=to_str+" ]";
		    }		    

		    //console.log(date_range);

		    acccumulator.push('publication_date='+date_range);
		    var finished_string = acccumulator.join('&');
		    console.log(finished_string);

		    window.location.href = window.location.href.split('?')[0]+"?"+finished_string;
		});		





    $( "#from-date" ).datepicker({
      defaultDate: "-1d",
      changeMonth: true,
      changeYear: true,
      yearRange: "c-100:c+50",
      numberOfMonths: 1,
      onClose: function( selectedDate ) {
        $( "#to-date" ).datepicker( "option", "minDate", selectedDate );
      }
    });

    $( "#to-date" ).datepicker({
      defaultDate: "+1d",
      changeMonth: true,
      changeYear: true,
      yearRange: "c-100:c+50",
      numberOfMonths: 1,
      onClose: function( selectedDate ) {
        $( "#from-date" ).datepicker( "option", "maxDate", selectedDate );
      }
    });

	$( "#search-review[title]" ).tooltip();

	});

})();
ngds.Map.SearchContext = {
	is_defined:function(elem) {
		if(this[elem] === null || typeof this[elem] === 'undefined') {
			return false;
		}
	return true;
	},
	create_preamble:function(){
		var preamble_container = this['preamble-container'] = $("<div/>",{class:"search-results-preamble-container"});
		var preamble = this['preamble'] = $("<span/>",{class:"search-results-preamble"});
		preamble_container.append(preamble);
		$(".map-search-results").append(preamble_container);
	},
	set_preamble_count:function(count) {
		if(!this.is_defined("preamble-container")) {
			this.create_preamble();
		}
		this['preamble'].text("Found $1 results for $2".replace("$1",count).replace("$2",this['query']));
	},
	set_results:function(results){
		this['results'] = results;
		this.initialize_pager();
	},
	initialize_pager:function() {
		this.begin = 0;
		this.end = this['results'].length;
		this.bunch = 5;
	},
	next:function() {
		this.clear_or_init_results_div();
		
	},
	prev:function() {

	},
	num_pages:function() {
		return this['results'].length;
	},
	clear_or_init_results_div:function() {
		if(!is_defined('results')) {
			this.create_results_div();
		}
		this['results'].text("");
	},
	create_results_div:function() {
		var results = this['results'] = $("<div/>",{class:"results"});
		$(".map-search-results").append(results);
	}
};
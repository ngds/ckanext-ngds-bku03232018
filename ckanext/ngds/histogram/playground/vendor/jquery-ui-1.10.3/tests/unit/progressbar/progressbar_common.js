/* Copyright (c) 2014, Siemens Coporate Technology and Arizona Geological Survey */
TestHelpers.commonWidgetTests( "progressbar", {
	defaults: {
		disabled: false,
		max: 100,
		value: 0,

		//callbacks
		change: null,
		complete: null,
		create: null
	}
});

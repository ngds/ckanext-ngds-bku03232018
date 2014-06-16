/* Copyright (c) 2014, Siemens Coporate Technology and Arizona Geological Survey */
TestHelpers.spinner = {
	simulateKeyDownUp: function( element, keyCode, shift ) {
		element
			.simulate( "keydown", { keyCode: keyCode, shiftKey: shift || false } )
			.simulate( "keyup", { keyCode: keyCode, shiftKey: shift || false } );
	}
};


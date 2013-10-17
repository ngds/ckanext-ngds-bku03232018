#!/bin/awk -f

BEGIN { head = 0; header_found= 0; }

{
    if ( head == 0 ) {
	if (header_found == 0) {
	    # Our comments begin with 
	    if (/#* ___NGDS_HEADER_BEGIN___*/) {
		header_found = 1;
	    } else { # first line is not a comment - so go on
		print $0;
		head = 1;
	    }
	} else { # in header_found mode --> wait for end of header
	    if (/#*___NGDS_HEADER_END___*/) {
		head= 1;
		print "\
/* ___NGDS_HEADER_BEGIN___\n\
 * \n\
 * National Geothermal Data System - NGDS\n\
 * https://github.com/ngds\n\
 * \n\
 * File: <filename>\n\
 * \n\
 * Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey\n\
 * \n\
 * Please Refer to the README.txt file in the base directory of the NGDS\n\
 * project:\n\
 * https://github.com/ngds/ckanext-ngds/README.txt\n\
 * \n\
 * ___NGDS_HEADER_END___ */\n\
"
	    }

	}
    } else { # Header part is over or no header, so print the rest
	print $0
    }
}

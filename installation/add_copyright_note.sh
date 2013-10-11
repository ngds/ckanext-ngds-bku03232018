#!/bin/bash
#
# ATTENTION:
#    Script needs to be run from the installation directory!
#


# find all JavaScript Files
#find ../. -iname "*.js" -a ! -wholename "*/vendor/*" -a ! -iname "*[-.]min.js" -a ! -name "jquery*" -exec ls '{}' \;


# Store the path of the installation directory:
export currentpath=$PWD
echo $currentpath


# Find all JavaScript files excluding those in directory "vendor" and those matching "jquery*" and
# those that do not already have our tag: " ___NGDS_HEADER_BEGIN___":
# For each found file create a new one that adds our JavaScript Header:
find . -iname "*.js" -a ! -wholename "*/vendor/*" \
                     -a ! -iname "*[-.]min.js"  \
                     -a ! -iname "jquery*" \
                     -a ! -execdir grep -q -i "___NGDS_HEADER_BEGIN___" '{}' \; \
     -execdir bash -c "awk -f $currentpath/add_copyright_note_JAVASCRIPT.awk '{}' > '{}'.NGDS_COPYRIGHT ; mv '{}' '{}'.NGDS_OLD ; mv '{}'.NGDS_COPYRIGHT '{}'" \;


# Find all Python files excluding those in directory "vendor" and
# those that do not already have our tag: " ___NGDS_HEADER_BEGIN___":
# For each found file create a new one that adds our Python Header:
find . -iname "*.py" -a ! -wholename "*/vendor/*" \
                     -a ! -execdir grep -q -i "___NGDS_HEADER_BEGIN___" '{}' \; \
     -execdir bash -c "awk -f $currentpath/add_copyright_note_PYTHON.awk '{}' > '{}'.NGDS_COPYRIGHT ; mv '{}' '{}'.NGDS_OLD ; mv '{}'.NGDS_COPYRIGHT '{}'" \;


# Find all Jinja template files (*.html) excluding those in directory "vendor" and
# those that do not already have our tag: " ___NGDS_HEADER_BEGIN___":
# For each found file create a new one that adds our Python Header:
find . -iname "*.html" -a ! -wholename "*/vendor/*" \
                       -a ! -execdir grep -q -i "___NGDS_HEADER_BEGIN___" '{}' \; \
     -execdir bash -c "awk -f $currentpath/add_copyright_note_HTML.awk '{}' > '{}'.NGDS_COPYRIGHT ; mv '{}' '{}'.NGDS_OLD ; mv '{}'.NGDS_COPYRIGHT '{}'" \;


# Find all CSSless template files (*.less) excluding those in directory "vendor" and
# those that do not already have our tag: " ___NGDS_HEADER_BEGIN___":
# For each found file create a new one that adds our Python Header:
find . -iname "*.less" -a ! -wholename "*/vendor/*" \
                       -a ! -execdir grep -q -i "___NGDS_HEADER_BEGIN___" '{}' \; \
     -execdir bash -c "awk -f $currentpath/add_copyright_note_HTML.awk '{}' > '{}'.NGDS_COPYRIGHT ; mv '{}' '{}'.NGDS_OLD ; mv '{}'.NGDS_COPYRIGHT '{}'" \;


# Find all CSS template files (*.css) excluding those in directory "vendor" and
# those that do not already have our tag: " ___NGDS_HEADER_BEGIN___":
# For each found file create a new one that adds our Python Header:
find . -iname "*.css" -a ! -wholename "*/vendor/*" \
                      -a ! -iname "*[-.]min.css"  \
                      -a ! -execdir grep -q -i "___NGDS_HEADER_BEGIN___" '{}' \; \
     -execdir bash -c "awk -f $currentpath/add_copyright_note_HTML.awk '{}' > '{}'.NGDS_COPYRIGHT ; mv '{}' '{}'.NGDS_OLD ; mv '{}'.NGDS_COPYRIGHT '{}'" \;


#!/bin/bash

merge_with_ckan=`grep 'merge_with_ckan=' merge.cfg | awk -F"=" '{print $2}'`

NGDS_i18n_DIR=`grep 'NGDS_i18n_DIR=' merge.cfg | awk -F"=" '{print $2}'`

CKAN_i18n_DIR=`grep 'CKAN_i18n_DIR=' merge.cfg | awk -F"=" '{print $2}'` #Ckan Default i18n directory

file_list="file_list.txt" #Temp file used to merge messages.

home_pyenv=`grep 'home_pyenv=' merge.cfg | awk -F"=" '{print $2}'` #Python env
ngds_home=`grep 'ngds_home=' merge.cfg | awk -F"=" '{print $2}'` #Python env

LOCALES=`ls -l --time-style="long-iso" $NGDS_i18n_DIR | egrep '^d' | awk '{print $8}'`

. $home_pyenv/bin/activate

# and now loop through the Locales:
for locale in $LOCALES
do
echo  "Processing messages of locale: ${locale}"

	ngds_po="$NGDS_i18n_DIR/$locale/LC_MESSAGES/ckan.po" 
	output_po=$ngds_po
	backup_po="$NGDS_i18n_DIR/$locale/LC_MESSAGES/ngds_bak.po" 
	ckan_po=""
	if [ "$merge_with_ckan" = "true" ]
		then
		echo "Creating backup of NGDS messages to ngds_bak.po"
		cp $ngds_po $backup_po
		if [ "$locale" = "en" ]
			then
			locale="en_GB"
		fi
		ckan_po="$CKAN_i18n_DIR/$locale/LC_MESSAGES/ckan.po"
		echo  "Merging with CKAN's locale: ${locale}"
	fi
	
echo "$ngds_po
$ckan_po" > $file_list

msgcat --use-first -f $file_list -o $output_po
done
cd $ngds_home
python setup.py compile_catalog
cd -
#Remove the temp file
/bin/rm $file_list
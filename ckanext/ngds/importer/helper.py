""" NGDS_HEADER_BEGIN

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey

Please refer the the README.txt file in the base directory of the NGDS project:
https://github.com/ngds/ckanext-ngds/blob/master/README.txt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.  https://github.com/ngds/ckanext-ngds
ngds/blob/master/LICENSE.md or
http://www.gnu.org/licenses/agpl.html

NGDS_HEADER_END """

import datetime as datetime
from ckan.lib.base import config
import ckan.controllers.storage as storage

log = __import__("logging").getLogger(__name__)

BUCKET = config.get('ckan.storage.bucket', 'default')

def upload_file_return_path(file_name=None, file_path=None):
    """
    Loads the input file into Pairtree system by creating unique directory name based on the current timestamp values.
    Reads the file and calls Pairtree storage to load the file into the server for the bulk upload process.
    """
    log.debug("file_name:%s, file_path: %s" % (file_name, file_path))

    if file_name is None or file_path is None:
        log.error("Either file_name or file_path is None")
        return None
    utc_time = datetime.datetime.utcnow()

    generated_dir = str(utc_time.year) +'-'+ str((utc_time.month)).zfill(2) +'-'+ str((utc_time.day)).zfill(2) +'T'+ str((utc_time.hour)).zfill(2) +':'+ str((utc_time.minute)).zfill(2)+':'+ str((utc_time.second)).zfill(2)

    log.debug("Generated directory %s" % generated_dir)

    label = generated_dir+'/'+file_name

    bucket_id = BUCKET

    params = {'filename-original': file_name, 'uploaded-by': u'admin', 'key': label}

    f = open(file_path+file_name, "rb") # notice the b for binary mode
    data = f.read()
    #storage.get_ofs().put_stream(bucket_id, label, stream.file, params)
    ofs = storage.get_ofs()
    ofs.put_stream(bucket_id, label, data, params)
    f.close()

    log.debug("%s File Uploaded successfully." % file_name)

    #uploaded_file_url = h.url_for('storage_file',label=label,qualified=True)
    uploaded_file_url = ofs.get_url(bucket_id,label)

    log.debug("uploaded_file_url: %s" % uploaded_file_url)

    return uploaded_file_url


def delete_files(file_path, files_to_delete=None, ignore_files=None):
    """
    Deletes the files from the disk. If the bulk upload fails initial upload validation then uploaded files should be
    deleted from the server. This function deletes the files under the provided file path and ignore any file if it
    is part of the ignore file list.
    """

    import os
    os.chdir(file_path)    

    if files_to_delete:
        files_to_iterate = files_to_delete
    else:
        files_to_iterate = os.listdir(".")

    for filename in files_to_iterate:
        isIgnore = False
        if ignore_files :
            if filename in ignore_files:
                isIgnore = True
        if not isIgnore:
            os.unlink(filename)

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

"""
This file contains the extended version of CKAN Client class.This client will be used during "bulk-upload" process
for creating datasets in CKAN.
"""

from ckanclient import CkanClient
import urlparse
import os
from datetime import datetime

class NgdsCkanClient(CkanClient):
    """
    Extends from CkanClient Class and overrides the upload_file method. Default upload_file method doesn't support
    binary files upload.
    """

    def __init__(self, base_location=None, api_key=None, is_verbose=False,
                 http_user=None, http_pass=None):
        self.base_netloc = urlparse.urlparse(base_location).netloc
        super(NgdsCkanClient, self).__init__(base_location=base_location, api_key=api_key, is_verbose=is_verbose,
                 http_user=http_user, http_pass=http_pass)

    def upload_file(self, file_path):
        '''Upload a file to a CKAN instance via CKAN's FileStore API.

        The CKAN instance must have file storage enabled.

        A timestamped directory is created on the server to store the file as
        if it had been uploaded via the graphical interface. On success, the
        URL of the file is returned along with an empty error message. On
        failure, the URL is an empty string.

        :param file_path: path to the file to upload, on the local filesystem
        :type file_path: string

        :returns: a (url, errmsg) 2-tuple containing the URL of the
            successufully uploaded file on the CKAN server (string, an empty
            string if the upload failed) and any error message from the server
            (string, an empty string if there was no error)
        :rtype: (string, string) 2-tuple

        '''
        # see ckan/public/application.js:makeUploadKey for why the file_key
        # is derived this way.
        ts = datetime.isoformat(datetime.now()).replace(':','').split('.')[0]
        norm_name  = os.path.basename(file_path).replace(' ', '-')
        file_key = os.path.join(ts, norm_name)
        auth_dict = self.storage_auth_get('/form/'+file_key, {})
        u = urlparse.urlparse(auth_dict['action'])

        import requests
        url = 'http://' + self.base_netloc + u.path

        headers = { 'Authorization': self.api_key,'X-CKAN-API-Key': self.api_key }

        res = requests.post(url,data={'key':file_key},files={'file': (os.path.basename(file_key), open(file_path, 'rb'))}, headers=headers)

        errcode = res.status_code
        errmsg = ''

        if errcode == 200:
            return 'http://%s/storage/f/%s' % (self.base_netloc, file_key), ''
        else:
            return '', errmsg

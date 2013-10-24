from Geoserver import Geoserver
from os import listdir, getcwd, makedirs, walk
from os.path import isfile, isdir, join, normpath
from urlparse import urlsplit
import urllib2
from urllib import urlretrieve
import json
import sys
import re

class ManageStyles:

    def __init__(self):
        self.model_url = 'http://schemas.usgin.org/contentmodels.json'
        self.geoserver = Geoserver.from_ckan_config()

    def get_sld_dir(self, folder_name='sld_files'):
        path = getcwd()
        parent = normpath(join(path, '..'))
        if folder_name in listdir(parent):
            return join(parent, folder_name)
        elif folder_name not in listdir(parent):
            makedirs(join(parent, folder_name))
            return join(parent, folder_name)
        else:
            error_msg = sys.exc_info()[0]
            return "Error: %s" % error_msg

    def get_content_models(self):
        url = self.model_url
        reader = urllib2.urlopen(url).read()
        data = json.loads(str(reader))
        return data

    def make_file_path(self, path):
        base_dir = self.get_sld_dir()
        if path is not None:
            this_path = urlsplit(path).path
            file_name = this_path.rsplit('/',1)[1]
            pattern_id = r'.*?\/files/(.*)/.*'
            path_id = re.search(pattern_id, this_path).group(1)
            pattern_safe_chars = re.compile('(-|\.)')
            path_folders = pattern_safe_chars.sub('_', path_id).rsplit('/')
            return join(base_dir, path_folders[0], path_folders[1], file_name)
        else:
            return None

    def get_sld_info(self, content_model=None):
        data = self.get_content_models()
        if content_model is None:
            return dict((model['label'], (version['uri'], version['sld_file_path'],
                        self.make_file_path(version['sld_file_path']))) for model in
                        data for version in model['versions'])
        else:
            return dict((model['label'], (version['uri'], version['sld_file_path'],
                        self.make_file_path(version('sld_file_path')))) for model in
                        data for version in model['versions'] if model['uri'] ==
                        content_model)

    def build_file_directory(self):
        data = self.get_sld_info()
        urls = [value[1] for value in data.itervalues()]
        for url in urls:
            file_path = self.make_file_path(url)
            if file_path is not None: makedirs(file_path)

    def download_styles(self):
        data = self.get_sld_info()
        for value in data.itervalues():
            url = value[1]
            path = value[2]
            if url is not None: urlretrieve(url, path)

    def make_file_path_list(self):
        these_paths = []
        base_dir = self.get_sld_dir()
        for paths, dirs, files in walk(base_dir):
            if len(dirs) == 0:
                these_paths.append(paths)
        return these_paths

a = Styles()

a.download_styles()
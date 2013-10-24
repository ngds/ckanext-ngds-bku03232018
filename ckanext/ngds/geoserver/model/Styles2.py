from Geoserver import Geoserver
from os import listdir, getcwd, makedirs, walk
from os.path import isfile, basename, join, normpath
from urlparse import urlsplit
import urllib2
from urllib import urlretrieve
import json
import sys
import re
import zipfile
from shutil import copyfileobj

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

    def make_file_path(self, path, download=True):
        base_dir = self.get_sld_dir()
        if path is not None:
            this_path = urlsplit(path).path
            file_name = this_path.rsplit('/', 1)[1]
            pattern_id = r'.*?\/files/(.*)/.*'
            path_id = re.search(pattern_id, this_path).group(1)
            pattern_safe_chars = re.compile('(-|\.)')
            path_folders = pattern_safe_chars.sub('_', path_id).rsplit('/')
            if download:
                return join(base_dir, path_folders[0], path_folders[1], file_name)
            else:
                return join(base_dir, path_folders[0], path_folders[1])
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
            file_path = self.make_file_path(url, False)
            if file_path is not None:
                makedirs(file_path)

    def download_styles(self):
        data = self.get_sld_info()
        for value in data.itervalues():
            url = value[1]
            path = value[2]
            if url is not None:
                urlretrieve(url, path)

    def make_file_path_list(self):
        these_paths = []
        base_dir = self.get_sld_dir()
        for paths, dirs, files in walk(base_dir):
            if len(dirs) == 0:
                these_paths.append(paths)
        return these_paths

    def get_style_file(self, path):
        this_path = path
        files = [f for f in listdir(this_path) if isfile(join(this_path,f)) if not f.startswith('.')]
        path_files = [join(this_path,f) for f in files]
        return path_files

    def get_style_file_list(self):
        these_paths = []
        paths = self.make_file_path_list()
        for path in paths:
            full_path = self.get_style_file(path)
            these_paths.append(full_path)
        return [path for sub_list in these_paths for path in sub_list]

    def handle_zipped_files(self):
        these_files = self.get_style_file_list()
        for f in these_files:
            if zipfile.is_zipfile(f):
                destination = f.rsplit('/', 1)[0]
                with zipfile.ZipFile(f) as zf:
                    for member in zf.namelist():
                        filename = basename(member)
                        if not filename:
                            continue
                        source = zf.open(member)
                        target = file(join(destination, filename), 'wb')
                        with source, target:
                            copyfileobj(source, target)

    def do_everything(self):
        self.build_file_directory()
        self.download_styles()
        self.handle_zipped_files()
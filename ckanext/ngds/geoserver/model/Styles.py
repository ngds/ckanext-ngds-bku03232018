from Geoserver import Geoserver
from os import listdir
from os.path import isfile, isdir, join
import urllib2
import json
import pprint

my_path = r"/Users/adrian/virtualenvs/ckan_env/src/ckanext-ngds/ckanext/ngds/geoserver/sld_files/"
content_model = "http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/"


class Styles:

    def __init__(self):
        self.model_url = 'http://schemas.usgin.org/contentmodels.json'
        self.geoserver = Geoserver.from_ckan_config()
        self.this_path = r"/Users/adrian/virtualenvs/ckan_env/src/ckanext-ngds/ckanext/ngds/geoserver/sld_files/"
        self.sld_dir = ""#path to directory of sld files

    def get_gs_styles(self):
        geoserver = self.geoserver
        return [style.name for style in geoserver.get_styles()]

    def get_sld_list(self, path):
        this_path = path
        files = [f for f in listdir(this_path) if isfile(join(this_path,f))]
        path_files = [this_path + f for f in files]
        return path_files

    def get_dir_list(self, path):
        this_path = path
        dirs = [d for d in listdir(this_path) if isdir(join(this_path,d))]
        return dirs

    def make_sld_path_list(self, path):
        this_path = path
        folders = self.get_dir_list(this_path)
        path_folders = [this_path + dir + '/' for dir in folders]
        base_slds = self.get_sld_list(this_path)
        path_slds = [self.get_sld_list(that_path) for that_path in path_folders]
        flat_path_slds = [item for sub_list in path_slds for item in sub_list]
        all_sld_paths = base_slds + flat_path_slds
        return all_sld_paths

    def delete_default_styles(self):
        geoserver = self.geoserver
        default_styles = ['burg','capitals','cite_lakes','dem','giant_polygon','grass',
                          'green','line','poi','point','poly_landmarks','polygon',
                          'pophatch','population','rain','raster','restricted','simple_roads',
                          'simple_streams','tiger_roads']
        for style in default_styles:
            this_style = geoserver.get_style(style)
            geoserver.delete(this_style)

    def load_style(self, style_name, style_path):
        geoserver = self.geoserver
        styles = [style.name for style in geoserver.get_styles()]
        if style_name not in styles:
            geoserver.create_style(style_name, open(style_path).read(), overwrite=True)
        else:
            pass

    def loop_load_styles(self):
        files = self.get_sld_list()
        for file in files:
            style_name = file[:-4]
            style_path = this_path + file
            self.load_style(style_name, style_path)
            print style_name

    def get_content_models(self):
        url = self.model_url
        reader = urllib2.urlopen(url).read()
        data = json.loads(str(reader))
        return data

    def get_sld(self, content_model=None):
        label = []
        data = self.get_content_models()
        if content_model is None:
            label = [model['sld_file_path'] for model in data for model in model['versions']]
        else:
            label = [model['label'] for model in data if model['uri'] == content_model]
        return label

    def get_uri(self):
        data = self.get_content_models()
        uri = [model['uri'] for model in data for model in model['versions']]
        return uri

a = Styles()
#print a.make_sld_path_list(my_path)
for i in a.get_sld():
    print i

for e in a.get_uri():
    print e
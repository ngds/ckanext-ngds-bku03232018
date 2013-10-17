from Geoserver import Geoserver
from os import listdir
from os.path import isfile, isdir, join

thatpath = r"/Users/adrian/virtualenvs/ckan_env/src/ckanext-ngds/ckanext/ngds/geoserver/sld_files/"


class Styles:

    def __init__(self):
        self.geoserver = Geoserver.from_ckan_config()
        self.sld_dir = ""#path to directory of sld files

    def styles(self):
        geoserver = self.geoserver
        return [style.name for style in geoserver.get_styles()]

    def get_sld_list(self):
        path = thatpath
        files = [f for f in listdir(path) if isfile(join(path,f))]
        return files

    def get_dir_list(self):
        path = thatpath
        dirs = [d for d in listdir(path) if isdir(join(path,d))]
        return dirs

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
            name = file[:-4]
            path = thatpath + file
            print path
            #self.load_style(name, path)




a = Styles()
a.loop_load_styles()
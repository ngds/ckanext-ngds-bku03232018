''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

__author__ = 'Vivek'
import os, subprocess, glob


class ScriptCompiler(object):
    mpath = None

    def __init__(self, mpath):
        self.mpath = mpath

    def compile_less(self):
        imports_less_path = os.path.join(self.mpath, 'public', 'css')
        main_less_file = os.path.join(imports_less_path, 'main.less')
        css_file = os.path.join(imports_less_path, 'main.css')
        call_string = "/usr/local/bin/lessc" + " -x --clean-css " + main_less_file + " " + css_file
        #subprocess.call(["/usr/local/bin/lessc " + main_less_file + " -o --yui-compress " + css_file], shell=True)
        print "Compile .less files:  " + call_string
        subprocess.call([call_string], shell=True)

    def minify_js(self):
        scripts_path = os.path.join(self.mpath, 'public', 'scripts')
        self._minify(scripts_path)

    def _minify(self, scripts_path):
        # print glob.glob(os.path.join(scripts_path, "*"))
        if os.path.isdir(scripts_path):
            map(lambda x: self._minify(x), glob.glob(os.path.join(scripts_path, "*")))
        else:
            if scripts_path.endswith('min.js'):
                return
            if not scripts_path.endswith('.js'):
                return
            print("Minify .js files:  " + "yui-compressor -o "),  # "," supresses newline
            print os.path.splitext(scripts_path)[0] + "-min.js " + scripts_path
            subprocess.call(["yui-compressor -o " + os.path.splitext(scripts_path)[0] + ".min.js " + scripts_path],
                            shell=True)




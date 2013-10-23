__author__ = 'kaffeine'

from ckanext.ngds.logic.file_processors.AbstractFileProcessor import AbstractFileProcessor
from ckanext.ngds.logic.file_processors.ContentModelConstants import ContentModelValue, BHT_1_5
import ckanext.ngds.logic.file_processors.CSVProcessors as csvprocessors
import csv


class CSVFileProcessor(AbstractFileProcessor):
    def declare_processes(self):
        plist = []

        if ContentModelValue(self.cm, self.cmv) == BHT_1_5:
            plist.append({
                'func': csvprocessors.hottest_well_temp,
                'metadata_field': 'hottest_well_temp'
            })
            plist.append({
                'func': csvprocessors.coolest_well_temp,
                'metadata_field': 'coolest_well_temp'
            })

        return plist

    def get_file(self):
        if not hasattr(self, 'fileObj'):
            self.csvfp = open(self.file, 'rb')
            self.fileObj = csv.DictReader(self.csvfp)
        return self.fileObj

    def close_file(self):
        self.csvfp.close()
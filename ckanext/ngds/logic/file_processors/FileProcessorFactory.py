__author__ = 'kaffeine'

from ckanext.ngds.logic.file_processors.CSVFileProcessor import CSVFileProcessor


class FileProcessorFactory(object):
    @classmethod
    def get_file_processor(cls, file_to_process, cm, cmv, res_id):
        if file_to_process.endswith('.csv'):
            return CSVFileProcessor(file_to_process, cm, cmv, res_id)
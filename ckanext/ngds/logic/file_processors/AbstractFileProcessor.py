__author__ = 'kaffeine'

import ckan.logic as logic


class AbstractFileProcessor(object):
    def __init__(self, file_to_process, content_model, content_model_version, resource_id):
        self.file = file_to_process
        self.resource_id = resource_id
        self.cm = content_model
        self.cmv = content_model_version

    def get_processes(self):
        return self.declare_processes()

    def declare_processes(self):
        pass

    def run_processes(self):
        ps = self.get_processes()

        result_collector = {

        }

        try:
            for process in ps:
                pfunc = process['func']
                metadata_field = process['metadata_field']
                output = pfunc(self.get_file())
                result_collector[metadata_field] = output
                print " ran csv processor and got : " + str(output)
        except Exception:
            pass
        finally:
            self.close_file()

        return result_collector

    def get_file(self):
        pass

    def close_file(self):
        pass
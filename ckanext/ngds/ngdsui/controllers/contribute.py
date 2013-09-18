"""
This controller class is responsible at a high level for managing the dataset and resource contribution workflow. This includes rendering of the dataset and resource contribution forms,
rendering of the bulk upload page and dataset and resource validation.
"""

from ckan.lib.base import *
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.lib.base import (request,
                           render,
                           model,
                           abort, h, g, c)
from ckan.logic import (tuplize_dict, clean_dict, parse_params, flatten_to_string_key, get_action, check_access, NotAuthorized)
from pylons import config
from ckanext.ngds.ngdsui.controllers.ngds import NGDSBaseController
import ckanext.ngds.lib.importer.helper as import_helper
from ckan.controllers.package import PackageController
from pylons.decorators import jsonify
import os
import shutil
import zipfile
from ckan.plugins import toolkit
import ckanext.ngds.lib.importer.validator as ngdsvalidator
from ckanext.ngds.ngdsui.misc.helpers import process_resource_docs_to_index


class ContributeController(NGDSBaseController):
    def index(self):

        """
        This function renders the contribute landing page for a node-in-a-box and the harvest page for the central node.
        """
        if not c.user:
            h.redirect_to(controller='user',
                              action='login', came_from=h.url_for(controller='ckanext.ngds.ngdsui.controllers.contribute:ContributeController',action='index'))

        if g.central:
            #TODO: Need to change this to point the correct controller
            url = h.url_for_static(controller='ckanext.harvest.controllers.view:ViewController')
            h.redirect_to(url)
        else:
            return render('contribute/contribute.html')

    def harvest(self):
        """
        This function renders the harvest source addition page.
        """
        c.action = 'save'
        return render('contribute/harvest_new.html')

    def bulk_upload(self):
        """
        This function renders the bulk upload form.
        """

        context = {'model': model, 'session': model.Session, 'user': c.user or c.author}

        try:
            check_access('package_create', context, None)
        except NotAuthorized, error:
            abort(401, error.__str__())

        return render('contribute/bulkupload_form.html')

    def bulk_upload_handle(self):
        """    
        This function is responsible for receiving a dataset excel file and a zip file from the bulk upload form, validating and initiating processing of the bulk upload.
        """
        context = {'model': model, 'session': model.Session, 'user': c.user or c.author}

        try:
            check_access('package_create', context, None)
        except NotAuthorized, error:
            abort(401, error.__str__())

            #Validate the dataset file.

        bulk_dir = config.get('ngds.bulk_upload_dir')

        from datetime import datetime

        ts = datetime.isoformat(datetime.now()).replace(':', '').split('.')[0]

        upload_dir = os.path.join(bulk_dir, ts)

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)


        # Recieve the dataset file to be processed.
        datasetfile = request.POST['datasetfile']

        if datasetfile == "":
            #raise Exception (_("Data file can't be empty."))
            abort(500, toolkit._("Data file can't be empty."))

        datafilename = datasetfile.filename

        datafilepath = os.path.join(upload_dir, datasetfile.filename.replace(os.sep, '_'))

        permanent_data_file = open(datafilepath, 'wb')
        shutil.copyfileobj(datasetfile.file, permanent_data_file)
        datasetfile.file.close()
        permanent_data_file.close()

        resourcefile = request.POST['resourceszip']
        resource_list = None
        resourcesfilename = None

        if resourcefile != "":
            resourcesfilename = resourcefile.filename
            resfilepath = os.path.join(upload_dir, resourcefile.filename.replace(os.sep, '_'))
            permanent_zip_file = open(resfilepath, 'wb')
            shutil.copyfileobj(resourcefile.file, permanent_zip_file)
            resourcefile.file.close()
            permanent_zip_file.close()

            zfile = zipfile.ZipFile(resfilepath)

            zfile.extractall(path=upload_dir)

            def dir_filter(s):
                if os.path.isdir(os.path.join(upload_dir, s)):
                    return False
                return True


            resource_list = filter(dir_filter, zfile.namelist())

        status, err_msg = self._validate_uploadfile(datafilepath, upload_dir, resource_list)

        if status == "INVALID":
            import_helper.delete_files(file_path=upload_dir, ignore_files=[datafilename, resourcesfilename])

        self._create_bulk_upload_record(c.user or c.author, datafilename, resourcesfilename, upload_dir, status,
                                        err_msg)

        url = h.url_for(controller='ckanext.ngds.ngdsui.controllers.contribute:ContributeController',
                        action='bulk_upload')
        redirect(url)

    def _validate_uploadfile(self, data_file, resource_path, resource_list):
        """
        This function is responsible for validating a bulk upload.
        """
        err_msg = ""
        try:
            validator = ngdsvalidator.NGDSValidator(filepath=data_file, resource_path=resource_path,
                                                    resource_list=resource_list)
            validator.validate()
            status = "VALID"
            h.flash_notice(toolkit._('Files Uploaded Successfully.'), allow_html=True)
        except Exception, e:
            err_msg = e.__str__()
            h.flash_error(toolkit._('Uploaded files are invalid.: %s ') % err_msg, allow_html=True)
            status = "INVALID"

        return status, err_msg

    def _create_bulk_upload_record(self, user, data_file, resources, path, status, comments):
        """
        This function is responsible for creating a bulk upload record.
        """

        userObj = model.User.by_name(c.user.decode('utf8'))

        data = {'data_file': data_file, 'resources': resources, 'path': path, 'status': status, 'comments': comments,
                'uploaded_by': userObj.id}
        data_dict = {'model': 'BulkUpload'}
        data_dict['data'] = data
        data_dict['process'] = 'create'

        #print "Data dict: ",data_dict

        context = {'model': model, 'session': model.Session, 'user': c.user or c.author}

        transaction_return = get_action('transaction_data')(context, data_dict)


    def create_responsible_party(self, data):

        """
        Creates the responsible party in the system and returns the node_id
        """
        data_dict = {'model': 'ResponsibleParty'}
        data_dict['data'] = data
        data_dict['process'] = 'create'

        context = {'model': model}

        data_dict = get_action('additional_metadata')(context, data_dict)

        #responsible.save()
        return data_dict

    def update_responsible_party(self, data):

        """
        Creates the responsible party in the system and returns the node_id
        """

        data_dict = {'model': 'ResponsibleParty'}
        data_dict['data'] = data
        data_dict['process'] = 'update'

        context = {'model': model}

        data_dict = get_action('additional_metadata')(context, data_dict)

        #responsible.save()

        return data_dict


    def bulkupload_list(self):
        """
        This function is responsible for rendering the bulk upload list page which in turn displays all the bulk uploads submitted to the system.
        """

        context = {'model': model, 'session': model.Session, 'user': c.user or c.author}

        try:
            check_access('package_create', context, None)
        except NotAuthorized, error:
            err_str = toolkit._('User %s not authorized to access bulk uploads') % c.user
            #abort(401,error.__str__())    
            abort(401, err_str)

        uploads = model.BulkUpload.get_all()

        data = {'id': 1}
        data_dict = {'model': 'BulkUpload'}
        data_dict['data'] = data
        data_dict['process'] = 'read'
        context = {'model': model, 'session': model.Session}
        c.bulkuploads = uploads

        return render('contribute/bulkupload_list.html')

    def bulkupload_package_list(self):
        """
        This function is responsible for displaying the list of packages that constitute a given bulk upload submission.
        """

        context = {'model': model, 'session': model.Session, 'user': c.user or c.author}

        try:
            check_access('package_create', context, None)
        except NotAuthorized, error:
            err_str = toolkit._('User %s not authorized to access bulk uploads') % c.user
            #abort(401,error.__str__())    
            abort(401, err_str)

        data = clean_dict(unflatten(tuplize_dict(parse_params(
            request.params))))

        uploaded_packages = model.BulkUpload_Package.by_bulk_upload(data['id'])

        c.uploaded_packages = uploaded_packages
        c.selected_upload = model.BulkUpload.get(data['id'])

        return render('contribute/bulkupload_list.html')

    def execute_bulkupload(self):
        """
        Executes a bulk upload job. This function can only be triggered by an admin via the bulk upload page.
        """
        context = {'model': model, 'session': model.Session, 'user': c.user or c.author}

        try:
            check_access('execute_bulkupload', context, None)
        except NotAuthorized, error:
            abort(401, error.__str__())

        from ckanext.ngds.lib.importer.importer import BulkUploader

        bulkLoader = BulkUploader()
        bulkLoader.execute_bulk_upload()

        h.flash_notice(toolkit._('Initiated Bulk Upload process and it is running in the background.'), allow_html=True)
        url = h.url_for(controller='ckanext.ngds.ngdsui.controllers.contribute:ContributeController',
                        action='bulkupload_list')
        redirect(url)

    @jsonify
    def validate_resource(self):
        """
        Validate a resource to ensure that it conforms to NGDS standards. For ex: if a resource specifies that it conforms to a content model, that validation occurs here.
        """
        data = clean_dict(unflatten(tuplize_dict(parse_params(
            request.params))))

        return toolkit.get_action("validate_resource")(None, data)


    def execute_fulltext_indexer(self):
        """
        Executes the fulltext indexer to index documents that were uploaded since the last indexer run.
        """
        process_resource_docs_to_index()

        return "Full text indexer is executed successfully. Have fun with searching through documents....."

    def new_metadata(self):
        """
        Process a dataset metadata submission and validate it. If valid, then proceed to add the dataset metadata and if not return the new_package_metadata page to display the errors so
        the user can try to fix his submission.
        """
        data = clean_dict(unflatten(tuplize_dict(parse_params(
            request.params))))
        result = toolkit.get_action('validate_dataset_metadata')(None, data)
        vars = {"data": data}
        if result['success'] == True:
            return PackageController().new_metadata(id=data['pkg_name'])
        else:
            vars["errors"] = result["errors"]
            return render('package/new_package_metadata.html', extra_vars=vars)

            # TODO : Is this really needed?
            # def additional_metadata(self):
            #     data = clean_dict(unflatten(tuplize_dict(parse_params(
            #         request.params))))
            #     return toolkit.get_action('validate_dataset_metadata')(None, data)
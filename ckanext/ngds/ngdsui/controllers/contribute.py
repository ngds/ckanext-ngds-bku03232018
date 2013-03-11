from ckan.lib.base import *
from ckan.lib.navl.dictization_functions import DataError, unflatten, validate
from ckan.lib.base import (request,
                           render,
                           model,
                           abort, h, g, c)
from ckan.logic import get_action
from ckan.logic import (tuplize_dict,
                        clean_dict,
                        parse_params,
                        flatten_to_string_key)
from pylons import config
from ckanext.ngds.ngdsui.controllers.ngds import NGDSBaseController

class ContributeController(NGDSBaseController):

 	def index(self):
		
		"""
		Renders contribute page.
		"""

		if g.central:
			nodes = model.HarvestNode.get_all()
			c.harvested_nodes = nodes

		return render('contribute/contribute.html')		

	def harvest(self):
		"""
		Create new Harvest node.
		"""
		c.action = 'save'
		return render('contribute/harvest_new.html')

	def upload(self):
		"""
		Render the upload page
		"""

		return render('contribute/upload.html')

	def edit(self,id):
		"""
		Editing the existing Harvest node.
		"""
		context = {'model': model, 'session': model.Session,'user': c.user or c.author}

		try:
			check_access('manage_nodes',context,data_dict)
		except NotAuthorized, error:
			abort(401,error.__str__())

		c.isEdit = True
		c.action = 'edit_save'
		c.node = self._read_node(id)
		return render('contribute/harvest_new.html')	

	def edit_save(self,id=None):
		"""
		Updating the edited  Harvest node.
		"""

		context = {'model': model, 'session': model.Session,'user': c.user or c.author}

		try:
			check_access('manage_nodes',context,data_dict)
		except NotAuthorized, error:
			abort(401,error.__str__())


		data = clean_dict(unflatten(tuplize_dict(parse_params(
            request.params))))	

		node_id = data['id'] or id

		print "Data Dict Values on Edit: " ,data

		#Update responsible Party

		data['id'] = data['node_admin_id']

		res_party_data = self.update_responsible_party(data)

		#Update Node Admin ID just to make sure if it is updated as part of edit. TODO: Handle new Responsible party creation
		data['node_admin_id'] = res_party_data['id']
		data['id'] = node_id

		data_dict = {'model':'HarvestNode'}
		data_dict['data']=data
		data_dict['process']='update'
		
		context = {'model': model}

		get_action('ngds_harvest')(context, data_dict)		

		#return self.read(node_id)

		print " Node ID: ", node_id

		url = h.url_for(controller='ckanext.ngds.ngdsui.controllers.contribute:ContributeController', action='read', id=node_id)
		redirect(url)

	def save(self,data=None):
		"""
		Create new Harvest node.
		"""

		harvestNode = model.HarvestNode(data)

		data = clean_dict(unflatten(tuplize_dict(parse_params(
            request.params))))							

		harvestNode.url = data['url']
		harvestNode.frequency = data['frequency']
		harvestNode.title = data['title']
		
		data_dict = self.create_responsible_party(data)

		harvestNode.node_admin_id = data_dict['id']
			
		print "Harvest the data: ",harvestNode

		harvestNode.save()

		
		"""
		data['node_admin_id'] = data_dict['id']
		data_dict = {'model':'HarvestNode'}
		data_dict['data']=data
		data_dict['process']='create'
		

		print "Data dict: ",data_dict

		context = {'model': model}

		get_action('ngds_harvest')(context, data_dict)		
		"""

		#return self.index()
		url = h.url_for(controller='ckanext.ngds.ngdsui.controllers.contribute:ContributeController', action='index')
		redirect(url)		

	def delete(self,id):

		"""
		Deletes Harvest node.
		"""

		data_dict = {'model':'HarvestNode'}
		data_dict['data']={'id':id}
		data_dict['process']='delete'

		print "Data dict: ",data_dict

		context = {'model': model}

		get_action('ngds_harvest')(context, data_dict)		

		url = h.url_for(controller='ckanext.ngds.ngdsui.controllers.contribute:ContributeController', action='index')
		redirect(url)		

 	def read(self,id):
		
		"""
		Fetches the details about a particular node.
		"""

		node = self._read_node(id)

		c.node = node

		return render('contribute/harvest_read.html')

	def _read_node(self,id):
	
		node = 	model.HarvestNode.by_id(id)
		return node

	def create_responsible_party(self,data):

		"""
		Creates the responsible party in the system and returns the node_id
		"""
		# responsible = model.ResponsibleParty(data['name'],data['email'])
		# responsible.organization = data['organization']
		# responsible.phone = data['phone']
		# responsible.street = data['street']
		# responsible.state = data['state']
		# responsible.city = data['city']
		# responsible.zip = data['zip']
		
		data_dict = {'model':'ResponsibleParty'}
		data_dict['data']=data
		data_dict['process']='create'
		

		print "Data dict: ",data_dict		
		context = {'model': model}

		data_dict = get_action('additional_metadata')(context, data_dict)

		#responsible.save()
		return  data_dict

	def update_responsible_party(self,data):

		"""
		Creates the responsible party in the system and returns the node_id
		"""
		# responsible = model.ResponsibleParty(data['name'],data['email'])
		# responsible.organization = data['organization']
		# responsible.phone = data['phone']
		# responsible.street = data['street']
		# responsible.state = data['state']
		# responsible.city = data['city']
		# responsible.zip = data['zip']
		
		data_dict = {'model':'ResponsibleParty'}
		data_dict['data']=data
		data_dict['process']='update'
		

		print "Data dict: ",data_dict		
		context = {'model': model}

		data_dict = get_action('additional_metadata')(context, data_dict)

		#responsible.save()
		return  data_dict		
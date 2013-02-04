from ckan.lib.base import *
from ckan.lib.base import (request,
                           render,
                           BaseController,
                           model,
                           abort, h, g, c)
from ckan.logic import get_action

class ContributeController(BaseController):

 	def index(self):
		
		"""
		Renders contribute page.
		"""
		data_dict = {
				'model': 'HarvestNode',
    			'process': 'read',
    			'data': {
        			"id":'all'
				 }             
		}
		
		context = {'model': model}

		nodes = get_action('ngds_harvest')(context, data_dict)		

		c.harvested_nodes = nodes
		
		print "Harvested Nodes: " , nodes

		return render('contribute/contribute.html')		

 	def read(self):
		
		"""
		Fetches the details about a particular node.
		"""
		node_id = 2

		data_dict = {
				'model': 'HarvestNode',
    			'process': 'read',
    			'data': {
        			"id":node_id
				 }           
		}
		
		context = {'model': model}

		nodes = get_action('ngds_harvest')(context, data_dict)		

		c.harvested_nodes = nodes	

		return render('contribute/contribute.html')	
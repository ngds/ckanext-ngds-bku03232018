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

		nodes = model.HarvestNode.get_all()

		c.harvested_nodes = nodes
		
		return render('contribute/contribute.html')		

 	def read(self):
		
		"""
		Fetches the details about a particular node.
		"""

		node_id = 2

		node = model.HarvestNode.by_id(node_id)

		c.selected_node = node

		return render('contribute/contribute.html')	
"""
This controller class is responsible purely for rendering top-level pages in the NGDS UI. These are the home page,map, about,
library search, contribute landing page and page links in the footer section of every NGDS Page. Each page has a corresponding render function
that is automatically invoked when a request to a specific URL path is made, and renders a template that in turn is responsible for constructing
an HTML page from a predefined template(s).
"""

from ckan.lib.base import *
from ckan.lib.base import (request,
                           render,
                           model, g, c)
from ckanext.ngds.ngdsui.controllers.ngds import NGDSBaseController

from sqlalchemy import desc
from ckan.lib.navl.dictization_functions import unflatten
from ckan.logic import (tuplize_dict, clean_dict, parse_params)

import ckan.lib.dictization.model_dictize as model_dictize
from ckanext.ngds.ngdsui.misc import helpers

from pylons.decorators import jsonify

import ckan.rating as rating


class HomeController(NGDSBaseController):
    def render_index(self):

        """
        This function renders the NGDS home page. The page sent to the user depends on the deployment of the system
        i.e. if the deployment is a central node, then the page sent is the central home page, if it is a node-in-a-box,
        the page sent will be the map page.
        """

        if g.node_in_a_box:
            return self.render_map()

        context = {'model': model, 'session': model.Session, 'user': c.user}

        activity_objects = model.Session.query(model.Activity).join(model.Package,
                                                                    model.Activity.object_id == model.Package.id). \
            filter(model.Activity.activity_type == 'new package').order_by(desc(model.Activity.timestamp)). \
            limit(5).all()
        activity_dicts = model_dictize.activity_list_dictize(activity_objects, context)
        c.recent_activity = activity_dicts

        c.image_files = helpers.get_home_images()
        helpers.get_contributors_list()

        return render('home/index_ngds.html')


    def render_map(self):

        """
        This function is responsible for rendering the Map Search page.
        """
        data = clean_dict(unflatten(tuplize_dict(parse_params(request.params))))
        if data.get('query'):
            c.query = data['query']

        return render('map/map.html')

    def render_library(self):

        """
        This function is responsible for rendering the Library Search page.
        """
        return render('library/library.html')

    def render_resources(self):

        """
        This function is responsible for rendering the Resources page.
        """
        return render('resources/resources.html')

    @jsonify
    def rating_submit(self):
        """
        Rates a dataset. Probably should be in its own py file or something... 
        """
        data = clean_dict(unflatten(tuplize_dict(parse_params(request.params))))
        rpackageId = data['rpackageId']
        ratingValue = data['ratingValue']
        log.debug("in set rating review %s %s %s", rpackageId, ratingValue, c.user)
        package = model.Package.get(rpackageId)
        rating.set_rating(c.user, package, ratingValue)

        return {
            'success': True
        }

    @jsonify
    def save_search(self):

        data = clean_dict(unflatten(tuplize_dict(parse_params(request.params))))

        user = model.User.by_name(c.user.decode('utf8'))

        data_dict = {'model': 'UserSearch'}
        data_dict['data'] = {'user_id': user.id, 'search_name': data['search_name'], 'url': data['url']}
        data_dict['process'] = 'create'
        context = {'model': model, 'session': model.Session}

        from ckanext.ngds.metadata.controllers.transaction_data import dispatch as trans_dispatch

        trans_dispatch(context, data_dict)

        return {
            'success': True
        }


    def initiate_search(self):
        """
        This function is responsible for processing requests from the home page to initiate either a map search or library search
        with a search query that is provided to it.
        """
        data = clean_dict(unflatten(tuplize_dict(parse_params(
            request.params))))

        query = ''

        if 'query' in data:
            query = data['query']

        if data['search-type'] == 'library':
            return redirect(h.url_for(controller='package', action='search', q=query, _tags_limit=0))
        else:
            return redirect(
                h.url_for(controller='ckanext.ngds.ngdsui.controllers.home:HomeController', action='render_map',
                          query=query))
            # return self.render_map(query)

    def render_partners(self):
        """
        This function is responsible for rendering the NGDS Partners' page via the template defined at templates/info/master/partners_master.html
        """
        return render('info/master/partners_master.html')

    def render_data(self):
        """
        This function is responsible for rendering the NGDS Data page via the template defined at templates/info/master/data_master.html
        """
        return render('info/master/data_master.html')

    def render_history(self):
        """
        This function is responsible for rendering the NGDS History page via the template defined at templates/info/master/history_master.html
        """
        return render('info/master/history_master.html')

    def render_new_to_ngds(self):
        """
        This function is responsible for rendering the New to NGDS page via the template defined at templates/info/master/new_to_ngds_master.html
        """
        return render('info/master/new_to_ngds_master.html')

    def render_faq(self):
        """
        This function is responsible for rendering the NGDS FAQ page via the template defined at templates/info/master/faq_master.html
        """
        return render('info/master/faq_master.html')

    def render_about(self):
        """
        This function is responsible for rendering the About page via the template defined at templates/info/master/about_master.html
        """
        return render('info/master/about_master.html')

    def render_contributors(self):
        """
        This function is responsible for rendering the About page via the template defined at templates/info/master/about_master.html
        """
        return render('home/contributors.html')

    def render_terms_of_use(self):
        """
        This function is responsible for rendering the T page via the template defined at templates/info/master/terms_of_use_master.html
        """
        return render('info/master/terms_of_use_master.html')

    def render_contact(self):
        """
        This function is responsible for rendering the Contact page via the template defined at templates/info/master/contact_master.html
        """
        return render('info/master/contact_master.html')
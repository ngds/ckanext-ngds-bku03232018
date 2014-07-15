import ckan.plugins as p
import ckan.model as model

class NGDSClient(p.SingletonPlugin):

    p.implements(p.IRoutes)
    p.implements(p.IConfigurer)
    p.implements(p.IAuthFunctions)
    p.implements(p.IFacets)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IPackageController)
    p.implements(p.IConfigurable)
    p.implements(p.IActions)
    p.implements(p.IDatasetForm)
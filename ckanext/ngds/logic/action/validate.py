''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

import json

### ----------------------------------------------------------------------------------------- ###
### ----------------------------------------------------------------------------------------- ###
### ----------------------------------------------------------------------------------------- ###
###                                                                                           ###
### READ THIS: https://github.com/ngds/ckanext-ngds/wiki/The-NGDS-Package-and-Resource-Schema ###
###                                                                                           ###
### ----------------------------------------------------------------------------------------- ###
### ----------------------------------------------------------------------------------------- ###
### ----------------------------------------------------------------------------------------- ###

# CKAN Toolkit provides an interface for reusable validation criteria
from ckan.plugins import toolkit as tk
optional = tk.get_validator('ignore_missing')
required = tk.get_validator('not_empty')

# Grab NGDS validators
from ckanext.ngds.logic.action import validators as ngds_rules

def ngds_create_schema(schema):
    """
    A schema used to validate Packages when they are created, i.e. during `package_create` actions. Please note that
    `package_create` happens when you fill in *the first page of the forms* that are exposed on the site. Subsequent
    pages trigger `package_update` actions.
    """

    # Make NGDS additions
    schema = _ngds_create_additions(schema)

    # And return the schema
    return schema

def _ngds_create_additions(schema):
    """
    This function adjusts a CKAN schema object to contain validation requirements of the NGDS.

    The schema object is a dictionary. Each key corresponds to a field in the CKAN Package. The values in the schema
    object are arrays of validation functions. CKAN offeres a number of validation functions which should be accessed
    through ckan.plugins.toolkit.get_validator. CKAN also commonly exposes Python types as items in the array. My
    assumption is that then the content is coerced into that type (for example, Unicode).

    See `./validators.py` for more description of validation functions.

    Adding the following code:

        schema['notes'] = [required, unicode]

    Would be equivalent to saying "There must be a field in the Package called "notes" and it must have content (see
    the definition of the `required` function above), and that content must be able to be coerced into a unicode object.
    """

    schema['notes'] = [required, unicode]
    schema['owner_org'] = [ngds_rules.apply_default_org]

    # Extras are a tricky beast. See below for more info
    schema['extras']['key'].append(validate_extras)

    return schema

def ngds_update_schema(schema):
    """
    A schema used to validate Packages when they are updated, i.e. during `package_update` actions. These happen
    more frequently than you might think. See `ngds_create_schema` above.
    """

    # Make NGDS additions
    schema = _ngds_create_additions(schema)
    schema = _ngds_update_additions(schema)

    # and return the schema
    return schema

def _ngds_update_additions(schema):
    """
    This basically adds resource validation to the package. The rules are conditional, based on the content in the
    `resource_format` field. Therefore, we can only add validation to that one field, and then the
    `validate_resources` function needs to make sure that other fields are in fact valid.

    However you have to add your addditional fields to the schema, otherwise they end up as "extras" attached to the
    resource.
    """

    ngds_resource_additions = {
        "resource_format": [required, validate_resources],
        "distributor": [optional],
        "protocol": [optional],
        "layer": [optional],
        "ordering_procedure": [optional],
        "content_model_uri": [optional],
        "content_model_version": [optional]
    }

    schema['resources'] = dict(schema['resources'].items() + ngds_resource_additions.items())

    return schema

def validate_extras(key, data, errors, context):
    """
    This function validates the extras on a package to make sure they conform to NGDS rules.

    *Important*: This function will be called for each extra in the array. That means you should only be validating
    the current extra. However, we also need to be sure that all the required fields are present, so there is
    redundancy in that check (it is done every time).

    *Also Important*: `key` will be a tuple like `('extras', 0, 'key')` and `data` will be a "flat" dictionary that
    has keys that are like that tuple and values that are basically primitives (string, boolean, number). The first
    thing we do is remap `data` into something more comprehensible -- a simple dictionary of key/value pairs
    representing the set of extras

    *More Notes*: Its really important to understand the relationship between `package_create`, `package_update`,
    and the web-based UI. The first form doesn't add any extras, and it fires `package_create`. The second form
    creates resources, and fires `package_update`. The third form adds extras and fires `package_update`.

    Fortunately, this function will not fire unless there are actually some extras included in the package,
    so its safe to put this in the `package_create` schema. This also ensures that pacakges that are created
    programmatically (i.e. harvested records) must satisfy the same validation criteria as those created through the
    web interface.
    """

    # Remap the messy data dictionary into a simple key/value object representing extras
    #  This is messy and could be botched by future changes to CKAN's validation internals
    indexes = [t[1] for t in data.keys() if t[0] == 'extras' and t[2] == 'key']
    extras = dict((data[('extras', num, 'key')], data[('extras', num, 'value')]) for num in indexes)

    # Define validation criteria for each of the extra NGDS fields
    required_criteria = {
        "authors": [required, ngds_rules.is_valid_json, ngds_rules.is_valid_list_of_contacts],
        "maintainer": [required, ngds_rules.is_valid_json, ngds_rules.is_valid_contact],
        "dataset_category": [required, ngds_rules.is_in_list([
            "Dataset", "Physical Collection", "Catalog",
            "Movie or Video", "Drawing", "Photograph",
            "Remotely Sensed Image", "Map", "Text Document",
            "Physical Artifact", "Desktop Application", "Web Application"
        ])],
        "status": [required, ngds_rules.is_in_list([
            "completed", "ongoing", "deprecated"
        ])],
        "publication_date": [required, ngds_rules.is_valid_date],
        "dataset_lang": [required],
        "spatial": [required, ngds_rules.is_valid_json, ngds_rules.is_valid_rectangle]
    }

    optional_criteria = {
        "spatial_word": [optional],
        "dataset_uri": [optional],
        "quality": [optional],
        "lineage": [optional]
    }

    # Make sure that required fields are all present
    required_fields = required_criteria.keys()
    existing_fields = extras.keys()
    overlap = list(set(existing_fields) & set(required_fields))
    if len(overlap) < len(required_fields):
        errors[key].append(_('Some required NGDS fields were not present'))
        return

    # Now validate the single key that we were given on this iteration
    field_name = data[key]

    # Check if this particular key satisfies all validation criteria
    criteria = required_criteria.get(field_name, optional_criteria.get(field_name, []))
    validation_runner(field_name, extras, errors, criteria)

    # Send and changes that the validation_runner made to the `extras` object back into the original `data` object
    reverser = dict((data[('extras', num, 'key')], ('extras', num, 'value')) for num in indexes)
    data[reverser[field_name]] = extras[field_name]

def validate_resources(key, data, errors, context):
    """
    This function will be invoked once per resource, and must check to see that all the fields in the resource are
    acceptable. The `key` will always be `('resources', some-integer, 'resource_format'). The integer can be used to
    find other values from the same resource. `data` is the "flat" version of the entire Package dictionary.
    """

    # Information about this resource that I can take from the given key
    resource_format = data[key]

    # Simplify the resource into a dictionary of key/value pairs. Sometimes the function is passed a dict with complex
    # tuples for keys, sometimes it is passed pretty simple ones.
    if len(key) > 1:
        resource_index = key[1]
        resource = dict((t[2], data[t]) for t in data.keys() if t[0] == 'resources' and t[1] == resource_index)
    else:
        resource = dict((t[1], data[t]) for t in data.keys())

    # A way to make sure I always have the right key, regardless of the idiosyncracies of what might get sent in
    def real_key(field_name):
        if len(key) > 1:
            return key[0:2] + (field_name,)
        else:
            return (field_name,)

    # Check for fields that are always required by NGDS for resources of any type
    field_name = 'resource_format'
    validation_runner(
        field_name,
        resource,
        errors,
        ["structured", "unstructured", "offline-resource", "data-service"],
        real_key(field_name)
    )

    field_name = 'distributor'
    validation_runner(
        field_name,
        resource,
        errors,
        [required, ngds_rules.is_valid_json, ngds_rules.is_valid_contact],
        real_key(field_name)
    )

    # Now things depend on the current resource's `resource_format`
    if resource_format in ['structured', 'unstructured']:
        # These are uploaded files. `format` is needed
        field_name = 'format'
        validation_runner(
            field_name,
            resource,
            errors,
            [optional],
            real_key(field_name)
        )

    if resource_format == 'structured':
        # These are content-model-aware file uploads
        field_name = 'content_model_uri'
        validation_runner(
            field_name,
            resource,
            errors,
            [required, ngds_rules.is_valid_model_uri],
            real_key(field_name)
        )

        field_name = 'content_model_version'
        validation_runner(
            field_name,
            resource,
            errors,
            [required, ngds_rules.is_valid_model_version],
            real_key(field_name)
        )

        # If the model version and uri are valid, then check the uploaded file against the content model
        if len(errors[real_key('content_model_uri')]) == 0 and len(errors[real_key('content_model_version')]) == 0:
            ngds_rules.check_uploaded_file(resource, errors, real_key('content_model'))

    if resource_format == 'data-service':
        # These are linked data services
        field_name = 'protocol'
        validation_runner(
            field_name,
            resource,
            errors,
            [ngds_rules.is_in_list(['OGC:WMS', 'OGC:WFS', 'OGC:WCS', 'OGC:CSW', 'OGC:SOS', 'OPeNDAP', 'ESRI', 'other'])],
            real_key(field_name)
        )

        field_name = 'layer'
        validation_runner(
            field_name,
            resource,
            errors,
            [optional],
            real_key(field_name)
        )

    if resource_format == 'offline-resource':
        # These are offline things
        field_name = 'ordering_procedure'
        validation_runner(
            field_name,
            resource,
            errors,
            [required],
            real_key(field_name)
        )


def validation_runner(field_name, data, errors, criteria, error_key=None):
    """
    This is a stand-in for CKAN's internal validation runner for situations where I want to call a bunch of validator
    functions (defined with signature `validator(key, data, errors, context)`), but I have customized some of the
    parameters and need to "mask" the default error handling. This happens in validation of resources and extras,
    where our validation requirements put us a little outside what CKAN is setup to handle.
    """

    # You have to be really careful about what you feed the `errors` object. If the keys are wrong you'll get 500
    # errors. This is a place that is likely to be broken by future CKAN changes. For example, you feed in different
    # keys to indicate invalid package.extras than you do to indicate invalid content contained in a resource.
    if error_key is None: error_key = (field_name,)

    for validation_function in criteria:
        # Make a stand-in for the errors object
        err = {field_name: []}

        # Fabricate an error indicator in the real `errors` object, in case this field fails to validate
        errors[error_key] = []

        # In case things go wrong...
        i_believe_there_was_a_problem = False

        try:
            # Run the validator function
            validation_function(field_name, data, err, {})
        except Exception as ex:
            i_believe_there_was_a_problem = True
        finally:
            # Union any errors into the real errors object
            errors[error_key] = list(set(errors[error_key]) | set(err[field_name]))

            # Stop processing validation criteria if there was an exception
            if i_believe_there_was_a_problem:
                break;
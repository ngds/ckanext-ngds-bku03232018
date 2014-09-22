'use strict';

/*
Here's what we want the ngds package schema to look like:
'cmd:resourceDescription': {
  'cmd:resourceTitle': {type: String},
  'cmd:resourceDescription': {type: String},
  'cmd:resourceURI': [{
    'cmd:citationIdentifier': {type: String},
    'cmd:scopedIdentifierAuthority': {
      'cmd:authorityURI': {type: String},
      'cmd:authorityLabel': {type: String}
    }
  }],
  'cmd:citedSourceAgents': {
    'cmd:relatedAgent': {
      'cmd:agentRole': {
        'cmd:agentRoleURI': {type: String},
        'cmd:agentRoleLabel': {type: String},
        'cmd:individual': {
          'cmd:personURI': {type: String},
          'cmd:personName': {type: String},
          'cmd:personPosition': {type: String}
        },
        'cmd:organizationName': [],
        'cmd:organizationURI': {type: String},
        'cmd:phoneNumber': {type: String},
        'cmd:contactEmail': {type: String},
        'cmd:contactAddress': {type: String}
      }
    }
  },
  'cmd:citationDates': {
    'cmd:EventDateObject': {
      'cmd:eventType': [{
        'cmd:dateTypeLabel': {type: String},
        'cmd:dateTypeURI': {type: String},
        'cmd:dateTypeVocabularyURI': {type: String}
      }],
      'cmd:dateTime': {type: String}
    }
  },
  'cmd:recommendedCitation': {type: String},
  'cmd:resourceContacts': {
    'cmd:relatedAgent': {
      'cmd:agentRole': {
        'cmd:agentRoleURI': {type: String},
        'cmd:agentRoleLabel': {type: String},
        'cmd:individual': {
          'cmd:personURI': {type: String},
          'cmd:personName': {type: String},
          'cmd:personPosition': {type: String}
        },
        'cmd:organizationName': [],
        'cmd:organizationURI': {type: String},
        'cmd:phoneNumber': {type: String},
        'cmd:contactEmail': {type: String},
        'cmd:contactAddress': {type: String}
      }
    }
  },
  'cmd:resourceAccessOptions': [{
    'cmd:distributor': {
      'cmd:relatedAgent': {
        'cmd:agentRole': {
          'cmd:agentRoleURI': {type: String},
          'cmd:agentRoleLabel': {type: String},
          'cmd:individual': {
            'cmd:personURI': {type: String},
            'cmd:personName': {type: String},
            'cmd:personPosition': {type: String}
          },
          'cmd:organizationName': [],
          'cmd:organizationURI': {type: String},
          'cmd:phoneNumber': {type: String},
          'cmd:contactEmail': {type: String},
          'cmd:contactAddress': {type: String}
        }
      }
    },
    'cmd:accessLinks': [{
      'cmd:LinkObject': {
        'cmd:url': {type: String},
        'cmd:linkRelation': [{
          'cmd:relLabel': {type: String},
          'cmd:relURI': {type: String}
        }],
        'cmd:linkTitle': {type: String},
        'cmd:linkTargetResourceType': {type: String},
        'cmd:linkContentResourceType': {type: String},
        'cmd:linkOverlayAPI': {
          'cmd:APILabel': {type: String},
          'cmd:API-URI': {type: String}
        },
        'cmd:linkProfile': {
          'cmd:profileLabel': {type: String},
          'cmd:profileURI': {type: String}
        },
        'cmd:linkParameters': [{
          'cmd:linkParameterLabel': {type: String},
          'cmd:linkParameterURI': {type: String},
          'cmd:linkParameterValue': {type: String}
        }],
        'cmd:linkDescription': {type: String},
        'cmd:linkTransferSize': {type: Number}
      }
    }]
  }],
  'cmd:geographicExtent': {
    'cmd:extentLabel': {type: String},
    'cmd:extentStatement': {type: String},
    'cmd:extentReference': {
      'cmd:referencedExtentLabel': {type: String},
      'cmd:referencedExtentURI': {type: String},
      'cmd:extentVocabularyURI': {type: String}
    },
    'cmd:boundingBoxWGS84': [{
      'cmd:northBoundLatitude': {type: Number, min: -90, max: 90},
      'cmd:southBoundLatitude': {type: Number, min: -90, max: 90},
      'cmd:eastBoundLongitude': {type: Number, min: -180, max: 180},
      'cmd:westBoundLongitude': {type: Number, min: -180, max:180}
    }],
    'cmd:geoJSONgeometry': {
      'cmd:extentGeometryType': {
        'cmd:geometryTypeLabel': {type: String},
        'cmd:geometryTypeURI': {type: String},
        'cmd:geometryTypeVocabularyURI': {type: String}
      },
      'cmd:extentGeometry': [https://raw.githubusercontent.com/fge/sample-json-schemas/master/geojson/geojson.json]
    },
    'cmd:verticalExtent': {
      'cmd:verticalExtentMinimum': {type: Number},
      'cmd:verticalExtentMaximum': {type: Number},
      'cmd:verticalExtentCRS': {
        'cmd:verticalCRSLabel': {type: String},
        'cmd:verticalCRS-URI': {type: String},
        'cmd:verticalCRSVocabularyURI': {type: String}
      }
    }
  },
  'cmd:resourceTemporalExtent': [{
    'temporalExtentBegin': {type: String},
    'temporalExtentEnd': {type: String}
  }],
  'cmd:resourceUsageConstraints': [{
    'cmd:constraintsStatement': {type: String},
    'cmd:constraintTerms': [{
      'cmd:constraintTypeLabel': {type: String},
      'cmd:constraintTypeURI': {type: String},
      'cmd:constraintTypeVocabularyURI': {type: String},
      'cmd:constraintTerm': {type: String},
      'cmd:constraintURI': {type: String},
      'cmd:constraintVocabularyURI': {type: String}
    }],
    'cmd:license': [{
      'cmd:licenseURI': {type: String},
      'cmd:licenseName': {type: String}
    }]
  }],
  'cmd:resourceBrowseGraphic': {
    'cmd:url': {type: String},
    'cmd:linkRelation': [#/definitions/Reference],
    'cmd:linkTitle': {type: String},
    'cmd:linkContentResourceType': {type: String}
  },
  'cmd:resourceLanguage': [#/definitions/Reference],
  'cmd:resourceSpatialDescription': {
    'cmd:resourceSpatialRepresentationType': {
      'cmd:resourceSpatialRepresentationTypeLabel': {type: String},
      'cmd:resourceSpatialRepresentationTypeURI': {type: String},
      'cmd:resourceSpatialRepresentationTypeVocabularyURI': {type: String}
    },
    'cmd:resourceSpatialReferenceSystem': {
      'cmd:resourceSpatialReferenceSystemLabel': {type: String},
      'cmd:resourceSpatialReferenceSystemURI': {type: String},
      'cmd:resourceSpatialReferenceSystemVocabularyURI': {type: String}
    }
  },
  'cmd:relatedResources': [{
    'cmd:LinkObject': {
      'cmd:url': {type: String},
      'cmd:linkRelation': [{
        'cmd:relLabel': {type: String},
        'cmd:relURI': {type: String}
      }],
      'cmd:linkTitle': {type: String},
      'cmd:linkTargetResourceType': {type: String},
      'cmd:linkContentResourceType': {type: String},
      'cmd:linkOverlayAPI': {
        'cmd:APILabel': {type: String},
        'cmd:API-URI': {type: String}
      },
      'cmd:linkProfile': {
        'cmd:profileLabel': {type: String},
        'cmd:profileURI': {type: String}
      },
      'cmd:linkParameters': [{
        'cmd:linkParameterLabel': {type: String},
        'cmd:linkParameterURI': {type: String},
        'cmd:linkParameterValue': {type: String}
      }],
      'cmd:linkDescription': {type: String},
      'cmd:linkTransferSize': {type: Number}
    }
  }]
}
*/

ckan.module('ngds-contribute', function (jQuery, _) {
  return {
    initialize: function () {
      var message
        , form
        , button
        , obj
        , data
        , injection
        ;

      obj = this;

      message = _('There are unsaved modifications to this form').fetch();
      this.el.incompleteFormWarning(message);
      // Internet Explorer 7 fix for forms with <button type="submit">
      if ($('html').hasClass('ie7')) {
        this.el.on('submit', function() {
          form = $(this);
          $('button', form).each(function() {
            button = $(this);
            $('<input type="hidden">').prop('name', button.prop('name')).prop('value', button.val()).appendTo(form);
          });
        });
      }

      $('#ngds-dataset-edit').submit(function (e) {
        data = obj.buildSchema();
        form = $(this);

        injection = $('<input>')
          .attr('type', 'hidden')
          .attr('name', 'ngds_package')
          .val(JSON.stringify(data));

        $('#ngds-dataset-edit').append($(injection));

        return true;
      })
    },
    buildSchema: function () {
      var doc
        , entry
        , basic
        , author
        , authors
        , geo
        , distributor
        , distributors
        , contact
        , obj
        , i
        , j
        ;

      obj = this;

      basic = $('#collapse-basic-fields .ngds-input-form');
      authors = $('#collapse-ngds-author-fields .ngds-input-form');
      geo = $('#collapse-ngds-geographic-extent-fields .ngds-input-form');
      distributors = $('#collapse-ngds-distributor-fields .ngds-input-form');
      contact = $('#collapse-ngds-metadata-contact-fields .ngds-input-form');

      doc = {};
      basic.find('input').each(function () {
        doc.ResourceID = obj.processInputs(this, 'resource_id');
        doc.Title = obj.processInputs(this, 'title');
        doc.Description = obj.processInputs(this, 'description');
        doc.PublicationDate = obj.processInputs(this, 'publication_date');
      });

      doc.Authors = [];
      for (i = 0; i < authors.length; i++) {
        entry = {};
        entry.ContactInformation = {};
        entry.ContactInformation.Address = {};
        author = $(authors[i]);
        author.find('input').each(function () {
          entry.Name = obj.processInputs(this, 'ngds-name');
          entry.OrganizationName = obj.processInputs(this, 'ngds-organization');
          entry.ContactInformation.Phone = obj.processInputs(this, 'ngds-phone');
          entry.ContactInformation.email = obj.processInputs(this, 'ngds-email');
          entry.ContactInformation.Address.Street = obj.processInputs(this, 'ngds-street');
          entry.ContactInformation.Address.City = obj.processInputs(this, 'ngds-city');
          entry.ContactInformation.Address.State = obj.processInputs(this, 'ngds-state');
          entry.ContactInformation.Address.Zip = obj.processInputs(this, 'ngds-zip');
        });
        doc.Authors.push(entry);
      }

      doc.Keywords = [];

      doc.GeographicExtent = {};
      doc.GeographicExtent.NorthBound = obj.processInputs(geo, 'ngds-geo-north');
      doc.GeographicExtent.SouthBound = obj.processInputs(geo, 'ngds-geo-south');
      doc.GeographicExtent.EastBound = obj.processInputs(geo, 'ngds-geo-east');
      doc.GeographicExtent.WestBound = obj.processInputs(geo, 'ngds-geo-west');

      doc.Distributors = [];
      for (j = 0; j < distributors.length; j++) {
        entry = {};
        entry.ContactInformation = {};
        entry.ContactInformation.Address = {};
        distributor = $(distributors[j]);
        distributor.find('input').each(function () {
          entry.Name = obj.processInputs(this, 'ngds-name');
          entry.OrganizationName = obj.processInputs(this, 'ngds-organization');
          entry.ContactInformation.Phone = obj.processInputs(this, 'ngds-phone');
          entry.ContactInformation.email = obj.processInputs(this, 'ngds-email');
          entry.ContactInformation.Address.Street = obj.processInputs(this, 'ngds-street');
          entry.ContactInformation.Address.City = obj.processInputs(this, 'ngds-city');
          entry.ContactInformation.Address.State = obj.processInputs(this, 'ngds-state');
          entry.ContactInformation.Address.Zip = obj.processInputs(this, 'ngds-zip');
        });
        doc.Distributors.push(entry);
      }

      doc.MetadataContact = {};
      doc.MetadataContact.Name = obj.processInputs(contact, 'ngds-name');
      doc.MetadataContact.OrganizationName = obj.processInputs(contact, 'ngds-organization');
      doc.MetadataContact.ContactInformation = {};
      doc.MetadataContact.ContactInformation.Phone = obj.processInputs(contact, 'ngds-phone');
      doc.MetadataContact.ContactInformation.email = obj.processInputs(contact, 'ngds-email');
      doc.MetadataContact.ContactInformation.Address = {};
      doc.MetadataContact.ContactInformation.Address.Street = obj.processInputs(contact, 'ngds-street');
      doc.MetadataContact.ContactInformation.Address.City = obj.processInputs(contact, 'ngds-city');
      doc.MetadataContact.ContactInformation.Address.State = obj.processInputs(contact, 'ngds-state');
      doc.MetadataContact.ContactInformation.Address.Zip = obj.processInputs(contact, 'ngds-zip');

      return doc;
    },
    processInputs: function (input, search, defVal) {
      if ($(input).attr('name') === search) {
        return $(input).val();
      } else {
        if (!defVal) {
          return 'undefined';
        }
        return defVal;
      }
    }
  };
});

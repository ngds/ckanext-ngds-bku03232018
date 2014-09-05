'use strict';

/*
Here's what we want the ngds package schema to look like:
ngdsPackage: {
  _id: 'undefined',
  Title: 'undefined',
  Description: 'undefined',
  PublicationDate: 'undefined',
  ResourceId: 'undefined',
  Authors: [{
    Name: 'undefined',
    OrganizationName: 'undefined',
    ContactInformation: {
      Phone: 'undefined',
      email: 'undefined',
      Address: {
        Street: 'undefined',
        City: 'undefined',
        State: 'undefined',
        Zip: 'undefined'
      }
    }
  }],
  Keywords: [],
  GeographicExtent: {
    NorthBound: 'undefined',
    SouthBound: 'undefined',
    EastBound: 'undefined',
    WestBound: 'undefined'
  },
  Links: [ngdsRecord objects should go here],
  Distributors: [{
    Name: 'undefined',
    OrganizationName: 'undefined',
    ContactInformation: {
      Phone: 'undefined',
      email: 'undefined',
      Address: {
        Street: 'undefined',
        City: 'undefined',
        State: 'undefined',
        Zip: 'undefined'
      }
    }
  }],
  MetadataContact: {
    Name: 'undefined',
    OrganizationName: 'undefined',
    ContactInformation: {
      Phone: 'undefined',
      email: 'undefined',
      Address: {
        Street: 'undefined',
        City: 'undefined',
        State: 'undefined',
        Zip: 'undefined'
      }
    }
  }
}

And here's what we want the ngds record schema to look like:
ngdsRecord: {
  URL: 'undefined',
  Name: 'undefined',
  Description: 'undefined',
  Distributor: 'undefined',
  ServiceType: 'undefined',
  Layer: 'undefined',
  ContentModelURI: 'undefined',
  ContentModelVersion: 'undefined'
},
*/

ckan.module('ngds-contribute', function (jQuery, _) {
  return {
    initialize: function () {
      var message
        , form
        , button
        , obj
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

        var schema = obj.buildSchema();

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
        , distributors
        , contact
        , obj
        , i
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

        });
        doc.Authors.push(entry);
      }

      doc.Keywords = [];

      doc.GeographicExtent = {};

      doc.Distributors = [];

      doc.MetadataContact = {};

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
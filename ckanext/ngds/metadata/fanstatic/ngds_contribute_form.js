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
          entry.Name = obj.processInputs(this, 'ngds-author-name');
          entry.OrganizationName = obj.processInputs(this, 'ngds-author-organization');
          entry.ContactInformation.Phone = obj.processInputs(this, 'ngds-author-phone');
          entry.ContactInformation.email = obj.processInputs(this, 'ngds-author-email');
          entry.ContactInformation.Address.Street = obj.processInputs(this, 'ngds-author-street');
          entry.ContactInformation.Address.City = obj.processInputs(this, 'ngds-author-city');
          entry.ContactInformation.Address.State = obj.processInputs(this, 'ngds-author-state');
          entry.ContactInformation.Address.Zip = obj.processInputs(this, 'ngds-author-zip');
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
          entry.Name = obj.processInputs(this, 'ngds-distributors-name');
          entry.OrganizationName = obj.processInputs(this, 'ngds-distributors-organization');
          entry.ContactInformation.Phone = obj.processInputs(this, 'ngds-distributors-phone');
          entry.ContactInformation.email = obj.processInputs(this, 'ngds-distributors-email');
          entry.ContactInformation.Address.Street = obj.processInputs(this, 'ngds-distributors-street');
          entry.ContactInformation.Address.City = obj.processInputs(this, 'ngds-distributors-city');
          entry.ContactInformation.Address.State = obj.processInputs(this, 'ngds-distributors-state');
          entry.ContactInformation.Address.Zip = obj.processInputs(this, 'ngds-distributors-zip');
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
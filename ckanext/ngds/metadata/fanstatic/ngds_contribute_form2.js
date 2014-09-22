'use strict';

ckan.module('metadata-contribute', function (jQuery, _) {
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
        this.el.on('submit', function () {
          form = $(this);
          $('button', form).each(function () {
            button = $(this);
            $('<input type="hidden">').prop('name', button.prop('name')).prop('value', button.val()).appendTo(form);
          })
        })
      }

      $('#md-dataset-edit').submit(function () {
        data = obj.buildSchema();
        form = $(this);
        injection = $('<input>')
          .attr('type', 'hidden')
          .attr('name', 'md-package')
          .val(JSON.stringify(data));
        $('#md-dataset-edit').append($(injection));
      })
    },
    buildSchema: function () {
      var obj
        , basic
        , doc
        , dateTime
        , citedSourceAgents
        , sourceAgents
        , sourceAgent
        , resourceContact
        , distributors
        , distribs
        , distributor
        , geo
        , i
        , j
        ;

      function buildRelatedAgent (section) {
        var agent
          , role
          ;

        agent = {};
        agent.relatedAgent = {};
        role = agent.relatedAgent.agentRole = {};
        role.individual = {};

        $(section).find('input').each(function () {
          role.individual.personName = obj.processInputs(this, 'md-person-name');
          role.individual.personPosition = obj.processInputs(this, 'md-person-position');
          role.organizationName = obj.processInputs(this, 'md-organization-name');
          role.phoneNumber = obj.processInputs(this, 'md-phone-number');
          role.contactEmail = obj.processInputs(this, 'md-contact-email');
          role.contactAddress = obj.processInputs(this, 'md-contact-address');
        });

        return agent;
      }

      obj = this;

      basic = $('#collapse-basic-fields .ngds-input-form');
      citedSourceAgents = $('#collapse-ngds-author-fields .ngds-input-form');
      resourceContact = $('#collapse-ngds-metadata-contact-fields .ngds-input-form');
      distributors = $('#collapse-ngds-distributor-fields .ngds-input-form');
      geo = $('#collapse-ngds-geographic-extent-fields .ngds-input-form');

      doc = {};
      doc.citationDates = {};
      doc.citationDates.EventDateObject = {};
      dateTime = doc.citationDates.EventDateObject.dateTime = {};
      basic.find('input').each(function () {
        if ($(this).attr('name') === 'title') {
          doc.resourceTitle = obj.processInputs(this, 'title');
        }
        doc.resourceDescription = obj.processInputs(this, 'description');
        dateTime = obj.processInputs(this, 'publication_date');
      });

      sourceAgents = [];
      for (i = 0; i < citedSourceAgents.length; i++) {
        sourceAgent = citedSourceAgents[i];
        sourceAgents.push(buildRelatedAgent(sourceAgent));
      }
      doc.citedSourceAgents = sourceAgents;

      doc.resourceContact = buildRelatedAgent(resourceContact);

      distribs = [];
      for (j = 0; j < distributors.length; j++) {
        distributor = distributors[j];
        distribs.push(distributor);
      }
      doc.resourceAccessOptions = {};
      doc.resourceAccessOptions.distributors = distribs;

      doc.geographicExtent = [{
        northBoundLatitude: obj.processInputs(geo, 'md-geo-north'),
        southBoundLatitude: obj.processInputs(geo, 'md-geo-south'),
        eastBoundLongitude: obj.processInputs(geo, 'md-geo-east'),
        westBoundLongitude: obj.processInputs(geo, 'md-geo-west')
      }];

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
  }
});
'use strict';

ckan.module('md-package-contribute', function (jQuery, _) {
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
            $('<input type="hidden">')
              .prop('name', button.prop('name'))
              .prop('value', button.val())
              .appendTo(form);
          })
        })
      }

      $('#md-dataset-edit').submit(function () {
        data = obj.buildSchema();
        form = $(this);
        injection = $('<input>')
          .attr('type', 'hidden')
          .attr('name', 'ngds_package')
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
        , geo
        , geoExt
        , i
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
          var name = $(this).attr('name');
          if (name === 'md-person-name') {
            role.individual.personName = $(this).val();
          }
          if (name === 'md-person-position') {
            role.individual.personPosition = $(this).val();
          }
          if (name === 'md-organization-name') {
            role.organizationName = $(this).val();
          }
          if (name === 'md-phone-number') {
            role.phoneNumber = $(this).val();
          }
          if (name === 'md-contact-email') {
            role.contactEmail = $(this).val();
          }
          if (name === 'md-contact-address') {
            role.contactAddress = $(this).val();
          }
        });

        return agent;
      }

      obj = this;

      basic = $('#collapse-basic-fields .ngds-input-form');
      citedSourceAgents = $('#collapse-ngds-author-fields .md-input-form');
      resourceContact = $('#collapse-ngds-metadata-contact-fields .md-input-form');
      geo = $('#collapse-ngds-geographic-extent-fields .md-input-form');

      doc = {};
      doc.citationDates = {};
      doc.citationDates.EventDateObject = {};
      dateTime = doc.citationDates.EventDateObject = {};

      basic.find('textarea').each(function () {
        var name = $(this).attr('name');
        if (name === 'notes') {
          doc.resourceDescription = $(this).val();
        }
      });

      basic.find('input').each(function () {
        var name = $(this).attr('name');
        if (name === 'title') {
          doc.resourceTitle = $(this).val();
        }
        if (name === 'publication_date') {
          dateTime.dateTime = $(this).val();
        }
      });

      basic.find('select').each(function () {
        var name = $(this).attr('name');
        if (name === 'md-usgin-content-model') {
          doc.usginContentModel = $(this).val();
        }
        if (name === 'md-usgin-content-model-version') {
          doc.usginContentModelVersion = $(this).val();
        }
      });

      sourceAgents = [];
      for (i = 0; i < citedSourceAgents.length; i++) {
        sourceAgent = citedSourceAgents[i];
        sourceAgents.push(buildRelatedAgent(sourceAgent));
      }
      doc.citedSourceAgents = sourceAgents;

      doc.resourceContact = buildRelatedAgent(resourceContact);

      geoExt = {};
      doc.geographicExtent = [];
      geo.find('input').each(function () {
        var name
          , north
          , south
          , east
          , west
          ;

        name = $(this).attr('name');
        if (name === 'md-geo-north') {
          geoExt.northBoundLatitude = parseFloat($(this).val());
        }
        if (name === 'md-geo-south') {
          geoExt.southBoundLatitude = parseFloat($(this).val());
        }
        if (name === 'md-geo-east') {
          geoExt.eastBoundLongitude = parseFloat($(this).val());
        }
        if (name === 'md-geo-west') {
          geoExt.westBoundLongitude = parseFloat($(this).val());
        }
      });
      doc.geographicExtent.push(geoExt);

      return doc;
    }
  }
});
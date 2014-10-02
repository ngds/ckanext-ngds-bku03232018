'use strict';

ckan.module('md-resource-contribute', function (jQuery, _) {
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

      $('#md-resource-edit').submit(function () {
        data = obj.buildSchema();
        form = $(this);
        injection = $('<input>')
          .attr('type', 'hidden')
          .attr('name', 'ngds_resource')
          .val(JSON.stringify(data));
        $('#md-resource-edit').append($(injection));
      })
    },
    buildSchema: function () {
      var obj
        , doc
        , info
        , resource
        , distributor
        , linkObj
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

      resource = $('#collapse-md-resource-fields .md-input-form');
      distributor = $('#collapse-md-distributor-fields .md-input-form');

      doc = {};
      doc.resourceAccessOptions = [];

      info = {};
      info.distributor = buildRelatedAgent(distributor);

      info.accessLinks = {};
      linkObj = info.accessLinks.LinkObject = {};

      resource.find('textarea').each(function () {
        var name = $(this).attr('name');
        if (name === 'description') {
          linkObj.linkDescription = $(this).val();
        }
      });

      resource.find('input').each(function () {
        var name = $(this).attr('name');
        if (name === 'name') {
          linkObj.linkTitle = $(this).val();
        }
      });

      resource.find('select').each(function () {
        var name = $(this).attr('name');
        if (name === 'md-usgin-content-model-layer') {
          doc.usginContentModelLayer = $(this).val();
        }
      });

      doc.resourceAccessOptions.push(info);

      return doc;
    }
  }
});
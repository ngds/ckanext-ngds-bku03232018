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

    },
    processInputs: function (input, search, defVal) {

    }
  }
});
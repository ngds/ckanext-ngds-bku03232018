'use strict';

ckan.module('ngds_add_distributor', function ($, _) {
  return {
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.on('click', this._onClick);
    },
    _onClick: function (event) {
      this.sandbox.client.getTemplate('ngds_distributor_form.html',
        this.options, this._onReceiveSnippet);
    },
    _onReceiveSnippet: function (html) {
      $('#collapse-ngds-distributor-fields .form-fields').append(html);
    }
  }
});
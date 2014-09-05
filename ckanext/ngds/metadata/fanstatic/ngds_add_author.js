'use strict';

ckan.module('ngds_add_author', function ($, _) {
  return {
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.on('click', this._onClick);
    },
    _onClick: function (event) {
      this.sandbox.client.getTemplate('ngds_author_form.html',
        this.options, this._onReceiveSnippet);
    },
    _onReceiveSnippet: function (html) {
      $('#collapse-ngds-author-fields .form-fields').append(html);
    }
  }
});
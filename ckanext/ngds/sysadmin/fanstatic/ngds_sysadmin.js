'use strict';

ckan.module('ngds_sysadmin', function ($, _) {
  return {
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.on('click', this._onClick);
    },
    _onClick: function (event) {
      this.sandbox.client.getTemplate('featured-data-contrib.html',
        this.options, this._onReceiveSnippet);
    },
    _onReceiveSnippet: function (html) {
      $('#featured-data-md').append(html);
    }
  }
});
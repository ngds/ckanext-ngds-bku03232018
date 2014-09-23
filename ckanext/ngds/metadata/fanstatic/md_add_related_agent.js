'use strict';

ckan.module('md_add_author', function ($, _) {
  return {
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.on('click', this._onClick);
    },
    _onClick: function (event) {
      this.sandbox.client.getTemplate('contrib_md_related_agent_form.html',
        this.options, this._onReceiveSnippet);
    },
    _onReceiveSnippet: function (html) {
      var target = $('#collapse-ngds-author-fields .form-fields .md-cited-source-agent');
      target.append('<hr>');
      target.append(html);
    }
  }
});
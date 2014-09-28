'use strict';

ckan.module('md_toggle_usgin', function ($, _) {
  return {
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.on('click', this._onClick);
    },
    _onClick: function (event) {
      var target
        , targetBtn
        , otherBtn
        , targetTab
        , otherTab
        ;

      target = event.currentTarget.id;
      target = target.split('toggle-')[1];

      if (target === 'structured-tab') {
        targetBtn = $('#toggle-structured-tab');
        otherBtn = $('#toggle-unstructured-tab');

        targetBtn.addClass('active');
        otherBtn.removeClass('active');

        targetTab = $('#structured-tab');
        otherTab = $('#unstructured-tab');

        otherTab.removeClass('active');
        targetTab.addClass('active');
      }

      if (target === 'unstructured-tab') {
        targetBtn = $('#toggle-unstructured-tab');
        otherBtn = $('#toggle-structured-tab');

        targetBtn.addClass('active');
        otherBtn.removeClass('active');

        targetTab = $('#unstructured-tab');
        otherTab = $('#structured-tab');

        otherTab.removeClass('active');
        targetTab.addClass('active');
      }
    }
  }
});
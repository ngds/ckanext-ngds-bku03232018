'use strict';

ckan.module('md_toggle_usgin', function ($, _) {
  return {
    data: {
      contentModels: ''
    },
    initialize: function () {
      var module = this;
      $.proxyAll(this, /_on/);
      module.el.on('click', this._onClick);
      module._getContentModels(function (res) {
        if (res.success) {
          module._buildContentModelSelect(res);
          module.data.contentModels = res.result;
        }
      });
      module._buildContentModelLayerVersionSelect();
    },
    _getContentModels: function (callback) {
      $.ajax({
        url: '/api/action/get_content_models',
        success: function (res) {
          if (res.success) {
            callback(res);
          }
        }
      })
    },
    _buildContentModelSelect: function (data) {
      var select
        , cm
        , i
        ;

      select = $('[name=md-usgin-content-model]');
      select.empty();

      for (i = 0; i < data.result.length; i++) {
        cm = data.result[i];
        select.append('<option value="' + cm.uri + '">' + cm.title + '</option>');
      }
    },
    _buildContentModelLayerVersionSelect: function () {
      var module = this;
      $('[name=md-usgin-content-model]').on('change', function (e) {
        var uri
          , versionSelect
          , models
          , model
          , versions
          , version
          , i
          , j
          ;

        uri = e.val;
        versionSelect = $('[name=md-usgin-content-model-version]');
        versionSelect.empty();

        models = module.data.contentModels;
        for (i = 0; i < models.length; i++) {
          model = models[i];
          if (model.uri === uri) {
            versions = model.versions;
          }
        }

        for (j = 0; j < versions.length; j++) {
          version = versions[j];
          versionSelect.append('<option value="' + version.uri + '">' + version.version + '</option>');
        }
      })
    },
    _loadForm: function (event) {
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
    },
    _onClick: function (event) {
      var module
        ;

      module = this;
      if (module.data.contentModels) {
        module._loadForm(event);
      } else {
        module._getContentModels(function (res) {
          if (res.success) {
            console.log(res);
            module.data.contentModels = res.result;
          }
        })
      }
    }
  }
});
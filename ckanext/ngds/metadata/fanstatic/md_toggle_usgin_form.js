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
          module.data.contentModels = res.result;
        }
      });
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

      for (i = 0; i < data.length; i++) {
        cm = data[i];
        select.append('<option value="' + cm.uri + '">' + cm.title + '</option>');
      }
      this._buildContentModelLayerVersionSelect();
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

        // 'e' and 'select' lose their scopes here, so make a direct call to
        // the DOM element again #aintnopartylikeajqueryparty
        uri = $('[name=md-usgin-content-model]').val();
        versionSelect = $('[name=md-usgin-content-model-version]');

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
    _onReceiveSnippet: function (html) {
      var target = $('#unstructured-tab .usgin-content-model-select');
      target.append(html);
      this._buildContentModelSelect(this.data.contentModels);
    },
    _onRemoveSnippet: function (html) {
      var target = $('#unstructured-tab .usgin-content-model-select');
      target.empty();
    },
    _loadForm: function (event) {
      var module
        , target
        , targetBtn
        , otherBtn
        , targetTab
        , otherTab
        ;

      module = this;
      target = event.currentTarget.id;
      target = target.split('toggle-')[1];

      if (target === 'structured-tab') {
        module.sandbox.client.getTemplate('contrib_md_usgin_content_model.html',
          module.options, module._onReceiveSnippet);

        targetBtn = $('#toggle-structured-tab');
        otherBtn = $('#toggle-unstructured-tab');

        targetBtn.addClass('active');
        otherBtn.removeClass('active');

        targetTab = $('#structured-tab');
        otherTab = $('#unstructured-tab');

        otherTab.addClass('active');
        targetTab.removeClass('active');
      }

      if (target === 'unstructured-tab') {
        module.sandbox.client.getTemplate('contrib_md_usgin_content_model.html',
          module.options, module._onRemoveSnippet);

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
'use strict';

ckan.module('ngds_geothermal_prospector', function ($, _) {
  return {
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.on('click', this._onClick);
    },
    _onClick: function (event) {
      var id = $('#' + event.currentTarget.id)
        , resId = id.attr('res_id')
        ;

      $.ajax({
        url: '/api/action/geothermal_prospector_url',
        type: 'POST',
        data: JSON.stringify({'id': resId}),
        success: function (data) {
          window.open(data.result, '_blank');
        }
      });
    }
  }
});
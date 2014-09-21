'use strict';

ckan.module('ngds_carousel', function ($, _) {
  return {
    initialize: function () {
      $(this).ready(function () {
        $('.carousel').carousel({
          interval: 5000
        })
      })
    }
  }
});
'use strict';

ckan.module('ngds_sysadmin', function ($, _) {
  return {
    initialize: function () {
      console.log('initialized for this element:', this.el);
    }
  }
});
'use strict';

angular.
  module('core.qpanel').
  factory('Setting', ['$resource',
    function($resource) {
    return $resource('setting/:section', {}, {
        query: {
          method: 'GET',
          params: {section: null},
          isArray: false
        }
      });
    }
  ]);

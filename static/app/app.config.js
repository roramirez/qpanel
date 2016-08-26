'use strict';

angular.
  module('qpanelApp').
  config(['$locationProvider' ,'$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');

      $routeProvider.
        when('/setting', {
          template: '<setting></setting>'
        }).

        otherwise('/setting');
    }
  ]);

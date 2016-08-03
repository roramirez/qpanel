'use strict';

// Register `setting` component, along with its associated controller and template
angular.
  module('setting').
  component('setting', {
    templateUrl: 'static/app/setting/setting.template.html',
    controller: ['Setting',
      function SettingController(Setting) {
        var self = this;
        self.settings = Setting.query(function(settings) {
            // do somethings
        });

        self.save = function save() {
            self.settings.$save();
        };

        self.isFreeSWITCH = function(){
            // refactor me
            var v = self.settings.general.freeswitch;
            if (v == "false" || v == "0") {
                return false;
            } else if (v == "true" || v == "1") {
                return true;
            }
            return v;
        }


      }
    ]

  });

angular.
  module('setting').
  directive('trueFalseCheckbox', function(){
      return {
          restrict: 'A',
          require: 'ngModel',
          link: function(scope, element, attrs, modelCtrl) {
             modelCtrl.$formatters.push(formatCheckBoxValue);
             function formatCheckBoxValue(viewValue) {
                  var v = viewValue.toString().toLowerCase();
                  if (v == "false" || v == "0") {
                      return false;
                  } else if (v == "true" || v == "1") {
                      return true;
                  }
                  return v;
            }
         }
      };
  });

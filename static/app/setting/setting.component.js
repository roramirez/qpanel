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

        self.addResetStats = function() {
            if (typeof self.settings.reset_stats === "undefined")
                self.settings.reset_stats = [];
            self.settings.reset_stats.push({'name': null, 'value': null});
        }

        self.addRename = function() {
            if (typeof self.settings.rename === "undefined")
                self.settings.rename = [];
            self.settings.rename.push({'name': null, 'value': null});
        }

        self.addRemoveRename = function(index) {
            self.settings.rename.splice(index, 1);
            delete self.settings.rename[index];
        }

        self.addRemoveResetStats = function(index) {
            self.settings.reset_stats.splice(index, 1);
            delete self.reset_stats.rename[index];
        }

        self.save = function save() {
            self.settings.$save();
        };

        self.isFreeSWITCH = function(){
            return self.settings.general.freeswitch;
        }

      }
    ]

  });

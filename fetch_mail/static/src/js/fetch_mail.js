odoo.define('fetch.mail.run', function(require) {
    'use strict';

    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;


    var Fet = Widget.extend({
        // events is an object (mapping) of an event to the function
        // or method to call when the event is triggered
//        className: '.p_test',
        template: 'Fetch',
        events: {
            'click .p_test': 'b_click',
        },

        b_click: function() {
            var fetch_model = new Model('cron.fetch');
            fetch_model.call('run_fetch_mail',[[]]);
        },


    });

    core.action_registry.add('run.fetch.mail', Fet);
});

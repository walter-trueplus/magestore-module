odoo.define('fetch.mail.run', function(require) {
    'use strict';

    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    var ListView = require('web.ListView');
    var QWeb = core.qweb;


    var Fet = Widget.extend({
        // events is an object (mapping) of an event to the function
        // or method to call when the event is triggered
        // className: '.p_test',
        template: 'Fetch',
        events: {
            'click .p_test': 'b_click',
        },

        b_click: function() {
            var fetch_model = new Model('mail.fetched');
            fetch_model.call('run_fetch_mail',[[]]);
        },

    });

    var Extends = ListView.include({
        // add listener for fetch_mail button
        render_buttons: function() {
            this._super.apply(this, arguments);
            this.$buttons.on('click', '.o_list_button_fetch_mail', this.proxy('fetch_all_mail'));

        },
        fetch_all_mail:function(){
            var self = this;
            var fetch_model = new Model('mail.fetched');
            fetch_model.call('run_fetch_mail',[[]]);
            for(var i = 0; i < 2; i++){
                location.reload();
            }
        },
    });


    core.action_registry.add('run.fetch.mail', Fet);
});

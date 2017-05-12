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
            var fetch_model = new Model('cron.fetch');
            fetch_model.call('run_fetch_mail',[[]]);
        },

    });

    var Extends = ListView.include({
//        init: function(){
//
//        },
        // add listener for fetch_mail button
        render_buttons: function() {
            this._super.apply(this, arguments);
            this.$buttons.on('click', '.o_list_button_fetch_mail', this.proxy('fetch_all_mail'));

        },
        fetch_all_mail:function(){
            var self = this;
            console.log('logllll');
            var fetch_model = new Model('cron.fetch');
            fetch_model.call('run_fetch_mail',[[]]);
//            var mail_fetch = new Model('mail.fetched');
//            mail_fetch.call('reload_page', [[]]);
//            this.do_action({
//                type: 'ir.actions.act_window',
//                res_model: "mail.fetched",
//                views: [[false, 'tree']],
//                target: 'current',
//                tag: 'reload',
//                nodestroy: true
//            });

//            var ir_ui_view = new Model('ir.ui.view');
////            id of form and tree will put to action open tree fetched mail
//            var form_fetch_mail_id,
//                tree_fetch_mail_id;
//            ir_ui_view.call('search',[[['arch_fs', '=', 'fetch_mail/views/views.xml']]]).then(function(data){
//                console.log(data);
//                self.do_action({
//                    type: 'ir.actions.act_window',
//                    res_model: 'mail.fetched',
//                    views: [[382, 'tree']],
//                });
//            });

        },
    });


    core.action_registry.add('run.fetch.mail', Fet);
});

odoo.define('create_user_from_excel_list.button_import_users', function (require) {
    "use strict";

    var core = require('web.core');
    var utils = require('web.utils');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    var config = require('web.config');
    var data = require('web.data');
    var DataExport = require('web.DataExport');
    var Pager = require('web.Pager');
    var pyeval = require('web.pyeval');
    var session = require('web.session');
    var Sidebar = require('web.Sidebar');
    var View = require('web.View');
    var Bus = require('web.Bus');
    var _t = core._t;
    var _lt = core._lt;
    var ListView = require('web.ListView');

    Widget.include({
        events: _.extend({}, Widget.prototype.events, {
            'click .import_users': 'button_clicked',
        }),
        button_clicked: function () {
            var self = this;
            var model_obj = new Model('ir.model.data');
            var view_id = model_obj.call('get_object_reference', ['create_user_from_excel_list', 'view_import_users']);
            self.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: 'import.users',
                views: [[view_id, 'form']],
                view_id : view_id,
                target: 'new'
            });
        },
    });
})
;


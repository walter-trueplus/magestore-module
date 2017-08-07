odoo.define('create_user_from_excel.button_import_user', function(require){
    'use strict';

    var Model = require('web.Model');
    var ListView = require('web.ListView');

    var Extends = ListView.include({
        render_buttons: function() {
            this._super.apply(this, arguments);
            this.$buttons.on('click', '.o_list_button_import_user', this.proxy('import_users'));
        },
        import_users: function(){
            var self = this;
            var invoice_model = new Model('import.users.wizard');

            invoice_model.call('get_id_of_view_import').then(function(result){
                self.do_action({
                    type: 'ir.actions.act_window',
                    name: 'Import Wizard',
                    res_model: 'import.users.wizard',
                    views: [[result, 'form']],
                    view_type: "form",
                    view_mode: "form",
                    target: 'new'
                });
            });
        },
    });
});

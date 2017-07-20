odoo.define('pos_add_note.pos_add_note', function (require) {
    "use strict";
    //console.log("da vao");
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    
    var utils = require('web.utils');

    var QWeb = core.qweb;
    var _t = core._t;
    var round_pr = utils.round_precision;
    var screens = require('point_of_sale.screens');
    var _super_order = models.Order.prototype;
    var _super_posmodel = models.PosModel.prototype;

    var PosAddNote = screens.ActionpadWidget.include({
        init: function (parent, options) {
            var self = this;
            this._super(parent, options);

            this.pos.bind('change:selectedClient', function () {
                self.renderElement();
            });
            this.pos = options.pos || (parent ? parent.pos : undefined);
        },
        events: _.extend({}, PosBaseWidget.prototype.events, {
            'click .add-note': 'button_clicked'
        }),
        button_clicked: function () {
            var order = this.pos.get_order();
            this.gui.show_popup('textarea', {
                title: _t('Add Note'),
                value: _t(''),
                confirm: function (note) {
                    this.gui.show_popup('confirm', {
                        title: _t('Note Added!'),
                    });
                    return order.set_note(note);
                },
            });
        },
    });

    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            _super_order.initialize.call(this, attributes, options);
            this.note = this.note || "";
        },
        set_note: function (note) {
            this.note = note;
            this.trigger('change', this);
        },
        get_note: function (note) {
            return this.note;
        },
        export_as_JSON: function () {
            var json = _super_order.export_as_JSON.call(this);
            json.note = this.note;
            return json;
        },
        init_from_JSON: function (json) {
            this.note = json.note;
            _super_order.init_from_JSON.apply(this, arguments);
        },
    });

    return {
        PosAddNote: PosAddNote,
    };
})
;


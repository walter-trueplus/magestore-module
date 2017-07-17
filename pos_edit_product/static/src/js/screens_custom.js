odoo.define('pos_edit_product.screens_custom', function (require) {
    "use strict";

    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var utils = require('web.utils');
    var formats = require('web.formats');

    var screens = require('point_of_sale.screens');

    var Orderline = PosBaseWidget.include({
        template: 'Orderline',
        init: function (parent, options) {
            this._super(parent, options);
            options = options || {};
            this.pos = options.pos || (parent ? parent.pos : undefined);
            this.chrome = options.chrome || (parent ? parent.chrome : undefined);
            this.gui = options.gui || (parent ? parent.gui : undefined);
            this.product = options.product;
        },
        events: _.extend({}, PosBaseWidget.prototype.events, {
            'click .edit-product': 'button_edit_click'
        }),
        //khi edit duoc click
        button_edit_click: function () {
            var order = this.pos.get_order();

            //tim orderline duoc selected
            if (order.get_selected_orderline()) {
                this.$('.selected .info').addClass('oe_hidden');//them class oe_hidden vao class info
                this.$('.selected .info-copy').removeClass('oe_hidden');//xoa class oe_hidden cua class info-copy
            }
            var self = this;
            //khi nhan enter => event
            this.$(".selected .input-quant").keydown(function (e) {
                if (e.keyCode == 13) {
                    var input_value = $(".selected .input-quant").val();
                    var number = parseFloat(input_value.replace(/,/g, ''));
                    self.set_quant(number);// call set_quant()
                }
            });
        },

        set_quant: function (quantity) {
            var order = this.pos.get_order();
            if (order.get_selected_orderline()) {
                return order.get_selected_orderline().set_quantity(quantity);//call set_quantity cua models Orderline
            }
        },
    });

    return {
        Orderline: Orderline,
    };

})
;


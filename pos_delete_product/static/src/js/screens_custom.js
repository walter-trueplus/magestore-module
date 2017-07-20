odoo.define('pos_delete_product.screens_custom', function (require) {
    "use strict";

    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var core = require('web.core');

    var utils = require('web.utils');


    var QWeb = core.qweb;
    var _t = core._t;

    var round_pr = utils.round_precision;
    var screens = require('point_of_sale.screens');

    var Orderline = PosBaseWidget.include({
        template: 'Orderline',
        init: function (parent, options) {
            this._super(parent);
            options = options || {};
            this.pos = options.pos || (parent ? parent.pos : undefined);
            this.chrome = options.chrome || (parent ? parent.chrome : undefined);
            this.gui = options.gui || (parent ? parent.gui : undefined);
            this.product = options.product;
        },
        events: _.extend({}, PosBaseWidget.prototype.events, {
            'click .delete-product': 'button_clicked'
        }),
        button_clicked: function (line) {
            var order = this.pos.get_order();
            var orderline = order.get_orderline(order.selected_orderline.id);
            return order.remove_orderline(orderline);
        },
    });
    return {
        Orderline: Orderline,
    };

})
;


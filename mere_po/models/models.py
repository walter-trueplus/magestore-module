# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError

class Handle(models.Model):
    _name = 'handle.purchase.order'

    @api.model
    def get_all_purchase_lines(self,lst_orders):
        list_order_lines = []
        partner_id = self.env['purchase.order'].search([('id', '=', int(lst_orders[0][0][0]))], limit=1).partner_id.id
        for lst_order in lst_orders[0]:
            lst_order_line = self.env['purchase.order.line'].search([('order_id', '=', int(lst_order[0]))])
            if self.env['purchase.order'].search([('id', '=', int(lst_order[0]))], limit=1).partner_id.id != partner_id:
                raise UserError("You must select order of same vendor!")
            list_order_lines.extend(list(lst_order_line))
        list_moves = []
        for order_line in list_order_lines:
            move = [0, False]
            move.append({'product_id': order_line.product_id.id,
                         'product_uom_qty': order_line.product_qty,
                         'product_uom': order_line.product_id.uom_id.id,
                         'name': order_line.product_id.name})
            list_moves.append(move)

        self.env['stock.picking'].create({'partner_id': partner_id,
                                             'move_type': 'direct',
                                             'picking_type_id': 1,
                                             'move_lines': list_moves,
                                             'location_id': 2,
                                             'location_dest_id': 2,
                                             'min_date': datetime.datetime.now()})

# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError

class Handle(models.Model):
    _name = 'handle.sale.order'

    @api.model
    def get_all_sale_order_lines(self,lst_orders):
        # khai bao list_order_line
        list_order_lines = []
        # set default parent_id
        partner_id = self.env['sale.order'].search([('id', '=', int(lst_orders[0][0][0]))], limit=1).partner_id.id
        # duyet toan bo list_order
        for lst_order in lst_orders[0]:
            # lay order_line
            lst_order_line = self.env['sale.order.line'].search([('order_id', '=', int(lst_order[0]))])
            for lst_o_l in lst_order_line:

            # kiem tra partner_id xem trung vs default k
            if self.env['sale.order'].search([('id', '=', int(lst_order[0]))], limit=1).partner_id.id != partner_id:
                raise UserError("You must select order of same partner!")

            list_order_lines.extend(list(lst_order_line))
        list_moves = []
        for order_line in list_order_lines:

            move = [0, False]
            move.append({'product_id': order_line.product_id.id,
                         'product_uom_qty': order_line.product_uom_qty,
                         'product_uom': order_line.product_id.uom_id.id,
                         'name': order_line.product_id.name})
            list_moves.append(move)

        self.env['stock.picking'].create({'partner_id': partner_id,
                                             'move_type': 'direct',
                                             'picking_type_id': 4,
                                             'move_lines': list_moves,
                                             'location_id': 2,
                                             'location_dest_id': 2,
                                             'min_date': datetime.datetime.now()})
#
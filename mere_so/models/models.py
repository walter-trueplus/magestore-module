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
        # khai bao source_document cho stock_picking moi
        source_document =''
        # set default parent_id
        partner_id = self.env['sale.order'].search([('id', '=', int(lst_orders[0][0][0]))], limit=1).partner_id.id
        # duyet toan bo list_order
        for lst_order in lst_orders[0]:
            # gan source_document moi
            sps = self.env['stock.picking'].search([('origin', '=', lst_order[1])])
            for sp in sps:
                if source_document:
                    source_document = source_document + ',' + sp.origin
                else:
                    source_document = sp.origin
            # khai bao mang trung gian lst_tmp
            # lst_tmp =[]
            # lay order_line
            lst_order_line = self.env['sale.order.line'].search([('order_id', '=', int(lst_order[0]))])
            # duyet toan bo lst_order_line
            for lst_o_l in lst_order_line:
                # check product_id cua tung lst_o_l : neu trung thi tang sl, neu k trung thi add
                if list_order_lines:
                    for item_tmp in list_order_lines:
                        if item_tmp.product_id == lst_o_l.product_id:
                            item_tmp.product_uom_qty += lst_o_l.product_uom_qty
                        else:
                            list_order_lines.append(lst_o_l)
                else:
                    list_order_lines.append(lst_o_l)
            # kiem tra partner_id xem trung vs default k
            if self.env['sale.order'].search([('id', '=', int(lst_order[0]))], limit=1).partner_id.id != partner_id:
                raise UserError("You must select order of same partner!")

        list_moves = []
        stock_pk = self.env['stock.picking'].search([('origin', '=', source_document)])
        if stock_pk:
            raise UserError("You had merge these order!, don't do it again!")

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
                                             'origin':source_document,
                                             'location_id': 2,
                                             'location_dest_id': 2,
                                             'min_date': datetime.datetime.now()})
#
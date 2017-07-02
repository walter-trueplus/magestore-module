# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError

class Handle(models.Model):
    _name = 'handle.sale.order'

    @api.model
    def get_all_sale_order_lines(self,list_orders):
        # khai bao list_order_line
        list_order_lines = []
        # khai bao source_document cho stock_picking moi
        source_document =''
        # set default parent_id
        partner_id = self.env['sale.order'].search([('id', '=', int(list_orders[0][0][0]))], limit=1).partner_id.id
        # duyet toan bo list_order
        for list_order in list_orders[0]:

            sale = self.env['sale.order'].search([('id', '=', int(list_order[0]))], limit=1)
            if sale.partner_id.id != partner_id:
                raise UserError("You must select order of same partner!")

            # gan source_document moi
            sps = self.env['stock.picking'].search([('origin', '=', list_order[1])])
            for sp in sps:
                if source_document:
                    source_document = source_document + ',' + sp.origin
                else:
                    source_document = sp.origin

            # xu ly product
            lst_order_line = self.env['sale.order.line'].search([('order_id', '=', int(list_order[0]))])
            if lst_order_line:
                for item in lst_order_line:
                    check = False
                    for i in list_order_lines:
                        if item.product_id == i.product_id:
                            i.product_uom_qty += item.product_uom_qty
                            check = True
                    if not check:
                        list_order_lines.append(item)
                    else:
                        print "trung"

            s = self.env['sale.order'].search([('id', '=', int(list_order[0]))], limit=1)
            if s.partner_id.id != partner_id:
                raise UserError("You must select order of same partner!")

        list_moves = []
        stock_pk = self.env['stock.picking'].search([('origin', '=', source_document)])
        print stock_pk
        if stock_pk:
            raise UserError("You had merge these order!, don't do it again!")

        for order_line in list_order_lines:
            move = [0, False]
            move.append({'product_id': order_line.product_id.id,
                         'product_uom_qty': order_line.product_uom_qty,
                         'product_uom': order_line.product_id.uom_id.id,
                         'name': order_line.product_id.name})
            list_moves.append(move)
        #
        self.env['stock.picking'].create({'partner_id': partner_id,
                                             'move_type': 'direct',
                                             'picking_type_id': 4,
                                             'move_lines': list_moves,
                                             'origin':source_document,
                                             'location_id': 2,
                                             'location_dest_id': 2,
                                             'min_date': datetime.datetime.now()})

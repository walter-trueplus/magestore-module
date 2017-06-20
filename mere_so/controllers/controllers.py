# -*- coding: utf-8 -*-
import json

import datetime

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request


class MereSo(http.Controller):

    @http.route('/so/merge', type='http', auth='user')
    def merge_so(self, data, token):
        abc = json.loads(data)
        list_order_lines = []
        for xyz in abc.get("rows"):
            orls = request.env['sale.order.line'].search([('order_id', '=', int(xyz[0]))])
            order_lst = request.env['sale.order'].search([('id', '=', int(xyz[0]))] , limit= 1)
            partnert = order_lst[0].partner_id.id;
            for odder in order_lst:
                if odder.partner_id != partnert:
                    raise ValidationError("You must select order of same partner!")

            list_order_lines.extend(list(orls))


        list_moves = []
        for order_line in list_order_lines:
            move = [0, False]
            move.append({'product_id': order_line.product_id.id,
                         'product_uom_qty': order_line.product_uom_qty,
                         'product_uom':order_line.product_id.uom_id.id,
                         'name': order_line.product_id.name})
            list_moves.append(move)

        request.env['stock.picking'].create({'partner_id':partnert,
                                             'move_type': 'direct',
                                             'picking_type_id': 4,
                                             'move_lines': list_moves,
                                             'location_id': 2,
                                             'location_dest_id': 2,
                                             'min_date': datetime.datetime.now()})
        return 'Success'

        # raise UserError(_("You must first select a partner!"))

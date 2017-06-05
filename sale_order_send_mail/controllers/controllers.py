# -*- coding: utf-8 -*-
from odoo import http
import odoo.http as http
from odoo.http import request
import os


class SaleOrderSendMail(http.Controller):

    @http.route('/sale_order_send_mail/done/<int:mailing_id>', type='http', website=True, auth='public')
    def mailing_accept(self, mailing_id, email=None, res_id=None, **post):
        rec = request.env['sale.order'].sudo().browse(int(mailing_id))
        rec.write({'state': 'done'})
        return "<h3>Thank you for accepting the order!</h3>"

    @http.route('/sale_order_send_mail/cancel/<int:mailing_id>', type='http', website=True, auth='public')
    def mailing_reject(self, mailing_id, email=None, res_id=None, **post):
        rec = request.env['sale.order'].sudo().browse(int(mailing_id))
        rec.write({'state': 'cancel'})
        return "<h3>You have declined the order!</h3>"

# -*- coding: utf-8 -*-
from odoo import http

# class StockConfigSettingCustom(http.Controller):
#     @http.route('/stock_notification_send_mail/stock_notification_send_mail/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_notification_send_mail/stock_notification_send_mail/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_notification_send_mail.listing', {
#             'root': '/stock_notification_send_mail/stock_notification_send_mail',
#             'objects': http.request.env['stock_notification_send_mail.stock_notification_send_mail'].search([]),
#         })

#     @http.route('/stock_notification_send_mail/stock_notification_send_mail/objects/<model("stock_notification_send_mail.stock_notification_send_mail"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_notification_send_mail.object', {
#             'object': obj
#         })
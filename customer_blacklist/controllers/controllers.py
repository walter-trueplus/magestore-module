# -*- coding: utf-8 -*-
from odoo import http

# class CustomerBlacklist(http.Controller):
#     @http.route('/customer_blacklist/customer_blacklist/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer_blacklist/customer_blacklist/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer_blacklist.listing', {
#             'root': '/customer_blacklist/customer_blacklist',
#             'objects': http.request.env['customer_blacklist.customer_blacklist'].search([]),
#         })

#     @http.route('/customer_blacklist/customer_blacklist/objects/<model("customer_blacklist.customer_blacklist"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer_blacklist.object', {
#             'object': obj
#         })
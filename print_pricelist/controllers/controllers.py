# -*- coding: utf-8 -*-
from odoo import http

# class PrintPricelist(http.Controller):
#     @http.route('/print_pricelist/print_pricelist/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/print_pricelist/print_pricelist/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('print_pricelist.listing', {
#             'root': '/print_pricelist/print_pricelist',
#             'objects': http.request.env['print_pricelist.print_pricelist'].search([]),
#         })

#     @http.route('/print_pricelist/print_pricelist/objects/<model("print_pricelist.print_pricelist"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('print_pricelist.object', {
#             'object': obj
#         })
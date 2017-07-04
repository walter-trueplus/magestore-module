# -*- coding: utf-8 -*-
from odoo import http

# class CustomSearch(http.Controller):
#     @http.route('/custom_search/custom_search/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_search/custom_search/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_search.listing', {
#             'root': '/custom_search/custom_search',
#             'objects': http.request.env['custom_search.custom_search'].search([]),
#         })

#     @http.route('/custom_search/custom_search/objects/<model("custom_search.custom_search"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_search.object', {
#             'object': obj
#         })
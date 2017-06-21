# -*- coding: utf-8 -*-
from odoo import http

# class MerePo(http.Controller):
#     @http.route('/mere_po/mere_po/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mere_po/mere_po/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mere_po.listing', {
#             'root': '/mere_po/mere_po',
#             'objects': http.request.env['mere_po.mere_po'].search([]),
#         })

#     @http.route('/mere_po/mere_po/objects/<model("mere_po.mere_po"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mere_po.object', {
#             'object': obj
#         })
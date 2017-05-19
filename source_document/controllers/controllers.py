# -*- coding: utf-8 -*-
from odoo import http

# class SourceDocument(http.Controller):
#     @http.route('/source_document/source_document/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/source_document/source_document/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('source_document.listing', {
#             'root': '/source_document/source_document',
#             'objects': http.request.env['source_document.source_document'].search([]),
#         })

#     @http.route('/source_document/source_document/objects/<model("source_document.source_document"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('source_document.object', {
#             'object': obj
#         })
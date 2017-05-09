# -*- coding: utf-8 -*-
from odoo import http

# class ExportModel(http.Controller):
#     @http.route('/export_model/export_model/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/export_model/export_model/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('export_model.listing', {
#             'root': '/export_model/export_model',
#             'objects': http.request.env['export_model.export_model'].search([]),
#         })

#     @http.route('/export_model/export_model/objects/<model("export_model.export_model"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('export_model.object', {
#             'object': obj
#         })
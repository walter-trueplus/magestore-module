# -*- coding: utf-8 -*-
from odoo import http

# class CheckDuplicateUsername(http.Controller):
#     @http.route('/check_duplicate_username/check_duplicate_username/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/check_duplicate_username/check_duplicate_username/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('check_duplicate_username.listing', {
#             'root': '/check_duplicate_username/check_duplicate_username',
#             'objects': http.request.env['check_duplicate_username.check_duplicate_username'].search([]),
#         })

#     @http.route('/check_duplicate_username/check_duplicate_username/objects/<model("check_duplicate_username.check_duplicate_username"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('check_duplicate_username.object', {
#             'object': obj
#         })
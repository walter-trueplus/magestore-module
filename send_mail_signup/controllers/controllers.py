# -*- coding: utf-8 -*-
from odoo import http

# class SendMailSignup(http.Controller):
#     @http.route('/send_mail_signup/send_mail_signup/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/send_mail_signup/send_mail_signup/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('send_mail_signup.listing', {
#             'root': '/send_mail_signup/send_mail_signup',
#             'objects': http.request.env['send_mail_signup.send_mail_signup'].search([]),
#         })

#     @http.route('/send_mail_signup/send_mail_signup/objects/<model("send_mail_signup.send_mail_signup"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('send_mail_signup.object', {
#             'object': obj
#         })
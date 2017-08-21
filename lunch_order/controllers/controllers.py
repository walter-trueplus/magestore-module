# -*- coding: utf-8 -*-
from odoo import http


# class WebsiteOrderLunch(http.Controller):
#     @http.route('/lunch_order/lunch_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

        #     @http.route('/lunch_order/lunch_order/objects/', auth='public')
        #     def list(self, **kw):
        #         return http.request.render('lunch_order.listing', {
        #             'root': '/lunch_order/lunch_order',
        #             'objects': http.request.env['lunch_order.lunch_order'].search([]),
        #         })

        #     @http.route('/lunch_order/lunch_order/objects/<model("lunch_order.lunch_order"):obj>/', auth='public')
        #     def object(self, obj, **kw):
        #         return http.request.render('lunch_order.object', {
        #             'object': obj
        #         })

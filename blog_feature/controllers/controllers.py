# -*- coding: utf-8 -*-
from odoo import http

# class BlogFeature(http.Controller):
#     @http.route('/blog_feature/blog_feature/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/blog_feature/blog_feature/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('blog_feature.listing', {
#             'root': '/blog_feature/blog_feature',
#             'objects': http.request.env['blog_feature.blog_feature'].search([]),
#         })

#     @http.route('/blog_feature/blog_feature/objects/<model("blog_feature.blog_feature"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('blog_feature.object', {
#             'object': obj
#         })
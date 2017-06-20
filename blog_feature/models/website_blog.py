# -*- coding :utf-8 -*-

from odoo import models, fields


class BlogPost(models.Model):
    _inherit = 'blog.post'
    is_feature = fields.Boolean('Post is feature')

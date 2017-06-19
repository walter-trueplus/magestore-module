# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    res_partner_ids = fields.Many2many('res.partner', string='Customer Groups')


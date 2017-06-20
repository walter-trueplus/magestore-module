# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    pricelist_ids = fields.Many2many('product.pricelist', string='Pricelists')

# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"
    reference_ids = fields.Many2one('sale.order', string='Source Document',
                                       compute="origin_compute", readonly=True,
                                       help="Reference of the document")

    @api.depends("origin")
    def origin_compute(self):
        for item in self:
            try:
                order_id = item.origin.split(":")[0]
                item.reference_ids = item.env['sale.order'].search([('name', '=', order_id)])
            except Exception:
                item.reference_ids= ""

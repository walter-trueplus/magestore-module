# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MrpProduction(models.Model):
    _name = "mrp.production"
    _inherit = "mrp.production"

    reference = fields.Many2one('sale.order', string='Source Document',
                                       compute="origin_compute",
                                       help="Reference of the document", store= True)

    @api.depends("origin")
    def origin_compute(self):
        for item in self:
            try:
                order_id = item.origin
                order_id = order_id.split(":")[0]
                item.reference = item.env['sale.order'].search([('name', '=', order_id)])
            except Exception:
                item.reference = False

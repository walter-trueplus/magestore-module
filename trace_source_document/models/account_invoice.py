# -*- coding : utf-8 -*-

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    origin_reference_ids = fields.Many2one('sale.order', string='Source Document', readonly=True,
                                       compute="origin_compute")

    @api.depends("origin")
    def origin_compute(self):
        for item in self:
            order_id = item.origin
            item.origin_reference_ids = item.env['sale.order'].search([('name', '=', order_id)])
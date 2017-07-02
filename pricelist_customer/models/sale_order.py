# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True, readonly=True,
                                   states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                   help="Pricelist for current sales order.", default=lambda self: self.env['product.pricelist'].search([], limit=1))

    @api.onchange('partner_id')
    def pricelist(self):
        partner_id= self.partner_id
        print partner_id
        if partner_id:
            pricelist =  self.env['product.pricelist'].search([('res_partner_ids', 'in', partner_id.id)])
            for item in pricelist:
                if item != self.env['product.pricelist']:
                    self.pricelist_id = item









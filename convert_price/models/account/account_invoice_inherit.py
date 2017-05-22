# -*- coding: utf-8 -*-

from odoo import models
from odoo import api
from odoo import fields
from num2words import num2words

class AccountInvoice(models.Model):
    _inherit='account.invoice'

    amount_total_text = fields.Text(string='Total (In text)', store=False, readonly=True,
                                    compute='_compute_amount_total_text')

    @api.depends('amount_total')
    def _compute_amount_total_text(self):
        option = self._get_lang_config()
        if option == 'eng':
            for sale_order in self:
                sale_order.amount_total_text ='In text: ' +num2words(sale_order.amount_total)
        elif option == 'viet':
            for sale_order in self:
                sale_order.amount_total_text = 'Bằng chữ: '+self.env['convert.to.vn'].number_to_text(sale_order.amount_total)

    @api.model
    def _get_lang_config(self):
        options=self.env['account.config.settings'].search([])
        if len(options)==0:
            return 'eng'#default
        else:
            return options[-1].language_option
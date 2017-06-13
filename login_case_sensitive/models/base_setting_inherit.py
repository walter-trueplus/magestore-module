# -*- coding: utf-8 -*-

from odoo import models
from odoo import fields
from odoo import api


class base_setting_inherit(models.TransientModel):
    _inherit = "base.config.settings"
    case_sensitive_option = fields.Boolean(string='Login case sensitively',help='Login Case Sensitively',default=True)

    @api.multi
    def set_case_sensitive_value(self):
        return self.env['ir.values'].sudo().set_default(
            'base.config.settings', 'case_sensitive_option', self.case_sensitive_option)


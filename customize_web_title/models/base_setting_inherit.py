# -*- coding: utf-8 -*-

from odoo import models
from odoo import fields
from odoo import api


class base_setting_inherit(models.TransientModel):
    _inherit = "base.config.settings"
    custom_web_title = fields.Char(string="Custom web title:", default="Odoo")

    @api.multi
    def set_custom_web_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'base.config.settings', 'custom_web_title', self.custom_web_title)

    # get custom title from database
    @api.model
    def get_custom_title(self):
        setting_records = self.env['base.config.settings'].search([])
        if len(setting_records) == 0:  # default title
            return 'Odoo'
        else:  # return custom title
            return setting_records[-1].custom_web_title

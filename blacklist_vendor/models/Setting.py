# -*- coding:utf-8 -*-
from odoo import fields, models, api


class Setting(models.TransientModel):
    _inherit = 'purchase.config.settings'

    warning_option = fields.Selection([(0, 'No warning'),
                                       (1, 'Warning'),
                                       (2, 'Eject create purchase')]
                                      ,
                                      string="Notify:")



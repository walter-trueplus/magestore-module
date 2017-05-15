# -*- coding:utf-8 -*-
from odoo import fields, models


class Setting(models.TransientModel):

    _inherit = 'sale.config.settings'

    warning_option=fields.Selection([(0,'No warning'),
                                     (1,'Warning'),
                                     (2,'Eject create purchase')]
                                    ,string="Notify option when create purchase order in case the vendor in black list")
# -*- coding:utf-8 -*-
from odoo import fields, models,api


class Setting(models.TransientModel):

    _inherit = 'sale.config.settings'

    warning_option=fields.Selection([(0,'No warning'),
                                     (1,'Warning'),
                                     (2,'Eject create purchase')]
                                    ,string="Notify option when create purchase order in case the vendor in black list")

    @api.onchange('warning_option')
    def on_warning_option_changed(self):
        print 'change:',self.warning_option


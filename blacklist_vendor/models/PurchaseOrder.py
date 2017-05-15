# -*- coding: utf-8 -*-

from odoo import _
from odoo import api
from odoo import exceptions
from odoo import models


class PurchaseOrder(models.Model):
    _name = "purchase.order"

    _inherit = "purchase.order"

    @api.model
    def create(self, vals):
        vendor_id = vals['partner_id']
        vendor = self.env['res.partner'].search([('id', '=', vendor_id)])
        print 'vendor in black list::', vendor.in_blacklist
        # check option when create purchase whie vendor in black list:
        # get the lastest record has been modify
        setting = self.env['purchase.config.settings'].search([])[-1]
        option = setting.warning_option
        if option == 0:  # create purcharse, do not show warning
            print 'do nothing'
            return super(PurchaseOrder, self).create(vals)
        elif option == 1:  # show warning
            print 'show warning'
            raise exceptions.UserError(_('You have created purchase order in case the vendor in black list!'))
            return super(PurchaseOrder, self).create(vals)
        elif option == 2:  # eject create purchase:
            print 'eject'
            raise exceptions.UserError(_('You can not create purchase order in case the vendor in black list'))

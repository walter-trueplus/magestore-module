# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExportModelData(models.Model):
    _name = "checking_model"

    ir_model = fields.Many2one('ir.model')

    def export_data(self):
        print "enter here"
        print "----------"
        res = self.env['ir.model'].search([('model', '=', self.ir_model.model)], limit=1)
        if res:
            for item in res.field_id:
                if item.name == "name":
                    product_ids = self.env[self.ir_model.model].search([])
                    for product_item in product_ids:
                        print product_item.name


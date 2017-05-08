# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExportModelData(models.Model):
    _name = "checking_model"

    ir_model = fields.Many2one('ir.model')

    @api.multi
    def export_data(self):
        print "enter here"
        print "----------"
        res = self.env['ir.model'].search([])
        for item in res:
            print item.name
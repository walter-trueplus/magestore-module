# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ExportModelData(models.Model):
    _name = "checking_model"

    ir_model = fields.Many2one('ir.model')
    model_fields = fields.Many2many('ir.model.fields')

    @api.multi
    @api.onchange('ir_model')
    def _compute_model(self):
        self.model_fields = self.env['ir.model.fields'].search([('model', '=', self.ir_model.model)])

    def export_data(self):
        print "enter here"
        print "----------"
        f = open("/Users/pwnux90/Desktop/output.txt", "a+")
        for item in self.model_fields:
            f.write(str(item) + " ")
        f.write("\n")
        data = self.env[str(self.ir_model.model)].search([])
        if data:
            for item_data in data:
                for item in self.model_fields:
                    f.write(str(item_data.item) + " ")
                print "\n"
            f.close()


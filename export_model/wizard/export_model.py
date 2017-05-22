# -*- encoding: utf-8 -*-
import base64
import cStringIO
import contextlib
import unicodecsv as csv

from odoo import api, fields, models


class ExportModel(models.TransientModel):
    _name = 'export.module'

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)
    ir_model = fields.Many2one('ir.model')
    model_fields = fields.Many2many('ir.model.fields', compute='_check_model')
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')

    @api.multi
    @api.onchange('ir_model')
    def _compute_model(self):
        self.model_fields = self.env['ir.model.fields'].search([('model', '=', self.ir_model.model)])

    @api.multi
    def _check_model(self):
        if self.ir_model:
            self.model_fields = None


    @api.multi
    def do_export2(self):
        if self.ir_model:
            limit = ['many2one', 'many2many', 'one2many']
            lst_name = []
            with contextlib.closing(cStringIO.StringIO()) as buf:
                writer = csv.writer(buf, delimiter=";", encoding="utf-8")
                for f in self.model_fields:
                    lst_name.append(f.name)
                writer.writerow((lst_name))
                lst_object = self.env[self.ir_model.model].search([])
                for object in lst_object:
                    line = []
                    for field in self.model_fields:
                        if field.ttype not in limit:
                            for temp in object.mapped(field.name):
                                line.append(temp)
                        else:
                            line.append('')
                    writer.writerow((line))
                out = base64.encodestring(buf.getvalue())
            self.write({
                'state': 'get',
                'data': out,
                'name': 'data.csv'
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.module',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

# -*- coding: utf-8 -*-
import base64
import cStringIO
import contextlib
import csv


from odoo import api, fields, models


class ExportEmployee(models.TransientModel):
    _name = 'export.employee.wizard'

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)
    employee_id = fields.Many2many('hr.employee', string="Employee", required=True)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')

    @api.multi
    def do_export2(self):
        if self.employee_id:
            with contextlib.closing(cStringIO.StringIO()) as buf:
                writer = csv.writer(buf, delimiter=":", quotechar='"')
                for employee in self.employee_id:
                    items = self.env['hr.employee'].search([('id', '=', employee.id)], limit=1)
                    for item in items:
                        writer.writerow(("BEGIN", "VCARD"))
                        writer.writerow(("VERSION", "3.0"))
                        writer.writerow(("N", item.name.encode('utf8') if item.name else ''))
                        writer.writerow(("FN", item.name.encode('utf8') if item.name else ''))
                        writer.writerow(("TEL;TYPE=CELL", item.mobile_phone if item.mobile_phone else ''))
                        writer.writerow(("TEL;TYPE=WORK", item.work_phone if item.work_phone else ''))
                        writer.writerow(("EMAIL;TYPE=WORK", item.work_email if item.work_email else ''))
                        writer.writerow(("ORG;CHARSET=UTF-8", item.parent_id.name.encode('utf8') if item.parent_id.name else ''))
                        writer.writerow(("TITLE", item.job_id.name.encode('utf8') if item.job_id.name else ''))
                        writer.writerow(("END", "VCARD"))

                out = base64.encodestring(buf.getvalue())
            self.write({
                'state': 'get',
                'data': out,
                'name': 'contact_info.vcf'
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.employee.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

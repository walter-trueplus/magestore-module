 # -*- coding: utf-8 -*-
import base64
import cStringIO
import contextlib
import csv


from odoo import api, fields, models


class ExportContact(models.TransientModel):
    _name = 'export.contact.wizard'

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)
    contact_id = fields.Many2many('res.partner', string="Contact", required=True)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')

    @api.multi
    def do_export2(self):
        if self.contact_id:
            with contextlib.closing(cStringIO.StringIO()) as buf:
                writer = csv.writer(buf, delimiter=":", quotechar='"')
                for contact in self.contact_id:
                    item = self.env['res.partner'].search([('id', '=', contact.id)], limit=1)
                    writer.writerow(("BEGIN", "VCARD"))
                    writer.writerow(("VERSION", "3.0"))
                    writer.writerow(("N", item.name.encode('utf8') if item.name else ''))
                    writer.writerow(("FN", item.name.encode('utf8') if item.name else ''))
                    writer.writerow(("TEL;TYPE=CELL", item.phone if item.phone else ''))
                    writer.writerow(("TEL;TYPE=WORK", item.mobile.encode('utf8') if item.mobile else ''))
                    writer.writerow(("EMAIL;TYPE=WORK", item.email if item.email else ''))
                    writer.writerow(("ORG;CHARSET=UTF-8", item.parent_id.name.encode('utf8') if item.parent_id.name else ''))
                    writer.writerow(("TITLE", item.title.name if item.title.name else ''))
                    writer.writerow(("END", "VCARD"))

                out = base64.encodestring(buf.getvalue())
            self.write({
                'state': 'get',
                'data': out,
                'name': 'contact_info.vcf'
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.contact.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

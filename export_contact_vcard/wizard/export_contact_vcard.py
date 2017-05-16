# -*- coding: utf-8 -*-
import base64
import cStringIO
import contextlib
import csv

from odoo import api, fields, models


# class ExportContact(models.TransientModel):
#     _name = 'export.contact.wizard'
#
#     name = fields.Char(string="File Name", readonly=True)
#     data = fields.Binary(string="File", readonly=True)
#
#     @api.multi
#     def do_export2(self, id):
#         if id:
#             print self.id
#             print id
#             with contextlib.closing(cStringIO.StringIO()) as buf:
#                 writer = csv.writer(buf, delimiter=":", quotechar='"')
#                 for item in self.env['res.partner'].search([('id', '=', id)], limit=1):
#                     print item
#                     writer.writerow(("BEGIN", "VCARD"))
#                     writer.writerow(("VERSION", "3.0"))
#                     writer.writerow(("END", "VCARD"))
#
#                 out = base64.encodestring(buf.getvalue())
#             self.create({
#                 'state': 'get',
#                 'data': out,
#                 'name': 'contact_info.vcf'
#             })
#         # compose_form = self.env.ref('export_contact_vcard.wizard_export_contact')
#         # res = {
#         #     'type': 'ir.actions.act_window',
#         #     # 'name': _('Customer Invoice'),
#         #     'res_model': 'export.contact.wizard',
#         #     'view_type': 'form',
#         #     'view_mode': 'form',
#         #     'res_id': self.id,
#         #     'views': [(compose_form.id, 'form')],
#         #     'view_id': compose_form.id,
#         #     'target': 'current',
#         #     # 'context': {'default_partner_id': client_id}
#         # }
#
#         compose_form = self.env.ref('export_contact_vcard.wizard_export_contact')
#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'export.contact.wizard',
#             'view_mode': 'form',
#             'view_type': 'form',
#             'views': [(compose_form.id, 'form')],
#             'view_id': compose_form.id,
#             'target': 'new',
#         }


class DownloadContact(models.Model):
    # _name = 'export.contact.wizard'
    _inherit = 'res.partner'

    data = fields.Binary(string="File", readonly=True)

    @api.multi
    def download(self):
        # id = self.id
        # print self.name
        # other_object = self.env['export.contact.wizard']
        # other_object.do_export2(id)
        # print self.id
        if self.id:
            with contextlib.closing(cStringIO.StringIO()) as buf:
                writer = csv.writer(buf, delimiter=":", quotechar='"')
                writer.writerow(("BEGIN", "VCARD"))
                writer.writerow(("VERSION", "3.0"))
                writer.writerow(("N", self.name.encode('utf8') if self.name else ''))
                writer.writerow(("FN", self.name.encode('utf8') if self.name else ''))
                writer.writerow(("TEL;TYPE=CELL", self.phone if self.phone else ''))
                writer.writerow(("TEL;TYPE=WORK", self.mobile.encode('utf8') if self.mobile else ''))
                writer.writerow(("EMAIL;TYPE=WORK", self.email if self.email else ''))
                writer.writerow(
                    ("ORG;CHARSET=UTF-8", self.parent_id.name.encode('utf8') if self.parent_id.name else ''))
                writer.writerow(("TITLE", self.title.name if self.title.name else ''))
                writer.writerow(("END", "VCARD"))

                out = base64.encodestring(buf.getvalue())
            self.write({
                'data': out,
                'name': 'contact_info.vcf'
            })
        compose_form = self.env.ref('export_contact_vcard.wizard_export_contact')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
        }

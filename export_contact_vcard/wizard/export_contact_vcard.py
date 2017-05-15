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

    @api.multi
    def do_export2(self, id):
        if id:
            with contextlib.closing(cStringIO.StringIO()) as buf:
                writer = csv.writer(buf, delimiter=":", quotechar='"')
                for item in self.env['res.partner'].search([('id', '=', id)], limit=1):
                    print item
                    writer.writerow(("BEGIN", "VCARD"))
                    writer.writerow(("VERSION", "3.0"))
                    writer.writerow(("END", "VCARD"))

                out = base64.encodestring(buf.getvalue())
            self.write({
                'state': 'get',
                'data': out,
                'name': 'contact_info.vcf'
            })
        compose_form = self.env.ref('export_contact_vcard.wizard_export_contact')
        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'export.contact.wizard',
        #     'view_mode': 'form',
        #     'view_type': 'form',
        #     'views': [(compose_form.id, 'form')],
        #     'view_id': compose_form.id,
        #     'target': 'new',
        # }


class DownloadContact(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def download(self):
        # print self.name
        # other_object = self.env['export.contact.wizard']
        # other_object.do_export2(self.id)
        # print self.id
        compose_form = self.env.ref('export_contact_vcard.wizard_export_contact')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.contact.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
        }
# -*- coding: utf-8 -*-
import base64
import cStringIO
import contextlib
import csv

from odoo import api, fields, models


class ExportContact(models.Model):
    _name = 'export.contact.wizard'

    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True, compute='download')


    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     context = self._context
    #     partner_id = context.get('params').get('id')
    #     partner_obj = self.env['res.partner'].browse(partner_id)
    #     with contextlib.closing(cStringIO.StringIO()) as buf:
    #         writer = csv.writer(buf, delimiter=":", quotechar='"')
    #         writer.writerow(("BEGIN", "VCARD"))
    #         # writer.writerow(("VERSION", "3.0"))
    #         # writer.writerow(("N", self.name.encode('utf8') if self.name else ''))
    #         # writer.writerow(("FN", self.name.encode('utf8') if self.name else ''))
    #         # writer.writerow(("TEL;TYPE=CELL", self.phone if self.phone else ''))
    #         # writer.writerow(("TEL;TYPE=WORK", self.mobile if self.mobile else ''))
    #         # writer.writerow(("EMAIL;TYPE=WORK", self.email if self.email else ''))
    #         # writer.writerow(
    #         #     ("ORG;CHARSET=UTF-8", self.parent_id.name.encode('utf8') if self.parent_id.name else ''))
    #         # writer.writerow(("TITLE", self.title.name if self.title.name else ''))
    #         # writer.writerow(("END", "VCARD"))
    #
    #         out = base64.encodestring(buf.getvalue())
    #     self.create({
    #         'data': out,
    #         'name': 'contact_info.vcf'
    #     })


    # @api.multi
    # def download(self):
    #     context = self._context
    #     partner_id = context.get('params').get('id')
    #     partner_obj = self.env['res.partner'].browse(partner_id)
    #     with contextlib.closing(cStringIO.StringIO()) as buf:
    #         writer = csv.writer(buf, delimiter=":", quotechar='"')
    #         writer.writerow(("BEGIN", "VCARD"))
    #         # writer.writerow(("VERSION", "3.0"))
    #         # writer.writerow(("N", self.name.encode('utf8') if self.name else ''))
    #         # writer.writerow(("FN", self.name.encode('utf8') if self.name else ''))
    #         # writer.writerow(("TEL;TYPE=CELL", self.phone if self.phone else ''))
    #         # writer.writerow(("TEL;TYPE=WORK", self.mobile if self.mobile else ''))
    #         # writer.writerow(("EMAIL;TYPE=WORK", self.email if self.email else ''))
    #         # writer.writerow(
    #         #     ("ORG;CHARSET=UTF-8", self.parent_id.name.encode('utf8') if self.parent_id.name else ''))
    #         # writer.writerow(("TITLE", self.title.name if self.title.name else ''))
    #         # writer.writerow(("END", "VCARD"))
    #
    #         out = base64.encodestring(buf.getvalue())
    #     self.write({
    #         'data': out,
    #         'name': 'contact_info.vcf'
    #     })
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'export.contact.wizard',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'res_id': self.id,
    #         'views': [(False, 'form')],
    #         'target': 'new',
    #     }


class DownloadContact(models.Model):
    _inherit = 'res.partner'
    name = fields.Char(string="File Name", readonly=True)
    data = fields.Binary(string="File", readonly=True)

    @api.multi
    def download(self):
        with contextlib.closing(cStringIO.StringIO()) as buf:
            writer = csv.writer(buf, delimiter=":", quotechar='"')
            writer.writerow(("BEGIN", "VCARD"))
            # writer.writerow(("VERSION", "3.0"))
            # writer.writerow(("N", self.name.encode('utf8') if self.name else ''))
            # writer.writerow(("FN", self.name.encode('utf8') if self.name else ''))
            # writer.writerow(("TEL;TYPE=CELL", self.phone if self.phone else ''))
            # writer.writerow(("TEL;TYPE=WORK", self.mobile if self.mobile else ''))
            # writer.writerow(("EMAIL;TYPE=WORK", self.email if self.email else ''))
            # writer.writerow(
            #     ("ORG;CHARSET=UTF-8", self.parent_id.name.encode('utf8') if self.parent_id.name else ''))
            # writer.writerow(("TITLE", self.title.name if self.title.name else ''))
            # writer.writerow(("END", "VCARD"))

            out = base64.encodestring(buf.getvalue())
        self.write({
            'data': out,
            'name': 'contact_info.vcf'
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.contact.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': 205,
            'views': [(False, 'form')],
            'target': 'new',
        }
        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': '/web/binary/download_document?model=res.partner&field=datas&id=%s&filename=contact_info.vcf' % (
        #         self.id),
        #     'target': 'self',
        # }
        #
        # @api.multi
        # def download(self):
        #     action = self.env['ir.actions.act_window'].with_context(partner_id=self.id).for_xml_id('export_contact_vcard', 'action_wizard_export_contact')
        #     return action

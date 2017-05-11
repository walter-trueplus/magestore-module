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


class DownloadContact(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def download(self):
        print self.name
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

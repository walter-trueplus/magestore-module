# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FetchMail(models.Model):
    _name = "mail.fetched"
    _description = "Fetched Mail"
    _inherit = "mail.thread"
    _order = "create_date"

    name = fields.Char('Mail Name')
    sender_email = fields.Char(
        string="Sender Email", compute="get_sender_email")

    @api.one
    def get_sender_email(self):
        if self.message_ids:
            self.sender_email = self.message_ids[0].email_from

    @api.one
    def get_body_email(self):
        if self.message_ids:
            self.body = self.message_ids[0].body

    def run_fetch_mail(self):
        self.env['ir.cron'].search(
            [('name', '=', 'Fetchmail Service')], limit=1).method_direct_trigger()


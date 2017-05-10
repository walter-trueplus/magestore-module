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


class MailCron(models.Model):
    _name = "cron.fetch"

    name = fields.Char(string="Fetch Mail")

    @api.multi
    def run_fetch_mail(self):
        self.env['ir.cron'].search(
            [('name', '=', 'Fetchmail Service')], limit=1).method_direct_trigger()


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    # ================================
    # ================================
    # ================================
    # We have two methods to create new record:
    # + use record in xml file
    # + use function tag in xml file and call to method of model
    # ================================
    # ================================
    # ================================

    @api.model
    def change_smtp_local_server(self):
        vals = {
            'name': 'Outgoing Gmail Server',
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 465,
            'smtp_encryption': 'ssl',
            'smtp_user': 'mars@trueplus.vn',
            'smtp_pass': 'marsorxmars'
        }
        local_server = self.search([('id', '=', 1)])
        if local_server:
            local_server.write(vals)
        else:
            self.create(vals)


class MailAlias(models.Model):
    _inherit = 'mail.alias'

    def get_fetch_mail_model_id(self):
        return 1

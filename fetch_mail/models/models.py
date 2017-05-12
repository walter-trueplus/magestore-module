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

    def reload_page(self):
        # self.ensure_one()
        # model_obj = self.env['ir.model.data']
        # data_id = model_obj._get_id('mail_fetched', 'view_fetch_mail_tree')
        # view_id = model_obj.browse(data_id).res_id
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'String',
        #     'tag': 'reload',
        #     'res_model': 'mail.fetched',
        #     'view_type': 'tree',
        #     'view_mode': 'form',
        #     'view_id': view_id,
        #     'target': 'current',
        #     'nodestroy': True,
        # }
        print 'oh yeeeeaaa'
        # return {'type': 'ir.actions.client', 'tag': 'reload'}
        self.env['cron.fetch'].run_fetch_mail()

class MailCron(models.Model):
    _name = "cron.fetch"

    name = fields.Char(string="Fetch Mail")

    @api.multi
    def run_fetch_mail(self):
        self.env['ir.cron'].search(
            [('name', '=', 'Fetchmail Service')], limit=1).method_direct_trigger()
        print "abc vao day de"
        return "dm co vao day khong"


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


class BaseSettings(models.TransientModel):
    _inherit = "base.config.settings"

    @api.model
    def set_domain_trueplus(self):
        IrConfigParam = self.env['ir.config_parameter']
        IrConfigParam.set_param('mail.catchall.domain', 'trueplus.vn')



class MailAlias(models.Model):
    _inherit = 'mail.alias'

    @api.model
    def create_mail_alias(self):
        alias_model_id = self.env['ir.model'].search([('model', '=', 'mail.fetched')])
        vals = {
            'alias_name': 'mars+fetch+mail',
            'alias_model_id': alias_model_id.id
        }
        self.create(vals)

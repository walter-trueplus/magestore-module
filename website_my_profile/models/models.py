# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = "res.partner"

    birthday = fields.Date(string='Birthday')
    # gender_id = fields.Many2one(
    #     'hr.employee.gender', string='Gender')
    gender = fields.Selection(
        [('Male', 'Male'), ('Female', 'Female'), ('Unknow', 'Unknow')],
        string='Gender')

    def get_value_gender(self):
        return ['Male', 'Female', 'Unknow']


class Gender(models.Model):
    _name = 'hr.employee.gender'

    name = fields.Char('Gender of The Employee')
    gender = fields.Char(string="Gender", default="Male")


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
    def change_smtp_server(self):
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
    def enable_reset_password_signup(self):
        IrConfigParam = self.env['ir.config_parameter']
        # we store the repr of the values, since the value of the parameter is a required string
        IrConfigParam.set_param('auth_signup.reset_password', True)
        IrConfigParam.set_param('auth_signup.allow_uninvited', True)
        IrConfigParam.set_param('auth_signup.template_user_id', 6)
        IrConfigParam.set_param('mail.catchall.domain', 'trueplus.vn')


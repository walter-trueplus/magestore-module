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
    def set_domain_and_enable_reset_signup(self):
        IrConfigParam = self.env['ir.config_parameter']
        template_user_id = self.env['res.users'].search([('active', '=', False), ('login', '=', 'portaltemplate')]).id
        if not template_user_id:
            template_user_id = 1
        IrConfigParam.set_param('mail.catchall.domain', 'trueplus.vn')
        IrConfigParam.set_param('auth_signup.reset_password', 'True')
        IrConfigParam.set_param('auth_signup.allow_uninvited', 'True')
        IrConfigParam.set_param('auth_signup.template_user_id', template_user_id)


class User(models.Model):
    _inherit = ['res.users']

    employee_id = fields.Many2one('hr.employee')

    @api.model
    def change_user_redirect_website_homepage(self):
        action_id = self.env['ir.actions.actions'].search([('name', '=', 'Website Homepage')])[0].id
        users_not_homepage = self.env['res.users'].search(['|',
                                                           ('active', '=', False),
                                                           '|',
                                                           ('action_id', '!=', action_id),
                                                           ('action_id', '=', None)])
        for user in users_not_homepage:
            user.write({'action_id': action_id})

    @api.model
    def create(self, vals):
        # create user
        new_user = super(User, self).create(vals)
        if new_user:
            user = self.search([('id', '=', new_user.id)])[0]
            action_id = self.env['ir.actions.actions'].search([('name', '=', 'Website Homepage')])[0].id
            user.write({'action_id': action_id})
        return user

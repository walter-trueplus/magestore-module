# -*- coding: utf-8 -*-
from odoo import fields, models, api
import sys
from datetime import datetime


class MyProfile(models.Model):
    _name = 'er.myprofile'
    _description = 'User profile page in kudos module'

    name = fields.Many2one('hr.employee', default=lambda self: self.env.user.id)
    avatar = fields.Html(string='User Avatar', compute='_compute_information_user')
    department = fields.Char(string='User Department', compute='_compute_information_user')
    team = fields.Char(string='Team member', compute='_compute_information_user')
    balance_point = fields.Integer(string='Point to give', compute='_compute_information_user')
    receive_point = fields.Integer(string='Point received', compute='_compute_information_user')
    all_time_point = fields.Integer(string='Point all time', compute='_compute_information_user')

    @api.depends('name')
    def _compute_information_user(self):
        # User Avatar
        self.avatar = '<img src="/web/image?model=hr.employee&amp;field=image_medium&amp;id=' + str(self.env.user.id)

        # User other information
        tmp_user = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
        if tmp_user:
            if not tmp_user.department_id.id:
                print str(datetime.now()) + ' INFO department is not existed.'
            else:
                # Department
                tmp_department = self.env['hr.department'].search([('id', '=', tmp_user.department_id.id)], limit=1)
                self.department = tmp_department.name

                # Team member
                tmp_member = self.env['hr.job'].search([('id', '=', tmp_user.job_id.id)], limit=1)
                self.team = tmp_member.name

                # Balance point
                self.balance_point = tmp_user.usr_balance_point

                # Receive point
                self.receive_point = tmp_user.usr_receive_point

                # All time receive point
                self.all_time_point = tmp_user.usr_point_all_time
        else:
            print str(datetime.now()) + ' _compute_deparment_user have a bug.'

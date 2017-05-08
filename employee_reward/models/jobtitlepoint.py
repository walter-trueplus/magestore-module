# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from datetime import datetime
import sys


class Jobtitlepoint(models.Model):
    _name = "er.point"
    _description = "Point base for employee reward"

    monthly_point = fields.Integer(string="Point allocation for month")
    job_id = fields.Many2one('hr.job', string="Job title")
    user_count = fields.Integer(compute='_compute_users', store=True)
    active = fields.Boolean('Active', default=True)

    @api.depends('job_id')
    def _compute_users(self):
        tmp_id = self.env['hr.employee'].search([('job_id', '=', self.job_id.id)])
        user_list = []
        for item in tmp_id:
            user_list.append(item.id)
        count_ = len(user_list)
        # print count_
        self.user_count = count_

    @api.model
    def create(self, vals):
        res = super(Jobtitlepoint, self).create(vals)
        for res_elm in res:
            user_point = self.env['hr.employee'].search([('job_id', '=', res_elm.job_id.id)])
            for record in user_point:
                record.usr_reset_point = res_elm.monthly_point
                record.usr_balance_point = res_elm.monthly_point
        return res

    @api.multi
    def write(self, vals):
        res = super(Jobtitlepoint, self).create(vals)
        for res_elm in res:
            user_point = self.env['hr.employee'].search([('job_id', '=', res_elm.job_id.id)])
            for record in user_point:
                record.usr_reset_point = res_elm.monthly_point
                record.usr_balance_point = res_elm.monthly_point
        return res

    @api.multi
    def monthly_reset(self):
        user_point = self.env['hr.employee'].search([('job_id', '=', self.job_id.id)])
        for record in user_point:
            record.usr_reset_point = self.monthly_point
            record.usr_balance_point = self.monthly_point
            record.usr_receive_point = 0
            record.usr_sent_point = 0
            record.usr_redeem_point = 0

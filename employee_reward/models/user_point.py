# -*- coding: utf-8 -*-

from odoo import models, fields, api
import sys
from datetime import datetime
from datetime import datetime


class UserPoint(models.Model):
    _inherit = "hr.employee"

    usr_reset_point = fields.Integer(default=0, string='Monthly point', store=True)
    usr_balance_point = fields.Integer(default=0, string='Balance point of users', store=True)
    usr_receive_point = fields.Integer(default=10, string="Received point of users", store=True)
    usr_redeem_point = fields.Integer(default=0, string="Redeemed point of users", store=True)
    usr_sent_point = fields.Integer(default=0, string="Sent point of users", store=True)
    usr_point_all_time = fields.Integer(default=0, string="All received point", store=True)

    @api.model
    def create(self, vals):
        res = super(UserPoint, self).create(vals)
        for rec_user in res:
            user_job = self.env['er.point'].search([('job_id', '=', rec_user.job_id.id)], limit=1)
            print user_job.monthly_point
            for rec_user_job in user_job:
                values = {
                    'usr_reset_point': rec_user_job.monthly_point,
                    'usr_balance_point': rec_user_job.monthly_point,
                    'job_id': rec_user_job.job_id.id
                }
                rec_user.write(values)
        return res

    @api.multi
    def write(self, vals):
        user_job = self.env['er.point'].search([('job_id', '=', vals.get('job_id'))], limit=1)
        if user_job:
            vals.update({
                'usr_reset_point': user_job.monthly_point,
                'usr_balance_point': user_job.monthly_point,
            })
        return super(UserPoint, self).write(vals)

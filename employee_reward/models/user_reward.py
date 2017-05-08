# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class user_reward(models.Model):
    _inherit = "er.reward"
    _description = "Using only for user reward"

    reward_status = fields.Integer(compute="_compute_reward_status")
    reward_missing_point = fields.Integer(compute="_compute_reward_status")

    @api.multi
    def action_redeem_reward(self):
        flag_error = False
        for item in self:
            user_login = self.env['hr.employee'].search([('user_id', '=', self.env.user.login)])
            for items in user_login:
                if items.usr_receive_point < item.point or items.usr_receive_point <= 0:
                    print "Cannot redeem."
                    flag_error = False
                else:
                    # item.number_available -= 1
                    # items.usr_redeem_point += item.point
                    print 'action_redeem_reward - enter here'
                    redeem_reward = item.name
                    requested_time = datetime.now()
                    self.env['er.reward.history'].create(
                        {'name': redeem_reward, 'history_reward_point': item.point,
                         'history_requested_date': requested_time, 'history_user': user_login.name})

                    self.env['er.user.history'].create({'name': redeem_reward, 'user_user': user_login.name,
                                                        'user_requested_date': requested_time})
                    tmp = self.env['hr.employee'].search([('name', '=', user_login.name)], limit=1)
                    tmp.usr_receive_point -= item.point
                    # print "creating for user history done."
                    flag_error = True

        if not flag_error:
            return {
                'warning': {
                    'title': "Insufficient points",
                    'message': "Cannot redeem.",
                }
            }
        else:
            return {
                'warning': {
                    'title': "Good points",
                    'message': "Redeem completed.",
                }
            }

    @api.multi
    def _compute_reward_status(self):
        for item in self:
            user_login = self.env['hr.employee'].search([('user_id', '=', self.env.user.login)])
            for user_ in user_login:
                print 'User login id: ' + str(self.env.user.login)
                print 'User receive point: ' + str(user_.usr_receive_point)
                # item.reward_missing_point = item.point - user_.usr_receive_point
                if item.point <= user_.usr_receive_point:
                    item.reward_status = 2
                if item.point > user_.usr_receive_point:
                    item.reward_missing_point = item.point - user_.usr_receive_point
                    item.reward_status = 1
                    print 'Missing point: ' + str(item.reward_missing_point)

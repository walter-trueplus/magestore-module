# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import sys


class redeem_management(models.Model):
    _name = "er.reward.history"
    _description = "Redeem management for administrator"

    name = fields.Char()
    history_reward_point = fields.Integer()
    history_user = fields.Char()
    history_requested_date = fields.Datetime()
    history_completed_date = fields.Datetime()
    history_status = fields.Char()

    def get_user(self):
        redeem_employee = self.env['er.user.history'].search([('user_user', '=', self.history_user)], limit=1)
        tmp = self.env['hr.employee'].search([('name', '=', redeem_employee.user_user)], limit=1)
        redeem_user = self.env['res.users'].search([('user_ids', '=', tmp.user_id.id)], limit=1)
        return redeem_user.partner_id.id

    @api.multi
    def set_approved(self):
        for elm in self:
            elm.history_status = 'approved'
            elm.history_completed_date = datetime.now()
            tmp_user = self.env['er.user.history'].search([('user_user', '=', elm.history_user)], limit=1)
            for item_tmp_user in tmp_user:
                print elm.history_status
                # sys.exit()
                item_tmp_user.user_reward_status = elm.history_status
                item_tmp_user.user_completed_date = elm.history_completed_date
                # point processing
                tmp_user = self.env['hr.employee'].search([('name', '=', elm.history_user)])
                tmp_user.usr_redeem_point += elm.history_reward_point
                # tmp_user.usr_receive_point -= elm.history_reward_point
                tmp_reward = self.env['er.reward'].search([('name', '=', elm.name)])
                tmp_reward.number_available -= 1

            recipients = []
            recipients.append(elm.get_user())

            post_message = {
                'partner_ids': recipients,
                'message_type': 'notification',
                'body': elm.name + ' request approved',
                'subtype': 'mail.mt_comment'
            }
            self.env['mail.thread'].message_post(**post_message)

    def set_denied(self):
        print 'starting denied.'
        self.history_status = 'denied'
        tmp_user = self.env['er.user.history'].search([('user_user', '=', self.history_user)])
        for item_tmp_user in tmp_user:
            item_tmp_user.user_reward_status = self.history_status
            item_tmp_user.user_completed_date = self.history_completed_date

    @api.multi
    def unlink(self):
        for item in self:
            user_history = self.env['er.user.history'].search([('user_user', '=', item.history_user)])
            print user_history
            user_history.unlink()
        return super(redeem_management, self).unlink()

# -*- coding: utf-8 -*-
from odoo import api, fields, models


class user_reward_history(models.Model):
    _name = 'er.user.history'
    _description = 'User reward history'

    name = fields.Char()
    user_user = fields.Char()
    user_requested_date = fields.Datetime()
    user_completed_date = fields.Datetime()
    user_reward_status = fields.Char(default='pending')

# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Quality(models.Model):
    _name = "er.quality"

    name = fields.Char(string="Quality Name", required=True, translate=True)
    title = fields.Char(string="Quality Title", required=True, translate=True)
    statement = fields.Text(string="Quality Statement", required=True, translate=True)
    partner_id = fields.Many2one('res.partner','Customer', default=lambda self: self.env.user.partner_id)
    active = fields.Boolean('Active', default=True)

# -*- coding: utf-8 -*-

from odoo import osv, fields, models


class res_partner(models.Model):

    _name = 'res.partner'
    _inherit = 'res.partner'

    lat = fields.Float(u'Latitude', digits=(9, 6)),
    lng = fields.Float(u'Longitude', digits=(9, 6)),
    # map = fields.Binary()
        
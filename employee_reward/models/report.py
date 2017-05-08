# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from datetime import datetime
from odoo.tools.sql import drop_view_if_exists

from odoo import models, fields, api


class TopSendPoint(models.Model):
    _inherit = "hr.employee"

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        context = self._context
        res = super(TopSendPoint, self).read(fields=fields, load=load)

        if context.get('search_top_receive', False):
            print 'R'
            lst = sorted(res, key=lambda x: x['usr_receive_point'], reverse=True)[0:5]
        elif context.get('search_top_send', False):
            print 'S'
            lst = sorted(res, key=lambda x: x['usr_sent_point'], reverse=True)[0:5]
        else:
            lst = res

        return lst

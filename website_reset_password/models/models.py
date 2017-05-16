# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api, exceptions, _

class ResetDirectError(Exception):
    pass

class ChangeMailError(Exception):
    pass

class ResUser(models.Model):
    _inherit = 'res.users'

    @api.constrains('login')
    def _check_login_valid_mail(self):
        for user in self:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", user.login):
                raise exceptions.ValidationError(
                    _("Invalid email address"))

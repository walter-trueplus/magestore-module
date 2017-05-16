# -*- coding: utf-8 -*-
import logging
import re
import werkzeug

from odoo import http, _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website_reset_password.models.models import ResetDirectError
from odoo.addons.web.controllers.main import Home
from odoo.exceptions import AccessDenied
from odoo.http import request


class PasswordSignup(Home):
    @http.route('/web/reset_password_direct', type='http', auth='public', website=True)
    def reset_password_direct(self, *args, **kw):
        qcontext = request.params.copy()
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_reset_password_direct(qcontext)
                qcontext['message'] = 'Changed password successful!'
            except ResetDirectError,AccessDenied:
                qcontext['error'] = qcontext.get('error_detail')
            except Exception:
                qcontext['error'] = 'Old password does not match'
        return request.render('website_reset_password.form_reset', qcontext)

    def do_reset_password_direct(self, qcontext):
        values = {key: qcontext.get(key) for key in ('login', 'old_password', 'new_password', 'retype_password')}
        if values.get('new_password') != values.get('retype_password'):
            qcontext['error_detail'] = 'Passwords do not match, please retype them.'
            raise ResetDirectError

        # if old password not correct, this will raise an Exception and close cr (cursor)
        #  and you can't not raise next of code below this line
        request.env['res.users'].change_password(values.get('old_password'), values.get('new_password'))

        # can't raise if old password not corrects
        print "can't run"
        print "run, not run , yesss"
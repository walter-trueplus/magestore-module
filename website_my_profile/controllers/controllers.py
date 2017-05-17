# -*- coding: utf-8 -*-
import logging
import re
import werkzeug

from odoo import http, _
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.http import request

_logger = logging.getLogger(__name__)


class MyProfile(website_account):
    @http.route()
    def details(self, redirect=None, **post):
        result = super(MyProfile, self).details(redirect, **post)
        self.MANDATORY_BILLING_FIELDS.extend(['birthday','login'])
        self.OPTIONAL_BILLING_FIELDS.extend(['active', 'gender'])
        # all value put in render function will becomes value of qcontext
        # see odoo.addons.website_portal.controllers.main in details function
        # values variable (type: dictionary) to be puted to render function
        # and all of that will be values of qcontext - awesome
        genders = request.env['res.partner'].get_value_gender()
        qcontext = result.qcontext
        qcontext['genders'] = genders
        qcontext['login'] = request.env['res.users'].sudo().search([('id', '=', request.session.uid)]).login
        return result


class PasswordSignup(AuthSignupHome):
    @http.route()
    def web_auth_signup(self, *args, **kw):
        res = super(PasswordSignup, self).web_auth_signup(*args, **kw)
        qcontext = res.qcontext
        if request.session.uid:
            return request.redirect('/')
        if qcontext.get('error_detail'):
            qcontext['error'] = qcontext['error_detail']
        return res

    def do_signup(self, qcontext):
        values = {key: qcontext.get(key) for key in (
            'login', 'name', 'birthday', 'password')}
        # user is internal user if share = FALSE
        user = request.env['res.users'].sudo().search([('login', '=', values.get('login'))])
        # if request has login value (user loged in or reset password with token)
        # don't check login
        if not user:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", values.get('login')):
                qcontext['error_detail'] = 'Your email is invalid'
                raise AssertionError

        if not values.values():
            qcontext['error_detail'] = 'The form was not properly filled in.'
            raise AssertionError
        if not values.get('password') == qcontext.get('confirm_password'):
            qcontext['error_detail'] = 'Passwords do not match; please retype them.'
            raise AssertionError

        supported_langs = [lang['code'] for lang in request.env[
            'res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang

        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

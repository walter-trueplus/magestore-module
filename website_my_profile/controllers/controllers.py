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
        self.MANDATORY_BILLING_FIELDS.append('birthday')
        self.OPTIONAL_BILLING_FIELDS.extend(['active', 'gender'])
        # all value put in render function will becomes value of qcontext
        # see odoo.addons.website_portal.controllers.main in details function
        # values variable (type: dictionary) to be puted to render function
        # and all of that will be values of qcontext - awesome
        genders = request.env['res.partner'].get_value_gender()
        qcontext = result.qcontext
        qcontext['genders'] = genders
        return result


class PasswordSignup(AuthSignupHome):

    @http.route()
    def web_auth_signup(self, *args, **kw):
        res = super(PasswordSignup, self).web_auth_signup(*args, **kw)
        qcontext = res.qcontext
        if qcontext.get('error_detail'):
            qcontext['error'] = qcontext['error_detail']
        return res

    def do_signup(self, qcontext):
        values = {key: qcontext.get(key) for key in (
            'login', 'name', 'birthday', 'password')}
            # user is internal user if share = FALSE
        user = request.env['res.users'].search([('login', '=', values.get('login'))], limit=1)
        is_external = False
        if user:
            is_external = user.share
        if not re.match(r"[^@]+@[^@]+\.[^@]+", values.get('login')) and is_external:
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

    # def do_reset_password_direct(self, qcontext):
    #     values = {key: qcontext.get(key) for key in (
    #         'login', 'old_password', 'password')}
    #
    #     if not values.values():
    #         qcontext['error_detail'] = 'The form was not properly filled in.'
    #         raise SignupError
    #
    #     if not values.get('password') == qcontext.get('confirm_password'):
    #         qcontext[
    #             'error_detail'] = 'New passwords do not match; please retype them.'
    #         raise SignupError
    #
    #     db = request.session.db
    #     old_password = values.get('old_password')
    #     new_password = values.get('new_password')
    #     login = values.get('login')
    #     uid = request.session.authenticate(db, login, password)
    #     g = request.env['res.users'].change_password(old_password, new_password)
    #     if not request.env['res.users'].change_password(old_password, new_password):
    #         qcontext['error_detail'] = "Old password doesn't correct."
    #         raise SignupError


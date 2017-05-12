# -*- coding: utf-8 -*-
import logging

from odoo import http
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request

_logger = logging.getLogger(__name__)


class MyProfile(website_account):
    @http.route()
    def details(self, redirect=None, **post):
        result = super(MyProfile, self).details(redirect, **post)
        self.MANDATORY_BILLING_FIELDS.append('birthday')
        self.OPTIONAL_BILLING_FIELDS.extend(['active', 'gender'])
        genders = request.env['res.partner'].get_value_gender()
        # all value put in render function will becomes value of qcontext
        # see odoo.addons.website_portal.controllers.main in details function
        # values variable (type: dictionary) to be puted to render function
        # and all of that will be values of qcontext - awesome
        qcontext = result.qcontext
        qcontext['genders'] = genders
        return result


class ResetPassword(AuthSignupHome):
    KEY_QCONTEXT = ['login', 'name', 'birthday', 'password']

    @http.route()
    def web_auth_reset_password(self, *args, **kw):
        result = super(ResetPassword, self).web_auth_reset_password(
            *args, **kw)
        qcontext = result.qcontext
        # get parameter in url
        if 'error' not in qcontext and 'reset_directly' in request.httprequest.query_string and qcontext.get(
                'reset_password_enabled'):
            print qcontext
            user = request.env['res.users'].search(
                [('id', '=', request.session.uid)])
            login = user.login
            if not login:
                login = 'not_empty'
            assert login, "No login provided."
            user = request.env['res.users'].search(
                [('login', '=', login)])
            partner = request.env['res.partner'].search(
                [('id', '=', user.partner_id.id)])
            qcontext['token'] = partner.signup_token
            qcontext['name'] = partner.name
            qcontext['login'] = login
            qcontext['birthday'] = partner.birthday
        return result

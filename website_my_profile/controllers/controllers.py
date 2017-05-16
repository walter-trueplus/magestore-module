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

    @http.route()
    def web_auth_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and 'reset_directly' in request.httprequest.query_string and qcontext.get(
                'reset_password_enabled'):
            user = request.env['res.users'].search(
                [('id', '=', request.session.uid)])
            assert user, "No login provided."
            login = user.login
            partner = request.env['res.partner'].search([('id', '=', user.partner_id.id)])
            qcontext['login'] = login
            qcontext['name'] = partner.name
            qcontext['reset_direct'] = "impressive"

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                if qcontext.get('token'):
                    self.do_signup(qcontext)
                    return super(AuthSignupHome, self).web_login(*args, **kw)
                else:
                    login = qcontext.get('login')
                    assert login, "No login provided."
                    if qcontext.get('old_password'):
                        self.do_reset_password_direct(qcontext)
                        # user = request.env['res.users'].search([('login', '=', login)])
                        values = {key: qcontext.get(key) for key in (
                            'login', 'password')}
                        request.env['res.partner'].write(values)
                        qcontext['message'] = _(
                            "Your password changed successfully")
                    else:
                        request.env['res.users'].sudo().reset_password(login)
                        qcontext['message'] = _(
                            "An email has been sent with credentials to reset your password")
            except SignupError:
                # qcontext['error'] = _("Could not reset your password")
                qcontext['error'] = qcontext.get('error_detail')
                _logger.exception('error when resetting password')
            except Exception, e:
                qcontext['error'] = e.message or e.name

        return request.render('auth_signup.reset_password', qcontext)

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

    def do_reset_password_direct(self, qcontext):
        values = {key: qcontext.get(key) for key in (
            'login', 'old_password', 'password')}

        if not values.values():
            qcontext['error_detail'] = 'The form was not properly filled in.'
            raise SignupError

        if not values.get('password') == qcontext.get('confirm_password'):
            qcontext[
                'error_detail'] = 'New passwords do not match; please retype them.'
            raise SignupError

        db = request.session.db
        password = values.get('old_password')
        login = values.get('login')
        uid = request.session.authenticate(db, login, password)

        if not uid:
            qcontext['error_detail'] = "Old password doesn't correct."
            raise SignupError

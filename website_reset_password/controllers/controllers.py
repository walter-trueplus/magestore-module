# -*- coding: utf-8 -*-
import logging
import re
import werkzeug

from odoo import http, _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website_reset_password.models.models import ResetDirectError, ChangeMailError
from odoo.addons.web.controllers.main import Home
from odoo.http import request
import re


def check_correct_format_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


class PasswordSignup(Home):
    @http.route('/web/reset_password_direct', type='http', auth='public', website=True)
    def reset_password_direct(self, redirect=None, *args, **kw):
        if not request.session.uid:
            return request.redirect('/')
        qcontext = request.params.copy()
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_reset_password_direct(qcontext)
                if check_correct_format_email(qcontext.get('login')):
                    request.env['res.users'].sudo().reset_password(qcontext.get('login'))
                qcontext['message'] = 'Changed password successful!'
                return request.redirect('/web')

            except ResetDirectError:
                qcontext['error'] = qcontext.get('error_detail')
            except Exception:
                qcontext['error'] = 'Could not reset password.'
        return request.render('website_reset_password.form_reset', qcontext)

    def do_reset_password_direct(self, qcontext):
        values = {key: qcontext.get(key) for key in ('old_password', 'new_password', 'retype_password')}
        uid = request.session.uid
        login = request.env['res.users'].sudo().search([('id', '=', uid)]).login
        qcontext['login'] = login

        if not login:
            qcontext['error_detail'] = 'No login provided.'
            raise ResetDirectError

        if values.get('new_password') != values.get('retype_password'):
            qcontext['error_detail'] = 'Passwords do not match, please retype them.'
            raise ResetDirectError

        # if old password not correct, this will raise an Exception and close cr (cursor : cr.close())
        #  and you can't not raise next of code below this line
        request.env['res.users'].sudo().change_password(values.get('old_password'), values.get('new_password'))

    @http.route('/web/change_email', type='http', auth='public', website=True)
    def change_email(self, *args, **kw):
        if not request.session.uid:
            return request.redirect('/')
        qcontext = request.params.copy()
        uid = request.session.uid
        current_login = request.env['res.users'].sudo().search([('id', '=', uid)]).login
        if kw:
            qcontext.update({'login': kw['login']})
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_change_email(qcontext)
                user = request.env['res.users'].sudo().search([('login', '=', current_login)])
                user.write({'login': qcontext.get('login')})
                # qcontext['message'] = 'Changed mail successful!'
                return request.redirect('/web/session/logout?redirect=/web/login', qcontext)
            except ChangeMailError:
                qcontext['error'] = qcontext.get('error_detail')
            except Exception:
                qcontext['error'] = 'Could not change email.'
        return request.render('website_reset_password.form_email', qcontext)

    def do_change_email(self, qcontext):
        uid = request.session.uid
        current_login = request.env['res.users'].sudo().search([('id', '=', uid)]).login

        if not qcontext.get('login') or not current_login:
            qcontext['error_detail'] = 'No login provided.Please go to Sign in page'
            raise ChangeMailError

        if request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))]) and qcontext.get(
                'login') != current_login:
            qcontext['error_detail'] = 'Another user is already registered using this login name.'
            raise ChangeMailError

        # request.session.authenticate(request.db, qcontext.get('login'), qcontext.get('password'))
        request.env['res.users'].change_password(qcontext.get('password'), qcontext.get('password'))

    @http.route()
    def web_login(self, redirect=None, **kw):
        res = super(PasswordSignup, self).web_login(redirect, **kw)
        if request.session.uid:
            return request.redirect('/')
        return res


class AuthSignup(AuthSignupHome):
    @http.route()
    def web_auth_reset_password(self, *args, **kw):
        res = super(AuthSignup, self).web_auth_reset_password(*args, **kw)
        if request.session.uid:
            return request.redirect('/')
        return res

# -*- coding: utf-8 -*-
#
from odoo.addons.auth_signup.controllers import main
from odoo import http , _
from odoo.http import request
import odoo


class Home(odoo.addons.web.controllers.main.Home):
    # @http.route('test/captcha', type='http',auth = "none",website=True)
    # def test(self):
    #     return "zxy"
    @http.route('/web/login', type='http', auth="none", website=True)
    def web_login(self,redirect=None, **kwargs):
        res_con= {}
        if 'g-recaptcha-response' in kwargs:
            print kwargs['g-recaptcha-response']
            res_con = request.website.is_captcha_valid(kwargs['g-recaptcha-response'])
            print res_con.get("error-codes")
            if "error-codes" in res_con :
                try:
                     if(res_con.get("error-codes")[1]=="missing-input-secret"or
                                                      res_con.get("error-codes")[1] == "invalid-input-secret"):
                        return super(Home, self).web_login(redirect, **kwargs)
                except:
                    print "aaa"
        vals = super(Home, self).web_login(redirect, **kwargs)
        values = request.params.copy()
        if 'g-recaptcha-response' in kwargs:
            if "success" in res_con and res_con.get("success") == True:
                del kwargs['g-recaptcha-response']
                return vals
            else:
                values['error'] = _("Please solve the captcha before submission.")
                return request.render('web.login', values)
        return vals

class AuthSignupHome(main.AuthSignupHome):
    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        res_con = {}
        if 'g-recaptcha-response' in kw:
            print kw['g-recaptcha-response']
            res_con = request.website.is_captcha_valid(kw['g-recaptcha-response'])
            print res_con.get("error-codes")
            if "error-codes" in res_con:
                try:
                    if (res_con.get("error-codes")[1] == "missing-input-secret" or
                                res_con.get("error-codes")[1] == "invalid-input-secret"):
                        return super(AuthSignupHome, self).web_auth_signup(*args, **kw)
                except:
                    print "aaa"
        qcontext = self.get_auth_signup_qcontext()
        vals =super(AuthSignupHome, self).web_auth_signup(*args, **kw)
        if 'g-recaptcha-response' in kw:
            if kw['g-recaptcha-response'] =="":
                return vals
            if request.website.is_captcha_valid(kw['g-recaptcha-response']):
                del kw['g-recaptcha-response']
                return vals
            else:
                qcontext['error'] = _("Please solve the captcha before submission.")
                return request.render('auth_signup.signup', qcontext)
        return vals

    @http.route('/web/reset_password', type='http', auth='public', website=True)
    def web_auth_reset_password(self, *args, **kw):
        if 'g-recaptcha-response' in kw:
            print kw['g-recaptcha-response']
            res_con = request.website.is_captcha_valid(kw['g-recaptcha-response'])
            print res_con.get("error-codes")
            if "error-codes" in res_con:
                try:
                    if (res_con.get("error-codes")[1] == "missing-input-secret" or
                                res_con.get("error-codes")[1] == "invalid-input-secret"):
                        return super(AuthSignupHome, self).web_auth_reset_password(*args, **kw)
                except:
                    print "aaa"
        qcontext = self.get_auth_signup_qcontext()
        vals =super(AuthSignupHome, self).web_auth_reset_password(*args, **kw)

        if 'g-recaptcha-response' in kw:
            if kw['g-recaptcha-response'] =="":
                return vals
            if request.website.is_captcha_valid(kw['g-recaptcha-response']):
                del kw['g-recaptcha-response']
                return vals
            else:
                qcontext['error'] = _("Please solve the captcha before submission.")
                return request.render('auth_signup.reset_password', qcontext)
        return vals
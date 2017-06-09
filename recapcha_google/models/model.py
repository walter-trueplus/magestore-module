# -*- coding utf-8 -*-
from odoo import fields, models
import requests
import json


class website(models.Model):
    _inherit = 'website'

<<<<<<< HEAD
    recaptcha_site_key = fields.Char(string='reCAPTCHA Site Key', default="6Lf77yIUAAAAAF9BR9bx-2C5QOq_WxBD5bEjq2Hm")
    recaptcha_private_key = fields.Char(string='reCAPTCHA Private Key', default="6Lf77yIUAAAAAD_KQHeTASJk5L6i056HcN6aYBkw")
=======
    recaptcha_site_key = fields.Char(string='reCAPTCHA Site Key')
    recaptcha_private_key = fields.Char(string='reCAPTCHA Private Key')
>>>>>>> dev

    def is_captcha_valid(self,response):
        for website in self:
            get_res = {'secret': website.recaptcha_private_key, 'response':response}
            try:
                response = requests.post('https://www.google.com/recaptcha/api/siteverify', params=get_res)
            except Exception, e:
                raise UserWarning(e.message)
            res_con = json.loads(response.content)
            if res_con.has_key('success') and res_con['success']:
                return True
        return False
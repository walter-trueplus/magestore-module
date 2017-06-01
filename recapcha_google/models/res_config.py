from odoo import fields, models


class website_config_settings(models.TransientModel):
    _inherit = 'website.config.settings'

    recaptcha_site_key = fields.Char(related="website_id.recaptcha_site_key",
                                     string='reCAPTCHA site Key')
    recaptcha_private_key = fields.Char(related="website_id.recaptcha_private_key",
                                        string='reCAPTCHA Private Key')

class BaseConfigSetting(models.TransientModel):
    _inherit = 'base.config.settings'
    auth_signup_reset_password = fields.Boolean(string='Enable password reset from Login page',
                                                help="This allows users to trigger a password reset from the Login page.",
                                                default =True)
    auth_signup_uninvited = fields.Boolean(string='Allow external users to sign up',
                                           help="If unchecked, only invited users may sign up.",
                                           default=True)



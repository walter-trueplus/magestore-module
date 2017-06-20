from odoo import api, SUPERUSER_ID, fields, models, _
from odoo.exceptions import AccessDenied
import logging

_logger = logging.getLogger(__name__)


class ResUser(models.Model):
    _inherit = "res.users"

    @classmethod
    def _login(cls, db, login, password):
        if not password:
            return False
        user_id = False
        try:
            with cls.pool.cursor() as cr:
                self = api.Environment(cr, SUPERUSER_ID, {})[cls._name]
                require_case_sensitively=self._get_login_option()
                if require_case_sensitively:
                    user = self.search([('login', '=', login)])
                else:
                    user=self.search([('login','=ilike',login)])
                if user:
                    user_id = user.id
                    user.sudo(user_id).check_credentials(password)
                    user.sudo(user_id)._update_last_login()
        except AccessDenied:
            _logger.info("Login failed for db:%s login:%s", db, login)
            user_id = False
        return user_id

    # get login option from database
    @api.model
    def _get_login_option(self):
        setting_records = self.env['base.config.settings'].search([])
        if len(setting_records) == 0:  # default title
            return 'True'
        else:  # return custom title
            return setting_records[-1].case_sensitive_option

# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions
import logging
import psycopg2
import itertools

ERROR_PREVIEW_BYTES = 200
_logger = logging.getLogger(__name__)


class User(models.Model):
    _inherit = ['res.users']

    employee_id = fields.Many2one('hr.employee')

    @api.model
    def create(self, vals):
        # create user
        new_user = super(User, self).create(vals)
        if new_user:
            user = self.search([('id', '=', new_user.id)], limit=1)
            if user:
                new_employee = self.env[
                    'hr.employee'].create({'name': user.name})

                employee = self.env['hr.employee'].search(
                    [('id', '=', new_employee.id)], limit=1)
                user.write({'employee_id': employee.id})
                employee.write({'user_id': user.id, 'work_email': user.login})
        return user

    @api.multi
    def unlink(self):
        # delete user also delete related employee
        for user in self:
            employee = self.env['hr.employee'].search(
                [('id', '=', user.employee_id.id)])
            if employee:
                employee.unlink()
        res = super(User, self).unlink()
        return res

    @api.multi
    def write(self, vals):
        # if login name change
        if 'login' in vals:
            employee = self.env['hr.employee'].search(
                [('id', '=', self.employee_id.id)])
            # change login of user
            employee.write({'work_email': vals['login']})

        res = super(User, self).write(vals)
        return res


class create_users_from_excel_list(models.TransientModel):
    _inherit = 'base_import.import'

    @api.multi
    def parse_preview(self, options, count=10):

        self.ensure_one()
        fields = self.get_fields(self.res_model)
        try:
            rows = self._read_file(options)
            headers, matches = self._match_headers(rows, fields, options)
            # Match should have consumed the first row (iif headers), get
            # the ``count`` next rows for preview
            del matches[2]
            del matches[3]
            del matches[4]
            del matches[5]
            del matches[6]
            del matches[7]
            del matches[8]
            del matches[9]
            preview = list(itertools.islice(rows, count))
            assert preview, "CSV file seems to have no content"
            header_types = self._find_type_from_preview(options, preview)
            if options.get('keep_matches', False) and len(options.get('fields', [])):
                matches = {}
                for index, match in enumerate(options.get('fields')):
                    if match:
                        matches[index] = match.split('/')

            return {
                'fields': fields,
                'matches': matches or False,
                'headers': headers or False,
                'headers_type': header_types or False,
                'preview': preview,
                'options': options,
                'advanced_mode': any([len(models.fix_import_export_id_paths(col)) > 1 for col in headers]),
                'debug': self.user_has_groups('base.group_no_one'),
            }
        except Exception, error:
            # Due to lazy generators, UnicodeDecodeError (for
            # instance) may only be raised when serializing the
            # preview to a list in the return.
            _logger.debug("Error during parsing preview", exc_info=True)
            preview = None
            if self.file_type == 'text/csv':
                preview = self.file[:ERROR_PREVIEW_BYTES].decode('iso-8859-1')
            return {
                'error': str(error),
                # iso-8859-1 ensures decoding will always succeed,
                # even if it yields non-printable characters. This is
                # in case of UnicodeDecodeError (or csv.Error
                # compounded with UnicodeDecodeError)
                'preview': preview,
            }

    @api.multi
    def do(self, fields, options, dryrun=False):

        self.ensure_one()
        self._cr.execute('SAVEPOINT import')
        length_head = len(self.parse_preview(options, 10)['headers'])
        length_pre = len(self.parse_preview(options, 10)['preview'])
        preview_obj = self.parse_preview(options, 10)['preview']
        headers_obj = self.parse_preview(options, 10)['headers']
        try:
            data, import_fields = self._convert_import_data(fields, options)
            # Parse date and float field
            data = self._parse_import_data(data, import_fields, options)

        except ValueError, error:
            return [{
                'type': 'error',
                'message': unicode(error),
                'record': False,
            }]

        _logger.info('importing %d rows...', len(data))
        import_result = self.env[self.res_model].with_context(import_file=True).load(import_fields, data)

        _logger.info('done')

        # If transaction aborted, RELEASE SAVEPOINT is going to raise
        # an InternalError (ROLLBACK should work, maybe). Ignore that.
        # TODO: to handle multiple errors, create savepoint around
        #       write and release it in case of write error (after
        #       adding error to errors array) => can keep on trying to
        #       import stuff, and rollback at the end if there is any
        #       error in the results.
        try:
            if dryrun:
                self._cr.execute('ROLLBACK TO SAVEPOINT import')
            else:
                self._cr.execute('RELEASE SAVEPOINT import')
                for j in range(0, length_head):
                    if headers_obj[j].lower() == u'sale' or headers_obj[j].lower() == u'sales':
                        for i in range(0, length_pre):
                            if preview_obj[i][j] == u'0':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('sales_team.group_sale_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})
                                    group_env = self.env.ref('sales_team.group_sale_salesman_all_leads',
                                                             False)  # All Documents
                                    group_env.write({'users': [(3, user_obj.id)]})
                                    group_env_1 = self.env.ref('sales_team.group_sale_salesman',
                                                               False)  # Own Document Only
                                    group_env_1.write({'users': [(3, user_obj.id)]})

                            elif preview_obj[i][j] == u'1':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('sales_team.group_sale_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})
                                    group_env = self.env.ref('sales_team.group_sale_salesman_all_leads',
                                                             False)  # All Documents
                                    group_env.write({'users': [(3, user_obj.id)]})

                            elif preview_obj[i][j] == u'2':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('sales_team.group_sale_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})

                    elif headers_obj[j].lower() == u'project':
                        for i in range(0, length_pre):
                            if preview_obj[i][j] == u'0':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('project.group_project_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})
                                    group_env = self.env.ref('project.group_project_user', False)  # User
                                    group_env.write({'users': [(3, user_obj.id)]})

                            elif preview_obj[i][j] == u'1':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('project.group_project_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})

                    elif headers_obj[j].lower() == u'account' or headers_obj[j].lower() == u'accounting & finance':
                        for i in range(0, length_pre):
                            if preview_obj[i][j] == u'0':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('account.group_account_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})
                                    group_env = self.env.ref('account.group_account_user', False)  # Accountant
                                    group_env.write({'users': [(3, user_obj.id)]})
                                    group_env_1 = self.env.ref('account.group_account_invoice', False)  # Billing
                                    group_env_1.write({'users': [(3, user_obj.id)]})

                            elif preview_obj[i][j] == u'1':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('account.group_account_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})
                                    group_env = self.env.ref('account.group_account_user', False)  # Accountant
                                    group_env.write({'users': [(3, user_obj.id)]})

                            elif preview_obj[i][j] == u'2':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('account.group_account_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})

                    elif headers_obj[j].lower() == u'employees' or headers_obj[j].lower() == u'employee':
                        for i in range(0, length_pre):
                            if preview_obj[i][j] == u'1':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('hr.group_hr_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})
                                    group_env = self.env.ref('hr.group_hr_user', False)  # Officer
                                    group_env.write({'users': [(3, user_obj.id)]})

                            elif preview_obj[i][j] == u'0':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('hr.group_hr_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})
                                    group_env = self.env.ref('hr.group_hr_user', False)  # Officer
                                    group_env.write({'users': [(3, user_obj.id)]})
                                    group_env_1 = self.env.ref('base.group_user', False)  # Employee
                                    group_env_1.write({'users': [(3, user_obj.id)]})
                                    employee_obj = self.env['hr.employee'].search(
                                        [('id', '=', user_obj.employee_id.id)])
                                    if employee_obj:
                                        employee_obj.unlink()

                            elif preview_obj[i][j] == u'2':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('hr.group_hr_manager', False)  # Manager
                                    group_e.write({'users': [(3, user_obj.id)]})

                    elif headers_obj[j].lower() == u'timesheet' or headers_obj[j].lower() == u'timesheets':
                        for i in range(0, length_pre):
                            if preview_obj[i][j] == u'0':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('hr_timesheet.group_hr_timesheet_user', False)  # Officer
                                    group_e.write({'users': [(3, user_obj.id)]})

                    elif headers_obj[j].lower() == u'administration' or headers_obj[j].lower() == u'administrator':
                        for i in range(0, length_pre):
                            if preview_obj[i][j] == u'0':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('base.group_system', False)  # Settings
                                    group_e.write({'users': [(3, user_obj.id)]})
                                    group_env = self.env.ref('base.group_erp_manager', False)  # Access Rights
                                    group_env.write({'users': [(3, user_obj.id)]})

                    elif headers_obj[j].lower() == u'home_action' or headers_obj[j].lower() == u'home action':
                        for i in range(0, length_pre):
                            if (preview_obj[i][j]).lower() == u'project' or (preview_obj[i][j]).lower() == u'projects':
                                user_id = import_result['ids'][i]
                                ir_action = self.env['ir.actions.actions'].search([('name', '=', 'Projects')])
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                user_obj.write({'action_id': ir_action[0].id})

                    elif headers_obj[j].lower() == u'contact creation' or headers_obj[j].lower() == u'contact_creation':
                        for i in range(0, length_pre):
                            if preview_obj[i][j] == u'0' or preview_obj[i][j] == u'':
                                user_id = import_result['ids'][i]
                                user_obj = self.env['res.users'].search([('id', '=', user_id)])

                                if user_id:
                                    group_e = self.env.ref('base.group_partner_manager', False)  # Contact Creation
                                    group_e.write({'users': [(3, user_obj.id)]})

        except psycopg2.InternalError:
            pass
        if dryrun == False:
            for a in range(0, length_head):
                if headers_obj[a].lower() == u'employee' or headers_obj[a].lower() == u'employees':
                    for b in range(0, length_pre):
                        if preview_obj[b][a] == u'1':
                            user_id_1 = import_result['ids'][b]
                            user_obj_1 = self.env['res.users'].search([('id', '=', user_id_1)])
                            group_env = self.env.ref('hr.group_hr_user', False)  # Officer
                            group_env.write({'users': [(3, user_obj_1.id)]})

                        elif preview_obj[b][a] == u'0':
                            user_id_2 = import_result['ids'][b]
                            user_obj_2 = self.env['res.users'].search([('id', '=', user_id_2)])

                            if user_id_2:
                                group_e = self.env.ref('hr.group_hr_manager', False)  # Manager
                                group_e.write({'users': [(3, user_obj_2.id)]})
                                group_env = self.env.ref('hr.group_hr_user', False)  # Officer
                                group_env.write({'users': [(3, user_obj_2.id)]})
                                group_env_1 = self.env.ref('base.group_user', False)  # Employee
                                group_env_1.write({'users': [(3, user_obj_2.id)]})
        return import_result['messages']

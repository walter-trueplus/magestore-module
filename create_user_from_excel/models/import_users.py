# -*- coding: utf-8 -*-

import base64
import re
import xlwt, xlrd, cStringIO
from . import read_users_in_file
from odoo import models, fields, api
from odoo.exceptions import UserError


class ImportUsers(models.TransientModel):
    _name = 'import.users.wizard'

    data = fields.Binary('File', required=True)
    data_err = fields.Binary('File Error')
    state = fields.Selection([('choose', 'choose'), ('get', 'get'), ('successful', 'successful')], default='choose')
    filename = fields.Char('Filename', required=True)

    @api.multi
    def do_import(self):
        data = base64.decodestring(self.data)
        file_type = self.filename.split('.')[-1]
        rfa = read_users_in_file.GetUser()

        if file_type == "xls":
            book = xlrd.open_workbook(file_contents=data, encoding_override='utf8')
            sheet1 = book.sheet_by_index(0)
            list_users = rfa.read_xls_file(sheet1, book)
        else:
            raise UserError("Import wizard doesn't support this file type!!")

        if list_users == 'Wrong file format':
            raise UserError("Wrong file format")
        file_error = self._import_users(list_users)
        if file_error:
            self.write({
                'state': 'get',
                'data_err': file_error,
                'filename': 'log_error.xls',
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'import.users.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'views': [(False, 'form')],
                'target': 'new',
            }
        else:
            self.write({
                'state': 'successful',
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'import.users.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'views': [(False, 'form')],
                'target': 'new',
            }

    def _import_users(self, list_users):
        list_error_datas = []
        for user in list_users:
            errors = user.get('errors')
            vals = {}
            if not errors:
                errors = ''

                username = user.get('username')
                if not username:
                    errors += 'Username can\'t be empty ; '
                else:
                    vals.update({
                        'name': username
                    })

                email = user.get('email')
                if not email:
                    errors += 'Email can\'t be empty ; '
                else:
                    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                        errors += 'Invalid email'
                    else:
                        check_user = self.env['res.users'].search([('login', '=', email)])
                    if check_user:
                        errors += 'Another user has this email address ; '
                    else:
                        vals.update({
                            'login': email
                        })

                contact_creation = str(user.get('contact_creation'))
                if not contact_creation or contact_creation in ['false', '0']:
                    contact_value = False
                elif contact_creation in ['true', '1']:
                    contact_value = True
                else:
                    errors += 'Invalid value for contact_creation; '
                    contact_value = 'Wrong'
                action_id = self.env['res.groups'].search([('name', '=', 'Contact Creation')], limit=1)
                if action_id:
                    vals.update({
                        'in_group_' + str(action_id.id): contact_value
                    })

                home_action = user.get('home_action')
                if not home_action:
                    home_action_id = False
                else:
                    home_action_id = self.env['ir.actions.actions'].search([('name', '=', home_action.title())],
                                                                           limit=1)
                    home_action_id = home_action_id.id
                if not home_action_id:
                    errors += 'Invalid value for home_action; '
                else:
                    vals.update({
                        'action_id': home_action_id
                    })

                sale = user.get('sale')
                sale_value = self.set_sel_group('Sales', sale)
                if isinstance(sale_value, basestring):
                    errors += sale_value
                elif sale_value != 99:
                    vals.update(sale_value)

                project = user.get('project')
                project_value = self.set_sel_group('Project', project)
                if isinstance(project_value, basestring):
                    errors += project_value
                elif project_value != 99:
                    vals.update(project_value)

                account = user.get('account')
                account_value = self.set_sel_group('Accounting & Finance', account)
                if isinstance(account_value, basestring):
                    errors += account_value
                elif account_value != 99:
                    vals.update(account_value)

                employee = user.get('employee')
                employee_value = self.set_sel_group('Employees', employee)
                if isinstance(employee_value, basestring):
                    errors += employee_value
                elif account_value != 99:
                    vals.update(employee_value)

                timesheet = user.get('timesheet')
                timesheet_value = self.set_sel_group('Timesheets', timesheet)
                if isinstance(timesheet_value, basestring):
                    errors += timesheet_value
                elif timesheet_value != 99:
                    vals.update(timesheet_value)

                administrator = user.get('administrator')
                administrator_value = self.set_sel_group('Administration', administrator)
                if isinstance(administrator_value, basestring):
                    errors += administrator_value
                elif administrator_value != 99:
                    vals.update(administrator_value)
            # if all values are ok, create record(s)
            if not errors:
                self.env['res.users'].sudo().create(vals)
            # else, record has wrong value with errors column
            else:
                error_data = {}
                error_data.update({
                    'username': user.get('username'),
                    'email': user.get('email'),
                    'contact_creation': user.get('contact_creation'),
                    'home_action': user.get('home_action'),
                    'sale': user.get('sale'),
                    'project': user.get('project'),
                    'account': user.get('account'),
                    'employee': user.get('employee'),
                    'timesheet': user.get('timesheet'),
                    'administrator': user.get('administrator'),
                    'errors': errors,
                })
                list_error_datas.append(error_data)

        if list_error_datas:
            file_error = self._export_users_errors(list_error_datas)
            return file_error

    @staticmethod
    def _export_users_errors(errors):

        wb = xlwt.Workbook(encoding='utf8')
        sheet = wb.add_sheet('sheet')
        sheet.write(0, 0, "username")
        sheet.write(0, 1, "email")
        sheet.write(0, 2, "contact_creation")
        sheet.write(0, 3, "home_action")
        sheet.write(0, 4, "sale")
        sheet.write(0, 5, "project")
        sheet.write(0, 6, "account")
        sheet.write(0, 7, "employee")
        sheet.write(0, 8, "timesheet")
        sheet.write(0, 9, "administrator")
        sheet.write(0, 10, "errors")
        index = 0

        for item in errors:
            sheet.write(index + 1, 0, item.get('username'))
            sheet.write(index + 1, 1, item.get('email'))
            sheet.write(index + 1, 2, item.get('contact_creation'))
            sheet.write(index + 1, 3, item.get('home_action'))
            sheet.write(index + 1, 4, item.get('sale'))
            sheet.write(index + 1, 5, item.get('project'))
            sheet.write(index + 1, 6, item.get('account'))
            sheet.write(index + 1, 7, item.get('employee'))
            sheet.write(index + 1, 8, item.get('timesheet'))
            sheet.write(index + 1, 9, item.get('administrator'))
            sheet.write(index + 1, 10, item.get('errors'))
            index += 1

        data_err = cStringIO.StringIO()
        wb.save(data_err)
        data_err.seek(0)
        out = base64.encodestring(data_err.read())
        data_err.close()

        return out

    @api.model
    def get_id_of_view_import(self):
        return self.env.ref('create_user_from_excel.import_user_form').id

    @api.multi
    def reload_tree_view(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }

    def set_sel_group(self, name, value):
        category = self.env['ir.module.category'].search([('name', '=', name), ('write_uid', '=', 1)], limit=1)
        res_group_ids = sorted(self.env['res.groups'].search([('category_id', '=', category.id)]).ids)
        sel_group = 'sel_groups_'
        # if this setting exist
        if res_group_ids:
            sel_group += '_'.join(list(map(str, res_group_ids)))
            # if column has empty value
            if value == '' or str(value) == '0.0':
                return {sel_group: False}
            # if column has valid value
            if self.is_int_number(value) and (value > 0 and value <= len(res_group_ids)):
                return {sel_group: int(res_group_ids[int(value) - 1])}
            else:
                return 'Setting for %s has invalid value ; ' % name.title()
        else:
            # if value is empty and this settings don't exist --> no add value to vals
            if not value:
                return 99
            else:
                return 'Setting for %s doesn\'t exist ; ' % name.title()

    def is_int_number(self, value):
        try:
            value = int(value)
            return isinstance(int(str(value)), int)
        except ValueError:
            return False

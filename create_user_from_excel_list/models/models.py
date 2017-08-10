# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import base64
import xlrd, xlwt, cStringIO
from odoo.exceptions import UserError


class import_users(models.TransientModel):
    _name = 'import.users'

    filename = fields.Char()
    data_file = fields.Binary(string="File")
    file_error = fields.Binary()

    @api.multi
    def import_file(self):
        if self.data_file == None:
            raise UserError('You haven\'t select a file!')
        file_type = self.filename.split('.')[-1]
        if file_type not in ('xlsx', 'xls'):
            raise UserError('File format is not supported yet!')
        data = base64.decodestring(self.data_file)
        excel = xlrd.open_workbook(file_contents=data)
        sh = excel.sheet_by_index(0)
        data_err = []
        for rx in range(1, sh.nrows):
            v = [sh.cell(rx, ry).value for ry in range(sh.ncols)]
            lst_err = []
            lst_err_setting = []
            username = v[0]
            login = v[1]
            if username == u'' and login == u'':
                lst_err.append("The value of username and email column must not be"
                               " null in row %s." % (rx + 1))
                username += 'u'
                login += 'u'
                new_user = self.env['res.users'].create({'name': username, 'login': login})
                user_obj = self.env['res.users'].search([('id', '=', new_user.id)])
            elif username == u'' and login != u'':
                lst_err.append("The value of username column must not be"
                               " null in row %s." % (rx + 1))
                username += 'u'
                new_user = self.env['res.users'].create({'name': username, 'login': v[1]})
                user_obj = self.env['res.users'].search([('id', '=', new_user.id)])
            elif username != u'' and login == u'':
                lst_err.append("The value of email column must not be"
                               " null in row %s." % (rx + 1))
                login += 'u'
                new_user = self.env['res.users'].create({'name': v[0], 'login': login})
                user_obj = self.env['res.users'].search([('id', '=', new_user.id)])
            else:
                new_user = self.env['res.users'].create({'name': v[0], 'login': v[1]})
                user_obj = self.env['res.users'].search([('id', '=', new_user.id)])
                if user_obj:
                    check_user = self.env['res.users'].search([('login', '=', login)])
                    if len(check_user) >= 2:
                        lst_err.append('Users can not have the same email.')

            contact_creation = v[2]
            if contact_creation in [u'', 0.0, 'false', 'FALSE']:
                self.unlink_group(user_obj, 'base.group_partner_manager')
            elif contact_creation in [u'true', 1.0, u'TRUE']:
                print 'aaa'
            else:
                lst_err.append('Invalid value for contact_creation in row %s. \n' % (rx + 1))

            home_action = v[3]
            if home_action:
                ir_action = self.env['ir.actions.actions'].search([('name', '=', v[3].title())])
                if not ir_action:
                    lst_err.append(
                        "Invalid value for home_action in row %s." %(rx+1))
                else:
                    new_user.write({'action_id': ir_action[0].id})
            elif home_action == u'':
                print home_action

            check_install = self.check_istall_module()
            sale = v[4]
            if sale in range(4) or sale == u'':
                if sale == u'' or int(sale) == 0:
                    if 'sales_team' in check_install:
                        self.unlink_group(user_obj, 'sales_team.group_sale_manager')
                        self.unlink_group(user_obj, 'sales_team.group_sale_salesman_all_leads')
                        self.unlink_group(user_obj, 'sales_team.group_sale_salesman')
                    else:
                        lst_err_setting.append('Setting for sale does not exist.')
                elif int(sale) == 1:
                    if 'sales_team' in check_install:
                        self.unlink_group(user_obj, 'sales_team.group_sale_manager')
                        self.unlink_group(user_obj, 'sales_team.group_sale_salesman_all_leads')
                    else:
                        lst_err_setting.append('Setting for sale does not exist.')
                elif int(sale) == 2:
                    if 'sales_team' in check_install:
                        self.unlink_group(user_obj, 'sales_team.group_sale_manager')
                    else:
                        lst_err_setting.append('Setting for sale does not exist.')
                elif int(sale) == 3:
                    if 'sales_team' not in check_install:
                        lst_err_setting.append('Setting for sale does not exist.')
            else:
                lst_err.append("The value of sale column must be"
                               " '0,1,2,3 or null' in row %s." % (rx + 1))

            project = v[5]
            if project in range(3) or project == u'':
                if project == u'' or int(project) == 0:
                    if 'project' in check_install:
                        self.unlink_group(user_obj, 'project.group_project_manager')
                        self.unlink_group(user_obj, 'project.group_project_user')
                    else:
                        lst_err_setting.append('Setting for project does not exist.')
                elif int(project) == 1:
                    if 'project' in check_install:
                        self.unlink_group(user_obj, 'project.group_project_manager')
                    else:
                        lst_err_setting.append('Setting for project does not exist.')
                elif int(project) == 2:
                    if 'project' not in check_install:
                        lst_err_setting.append('Setting for project does not exist.')
            else:
                lst_err.append("The value of project column must be"
                               " '0,1,2 or null' in row %s." % (rx + 1))

            account = v[6]
            if account in range(4) or account == u'':
                if account == u'' or int(account) == 0:
                    if 'account' in check_install:
                        self.unlink_group(user_obj, 'account.group_account_manager')
                        self.unlink_group(user_obj, 'account.group_account_user')
                        self.unlink_group(user_obj, 'account.group_account_invoice')
                    else:
                        lst_err_setting.append('Setting for account does not exist.')
                elif int(account) == 1:
                    if 'account' in check_install:
                        self.unlink_group(user_obj, 'account.group_account_manager')
                        self.unlink_group(user_obj, 'account.group_account_user')
                    else:
                        lst_err_setting.append('Setting for account does not exist.')
                elif int(account) == 2:
                    if 'account' in check_install:
                        self.unlink_group(user_obj, 'account.group_account_manager')
                    else:
                        lst_err_setting.append('Setting for account does not exist.')
                elif int(account) == 3:
                    if 'account' not in check_install:
                        lst_err_setting.append('Setting for account does not exist.')
            else:
                lst_err.append("The value of account column must be"
                               " '0,1,2,3 or null' in row %s." % (rx + 1))

            employee = v[7]
            if employee in range(4) or employee == u'':
                if employee == u'' or int(employee) == 0:
                    if 'hr' in check_install:
                        self.unlink_group(user_obj, 'hr.group_hr_manager')
                        self.unlink_group(user_obj, 'hr.group_hr_user')
                        self.unlink_group(user_obj, 'base.group_user')
                    else:
                        lst_err_setting.append('Setting for employee does not exist.')
                elif int(employee) == 1:
                    if 'hr' in check_install:
                        self.unlink_group(user_obj, 'hr.group_hr_manager')
                        self.unlink_group(user_obj, 'hr.group_hr_user')
                    else:
                        lst_err_setting.append('Setting for employee does not exist.')
                elif int(employee) == 2:
                    if 'hr' in check_install:
                        self.unlink_group(user_obj, 'hr.group_hr_manager')
                    else:
                        lst_err_setting.append('Setting for employee does not exist.')
                elif int(employee) == 3:
                    if 'hr' not in check_install:
                        lst_err_setting.append('Setting for employee does not exist.')
            else:
                lst_err.append("The value of employee column must be"
                               " '0,1,2,3 or null' in row %s." % (rx + 1))

            timesheet = v[8]
            if timesheet in range(2) or timesheet == u'':
                if timesheet == u'' or int(timesheet) == 0:
                    if 'hr_timesheet' in check_install:
                        self.unlink_group(user_obj, 'hr_timesheet.group_hr_timesheet_user')
                    else:
                        lst_err_setting.append('Setting for timesheet does not exist.')
                elif int(timesheet) == 1:
                    if 'hr_timesheet' not in check_install:
                        lst_err_setting.append('Setting for timesheet does not exist.')
            else:
                lst_err.append(("The value of timesheet column must be "
                                "'0,1 or null' in row %s.") % (rx + 1))

            admin = v[9]
            if admin in range(3) or admin == u'':
                if int(admin) == 1:
                    self.add_user_in_group(user_obj, 'base.group_erp_manager')
                if int(admin) == 2:
                    self.add_user_in_group(user_obj, 'base.group_system')
            else:
                lst_err.append(("The value of administrator column must be "
                                "'0,1,2 or null' in row %s.") % (rx + 1))
            data_err += lst_err
            data_err += lst_err_setting
            if lst_err:
                new_user.unlink()
        if data_err:
            file_err = self._export_users_errors(data_err)
            ir_model_data = self.env['ir.model.data']
            view_id = ir_model_data.get_object_reference('create_user_from_excel_list', 'view_list_error')[1]
            self.write({
                'file_error': file_err,
                'filename': 'log_error.xls',
            })
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'import.users',
                'views': [(view_id, 'form')],
                'view_id': view_id,
                'res_id': self.id,
                'target': 'new',
            }

    def check_istall_module(self):
        list_module_install = []
        module_install = self.env['ir.module.module'].search([('state', '=', 'installed')])
        for i in range(len(module_install)):
            list_module_install.append(module_install[i].name)
        return list_module_install

    def unlink_group(self, user_obj, x):
        group = self.env.ref(x, False)
        group.write({'users': [(3, user_obj.id)]})

    def add_user_in_group(self, user_obj, x):
        group = self.env.ref(x)
        group.write({'users': [(4, user_obj.id)]})

    @staticmethod
    def _export_users_errors(data_err):
        wb = xlwt.Workbook(encoding='utf8')
        sheet = wb.add_sheet('sheet')
        data_err.sort()
        check = data_err[0]
        data_err_node = []
        data_err_node.append(check)
        for data in data_err:
            if check != data:
                data_err_node.append(data)
                check = data
        for index in range(len(data_err_node)):
            sheet.write(index, 0, data_err_node[index])
        data_error = cStringIO.StringIO()
        wb.save(data_error)
        data_error.seek(0)
        out = base64.encodestring(data_error.read())
        data_error.close()

        return out

    def reload_tree_view(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }


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

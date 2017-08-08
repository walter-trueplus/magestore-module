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
            vals = {}
            username = v[0]
            if username == u'':
                lst_err.append("The value of username column must not be"
                               " null in row %s." % (rx))
            else:
                vals.update({'name': v[0]})
            login = v[1]
            if login == u'':
                lst_err.append("The value of login column must not be"
                               " null in row %s." % (rx))
            else:
                check_user = self.env['res.users'].search([('login', '=', login)])
                if check_user:
                    lst_err.append('Another user has this email address.')
                else:
                    vals.update({'login': v[1]})

            contact_creation = v[2]
            contact_value = None
            if not contact_creation or contact_creation in [u'false', 0, '', u'FALSE']:
                contact_value = False
            elif contact_creation in [u'true', 1.0, u'TRUE']:
                contact_value = True
            else:
                lst_err.append('Invalid value for contact_creation in row %s. \n' % (rx))
            action_id = self.env['res.groups'].search([('name', '=', 'Contact Creation')], limit=1)
            if action_id:
                vals.update({
                    'in_group_' + str(action_id.id): contact_value
                })

            home_action = v[3]
            if home_action == u'project':
                ir_action = self.env['ir.actions.actions'].search([('name', '=', 'Projects')])
                if not ir_action:
                    lst_err.append("Invalid value for home_action.")
                else:
                    vals.update({'action_id': ir_action[0].id})
            elif home_action == u'':
                print home_action
            else:
                lst_err.append("The value of home_action column must be"
                               " 'project or null' in row %s." % (rx))

            sale = v[4]
            if sale in range(4) or sale == u'':
                group_value = self.set_sel_group('Sales', sale)
                if isinstance(group_value, basestring):
                    lst_err.append(group_value)
                elif group_value != 99:
                    vals.update(group_value)
            else:
                lst_err.append("The value of sale column must be"
                               " '0,1,2,3 or null' in row %s." % (rx))

            project = v[5]
            if project in range(3) or project == u'':
                group_value = self.set_sel_group('Project', project)
                if isinstance(group_value, basestring):
                    lst_err.append(group_value)
                elif group_value != 99:
                    vals.update(group_value)
            else:
                lst_err.append("The value of project column must be"
                               " '0,1,2 or null' in row %s." % (rx))

            account = v[6]
            if account in range(4) or account == u'':
                group_value = self.set_sel_group('Accounting & Finance', account)
                if isinstance(group_value, basestring):
                    lst_err.append(group_value)
                elif group_value != 99:
                    vals.update(group_value)
            else:
                lst_err.append("The value of account column must be"
                               " '0,1,2,3 or null' in row %s." % (rx))

            employee = v[7]
            if employee in range(4) or employee == u'':
                group_value = self.set_sel_group('Employees', employee)
                if isinstance(group_value, basestring):
                    lst_err.append(group_value)
                elif group_value != 99:
                    vals.update(group_value)
            else:
                lst_err.append("The value of employee column must be"
                               " '0,1,2,3 or null' in row %s." % (rx))

            timesheet = v[8]
            if timesheet in range(2) or timesheet == u'':
                group_value = self.set_sel_group('Timesheets', timesheet)
                if isinstance(group_value, basestring):
                    lst_err.append(group_value)
                elif group_value != 99:
                    vals.update(group_value)
            else:
                lst_err.append(("The value of timesheet column must be "
                                "'0,1 or null' in row %s.") % (rx))

            admin = v[9]
            if admin in range(3) or admin == u'':
                group_value = self.set_sel_group('Administration', admin)
                if isinstance(group_value, basestring):
                    lst_err.append(group_value)
                elif group_value != 99:
                    vals.update(group_value)
            else:
                lst_err.append(("The value of administrator column must be "
                                "'0,1,2 or null' in row %s.") % (rx))
            data_err += lst_err
            if not lst_err:
                self.env['res.users'].sudo().create(vals)
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

    @staticmethod
    def _export_users_errors(data_err):
        wb = xlwt.Workbook(encoding='utf8')
        sheet = wb.add_sheet('sheet')
        index = 0
        for i in range(len(data_err)):
            sheet.write(index, 0, data_err[i])
            index += 1
        data_error = cStringIO.StringIO()
        wb.save(data_error)
        data_error.seek(0)
        out = base64.encodestring(data_error.read())
        data_error.close()

        return out

    def set_sel_group(self, name, value):
        category = self.env['ir.module.category'].search([('name', '=', name), ('write_uid', '=', 1)], limit=1)
        res_group_ids = sorted(self.env['res.groups'].search([('category_id', '=', category.id)]).ids)
        sel_group = 'sel_groups_'
        # if this setting exist
        if res_group_ids:
            sel_group += '_'.join(list(map(str, res_group_ids)))
            # if column has empty value
            if value == '' or int(value) == 0:
                return {sel_group: False}
            # if column has valid value
            elif int(value) and (value > 0 and value <= len(res_group_ids)):
                return {sel_group: int(res_group_ids[int(value) - 1])}

        else:
            if not value:
                return 99
            # if value is empty and this settings don't exist --> no add value to vals
            return 'Setting for %s doesn\'t exist ; ' % name.title()

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

# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api


class Department(models.Model):
    _inherit = "hr.department"
    number_hit = fields.Integer(string="Number hit", compute="create_number", store=True)
    _order = "number_hit desc"

    @api.depends("parent_id")
    def create_number(self):
        for item in self:
            if item.parent_id:
                department = self.env['hr.department'].search([('id', '=', item.parent_id.id)])
                item.number_hit = department.number_hit + 1
            else:
                item.number_hit = 1

class View(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('myview', "MyView")])




class ChartConfig(models.Model):
    _name = "chart_config"

    @api.model
    def search_department(self):
        chart_config = {}
        chart = {
                "container": '#basic-example',
                "connectors": {'type': 'step'},
                "node": {'HTMLclass': 'nodeExample1'}
                }
        chart_config['chart'] = chart
# -----------------------
        node_structure = {}
        company = ""
        for i in self.env['res.company'].search([]):
            company = i
            break
        text = {
             'name': company.name,
             'title': company.website,
             'contact': company.phone,
        }
        node_structure['text'] = text
        node_structure['children'] = []
        # so luong bac trong bieu do
        hierarchy_count = self.env['hr.department'].search([], limit=1).number_hit
        a = 1
        if self.env['hr.department'].search([("number_hit", "=", a)]):
            node_parent = self.env['hr.department'].search([("number_hit", "=", a)])
            for depart in node_parent:

                def get_inf(self, depart, i):
                    child = {}
                    if self.env['hr.department'].search([("number_hit", "=", i)]):
                        # Lay ten quan ly cua phong ban hien tai
                        manager = "None"
                        if depart.manager_id:
                            manager = self.env['hr.employee'].search([('id', '=', depart.manager_id.id)]).name
                        # dict bieu dien thong tin hien tai cua phong ban
                        child['text'] = {
                            'name': depart.name,
                            'title': "Manager: " + manager,
                        }
                        if self.env['hr.department'].search([("number_hit", "=", i + 1)]):
                            node_child = self.env['hr.department'].search([("number_hit", "=", i + 1)])
                            # Kiem tra phong ban hien tai con phong ban nho hon hay ko
                            child['children']=[]
                            for c in node_child:
                                if c.parent_id == depart:
                                    child['stackChildren'] = True
                                    child['children'].append(get_inf(self, c, i+1))

                    return child
                node_structure['children'].append(get_inf(self, depart, a))

        chart_config['nodeStructure'] = node_structure
        return chart_config


class ActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    view_mode = fields.Selection(selection_add=[('myview', "MyView")])


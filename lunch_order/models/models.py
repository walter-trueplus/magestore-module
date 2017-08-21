# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
from odoo import exceptions


class my_lunch(models.Model):
    _name = 'my.lunch.order'

    date = fields.Date('Select date', default=fields.Date.today())
    user_id = fields.Many2one('res.users', 'User name', required=True)
    menu_id = fields.Many2one('my.menu.of.day', 'Select menu')
    list_food = fields.Text('List of food', readonly=True, compute='onchange_menu_id')
    total = fields.Float('Total price', readonly=True, related='menu_id.total')

    # onchange date => change menu_id
    @api.onchange('date')
    def onchange_date(self):
        self.menu_id = None
        self.list_food = None
        self.total = None
        if self.date:
            menu_obj = self.env['my.menu.of.day'].search([('date', '=', self.date)])
            res = {}
            if menu_obj:
                ids = menu_obj.ids
                res['domain'] = {'menu_id': [('id', 'in', ids)]}
                return res
            else:
                res['domain'] = {'menu_id': [('id', 'in', [])]}
                return res

    @api.onchange('menu_id')
    def onchange_menu_id(self):
        list = ''
        for r in self:
            if r.menu_id:
                menu_obj = self.env['my.menu.of.day'].search([('menu_name', '=', r.menu_id.menu_name)])
                if menu_obj:
                    for i in range(len(menu_obj.order_line)):
                        list += menu_obj.order_line[i].product_id.name
                        list += ': '
                        list += unicode(menu_obj.order_line[i].product_id.product_price)
                        list += '\n'
                    r.list_food = list

    @api.multi
    def name_get(self):
        result = []
        for r in self:
            name = u'%s' % (u'Lunch Order %s' % (r.id))
            result.append((r.id, name))

        return result

class my_menu_of_day(models.Model):
    _name = 'my.menu.of.day'

    order_line = fields.One2many('my.lunch.order.line', 'order_id', 'List of food')
    date = fields.Date(default=fields.Date.today())
    total = fields.Float('Total', readonly=True, compute='onchange_order_line')
    menu_name = fields.Integer('Menu', required=True, help='Enter a number in this field')

    @api.depends('order_line')
    def onchange_order_line(self):
        temp = 0.00
        for r in self:
            rs = r.order_line
            for i in range(len(rs)):
                temp += rs[i].price
            r.total = temp
            temp = 0.00

    @api.multi
    def name_get(self):
        result = []
        for r in self:
            name = u'%s' % (u'Menu %s' % (r.menu_name))
            result.append((r.id, name))

        return result

    _sql_constraints = [
        ('menu_name',
         'UNIQUE (menu_name)',
         'Menu must be unique!')
    ]


class my_lunch_order_line(models.Model):
    _name = 'my.lunch.order.line'

    product_id = fields.Many2one('my.lunch.product', 'Product')
    price = fields.Float('Price', readonly=True, related='product_id.product_price')
    note = fields.Char('Note')
    order_id = fields.Many2one('my.menu.of.day', 'Order', ondelete='cascade', required=True)


class my_lunch_product(models.Model):
    _name = 'my.lunch.product'

    name = fields.Char('Product', required=True)
    description = fields.Text('Description')
    product_price = fields.Float('Price')

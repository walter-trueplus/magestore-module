# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import AccessError, ValidationError


class my_lunch(models.Model):
    _name = 'my.lunch.order'

    date = fields.Date('Select Date', default=fields.Date.today(), required=True)
    user_id = fields.Many2one('res.users', 'User Name', required=True)
    menu_id = fields.Many2one('my.menu.of.day', 'Select Menu', required=True)
    list_food = fields.One2many('my.lunch.order.line', 'List of Food', readonly=True,
                                related='menu_id.order_line')
    total = fields.Float('Total Price', readonly=True, related='menu_id.total')
    cashmove = fields.One2many('my.lunch.cashmove', 'order_id', 'Cash Move')
    state = fields.Selection([('new', 'New'),
                              ('confirmed', 'Received'),
                              ('ordered', 'Ordered'),
                              ('cancelled', 'Cancelled')],
                             'Status', readonly=True, index=True, default='new')

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

    @api.multi
    def name_get(self):
        result = []
        for r in self:
            name = u'%s' % (u'Lunch Order %s' % (r.id))
            result.append((r.id, name))

        return result

    @api.constrains('date')
    def constrains_date(self):
        today = fields.Datetime.now()
        if self.date < fields.Datetime.from_string(today).strftime("%Y-%m-%d"):
            raise ValidationError('The date of your order is in the past.')

    @api.one
    def order(self):
        if self.user_has_groups("lunch_order.group_my_lunch_manager"):
            self.state = 'ordered'
        else:
            raise AccessError(_("Only your lunch manager processes the orders."))

    @api.one
    def confirm(self):
        if self.user_has_groups("lunch_order.group_my_lunch_manager"):
            if self.state != 'confirmed':
                values = {
                    'user_id': self.user_id.id,
                    'amount': -self.total,
                    'order_id': self.id,
                    'state': 'order',
                    'date': self.date,
                }
            self.env['my.lunch.cashmove'].create(values)
            self.state = 'confirmed'
        else:
            raise AccessError(_("Only your lunch manager sets the orders as received."))

    @api.one
    def cancel(self):
        if self.user_has_groups("lunch_order.group_my_lunch_manager"):
            self.state = 'cancelled'
            self.cashmove.unlink()
        else:
            raise AccessError(_("Only your lunch manager cancels the orders."))


class my_menu_of_day(models.Model):
    _name = 'my.menu.of.day'

    order_line = fields.One2many('my.lunch.order.line', 'order_id', 'List of food')
    date = fields.Date(default=fields.Date.today(), required=True)
    total = fields.Float('Total', readonly=True, compute='onchange_order_line')
    menu_name = fields.Char('Menu', required=True, help='Enter a number in this field')

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

    @api.constrains('menu_name')
    def check_menu_name_is_unique(self):
        menu_of_day = self.search([])
        for r in menu_of_day:
            if self.id != r.id:
                if self.menu_name == r.menu_name:
                    raise ValidationError('Menu must be unique!')


class my_lunch_order_line(models.Model):
    _name = 'my.lunch.order.line'

    product_id = fields.Many2one('product.template', 'Product', domain=[('is_food', '=', True)])
    price = fields.Float('Price', readonly=True, related='product_id.list_price')
    note = fields.Char('Note')
    order_id = fields.Many2one('my.menu.of.day', 'Order', ondelete='cascade', required=True)


class my_lunch_cashmove(models.Model):
    _name = 'my.lunch.cashmove'

    user_id = fields.Many2one('res.users', 'User',
                              default=lambda self: self.env.uid)
    date = fields.Date('Date', required=True, default=fields.Date.context_today)
    amount = fields.Float('Amount', required=True,
                          help='Can be positive (payment) or negative (order or '
                               'payment if user wants to get his money back)')
    order_id = fields.Many2one('my.lunch.order', 'Order', ondelete='cascade')
    state = fields.Selection([('order', 'Order'), ('payment', 'Payment')],
                             'Is an order or a payment', default='payment')

    @api.multi
    def name_get(self):
        return [(cashmove.id, '%s %s' % (_('Lunch Cashmove'), '#%d' % cashmove.id)) for cashmove in self]


class my_lunch_product(models.Model):
    _inherit = 'product.template'

    is_food = fields.Boolean('Is Food', default=False)

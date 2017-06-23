# -*- coding: utf-8 -*-
__author__ = 'Magestore'

from odoo import models, fields, api, exceptions, _
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
import os


class StockNotificationSendMail(models.Model):
    _name = 'stock.notification.send.mail'

    def _get_current_minimum_quant(self):
        stock_noti_obj = self.search([])
        stock_minimum_quant = None
        if stock_noti_obj:
            stock_minimum_quant = stock_noti_obj['minimum_quant']
        return stock_minimum_quant

    def _get_current_email_address(self):
        stock_noti_obj = self.search([])
        mail_add = None
        if stock_noti_obj:
            mail_add = stock_noti_obj['email_address']
        return mail_add

    @api.model
    def name_get(self):
        result = []
        for r in self:
            name = u'%s' % (u'Config')
            result.append((r.id, name))

        return result

    @api.model
    def create(self, vals):
        obj = self.env['stock.notification.send.mail'].search([('id', '>', 0)])
        for r in obj:
            r.unlink()
        return super(StockNotificationSendMail, self).create(vals)

    def _check_minimum_quant(self):
        stock_quant_obj = self.env['stock.quant'].search([('id', '>', 0)])
        mail_mail_obj = self.env['mail.mail']
        mail_content = []
        body_html = ''
        mail_to = ''
        if stock_quant_obj:
            stock_noti_obj = self.env['stock.notification.send.mail'].search([('id', '>', 0)])
            for r in stock_quant_obj:
                quant = self.env['stock.quant'].search([('id', '=', r.id)])
                qty = quant['qty']

                res_users_obj = self.env['res.users'].search([('id', '=', self._uid)])

                if qty and stock_noti_obj:
                    if stock_noti_obj['minimum_quant'] > int(qty):

                        # create and send mail
                        body_html+= 'Product: %s, the current quantity in stock: %s<br/> ' % (r.product_id.product_tmpl_id.name,
                                                                                     int(qty))

                        if stock_noti_obj['email_address']:
                            mail_to = stock_noti_obj['email_address']

                        else:
                            mail_to = res_users_obj.email
            body_html+= 'less than minimum quantity: %s' % (stock_noti_obj['minimum_quant'])
            mail_content.append(mail_mail_obj.create({
                'subject': 'Notification',
                'email_to': mail_to,
                'body_html': body_html
            }))
            mail_mail_obj.send(mail_content)

    minimum_quant = fields.Integer('Minimum Quantity in Stock', required=True, default=_get_current_minimum_quant)
    email_address = fields.Char('Email Address', default=_get_current_email_address)

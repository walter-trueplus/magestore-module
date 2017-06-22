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
        query = "DELETE FROM stock_notification_send_mail WHERE id >= 0"
        res = self._cr.execute(query)
        if res == None:
            return super(StockNotificationSendMail, self).create(vals)

    def _check_minimum_quant(self):
        query = "SELECT SUM(qty) AS sum_qty FROM stock_quant"
        self._cr.execute(query)
        total_quant = self._cr.dictfetchone()
        sum_qty = total_quant['sum_qty']

        query2 = "SELECT minimum_quant, email_address FROM stock_notification_send_mail snsm order by snsm.id desc LIMIT 1"
        self._cr.execute(query2)
        stock_noti_obj = self._cr.dictfetchone()

        mail_mail_obj = self.env['mail.mail']
        res_users_obj = self.env['res.users'].search([('id', '=', self._uid)])
        mail_content = []
        if sum_qty != None and stock_noti_obj != None:
            if stock_noti_obj['minimum_quant'] > int(sum_qty):

                # create and send mail
                if stock_noti_obj['email_address'] == None:
                    mail_content.append(mail_mail_obj.create({
                        'email_to': res_users_obj.email,
                        'body_html': '<pre><span class="inner-pre" style="font-size: 15px">'
                                     'Số lượng sản phẩm hiện tại trong kho là %s, '
                                     'nhỏ hơn số lượng tối thiểu là %s</span></pre>' % (
                                         int(sum_qty), stock_noti_obj['minimum_quant'])
                    }))
                    mail_mail_obj.send(mail_content)
                else:
                    mail_content.append(mail_mail_obj.create({
                        'email_to': stock_noti_obj['email_address'],
                        'body_html': '<pre><span class="inner-pre" style="font-size: 15px">'
                                     'Số lượng sản phẩm hiện tại trong kho là %s, '
                                     'nhỏ hơn số lượng tối thiểu là %s</span></pre>' % (
                                         int(sum_qty), stock_noti_obj['minimum_quant'])
                    }))
                    mail_mail_obj.send(mail_content)

    minimum_quant = fields.Integer('Minimum Quantity in Stock', required=True, default=_get_current_minimum_quant)
    email_address = fields.Char('Email Address', default=_get_current_email_address)

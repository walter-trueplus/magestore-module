# -*- coding: utf-8 -*-
{
    'name': "Stock notification send mail",

    'description': """
        - Add a minimum_quant field to the stock notification send mail to check the minimum quantity for the product.
        - Add an email_address field to the stock notification send mail to send an email to that email (if left blank, it will email the logged in user).
        - Only managers are set minimum_quant and email_address. Users is only seen.
    """,

    'author': "Magestore",

    'website': "http://www.magestore.com",

    'depends': ['base', 'stock', 'project'],

    'data':[
        'security/stock_notification_send_mail_security.xml',
        'security/ir.model.access.csv',
        'views/stock_notification_send_mail.xml',
    ],

    'application': True,
}
# -*- coding: utf-8 -*-
{
    'name': "sale_order_send_mail",

    'description': """
        The module overrides the send button in the sale order
        and its purpose is to allow the person to accept or reject
        the order by clicking on the link in the mail.
    """,

    'author': "magestore.com",

    'website': "http://www.magestore.com",

    'depends': ['base', 'sale', 'mail'],

    'data': [
        'data/email_template_edi_sale_custom.xml'
        # 'security/ir.model.access.csv',
    ],
}
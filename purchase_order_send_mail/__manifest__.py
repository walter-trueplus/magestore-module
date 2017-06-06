# -*- coding: utf-8 -*-
{
    'name': "purchase_order_send_mail",

    'description': """
        The module overrides the send button in the purchase order
        and its purpose is to allow the person/company to accept or reject
        the order by clicking on the link in the mail.
    """,

    'author': "Magestore",

    'website': "http://www.magestore.vn",

    'depends': ['base', 'purchase', 'mail', 'stock'],

    'data': [
        # 'security/ir.model.access.csv',
        'data/email_template_edi_purchase_custom.xml',
        # 'views/templates.xml',
    ],
}
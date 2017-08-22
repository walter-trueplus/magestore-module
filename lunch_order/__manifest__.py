# -*- coding: utf-8 -*-
{
    'name': "Lunch order",

    'description': """
        + Lunch order.
    """,

    'author': "magestore.com",
    'website': "http://www.magestore.com",

    'depends': ['base', 'product'],

    'data': [
        'security/lunch_order_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'application': True,
}
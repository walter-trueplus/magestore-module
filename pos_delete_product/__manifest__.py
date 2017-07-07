# -*- coding: utf-8 -*-
{
    'name': "POS delete product",

    'description': """
         Can delete POS order line immediately:
        + Add delete icon in POS order line.
        + Click delete, the POS order line is deleted, need not to delete by quantity.
    """,

    'author': "Magestore",

    'website': "http://www.magestore.com",

    'depends': ['base', 'point_of_sale'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],

    'application': True,
    'qweb': ['static/src/xml/pos_template_custom.xml'],
}
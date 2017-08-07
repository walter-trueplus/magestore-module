# -*- coding: utf-8 -*-
{
    'name': "POS edit product",

    'description': """
         Can edit qty of POS order line:

        + Add 'edit' icon in POS order line.
        + Click 'edit' icon, can edit the qty of product.
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

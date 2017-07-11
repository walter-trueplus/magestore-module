# -*- coding: utf-8 -*-
{
    'name': "POS add note",

    'description': """
        Can add additional note to POS order in POS screen:

        + Add free text box for additional note.
        + Additional note will be displayed in bill.
    """,

    'author': "Magestore",

    'website': "http://www.magestore.com",

    'depends': ['base', 'point_of_sale'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],

    'application': True,
    'qweb': ['static/src/xml/pos_template_custom_add_note.xml'],
}

# -*- coding: utf-8 -*-

{
    'name': 'Web Export Current View',
    'version': '10.0.1.0.0',
    'category': 'Web',
    'author': 'Henry Zhou, Agile Business Group, \
            Odoo Community Association (OCA)',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    'depends': [
        'web','hr'
    ],
    "data": [
        'views/web_export_view_view.xml',
        'views/inherit_employee_treeview.xml',
        'views/inherit_contact_treeview.xml',
    ],
    'qweb': [
        "static/src/xml/web_export_view_template.xml",
    ],
    'installable': True,
    'auto_install': False,
}

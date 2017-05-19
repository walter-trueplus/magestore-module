# -*- coding: utf-8 -*-

{
    'name': 'Download Employee',
    'version': '1.0.0',
    'category': 'Tools',
    'sequence': 2,
    'author': 'Magestore',
    'website': 'http://www.magestore.com',
    'summary': 'Export Contact',
    'description': """This module allow user to export employee to vCard file and download directly""",
    'depends': ['hr'
    ],
    'data': [
        'wizard/export_employee_vcard.xml',
        'wizard/button_export_in_detail_view.xml',
    ],
    'sequence': 2,
    'application': True,
    'installable': True,
    'auto_install': False,
}

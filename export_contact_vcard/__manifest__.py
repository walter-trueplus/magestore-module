# -*- coding: utf-8 -*-

{
    'name': 'Download contact',
    'version': '1.0.0',
    'category': 'Tools',
    'sequence': 2,
    'author': 'Magestore',
    'website': 'http://www.magestore.com',
    'summary': 'Export Contact',
    'description': """This module allow user to export contact to vCard file and download directly""",
    'depends': ['base'],
    'data': [
        'wizard/export_contact_vcard.xml',
        'wizard/button_export_in_detail_view.xml',
    ],
    'qweb': ['static/src/xml/qweb.xml'],
    'sequence': 2,
    'application': True,
    'installable': True,
    'auto_install': False,
}

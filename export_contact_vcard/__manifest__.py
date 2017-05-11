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
    'depends': [
    ],
    'data': [
        'wizard/export_contact_vcard.xml',
        'wizard/button_export_in_detail_view.xml',
    ],
    'sequence': 2,
    'application': False,
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

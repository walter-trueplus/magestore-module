# -*- coding: utf-8 -*-
{
    'name': "export_calendar",

    'description': """
        this module allow user export vcalendar to import at orther device
    """,

    'author': "Magestore.vn",
    'website': "http://www.magestore.vn",

    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','calendar'],

    # always loaded
    'data': [
        'wizard/button_export.xml',
        'wizard/export_calendar.xml',
    ],
     'application': True,
}
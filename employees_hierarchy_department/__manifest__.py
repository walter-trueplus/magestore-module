# -*- coding: utf-8 -*-
{
    'name': "Employees Hierarchy Department",

    'description': """
        Make department have hierarchy and draw simple chart.
    """,

    'author': "Magestore",
    'website': "http://www.magestore.com",

    'depends': ['base', 'hr', 'web'],

    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'application': True,
    'qweb': ['static/src/xml/hierarchy_department.xml'],
}
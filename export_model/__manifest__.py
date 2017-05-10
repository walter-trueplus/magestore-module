# -*- coding: utf-8 -*-
# edited by mars
{
    'name': "Export Model",
    'summary': """Export Model""",
    'description': """Exporting any model""",
    'author': "Magestore",
    'website': "http://www.magestore.com",
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/export_model_views.xml',
    ],
    'application': True,
}
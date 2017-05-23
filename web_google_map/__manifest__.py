# -*- coding: utf-8 -*-

{
    'name': 'Web Google Map',
    'version': '0.5.0',
    'category': 'Added functionality / Widgets',
    'description': """

    <field name="map" widget="gmap" />


""",
    'author': 'simplee.fr - Infosreda LLC',
    'website': '=.=',
    'depends': ['base', 'web'],
    'data': [
        'views/template.xml',
        'views/gmap_view.xml',
    ],
    'update_xml': [],
    'active': True,
    'web': True,
    'qweb': ['static/src/xml/base.xml', ],
    'images': ['images/map.png', ],
}

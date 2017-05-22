{
    'name': 'black list vendor',
    'depends': ['base','purchase','contacts'],
    'desciption': 'Notify while create purchase order in case the vendor in black list',
    'data': [
        'view/vendor_view.xml',
        'view/setting.xml'
    ],
    'application': True,

}

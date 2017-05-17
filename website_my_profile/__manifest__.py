# -*- coding: utf-8 -*-
{
    'name': "My Profiles Website",

    'summary': """
        Create Change Password button and change some properties of My Account page.""",

    'description': """
        This module will adds some property for /my/account page and /web/signup page:
        
        + Add change password button to /my/account page: if that is not first time the user change password,Odoo will direct redirect to /web/reset_password page and the user can change the password directly
        + Add and delete properties of /my/account page
        
            + Delete Company Name and Zip / Postal Code properties
            + Add Gender, Active and Birthday properties

        If you choose reset password from /web/login url, an email will be send to
        your email if your email address is valid, if not: the email will be send to
        mars@trueplus.vn (can change)
        
        If you click Reset Password button in /my/account and it's your first time 
        you reset password, an email will be send to
        your email. 
        If not first time, you will be redirect to /web/reset_password?reset_directly=directly""",

    'author': "magestore.com",
    'website': "magestore.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'website_portal', 'auth_signup', 'mail', 'fetchmail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    'application': True,
}

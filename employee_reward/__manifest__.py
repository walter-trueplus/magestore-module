# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Employee Rewards',
    'version' : '1.0',
    'summary': 'Employee Rewards',
    'sequence': 30,
    'description': """Employee Rewards module
    """,
    'category': 'Rewards',
    'website': 'https://www.magestore.com',
    'images' : [''],
    'depends' : ['base_setup', 'hr_recruitment', 'hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/employee-reward-template.xml',
        'views/message-point.xml',
        'views/jobtitle-point.xml',
        'views/quality.xml',
        'views/reward.xml',
        'views/redeem-management.xml',
        'views/user_point.xml',
        'views/user_reward.xml',
        'views/user_reward_history.xml',
        'views/message.xml',
        'views/my_profile.xml',
        'views/top_receive_point.xml',
        'views/top_send_point.xml',
        'data/cron_reset_point.xml',
        'views/manage-wall-message.xml',
    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "SMS 2-way integration",
    'category': 'Extra Tools',
    'summary': """Send sms 2 way integration.""",
    'version': '15.0.0.1',
    'author': "",
    'website': 'https://www.candidroot.com/',
    'sequence': 2,
    'description': """This module allows you to send sms using api""",
    'depends': ["marketing_automation", "sms"],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'qweb': [],
    'images' : ['static/description/banner.png'],
    'installable': True,
    'live_test_url': 'https://youtu.be/XTBuZzlva3I',
    'currency': 'USD',
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

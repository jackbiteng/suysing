# -*- coding: utf-8 -*-
{
    'name' : 'Google Drive API Integration',
    'version' : '15.0.2',
    'summary': 'Read Google Drive Files using API',
    'sequence': 100,
    'description': """
        Read Files From Google Drive Folder and Dump into Odoo
        =====================
        - Lead
    """,
    'category': 'Sales',
    'author': 'IshanOdooApps',
    'website': 'https://ishanodooapps.in/googledriveintegration',
    'depends' : ['sale_management', 'crm', 'sales_team'],
    'data': [
        'security/drive_security.xml',
        'security/ir.model.access.csv',
        'data/lead_cron.xml',
        'views/drive_reading_history_views.xml',
        'views/drive_config_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
    'external_dependencies': {
        'python': ['google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib']
    },
}

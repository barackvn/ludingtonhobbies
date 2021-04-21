# -*- coding: utf-8 -*-
{
    'name': "Manage Employee",

    'summary': """
        This module is developed to manage the employees check in
        and check out and sending notifications to manager""",

    'description': """
        This module is developed to manage the employees check in
        and check out and sending notifications to manager
    """,

    'author': "Fazal Ur Rahman",
    'category': 'Extra Tools',
    'version': '13.0.0.1',

    'depends': ['base', 'hr', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}

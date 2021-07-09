# -*- coding: utf-8 -*-
{
    'name': "Purchase Mail",

    'summary': """
        This module is developed to add the functionality of sending
        a report with the purchase mail that is being sent.""",

    'description': """
        This module is developed to add the functionality of sending
        a report with the purchase mail that is being sent.
    """,

    'author': "Fazal Ur Rahman",
    'category': 'Extra Tools',
    'version': '14.0.0.1',

    'depends': ['base', 'purchase', 'report_xlsx'],

    'data': [
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

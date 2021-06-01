# -*- coding: utf-8 -*-
{
    'name': "Open Special Orders",

    'summary': """
        This module is developed to add the functionality of sending the
        mails daily with the special orders data report.""",

    'description': """
        This module is developed to add the functionality of sending the
        mails daily with the special orders data report.
    """,

    'author': "Fazal Ur Rahman",
    'category': 'Extra Tools',
    'version': '13.0.0.1',

    'depends': ['base', 'purchase'],

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

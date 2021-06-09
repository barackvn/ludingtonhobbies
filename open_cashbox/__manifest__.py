# -*- coding: utf-8 -*-
{
    'name': "Open Cash Box",

    'summary': """
        This module is developed to add the button for opening the cash
        box from the point of sale sessions form view.""",

    'description': """
        This module is developed to add the button for opening the cash
        box from the point of sale sessions form view.
    """,

    'author': "Fazal Ur Rahman",
    'category': 'Extra Tools',
    'version': '13.0.0.1',

    'depends': ['base', 'point_of_sale'],

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

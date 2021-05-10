# -*- coding: utf-8 -*-
{
    'name': "Replenishment Task",

    'summary': """
        This module is developed to handle the customized requirements
        related to the product replenishment.""",

    'description': """
        This module is developed to handle the customized requirements
        related to the product replenishment.
    """,

    'author': "Fazal Ur Rahman",
    'category': 'Extra Tools',
    'version': '13.0.0.1',

    'depends': ['base', 'stock', 'purchase'],

    'data': [
        'security/ir.model.access.csv',
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

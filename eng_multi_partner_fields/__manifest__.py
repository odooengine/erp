# -*- coding: utf-8 -*-
{
    'name': "Multi Payment Partner Fields",

    'summary': """
        Make A Select Field On Res Partner""",

    'description': """
        Make A Select Field On Res Partner with Four Respective Values
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Base',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/partner_views.xml',
    ],

}

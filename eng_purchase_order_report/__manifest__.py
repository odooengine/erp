# -*- coding: utf-8 -*-
{
    'name': "Purchase Order Report",

    'summary': """
        This Module Prints Purchase Order Report """,

    'description': """
        This Module Prints Purchase Order Report
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'views/views.xml',
        'reports/purchase_report.xml',
        'reports/purchase_template.xml',
    ],

}

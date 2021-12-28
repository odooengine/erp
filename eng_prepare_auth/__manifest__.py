# -*- coding: utf-8 -*-
{
    'name': "Engine Prepare Auth Reports",

    'summary': """
        Add A Row with Prepare and Auth On Multiple Reports""",

    'description': """
        Add A Row with Prepare and Auth On Multiple Reports. Invoice, Bill, Sale, Purchase, Manufacturing and Payments
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'All',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'stock', 'sale', 'purchase', 'mrp', 'manager_all_approvals'],

    # always loaded
    'data': [
        'reports/invoice_report.xml',
        'reports/mrp_report.xml',
        'reports/payment_report.xml',
        'reports/purchase_report.xml',
        'reports/sale_report.xml',
        'reports/stock_report.xml',
    ],

}

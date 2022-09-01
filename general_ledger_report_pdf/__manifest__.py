# -*- coding: utf-8 -*-
{
    'name': "General Ledger PDF",

    'summary': """
        General Ledger PDF""",

    'description': """
        General Ledger PDF
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'account',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_reports'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/general_report_wizard.xml',
        'report/sale_report.xml',
        'views/views.xml',
    ],

}

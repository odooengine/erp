# -*- coding: utf-8 -*-
{
    'name': "sale_home_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'report/report.xml',
        'report/custom_header_footer.xml',
        'report/sale_report_hic.xml',
        'report/invoice_report_hic.xml',
        'report/report_hic.xml',
        'report/payment_report_hic.xml',
        'report/custom_header_footer_hic_ntn.xml',
        'report/custom_header_footer_ntn.xml',
        'report/sale_report_with_ntn_hic.xml',
        'report/sale_report_ntn.xml',
        'report/invoice_report_with_ntn_hic.xml',
        'report/invoice_report_ntn.xml',
        # 'report/delivery_slip_hic.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}

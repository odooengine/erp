# -*- coding: utf-8 -*-
{
    'name': "Xpath Fields",

    'summary': """
        Show Fields In Header of Sale Purchase Inventory""",

    'description': """
        Show Fields In Header of Sale Purchase Inventory from Notebook Pages
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'All',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase', 'stock', 'sale_stock', 'mrp', 'account'],

    # always loaded
    'data': [
        'views/stock_sale_purchase_account_mrp_views.xml',
    ],

}

# -*- coding: utf-8 -*-
{
    'name': "Product Format",

    'summary': """
        Add New Menus In Product Under Configuration and Generate the Product Code """,

    'description': """
        Add New Menus In Product Under Configuration and Generate the Product Code
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '14.0.0.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product', 'mail', 'stock_account', 'mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/server.xml',
        'security/security.xml',
        'views/accessories_type_views.xml',
        'views/age_group_views.xml',
        'views/calender_season_views.xml',
        'views/class_views.xml',
        # 'views/department_views.xml',
        'views/item_category_views.xml',
        'views/item_sub_category_views.xml',
        'views/life_type_views.xml',
        'views/line_item_views.xml',
        'views/mrp_views.xml',
        'views/product_group_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/size_views.xml',
        'views/stock_views.xml',
        # 'views/sub_department_views.xml',
        'views/year_views.xml',
    ],

}

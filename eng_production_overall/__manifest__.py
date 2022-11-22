# -*- coding: utf-8 -*-
{
    'name': "Engine Production",

    'summary': """
        Production""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Atif",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'stock', 'purchase', 'product', 'material_purchase_requisitions', 'hr', 'eng_product_format', 'manager_all_approvals'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/production_view.xml',
        'wizard/produced_wizard.xml',
        'views/picking_views.xml',
    ],

}

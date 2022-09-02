# -*- coding: utf-8 -*-
{
    'name': "Engine BOM Approval",

    'summary': """
        This Module Will Create BOM Approval With One Approval""",

    'description': """
        This Module Will Create BOM Approval With One Approval
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/bom_approval_views.xml',
    ],

}

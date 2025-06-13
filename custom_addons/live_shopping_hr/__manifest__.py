# -*- coding: utf-8 -*-
{
    'name': "Casa&Biouty Live Shopping Beta",

    'summary': "Gestion de live online",

    'description': """
Module de gestion de live et d'achat de produit online .
    """,

    'author': "Casa&Biouty",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Timesheets',
    'version': '1.2',

    'installable': True,
    "application": True,
    
    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'uom', 'sale', 'purchase','account'],

    # always loaded
    'data': [
        'security/group_users.xml',
        'security/ir.model.access.csv',
        'data/ir.sequence.xml',
        'wizards/search_product_wizard.xml',
        'views/menu_view.xml',
        'views/res_company_custom_view.xml',
        'views/live_shopping_view.xml',
        'report/barcode_label_report.xml',
        'report/ticket_invoice_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'license': 'LGPL-3',
}


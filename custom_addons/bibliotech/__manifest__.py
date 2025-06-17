# -*- coding: utf-8 -*-
{
    'name': "Bibliotech",

    'summary': "Application de gestion de module",

    'description': """
Module d'application de gestion de livre
    """,

    'author': "Bibliotech Company",
    'website': "https://www.yourcompany.com",

    'application': True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    "data": [
        "security/livre_security.xml",
        "security/ir.model.access.csv",
        "views/category_view.xml",
        "views/livre_view.xml",
        "views/menu_view.xml",
        "reports/fiche_lecture.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

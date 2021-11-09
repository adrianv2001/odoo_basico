# -*- coding: utf-8 -*-
{
    'name': "odoo_basico",

    'summary': """
        Módulo 2 de Odoo, Agrupamientos y Filtros""",

    'description': """
        Agrupamientos de informacion para ver los datos en la cista tree colapsados por el valor de un campo
        Filtros de informacion para filtrar los valores de una tabla depeniendo de las condiciones que definamos
    """,

    'author': "Adrian Vidal",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/informacion.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

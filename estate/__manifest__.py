# -*- coding: utf-8 -*-
{
    'name': 'Real Estate',
    'version': '1,0',
    'author': 'Aisha Aboalatta',
    'company': 'Asasat Advanced Systems',
    'depends': ['base_setup'],
    'data': ['security/ir.model.access.csv',
             'views/estate_property_views.xml',
             'views/estate_property_type_views.xml',
             'views/estate_property_tag_views.xml'
             ],
    'installable': True,
    'application': True,
}

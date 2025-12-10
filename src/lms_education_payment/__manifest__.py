# -*- coding: utf-8 -*-

{
    'name': 'Education',
    'version': '1.0',
    'depends': ['lms_education', 'lms_payment'],
    'auto_install': ['lms_education', 'lms_payment'],

    'data': [
        'security/ir.model.access.csv',



    ],
    'installable': True,
    'application': True,
}

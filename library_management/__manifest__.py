{
    'name': "Library Management System",
    'author': "Mohamed Hassan",
    'category': '',
    'version': '17.0.1',
    'depends': ['base','mail'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/library_book_view.xml',
        'views/library_loan_view.xml',
        'views/library_dashboard_view.xml',
        'views/res_partner_view.xml',
        'reports/loan_report.xml',
    ],
    'application': True,
}
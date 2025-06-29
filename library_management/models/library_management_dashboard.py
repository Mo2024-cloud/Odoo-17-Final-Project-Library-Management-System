from odoo import models, fields, api
from datetime import timedelta


class LibraryManagementDashboard(models.TransientModel):
    _name = 'library.management.dashboard'
    _description = 'Library Management Dashboard'

    overdue_loan_ids = fields.Many2many('library.loan', compute='_compute_dashboard_data')
    top_borrowed_book_ids = fields.Many2many('library.book', compute='_compute_dashboard_data')

    def _compute_dashboard_data(self):
        # Get overdue loans (14+ days)
        overdue_loans = self.env['library.loan'].search([
            ('return_date', '<', fields.Date.today()),
            ('status', '=', 'active'),
            ('return_date', '<', (fields.Date.today() - timedelta(days=14)))
        ])

        # Get top 3 borrowed books
        top_books = self.env['library.book'].search([], order='loan_count desc', limit=3)

        self.update({
            'overdue_loan_ids': [(6, 0, overdue_loans.ids)],
            'top_borrowed_book_ids': [(6, 0, top_books.ids)]
        })

    def action_open_overdue_loans(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Overdue Loans',
            'res_model': 'library.loan',
            'view_mode': 'tree,form',
            'domain': [('return_date', '<', fields.Date.today())],
        }

    def action_open_top_books(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Top Borrowed Books',
            'res_model': 'library.book',
            'view_mode': 'tree,form',
        }
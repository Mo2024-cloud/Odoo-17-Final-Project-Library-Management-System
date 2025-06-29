from odoo import models,fields,api
from odoo.exceptions import ValidationError

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Library Loan'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'partner_id'

    borrow_date = fields.Date(tracking=1)
    return_date = fields.Date(tracking=1)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ],default='draft',tracking=True)

    # Relation With library.loan , library.book.line
    book_id = fields.Many2one('library.book', required=True)
    partner_id = fields.Many2one('res.partner', required=True)

    # Action That Handles Draft Button
    def action_draft(self):
        for rec in self:
            rec.status = 'draft'

    # Action That Handles Borrowed Button
    def action_borrowed(self):
        for loan in self:
            if loan.book_id.status == 'borrowed':
                raise ValidationError("Book is already borrowed.")
            loan.status = 'borrowed'
            loan.book_id.status = 'borrowed'
            # for rec in self:
            #     rec.status = 'borrowed'

    # Action That Handles Returned Button
    def action_returned(self):
        self.write({'status':'returned'})
        self.book_id.write({'status':'available'})
        # for rec in self:
        #     rec.status = 'returned'


    # Function to detect overdue loans depend on rec.return_date to Automatic rec.status = 'overdue'
    def check_overdue_loans_date(self):
        loan_ids = self.search([])
        for rec in loan_ids:
            if rec.return_date and rec.return_date < fields.date.today():
                rec.status = 'overdue'
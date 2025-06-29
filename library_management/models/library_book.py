from email.policy import default

from odoo import fields,api,models
from odoo.tools import unique
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _rec_name = 'title'

    title = fields.Char(required=True)
    author = fields.Char()
    isbn = fields.Char(size=13,required=True)
    publication_year = fields.Integer()
    status = fields.Selection([
        ('available','Available'),
        ('borrowed','Borrowed')
    ],default='available')
    active = fields.Boolean(default=True)

    # Relation With library.loan , library.book.line
    loan_ids = fields.One2many('library.loan','book_id')
    line_ids = fields.One2many('library.book.line','book_id')

    loan_count = fields.Integer(compute='_compute_loan_count', string="Times Borrowed", store=True)

    _sql_constraints = [
        ('unique_isbn','unique("isbn")','This ISBN Number Already Exist')
    ]

    # Action That Handles available Button
    def action_available(self):
        for rec in self:
            rec.status = 'available'

    # Action That Handles available Button
    def action_borrowed(self):
        for rec in self:
            rec.status = 'borrowed'

    # Validations and Constrains to detect if ISBN Not Equal 13 Or Not Digit
    @api.constrains('isbn')
    def _check_isbn_length(self):
        for book in self:
            if len(book.isbn) != 13 or not book.isbn.isdigit():
                raise ValidationError("ISBN must be exactly 13 digits.")

    @api.depends('loan_ids')
    def _compute_loan_count(self):
        for book in self:
            book.loan_count = len(book.loan_ids)

class LibraryLine(models.Model):
    _name = 'library.book.line'

    book_id = fields.Many2one('library.book')
    price = fields.Float()
    description = fields.Char()
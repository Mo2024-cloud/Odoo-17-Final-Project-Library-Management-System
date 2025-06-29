from odoo import models,fields,api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_library_member = fields.Boolean()
    loan_ids = fields.One2many('library.loan','partner_id')
    loan_count = fields.Integer(compute='_compute_loan_count')

    def _compute_loan_count(self):
        for partner in self:
            partner.loan_count = self.env['library.loan'].search_count([
                ('partner_id','=',partner.id),
                ('status','in',['borrowed','overdue'])
            ])

    # Function Smart Button on res.partner to view member’s loans
    def action_open_related_loan(self):
        self.ensure_one()

        if len(self.loan_ids) == 1:
            # Single loan - open directly in form view
            return {
                'type': 'ir.actions.act_window',
                'name': 'Library Loan',
                'res_model': 'library.loan',
                'res_id': self.loan_ids.id,
                'view_mode': 'form',
                'target': 'current',
            }
        else:
            # Multiple loans - show tree view
            action = self.env['ir.actions.act_window']._for_xml_id('library_management.library_loan_action')
            action.update({
                'domain': [('id', 'in', self.loan_ids.ids)],
                'context': {'default_book_id': self.id},
            })
            return action
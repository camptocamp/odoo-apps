# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api


class Invoice(models.Model):
    _inherit = "account.invoice"

    def search_duplicate_invoices(self, operator, value):
        query = """
        SELECT id
        FROM account_invoice
        WHERE type = 'in_invoice' AND state !=  'cancel'
        AND (partner_id, amount_total) IN (
            SELECT partner_id, amount_total
            FROM account_invoice
            WHERE type = 'in_invoice' AND state !=  'cancel'
            GROUP BY partner_id, amount_total
            HAVING count(*) %s %s)
        """ % (operator, value)
        self.env.cr.execute(query)
        results = self.env.cr.fetchall()

        return [('id', 'in', sum(results, ()))]

    def _get_duplicate_invoices(self):
        """Retrieve duplicated supplier invoices"""
        for invoice in self:
            dupl_invs = self.search(
                [('id', '!=', invoice.id),
                 ('type', '=', 'in_invoice'),
                 ('partner_id', '=', invoice.partner_id.id),
                 ('amount_total', '=', invoice.amount_total),
                 ('state', '!=', 'cancel')]
            )

            invoice.update({
                'duplicate_invoice_count': len(dupl_invs.ids),
                'duplicate_invoice_ids': dupl_invs.ids})

    @api.multi
    def action_view_duplicate_invoices(self):
        invoices = self.mapped('duplicate_invoice_ids')
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            action['views'] = [(self.env.ref('account.invoice_form').id,
                                'form')]
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    duplicate_invoice_count = fields.Integer(
        string='# Duplicated Invoices',
        compute='_get_duplicate_invoices',
        readonly=True,
        search=search_duplicate_invoices)
    duplicate_invoice_ids = fields.Many2many(
        "account.invoice", string='Duplicate Invoices',
        compute="_get_duplicate_invoices", readonly=True, copy=False)

# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import UserError, AccessError


class Picking(models.Model):
    _inherit = "stock.picking"

    invoice_id = fields.Many2one(
        'account.move',
        string='Vendor Bill',
        readonly=True,
        copy=False,
        help='The vendor bill created from this Goods Receipt Note (GRN).',
    )

    def action_view_vendor_bill(self):
        self.ensure_one()
        if not self.invoice_id:
            raise UserError("No Vendor Bill linked to this picking.")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Vendor Bill',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def set_purchase_move_lines(self):
        purchase_move_lines = []
        for line in self.move_ids:
            # Get quantity done from move lines
            qty_done = sum(line.move_line_ids.mapped('quantity'))
            purchase_move_lines.append((0, 0, {
                'product_id': line.product_id and line.product_id.id or False,
                'quantity': qty_done or 0,
                'price_unit': line.purchase_line_id.price_unit or 0,
                'tax_ids': line.purchase_line_id.taxes_id or False,
                'purchase_line_id': line.purchase_line_id and line.purchase_line_id.id or False,
            }))
        return purchase_move_lines

    def set_purchase_move_info(self):
        purchase_vals = {
            'move_type': 'in_refund',
            'invoice_date': fields.Date.today(),
            'partner_id': self.purchase_id.partner_id and self.purchase_id.partner_id.id or False,
            'currency_id': self.purchase_id.currency_id and self.purchase_id.currency_id.id or False,
            'invoice_line_ids': self.set_purchase_move_lines()
        }
        return purchase_vals

    def action_create_vendor_bill(self):
        if not self:
            return

        # Restrict to Purchase User group only
        if not self.env.user.has_group('bill_from_grn.group_bill_creator'):
            raise AccessError("You do not have the access rights to create a Vendor Bill.")

        # Check all pickings are in 'done' state
        if any(picking.state != 'done' for picking in self):
            raise UserError("All selected pickings must be validated (Done) before creating a vendor bill.")

        purchase = self[0].purchase_id
        if not purchase:
            raise UserError("No related purchase order found.")

        if any(picking.invoice_id and picking.invoice_id.state != 'cancel' for picking in self):
            raise UserError(_("One or more of the selected pickings already have bills."))

        if any(picking.picking_type_code != 'incoming' for picking in self):
            raise UserError("All selected pickings must be incoming shipments.")

        purchase = purchase.with_company(purchase.company_id)
        sequence = 10
        invoice_vals = purchase._prepare_invoice()

        for picking in self:
            for move in picking.move_ids:
                purchase_line = move.purchase_line_id
                if not purchase_line:
                    continue

                # Get quantity done from move lines
                qty_done = sum(move.move_line_ids.mapped('quantity'))

                # Use product UoM rounding for precision
                if float_is_zero(qty_done, precision_rounding=move.product_uom.rounding):
                    continue

                if float_is_zero(purchase_line.qty_to_invoice, precision_rounding=purchase_line.product_uom_id.rounding):
                    continue

                # Convert stock UoM to PO line UoM
                converted_qty = move.product_uom._compute_quantity(
                    qty_done,
                    purchase_line.product_uom_id,
                    round=False
                )

                line_vals = purchase_line._prepare_account_move_line()
                line_vals.update({
                    'quantity': converted_qty,
                    'price_unit': purchase_line.price_unit,
                    'product_uom_id': purchase_line.product_uom_id.id,
                    'sequence': sequence,
                })
                invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                sequence += 1

        if not invoice_vals['invoice_line_ids']:
            raise UserError("No products found to invoice.")

        # Link GRNs to the invoice
        invoice_vals['grn_ids'] = [(6, 0, self.ids)]

        # Create and post the invoice
        invoice = self.env['account.move'].create(invoice_vals)
        # invoice.action_post()

        # Link invoice to each picking
        self.write({'invoice_id': invoice.id})

        # Show the invoice form view
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

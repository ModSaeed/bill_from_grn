from odoo import models, fields, api, _
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import UserError, AccessError

class AccountMove(models.Model):
    _inherit = 'account.move'

    grn_ids = fields.Many2many(
        'stock.picking',
        'account_move_grn_rel',
        'move_id',
        'picking_id',
        string='Related GRNs',
        domain=[('picking_type_code', '=', 'incoming')],
        copy=False,
        help="List of incoming shipments (GRNs) related to this vendor bill.",
    )


    @api.model
    def action_create_combined_vendor_bill(self, grn_ids=None):
        """
        Create a vendor bill from GRNs
        """
        # Restrict to Purchase User group only
        if not self.env.user.has_group('bill_from_grn.group_bill_creator'):
            raise AccessError(_("You do not have the access rights to create a Vendor Bill."))

        grns = self.env['stock.picking'].browse(grn_ids or [])

        if not grns:
            raise UserError(_("Please select at least one GRN"))

        # Validate GRNs
        if grns:
            if any(grn.state != 'done' for grn in grns):
                raise UserError(_("All selected GRNs must be validated (Done) before creating a vendor bill."))

            if any(grn.invoice_id and grn.invoice_id.state != 'cancel' for grn in grns):
                raise UserError(_("One or more of the selected GRNs already have bills not cancelled."))

            if any(grn.picking_type_code != 'incoming' for grn in grns):
                raise UserError(_("All selected pickings must be incoming shipments."))


        # Get purchase order - must be the same for all records
        purchase_orders = (grns.mapped('purchase_id'))
        if len(purchase_orders) > 1:
            raise UserError(_("All selected GRNs must be from the same Purchase Order."))

        purchase = purchase_orders[0] if purchase_orders else False
        if not purchase:
            raise UserError(_("No related purchase order found."))

        # Validate same vendor
        vendors = (grns.mapped('partner_id'))
        if len(vendors) > 1:
            raise UserError(_("All selected records must have the same vendor."))

        purchase = purchase.with_company(purchase.company_id)
        sequence = 10
        invoice_vals = purchase._prepare_invoice()

        # Process GRN lines
        for grn in grns:
            for move in grn.move_ids_without_package:
                purchase_line = move.purchase_line_id
                if not purchase_line:
                    continue

                # Get quantity done from move lines
                qty_done = sum(move.move_line_ids.mapped('quantity'))

                # Use product UoM rounding for precision
                if float_is_zero(qty_done, precision_rounding=move.product_uom.rounding):
                    continue

                if float_is_zero(purchase_line.qty_to_invoice, precision_rounding=purchase_line.product_uom.rounding):
                    continue

                # Convert stock UoM to PO line UoM
                converted_qty = move.product_uom._compute_quantity(
                    qty_done,
                    purchase_line.product_uom,
                    round=False
                )

                line_vals = purchase_line._prepare_account_move_line()
                line_vals.update({
                    'quantity': converted_qty,
                    'price_unit': purchase_line.price_unit,
                    'product_uom_id': purchase_line.product_uom.id,
                    'sequence': sequence,
                })
                invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                sequence += 1

        if not invoice_vals['invoice_line_ids']:
            raise UserError(_("No products found to invoice."))

        # Link both GRNs to the invoice
        if grns:
            invoice_vals['grn_ids'] = [(6, 0, grns.ids)]

        # Create the invoice
        invoice = self.env['account.move'].create(invoice_vals)

        # Link invoice to each GRN
        if grns:
            grns.write({'invoice_id': invoice.id})

        # Show the invoice form view
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }
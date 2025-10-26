# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CombinedBillingWizard(models.TransientModel):
    _name = 'combined.billing.wizard'
    _description = 'Combined Billing Wizard'

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        required=True,
        help='Select the purchase order to create bill from'
    )

    grn_ids = fields.Many2many(
        'stock.picking',
        'combined_billing_grn_rel',
        'wizard_id',
        'picking_id',
        string='GRNs (Goods Receipt Notes)',
        domain="[('purchase_id', '=', purchase_order_id), ('picking_type_code', '=', 'incoming'), ('state', '=', 'done'), '|', ('invoice_id', '=', False), ('invoice_id.state', '=', 'cancel')]",
        help='Select GRNs to include in the vendor bill'
    )


    @api.onchange('purchase_order_id')
    def _onchange_purchase_order(self):
        """Auto-load eligible GRNs when purchase order changes"""
        if self.purchase_order_id:
            # Find eligible GRNs
            eligible_grns = self.env['stock.picking'].search([
                ('purchase_id', '=', self.purchase_order_id.id),
                ('picking_type_code', '=', 'incoming'),
                ('state', '=', 'done'),
                '|',
                ('invoice_id', '=', False),
                ('invoice_id.state', '=', 'cancel')
            ])

            # Auto-select all eligible records
            self.grn_ids = [(6, 0, eligible_grns.ids)]
        else:
            self.grn_ids = [(5, 0, 0)]

    def action_create_bill(self):
        """Create vendor bill from selected GRNs"""
        self.ensure_one()

        if not self.grn_ids:
            raise UserError(_("Please select at least one GRN."))

        return self.env['account.move'].action_create_combined_vendor_bill(
            grn_ids=self.grn_ids.ids
        )
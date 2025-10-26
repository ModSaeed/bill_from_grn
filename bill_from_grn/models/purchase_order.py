# -*- coding: utf-8 -*-

from odoo import models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_create_combined_vendor_bill(self):
        """
        Open wizard to create vendor bill from GRNs
        """
        self.ensure_one()

        # Create wizard with pre-filled purchase order
        wizard = self.env['combined.billing.wizard'].create({
            'purchase_order_id': self.id,
        })

        return {
            'name': _('Create Combined Vendor Bill'),
            'type': 'ir.actions.act_window',
            'res_model': 'combined.billing.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }
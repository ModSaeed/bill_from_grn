# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import UserError


class CombinedBillingFromSelectionWizard(models.TransientModel):
    _name = 'combined.billing.selection.wizard'
    _description = 'Create Bill from Selected GRNs/Services'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        context = self.env.context

        # Get active model and IDs from context
        active_model = context.get('active_model')
        active_ids = context.get('active_ids', [])

        if active_model == 'stock.picking':
            res['grn_ids'] = active_ids

        return res

    def action_create_combined_bill(self):
        """Open wizard to combine with other records or create bill directly"""
        context = self.env.context
        active_model = context.get('active_model')
        active_ids = context.get('active_ids', [])

        # Determine which records we have
        grn_ids = []

        if active_model == 'stock.picking':
            grn_ids = active_ids

        # Get purchase order from the records
        purchase_order = False
        if grn_ids:
            grns = self.env['stock.picking'].browse(grn_ids)
            purchase_order = grns[0].purchase_id if grns else False

        # Open wizard to allow selecting additional records
        wizard = self.env['combined.billing.wizard'].create({
            'purchase_order_id': purchase_order.id if purchase_order else False,
            'grn_ids': [(6, 0, grn_ids)]
        })

        return {
            'name': _('Create Combined Vendor Bill'),
            'type': 'ir.actions.act_window',
            'res_model': 'combined.billing.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }
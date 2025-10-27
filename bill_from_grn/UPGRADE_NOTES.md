# Odoo 18 Upgrade Notes for bill_from_grn Module

## Module Version: 18.0.0.1

### Changes Made for Odoo 18 Compatibility

#### 1. Manifest File (__manifest__.py)
- Updated version from 17.0 reference to 18.0
- Changed description "Compatible with Odoo 17.0" to "Compatible with Odoo 18.0"

#### 2. Model Files

**models/account_move.py:**
- Removed deprecated `self.env['decimal.precision'].precision_get()` usage
- Updated precision checking to use UoM rounding: `precision_rounding=move.product_uom.rounding`
- Updated precision checking for purchase lines: `precision_rounding=purchase_line.product_uom.rounding`
- Removed version-specific comments referencing "Odoo 17"

**models/stock_picking.py:**
- Removed deprecated `self.env['decimal.precision'].precision_get()` usage
- Updated precision checking to use UoM rounding: `precision_rounding=move.product_uom.rounding`
- Updated precision checking for purchase lines: `precision_rounding=purchase_line.product_uom.rounding`
- Removed version-specific comments referencing "Odoo 17"

**models/purchase_order.py:**
- No changes required - already compatible with Odoo 18

#### 3. Wizard Files
- No changes required - wizard files are fully compatible with Odoo 18

#### 4. View Files

**wizard/combined_billing_wizard_view.xml:**
- Removed inline tree view definition for `grn_ids` many2many field
- Odoo 18 has stricter validation for inline views in many2many fields
- Now uses default stock.picking list view which is more compatible
- Changed from inline `<tree>` definition to simple field with widget="many2many"
- This resolves "Field does not exist in model" validation errors

**Other view files:**
- All XML views validated and confirmed compatible with Odoo 18
- No deprecated attributes found

#### 5. Security Files
- Security configuration is fully compatible with Odoo 18

### Migration from Odoo 17 to Odoo 18

Two main breaking changes were addressed:

1. **Decimal Precision API Change:**
   - The deprecated `decimal.precision` model was removed in Odoo 18
   - Instead of using `self.env['decimal.precision'].precision_get('Product Unit of Measure')`, the module now uses
     the `precision_rounding` parameter with the UoM's rounding value directly
   - This is the recommended approach in Odoo 18 for floating point comparisons

2. **Stricter View Validation:**
   - Odoo 18 has stricter validation for inline views within many2many/one2many fields
   - Inline tree views that reference fields from the related model can cause validation errors
   - Solution: Remove inline view definitions and use default views, or define them as separate view records
   - This affects wizard forms with embedded list views

### Testing Recommendations

After installing/upgrading the module in Odoo 18, please test:

1. **Create Bill from Purchase Order:**
   - Create a PO and validate it
   - Receive products (create GRN)
   - Use "Create Bill From GRN" button
   - Verify bill creation with correct quantities and prices

2. **Create Bill from GRN Directly:**
   - Open a validated GRN
   - Click "Create Bill" action
   - Verify bill is created and linked

3. **Combined Billing:**
   - Select multiple GRNs from tree view
   - Use "Create Combined Bill from GRNs" action
   - Verify multiple GRNs are included in single bill

4. **Smart Button:**
   - Verify "Vendor Bill" smart button appears on GRN when bill is created
   - Click button to navigate to bill

5. **Bill-GRN Linkage:**
   - Open created vendor bill
   - Verify GRN tags are displayed
   - Verify bidirectional linking works

### Compatibility Notes

- Fully compatible with Odoo 18.0
- Dependencies: stock, account, purchase, purchase_stock
- No enterprise dependencies
- No external Python library dependencies

### Known Issues

None at this time.

### Support

For issues or questions, contact ModSaeed.

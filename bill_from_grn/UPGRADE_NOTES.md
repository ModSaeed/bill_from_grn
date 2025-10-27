# Upgrade Notes for bill_from_grn Module

## Current Version: 19.0.0.1

---

## Odoo 19 Upgrade (19.0.0.1)

### Changes Made for Odoo 19 Compatibility

#### 1. Manifest File (__manifest__.py)
- Updated version from 18.0.0.1 to 19.0.0.1
- Changed description "Compatible with Odoo 18.0" to "Compatible with Odoo 19.0"

#### 2. View Files

**views/stock_picking_view.xml:**
- Updated `invisible` attribute syntax to use modern Python boolean expressions
- Changed `invisible="invoice_id == False"` to `invisible="not invoice_id"`
- This aligns with Odoo 19's standardized invisible attribute syntax
- Removed `groups_id` field from server action definitions
- In Odoo 19, `ir.actions.server` no longer supports the `groups_id` field
- Security is now handled exclusively in Python code using `has_group()` checks

**views/purchase_order_view.xml:**
- Updated xpath to use more robust positioning
- Changed from `position="after"` on specific button to `position="inside"` on header
- The previous xpath relied on `action_create_invoice` button which may have changed in Odoo 19
- New approach is more resilient to view structure changes

**Other view files:**
- All other XML views validated and confirmed compatible with Odoo 19
- No additional changes required

#### 3. Model Files

**models/stock_picking.py:**
- Replaced `move_ids_without_package` with `move_ids`
- In Odoo 19, `move_ids_without_package` field has been removed from `stock.picking`
- The field `move_ids` now includes all moves regardless of package
- Updated in methods: `set_purchase_move_lines()` and `action_create_vendor_bill()`
- Replaced `purchase_line.product_uom` with `purchase_line.product_uom_id`
- In Odoo 19, purchase order line UoM field changed from Many2one-like to proper Many2one field

**models/account_move.py:**
- Replaced `move_ids_without_package` with `move_ids`
- Updated in method: `action_create_combined_vendor_bill()`
- Replaced `purchase_line.product_uom` with `purchase_line.product_uom_id`
- Field name standardization in Odoo 19

**models/purchase_order.py:**
- No changes required - already compatible with Odoo 19

#### 4. Wizard Files
- All wizard files confirmed compatible with Odoo 19
- No changes required

#### 5. Security Files

**security/groups.xml:**
- Removed `category_id` field from group definitions
- In Odoo 19, the `category_id` field has been removed from `res.groups` model
- Groups no longer support categorization
- This is a breaking change from Odoo 18

### Migration from Odoo 18 to Odoo 19

Key breaking changes addressed in this upgrade:

1. **Group Category Removal:**
   - Odoo 19 removed the `category_id` field from `res.groups` model
   - Groups no longer support categorization
   - Removed all `category_id` field references from group definitions
   - This is a major breaking change that affects all modules defining groups

2. **Server Action Groups Removal:**
   - Odoo 19 removed the `groups_id` field from `ir.actions.server` model
   - Server actions can no longer be restricted by groups in XML definitions
   - Security must now be handled in Python code using `self.env.user.has_group()` checks
   - All `groups_id` references removed from server action records
   - The module already implements proper security checks in Python, so functionality is preserved

3. **View Inheritance Changes:**
   - Odoo 19 may have changed button names and positions in standard views
   - XPath expressions that rely on specific button names can break
   - Best practice: Use more generic xpaths (e.g., `//header` instead of `//header/button[@name='specific_button']`)
   - Changed purchase order view to add button to header directly instead of positioning after a specific button

4. **Stock Picking Field Removal:**
   - Odoo 19 removed the `move_ids_without_package` field from `stock.picking` model
   - All code now uses `move_ids` which includes all moves
   - This affects any code that iterated over stock moves in pickings
   - Changed in both `stock_picking.py` and `account_move.py`

5. **Purchase Order Line Field Rename:**
   - Odoo 19 renamed `product_uom` to `product_uom_id` in `purchase.order.line` model
   - This is part of field name standardization across Odoo
   - All references updated: `purchase_line.product_uom` → `purchase_line.product_uom_id`
   - Changed in both `stock_picking.py` and `account_move.py`

6. **Invisible Attribute Syntax:**
   - Odoo 19 standardizes the `invisible` attribute in views to use clean Python boolean expressions
   - Changed from comparison syntax (`== False`) to boolean syntax (`not field`)
   - This improves readability and follows Odoo's modern view standards

### Compatibility Notes

- Fully compatible with Odoo 19.0
- Dependencies: stock, account, purchase, purchase_stock
- No enterprise dependencies
- No external Python library dependencies
- Backward compatible upgrade path from 18.0.0.1

---

## Previous Version: 18.0.0.1

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

- Fully compatible with Odoo 19.0
- Dependencies: stock, account, purchase, purchase_stock
- No enterprise dependencies
- No external Python library dependencies

### Known Issues

None at this time.

### Support

For issues or questions, contact ModSaeed.

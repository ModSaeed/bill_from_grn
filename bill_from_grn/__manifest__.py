{
    "name": "Bill From GRNs - Purchase Receipt Billing",
    "summary": """
        Create Vendor Bills directly from Goods Receipt Notes (GRNs).
        Link bills to inbound receipts with flexible billing options from
        Purchase Orders or Receipts.
    """,
    "description": """
        Purchase GRN Bill - Advanced Billing Management
        ================================================

        This module streamlines the vendor billing process by enabling direct 
        bill creation from Goods Receipt Notes (GRNs), providing a flexible 
        and efficient way to manage purchase-to-payment workflows.

        Key Features
        ------------
        * **Create Bills from Purchase Orders**: Select one or multiple GRNs 
          from purchase orders to generate consolidated or individual vendor bills

        * **Create Bills from GRNs Directly**: Generate vendor bills directly 
          from the receipt/picking form without navigating to purchase orders

        * **Direct GRN-Bill Linkage**: Maintain clear traceability with direct 
          links between bills and their corresponding receipt documents

        * **Multi-GRN Billing**: Combine multiple receipts into a single bill 
          for consolidated vendor payments

        * **Flexible Workflow**: Choose the billing approach that best fits 
          your business process - either from PO or GRN

        Main Benefits
        -------------
        ✓ Reduces manual data entry and potential errors
        ✓ Improves billing accuracy by linking directly to received quantities
        ✓ Accelerates the accounts payable process
        ✓ Provides better tracking between receipts and bills
        ✓ Supports partial billing scenarios
        ✓ Enables consolidated billing for multiple receipts

        How It Works
        ------------
        **Option 1: From Purchase Order**
        1. Open a Purchase Order
        2. Access the "Create Bill from GRN" option
        3. Select one or multiple GRNs associated with the PO
        4. Generate the bill with automatic quantity and price population

        **Option 2: From GRN/Receipt**
        1. Open a validated Goods Receipt Note (stock picking)
        2. Click "Create Bill" button
        3. Bill is automatically created and linked to the receipt
        4. Review and validate the bill

        Technical Details
        -----------------
        * Compatible with Odoo 18.0
        * Integrates seamlessly with Stock, Purchase, and Accounting modules
        * Maintains data integrity with proper document linking
        * Supports standard Odoo workflows and permissions

        Use Cases
        ---------
        • Manufacturing companies receiving materials in multiple shipments
        • Distributors managing partial deliveries from suppliers
        • Organizations requiring strict matching between receipts and bills
        • Businesses needing consolidated billing for cost efficiency
        • Companies implementing 3-way matching (PO-Receipt-Bill)

        Security
        --------
        Includes dedicated security groups and access rights to control
        bill creation permissions from GRNs.

        Support & Updates
        -----------------
        For support, feature requests, or bug reports, please contact ModSaeed.
        Regular updates ensure compatibility with latest Odoo versions.
    """,
    "version": "18.0.0.1",
    "author": "ModSaeed",
    "website": "",
    "category": "Invoicing",
    "license": "OPL-1",
    "price": 49.00,
    "currency": "EUR",
    "depends": ["stock", "account", "purchase", "purchase_stock"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/stock_picking_view.xml",
        "views/account_move.xml",
        "views/purchase_order_view.xml",
        "wizard/combined_billing_wizard_view.xml"
    ],
    "images": [
        "static/description/banner.png",
        "static/description/icon.png",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
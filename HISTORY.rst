.. :changelog:

.. Template:

.. 0.0.1 (2016-05-09)
.. ++++++++++++++++++

.. **Features and Improvements**

.. **Bugfixes**

.. **Build**

.. **Documentation**

Release History
---------------

latest (unreleased)
+++++++++++++++++++

**Data**
* BSSFL-318: Journal entries

**Features and Improvements**

* BSSFL-462: Payment Terms on the Internal Purchase Order
* BSSFL-461: DN/Invoice today date
* BSSFL-465: Exchange difference move line label

**Bugfixes**

* BIZ-1131: Error validating stock.picking

**Build**

**Documentation**


10.13.0 (2018-01-18)
++++++++++++++++++++

**Data**
* BSSFL-452: Process missing RMA Wait Cust. OK (quotation sent)
* BSSFL-457: Sync RMA, Repair and Sale names

**Features and Improvements**

* BSSFL-446: RMA, repair order and sale order with same name
* BSSFL-453: Install module account_bank_statement_import_camt
* BSSFL-448: Propagate delivery method from SO to DO

**Bugfixes**

* BSSFL-458: Multiple sale orders confirmation
* BSSFL-455: Module instalation account_bank_statement_import_camt incremental
* BSSFL-450: Setting email office 365
* BSSFL-447: Propagate delivery info
* BSSFL-449: Confirm DO with SNs on 2 or more different products

**Build**

**Documentation**


10.12.0 (2018-01-11)
++++++++++++++++++++

**Data**

* BSSFL-445: Serial number history stock moves

**Features and Improvements**

* BSSFL-444: Add notes on serial number
* BIZ-1089: Adaptation du rapport DN-Invoice
* BIZ-1084: Add stock.picking.type column on stock.picking tree view

**Bugfixes**

**Build**

**Documentation**


10.11.1 (2017-12-29)
++++++++++++++++++++

**Data**

* BSSFL-434: Payment mode
* BSSFL-437: Assets data

**Features and Improvements**

**Bugfixes**

* BSSFL-436: Sale order type for inc
* BSSFL-435: Default values for partners
* BSSFL-438: Calculate the invoices amount tax

**Build**

**Documentation**


10.11.0 (2017-12-27)
++++++++++++++++++++

**Data**

* BSSFL-426: Currency rate
* BSSFL-427: Load with S3
* BSSFL-416: Add new taxes

**Features and Improvements**

* BSSFL-429: Repair form design
* BSSFL-418: Settings email
* BSSFL-365: Import repair line
* BSSFL-402: Add date delivered field on DO
* BSSFL-272 : Update res.company to include account cutoff settings
* BSSFL-417: Pay PO to another partner bank account

**Bugfixes**

* BSSFL-431: Cant retrieve lot on stock
* BSSSFL-432: Validate inventory
* BSSFL-420: Generic exception on receive rma data
* BSSFL-430: Invoice compute_sale_orders
* BSSFL-421: No customer phone or mobile, sale exception not found
* BSSFL-425: Add xml_id in sensefly inc partner
* BSSFL-428: Reconfigure RMA routes for both companies

**Build**

**Documentation**


10.10.1 (2017-12-18)
+++++++++++++++++++

**Data**

* BSSFL-405: Reordering Rules

**Features and Improvements**

* BSSFL-413: PO partner reference
* BSSFL-414: Invoice taxes

**Bugfixes**

* BSSFL-408: SO exception rules archive
* BSSFL-409: Update customer payment term
* BIZ-930 All sale order lines must be ready to invoice to set the sale order status as ready to invoice
* BSSFL-410: Update product account

**Build**

**Documentation**


10.10.0 (2017-12-15)
++++++++++++++++++++

**Data**

* BSSFL-287: Add customer invoices data
* BSSFL-381: Run currency update after install
* BSSFL-316: RMA data migration
* BSSFL-397: Inventory categories
* BSSFL-373: Add product accounts data
* BSSFL-392: Add the partners properties data
* BSSFL-396: Add Delivery methode data
* BSSFL-107: Add routing data
* BSSFL-108: Initial stock inventory

**Features and Improvements**

* BSSFL-389: Move drone info into repair order
* BSSFL-242: Add sale order exception rules
* BSSFL-262: Add work order user
* BSSFL-395: Configure Repair locations
* BSSFL-352: Add security group to reset RMAs
* BSSFL-387: Repair state draft and open
* BSSFL-391: Add RMA smart button in repair

**Bugfixes**

* BSSFL-382: Product responsibles
* BSSFL-383: Add S3 read in data_all.py
* BSSFL-394: Product followers
* BSSFL-385: Routes configuration


10.9.1 (2017-12-06)
+++++++++++++++++++

**Features and Improvements**

* BSSFL-379: Fix xmlid __setup__.company_mte
* BIZ-905: Settings Purchase
* BIZ-908: Settings Inventory
* BIZ-909: Settings Accounting


10.9.0 (2017-12-04)
+++++++++++++++++++

**Data**

* Update units of measure data
* Add RMA inventory route

**Features and Improvements**

* Procurement rule Stock -> Packs with 1 day of delay
* RMA closed is readonly
* Update company logo
* Install account_financial_report_qweb module
* Country date formats
* Make team mandatory on PO
* RMA security groups
* Repair report
* Do not install PLM and Quality modules
* Zendesk ticket numbers validation
* BSSFL-306: Create a Sensefly state on sale order

**Bugfixes**

* DN/Invoice report, column delivered quantity alignment
* RMA reception with source document
* Add stock-logistics-warehouse in Dockerfile
* Setting the week period the manufacturing
* Print custom invoice report
* MRP Repair invoicable field not updated
* Pick and Pack picking types active
* RMA open, with product to receive and not to exchange, generates SO line

**Build**

* Update users group in demo mode

**Documentation**


10.8.1 (2017-11-09)
+++++++++++++++++++

**Build**

* Disable a failing test reported to be reported as a bug


10.8.0 (2017-11-09)
+++++++++++++++++++

**Data**

* Add pricelist data and price category data
* Desactive incoterms data
* Add waves data
* Add account assets
* Add account supplier invoices data
* Add purchase order data
* Add partner vat numbers

**Features and Improvements**

* Activate auto currency update
* Add group to allow to force availability on stock operations
* Add sensefly emoji module
* Add invoice bank details linked to payment mode
* Propagate delivery info from Freight Labeling to Delivery Orders
* Assign technician to Repair Order
* Rename button Create procurements to Validate the payment
* Configure SA Invoicing and Payments default purchase tax
* Install module stock_available_immediately
* Add purchase order confirmation field
* Add account asset category data
* Add bill of materials data
* Use 3 distinct services to import RMA MRP repair lines
* Allow to add additional description on sale order lines imported from RMA MRP repair line
* Install module sale_layout_category_product

**Bugfixes**

* Rma config webhook base url
* Replace quotation/order report on mail template
* Default invoice method
* Reset delivery method (except for delivery method managers)
* Assign pricelist to SO depending on RMA decision
* Layout DN/Invoice

**Build**

* Updates in odoo/external-src/account-analytic
* Updates in odoo/external-src/account-closing
* Updates in odoo/external-src/account-financial-reporting
* Updates in odoo/external-src/account-financial-tools

  * Remove all pending PR

* Updates in odoo/external-src/account-invoicing

    * New version of module account_invoice_fiscal_position_update

* Updates in odoo/external-src/bank-payment

    * New version of module account_payment_mode
    * New version of module account_payment_order

* Updates in odoo/external-src/bank-statement-reconcile
* Updates in odoo/external-src/enterprise

    * New version of module mrp_plm
    * New version of module helpdesk
    * New version of module account_reports_followup
    * New version of module account_reports

* Updates in odoo/external-src/l10n-switzerland

  * Remove all pending PR

* Updates in odoo/external-src/odoo-prototype
* Updates in odoo/external-src/odoo-usability
* Updates in odoo/external-src/partner-contact
* Updates in odoo/external-src/reporting-engine
* Updates in odoo/external-src/sale-workflow
* Updates in odoo/external-src/server-tools

  * Remove all pending PR

* Updates in odoo/external-src/stock-logistics-warehouse
* Updates in odoo/external-src/stock-logistics-workflow
* Updates in odoo/external-src/web

  * Remove all pending PR

* Updates in odoo/src

    * New version of module mrp_repair
    * New version of module sale
    * New version of module calendar
    * New version of module base_action_rule
    * New version of module web
    * New version of module base_setup
    * New version of module board
    * New version of module mail
    * New version of module sale_stock
    * New version of module stock
    * New version of module product
    * New version of module bus
    * New version of module web_calendar
    * New version of module delivery
    * New version of module base
    * New version of module report
    * New version of module purchase
    * New version of module account
    * New version of module resource
    * New version of module mrp
    * New version of module account_asset
    * New version of module web_kanban
    * New version of module crm
    * New version of module sales_team
    * New version of module stock_account

10.7.0 (2017-10-23)
+++++++++++++++++++

**Data**

* Add account asset category
* Add the email template invoicing
* Add payments term
* Add sale layout section
* Add sequences
* Add sales order
* Add Journals
* Refresh users
* Refresh the customers
* Refresh the analytic tag (add code field )
* Refresh data for full mode (product, customers, sales order, users)
* Refresh the serial number
* Add missing accounts

**Features and Improvements**

* Activate pick pack ship delivery steps
* Renaming Pick and Pack types to  Reserve & Pack and Freight labeling
* Renaming menu entry Customer Invoices to Customer Invoices / Refunds
* Invoice delivered quantities configuration
* Configure Swiss fiscal position
* Add delivery method manager group and reset delivery method onchange SO line
* Add sale terms and conditions on report
* Purchase reports
* Add field on DO confirming the physical reception of the goods by the customer
* Add shipped date field and button shipped
* Add stock inventory category filter on inventory adjustments
* Add shipping costs calculated filter
* Always create one invoice per sale order
* Automatically add Lot/Serial number to next picking packing operation
* Add supplier duplicated invoices list view
* Add selection field Validation state on product template
* Add flags down payment required on payment term and down payment missing on sale order
* Add flags down payment required on partner and down payment missing on invoice
* Add flags down payment required on payment term and down payment missing on sale order
* Do not create procurements if down payment is missing
* Allow to create procurements manually once down payment exists
* Change behavior of invoicing policy on delivered quantity, now only fully delivered sale order lines are invoicable
* Install sale_partner_incoterm module
* Install module account tag category
* Add module rma webhook
* Install module sf_mrp

**Bugfixes**

* Add mysensefly.interface security rules
* Add missing field show_button_shipped in picking view
* Rename button, make "Start Working" invisible and fix move creation on mrp.workorders
* Fix account move view with Team and Project labels
* Fix MRP Repair flow and use 'To analyze' if RMA is 'To invoice'
* Fix singleton error when invoicing two orders

**Build**

* Update submodule OCA/account-analytic
* Fix url for account-invoicing repository
* Rename modules according to changes in OCA/account-analytic
* Move full mode data to an S3 bucket
  to configure access on integration and production server
  the following environment variables must be set:

  - USE_S3=True
  - AWS_ACCESS_KEY_ID=xxxxxx
  - AWS_SECRET_ACCESS_KEY=xxxxxxxx
  - AWS_BUCKETNAME=prod-sf-odoo-data
  - AWS_REGION=eu-central-1

10.6.0 (2017-10-02)
+++++++++++++++++++

**Features and Improvements**

* Add section on quotation and invoice reports
* Install module sale_validity
* Labeling analytic account/tags columns as Project/Team
* Add product validated field
* Add product followers and product responsible role
* Add module sale invoicing with delivery order partner fiscal position
* Add sensefly invoice report
* Add Delivery note / invoice report
* Add team on manufacturing order
* Install module sale_product_set and sale_product_set_layout
* Hide unit price field on mrp repair line
* Set 'add' as default value on mrp repair line
* Install modules account_cutoff_accrual_base and account_cutoff_accrual_picking
* Add RMA Settings to define RMA repair service product
* Add RMA picking type
* Add units measure data
* Add Bank account partners data

**Bugfixes**

* Run create data ranges song
* Delivery Slip layout
* Refresh the country states data
* Refresh customers data, error with the parent_id
* Refresh suppliers data, error with the country and state
* Fix warehouse creation, sequences names and company
* Allow to cancel RMA
* Require lot number if RMA product is tracked
* Add lot number on RMA incoming picking
* Set RMA default values
* Add serial number data

**Build**

* Fix module dependencies to sf_report
* Upgrade Docker image to 2.4.0


10.5.0 (2017-09-19)
+++++++++++++++++++

**Features and Improvements**

* Create date ranges (accounting periods) for 2017
* Install module sf_terms_and_conditions
* Add and delete the chart of account data
* RMA decision fields adaptation
* Add Fiscal position data
* RMA : Mark reception picking as to do
* Install modules sale_analytic_tag_default and purchase_analytic_tag_default
* Add Bank data
* Install module sale_order_type
* Install module sf_rma_sale_order

**Bugfixes**

* Fix generate sales forecast lines
* fixed migration to avoid uninstallation of module sf_sale_order_delivery_info
* Added path of stock-logistics-workflow repository to Dockerfile
* Allow to add operations on mrp.repair until it is done
* Do not set technician creating mrp.repair from rma
* Fix error ending mrp.repair through RMA menu
* fixed bank-payment submodule to avoid error on creation of payment order

**Build**

* Remove unused PO files to reduce docker image size
* Upgrade docker-compose to 1.17.1

**Documentation**


10.4.0 (2017-09-07)
+++++++++++++++++++

**Features and Improvements**

* Add date of transfer on DO form and tree
* Add draft image to be used over the reports
* Add link beetween DO and Crystal report packing list
* Quotation / Order report
* Add carrier accounts on partner
* Add secondary vendor field on purchase order
* Add sale order main partner to invoice email template
* Jounal item credit/debit calculation on change amount currency
* Install module l10n_ch_import_cresus
* Install module stock_picking_invoice_link
* Activate the Drop shipping settings
* Install module account_reversal
* Install module base_partner_merge
* Install module sf_sale_order_delivery_info
* Install modules analytic_tag_default, sale_analytic_tag_dimension, purchase_analytic_tag_dimension
* Add RMA kanban and calendar views
* Install module product_price_category
* Install module auth_totp
* Customization of MRP Repair workflow
* Install module sale_order_lot_selection
* Install module note
* Update settings for accounting, logistics, manufacturing and sales

**Bugfixes**

* RMA :

  * Rename 'To offer' in 'Commercial gesture'
  * Add object label on smart buttons
  * Add unique constraint on zendesk reference

**Build**

* Update submodule OCA/server-tools (fixes General settings menu bug)


10.3.0 (2017-08-10)
+++++++++++++++++++

**Features and Improvements**

* Add business financial consolidation account (bfc_account) on account
* Add ribbon in non prod instances
* Add functional field on supplier invoice showing duplicated invoices
* Smart button on supplier invoice showing duplicated invoices
* BSSFL-65: Add LDAP configuration
* Add RMA module
  Create new object sf.rma to link with mrp.repair, sale.order and stock.picking.
  This object will be used from zendesk.
* Add an icon to the RMA module
* Add Work centers data
* Add partner categories data
* Add cost budget estimation module
* Rename warehouse SA
* Add RMA causes data
* Add product category data
* Add PL name data in account tag
* Add Parrot category data in account tag
* Add sensefly header and footer to be used in all reports
* Replacement of standard Delivery Slip report
* Add groups to users data
* Compute time on work orders without start/stop button

**Bugfixes**

* Fix error on 'stock.picking' when using serial number products with qty > 1
* Write warranty end date on production lot only at first outgoing picking
* LDAP configuration, fix username


10.2.0 (2017-07-12)
+++++++++++++++++++

**Features and Improvements**

* Add active field on journal
* Add field owner in account analytic
* Add Sales forecast module
* Add Partner: Customer, supplier (draft)
* Add the import Sales Team / Channel to demo and install songs
* Add the import "Drone type" to demo and install songs
* Active multi location in a warehouse
* Import the stock locations
* For the company "senseFly Inc"
  * Add a warehouse
  * Add locations WH and Stock
* Configuration settings on main company
* Install module 'Sensfly RMA MRP Repair'
* Add warranty end date on stock production lot for serial numbers
* Add Analytic Tags data: dimension and tags
* Add Analytic account data (project)

**Bugfixes**

* Fix sf_drone_info tests by making it flexing about currency

**Build**

* Upgrade Docker image to 10.0-2.3.0
* Update odoo/src to latest commit


10.1.0 (2017-06-15)
+++++++++++++++++++

**Features and Improvements**

* Add Intragroup field on partners
* Add sensfly website / ERP interface
  The interface class implements a generic method "call" to be called through xmlrpc.
* Add sales team on countries
* Remove Quality module
* Add sale exceptions and partner identification
* Add a second company based in Washington DC
* Setup MRP, Purchase, Sales and Logistics
* Add Entity type on partners
* Add Custom field on countries
* Add boolean field to tell that the location has department link to an analytic account
* Add Helpdesk module custom


**Build**

* Add OCA sale-workflow
* Sync from odoo-template
* Load entrypoints


10.0.0 (2017-05-18)
+++++++++++++++++++

**Features and Improvements**

* Base setup
* Add sf_drone_info_module
* Define custom report layout
* Add user data
* Install basic OCA modules

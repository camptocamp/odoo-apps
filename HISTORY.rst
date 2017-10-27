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
* Add pricelist data and price category data

* Desactive incoterms data

* Add waves data

* Add account assets

* Add account supplier invoices data

**Features and Improvements**

* Add group to allow to force availability on stock operations

* Add sensefly emoji module

* Add invoice bank details linked to payment mode

* Assign technician to Repair Order

Rename button Create procurements to Validate the payment

* Configure SA Invoicing and Payments default purchase tax
* Install module stock_available_immediately

**Bugfixes**

* Rma config webhook base url

* Replace quotation/order report on mail template

* Default invoice method

* Reset delivery method (except for delivery method managers)

**Build**

**Documentation**


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
* Add purchase order confirmation field
* Add account asset category data
* Add bill of materials data
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
* Use 3 distinct services to import RMA MRP repair lines
* Allow to add additional description on sale order lines imported from RMA MRP repair line
* Install module sale_layout_category_product

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

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

**Features and Improvements**

* Install module sf_terms_and_conditions
* Add and delete the chart of account data
* RMA decision fields adaptation
* Add Fiscal position data

**Bugfixes**

* fixed migration to avoid uninstallation of module sf_sale_order_delivery_info
* Added path of stock-logistics-workflow repository to Dockerfile

**Build**

**Documentation**


10.4.0 (2017-09-07)
+++++++++++++++++++

**Features and Improvements**

* Add date of transfer on DO form and tree
* Add draft image to be used over the reports
* Add carrier accounts on partner
* Add secondary vendor field on purchase order
* Add sale order main partner to invoice email template
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

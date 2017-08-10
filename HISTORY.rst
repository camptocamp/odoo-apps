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

**Bugfixes**

* Fix error on 'stock.picking' when using serial number products with qty > 1
* Write warranty end date on production lot only at first outgoing picking

**Build**

**Documentation**


10.2.0 (2017-07-12)
+++++++++++++++++++

**Features and Improvements**

* Add active field on journal
* Add field owner in account analytic
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

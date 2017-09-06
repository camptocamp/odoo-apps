=============================
Sensefly Terms and Conditions
=============================

This module defines terms and conditions for sales and purchase.

You can define sales and purchase terms and conditions as HTML in the related
module settings for each company.

A checkbox is also added on Partners to select if terms and conditions should
be printed on this partner's orders.

Usage
=====

Call the related template inside HTML element `<div class="page">` in the
report using :

Purchase :

```<t t-call="sf_terms_and_conditions.purchase_terms_and_conditions" />```

Sale :

```<t t-call="sf_terms_and_conditions.sale_terms_and_conditions" />```

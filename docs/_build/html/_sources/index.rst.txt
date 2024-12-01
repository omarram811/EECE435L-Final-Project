.. EECE435L Final Project - E-Commerce Application documentation master file, created by
   sphinx-quickstart on Sun Dec  1 15:20:03 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EECE435L Final Project - E-Commerce Application documentation
=============================================================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   app
   modules

Submodules
----------

The following submodules are included in this project:

1. **app.database**: Contains database models used throughout the application.
2. **app.services**: Implements the various core services of the application, such as handling customers, inventory, sales, and reviews.
3. **app.utils**: Provides utility functions such as authentication and validation.

To learn more about these modules, follow the links below to their documentation.

app.database
-------------

.. toctree::
   :maxdepth: 2

   app.database.models

app.services
------------

.. toctree::
   :maxdepth: 2

   app.services.customers
   app.services.inventory
   app.services.reviews
   app.services.sales

app.utils
---------

.. toctree::
   :maxdepth: 2

   app.utils.authentication
   app.utils.validation
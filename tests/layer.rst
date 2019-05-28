============
Pytest Crate
============

Pytest fixtures can also be used in doctests, however, doctests always capture
the outout of any method calls.

Therefore the pytest fixture must not print anything to stdout/stderr but
rather use a logger.

.. code-block::

   >>> crate = getfixture("crate")

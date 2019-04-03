==============
Pytest CrateDB
==============

``pytest-crate`` is a plugin for pytest_ for writing integration tests that
interact with CrateDB_.

Usage
=====

``pytest-crate`` provides a ``crate`` session fixture which downloads, starts
and stops a CrateDB node.

.. code-block:: python

   >>> def test_database_access(crate):
   ...     # perform database access
   ...     ...

The CrateDB version can be specified using the ``--crate-version`` option when
running ``pytest``. By default, the latest stable version of CrateDB is used.

See `<tests/test_layer.py>`_ for further examples.


.. _pytest: https://docs.pytest.org
.. _CrateDB: https://crate.io

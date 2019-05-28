==========================
Changelog for pytest-crate
==========================

Unreleased
==========

2019/05/28 0.3.0
================

- Replace ``print`` statements with ``logging.debug`` statements so that
  retrieving the fixture does not produce output that is captured in doctests.
  This may break existing usages of the fixture in doctests in case the output
  of the ``getfixture`` method was matched.

2019/04/05 0.2.0
================

- Allow additional CrateDB settings in the ``crate_layer`` factory fixture
  which are applied on node start.

- Expose addresses of started CrateDB nodes

2019/04/05 0.1.0
================

- Initial pytest plugin

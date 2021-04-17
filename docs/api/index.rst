traytable methods
=================

Note that the submodules ``traytable.screens`` and ``traytable.wells`` exist purely for bookkeeping, and all four methods below (``screen()``, ``tray()``, ``clonetray()`` and ``well()`` are available from the top-level ``import traytable``.

Making screens and trays
------------------------

.. automodule:: traytable.screens
   :members: screen, tray, clonetray

Logging crystals
----------------

.. automodule:: traytable.wells
   :members: well

The methods ``setrows()`` and ``setcols()`` are exported by the package, but not documented here because their use is not recommended, and they may be deprecated in a future version.

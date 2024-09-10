pip-sbom - The (SBOM extended) Python Package Installer
==================================

This extended version of pip proves that it's easy and efficient to generate SBOM directly from the Python Package Installer. :confetti_ball:

No asset of pip was modified to include the SBOM generation command.
We introduced `networkx` and `cyclonedx-python-lib` in vendor packages.

You can use the `pip sbom` command by just installing the exteded pip version::

   pip wheel --no-deps -w dist .

Then the `sbom` command can be used with the following syntax::

   pip sbom <wheel or source distribution of you project> <name of the root component of the project>

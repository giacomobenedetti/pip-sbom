pip-sbom - The (SBOM extended) Python Package Installer
==================================

This extended version of pip proves that it's easy and efficient to generate SBOM directly from the Python Package Installer. :confetti_ball:

This is a plain fork of [pip](https://github.com/pypa/pip). We introduced the core code and procedure to generate the SBOM, while keeping the original structure and code of pip intact. The `cyclonedx-python-lib` library was added to the vendor packages solely to handle the formatting and serialization of the generated SBOM.

You can use the `pip sbom` command by just installing the exteded pip version::

```sh
pip wheel --no-deps -w dist .
```

Then the `sbom` command can be used with the following syntax::

```sh
pip sbom <wheel or source distribution of you project> <name of the root component of the project>
```

## Cite Me
This tools is part of a research project presented at the 23rd International Conference on Applied Cryptography and Network Security (23rd-26th June 2025 @ Munich, Germany).
If you use pip-sbom in a scientific publication, we would appreciate using the following citations:

```
@inproceedings{10.1007/978-3-031-95764-2_19,
author = {Benedetti, Giacomo and Cofano, Serena and Brighente, Alessandro and Conti, Mauro},
title = {The Impact of SBOM Generators on Vulnerability Assessment in Python: A Comparison and a Novel Approach},
year = {2025},
isbn = {978-3-031-95763-5},
publisher = {Springer-Verlag},
address = {Berlin, Heidelberg},
url = {https://doi.org/10.1007/978-3-031-95764-2_19},
doi = {10.1007/978-3-031-95764-2_19},
pages = {487–509},
numpages = {23},
keywords = {Software Bill of Materials, Vulnerability Assessment, Dependency Network, Software Supply Chain Security},
location = {Munich, Germany}
}
```

pip-sbom - The (SBOM extended) Python Package Installer
==================================

This extended version of pip proves that it's easy and efficient to generate SBOM directly from the Python Package Installer. :confetti_ball:

This is a plain fork of [pip](https://github.com/pypa/pip). We implemented the SBOM generation command and procedure keeping the original structure and code of pip.
We introduced `networkx` and `cyclonedx-python-lib` in vendor packages.

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
@misc{benedetti2024impactsbomgeneratorsvulnerability,
      title={The Impact of SBOM Generators on Vulnerability Assessment in Python: A Comparison and a Novel Approach}, 
      author={Giacomo Benedetti and Serena Cofano and Alessandro Brighente and Mauro Conti},
      year={2024},
      eprint={2409.06390},
      archivePrefix={arXiv},
      primaryClass={cs.CR},
      url={https://arxiv.org/abs/2409.06390}, 
}
```

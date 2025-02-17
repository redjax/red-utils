# red-utils <!-- omit in toc -->

![GitHub Created At](https://img.shields.io/github/created-at/redjax/red-utils)
![GitHub last commit](https://img.shields.io/github/last-commit/redjax/red-utils)
![GitHub commits this year](https://img.shields.io/github/commit-activity/y/redjax/red-utils)
![GitHub Latest Release](https://img.shields.io/github/release-date/redjax/red-utils)
![PyPI - Version](https://img.shields.io/pypi/v/red-utils)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/redjax/red-utils/latest)
![PyPI - Downloads](https://img.shields.io/pypi/dm/red-utils)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/redjax/red-utils/tests.yml)
![GitHub repo size](https://img.shields.io/github/repo-size/redjax/red-utils)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/redjax/red-utils)

⚠️**Important**⚠️: This is my first Python package. I'm experimenting with CI/CD and Pypi. This library is most likely not useful to anyone else, may be broken at times, may undergo refactors with little to no notice/documentation, and all that other awful stuff that comes with being an amateur developer doing this in their free time 🙃

# Table of Contents <!-- omit in toc -->

- [Description](#description)
- [Installation](#installation)
  - [Installation - with dependency groups](#installation---with-dependency-groups)
- [Developing red-utils](#developing-red-utils)

# Description

- 🔗 [Project Home - Github Repository](https://github.com/redjax/red-utils)
- 🐍 [Red Utils on Pypi](https://pypi.org/project/red_utils/)
- 📖 [Red Utils Docs](https://red-utils.readthedocs.io/en/latest/)

`red_utils` is a monorepo package, with extra "bolt-on" functionality for packages I use frequently. The base install includes functionality for `stdlib` packages like [`pathlib`](./packages/std/path-utils/) and [`list`](./packages/std/list-utils/)/[`dict`](./packages/std/dict-utils/) types. These packages do not require any external dependencies, and are always present in `red_utils` installs.

This package also includes optional dependencies, defined in the `[project.optional-dependencies]` section of the repository's [`pyproject.toml`](./pyproject.toml). You can install specific packages for 3rd party tools, like [`httpx_utils`](./packages/ext/httpx-utils/) for the [`httpx` requests client](https://www.python-httpx.org), by adding them as optional dependencies during installs: `pip install red-utils[httpx_utils]`.

The utilities are broken down into 2 modules:

- [`std`](./packages/std): Utilities with no external dependencies, only the Python `stdlib`.
- [`ext`](./packages/ext): Utilities for dependencies like `loguru` and `msgpack`
  - Note: It is generally a good practice to import `ext` modules as a whole, instead of importing functions/variables from the module.
  - This is because some of the function names I chose may be common (like `get_ts()` in the `ext.time_utils` module).
  - Example:
    ```
    from red_utils.ext import time_utils

    now = time_utils.get_ts()
    ```

    or, with `pendulum`:
    ```
    from red_utils.ext.time_utils import pendulum_utils

    now = pendulum_utils.get_ts()
    ```
     
Packages can import code from modules in the [`shared/`](./shared/) path. Modules in this path should not have any external dependencies, and should not try to import from any package in the `packages/` directory (to avoid `ImportError`s due to circular package imports).

# Installation

This project uses dependencies groups, meaning it can be installed with `pip install red-utils` for the base package, or with dependency groups like `pip install red-utils[all]` (to install all packages with a corresponding red-util module), `pip install red-utils[httpx]` (to install some helpful packages for HTTP requests, i.e. `httpx` and `diskcache`), and more. You can install multiple dependency groups with commans, like `pip install red-utils[httpx,diskcache]`.

Note that the methods below will only install `stdlib` packages, no support for 3rd party packages (see the [Installation - with dependency groups](#installation---with-dependency-groups) section).

- pip
  - `pip install red-utils`
- pdm
  - `pdm add red-utils`
- uv
  - `uv add red-utils`

## Installation - with dependency groups

This package also includes optional dependencies, defined in the `[project.optional-dependencies]` section of the repository's [`pyproject.toml`](./pyproject.toml).

Some examples of installing specific dependency groups, adding utilities for specific 3rd party apps:

- Install `red-utils` with all optional dependency groups:
  - pip: `pip install red-utils[all]`
  - pdm: `pdm add red-utils[all]`
  - uv: `uv add red-utils[all]`
- Install `red-utils` with support for the `httpx` package:
  - pip: `pip install red-utils[httpx]`
  - pdm: `pdm add red-utils[httpx]`
  - uv: `uv add red-utils[httpx]`
- Install `red-utils` with support for the `sqlalchemy` and `loguru` packages:
  - pip: `pip install red-utils[sqlalchemy,loguru]`
  - pdm: `pdm add red-utils[sqlalchemy,loguru]`
  - uv: `uv add red-utils[sqlalchemy,loguru]`

# Developing red-utils

Please see the [developing docs](docs/developing.md) for instructions on setting up a dev environment to work on `red-utils`.

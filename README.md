# red-utils

⚠️**Important**⚠️: This is my first Python package. I'm experimenting with CI/CD and Pypi. This library is most likely not useful to anyone else, may be broken at times, may undergo refactors with little to no notice/documentation, and all that other awful stuff that comes with being an amateur developer doing this in their free time 🙃

# Table of Contents

- [red-utils](#red-utils)
- [Table of Contents](#table-of-contents)
- [Description](#description)
  - [Project Home - Github Repository](#project-home---github-repository)
  - [Dynamic imports](#dynamic-imports)
- [Installation](#installation)
  - [Dependency groups:](#dependency-groups)
  - [Pip](#pip)
  - [PDM](#pdm)
- [Modules](#modules)

# Description

## [Project Home - Github Repository](https://github.com/redjax/red-utils)


A collection of utility scripts/functions that I use frequently. Includes helper functions/default variables for libraries like `loguru`, `diskcache`, and `msgpack`.

The utilities are broken down into 2 modules:

- `std`: Utilities with no external dependencies, only the Python `stdlib`.
- `ext`: Utilities for dependencies like `loguru` and `msgpack`
  - Note: It is generally a good practice to import `ext` modules as a whole, instead of importing functions/variables from the module.
  - This is because some of the function names I chose may be common (like `get_ts()` in the `ext.time_utils` module).
  - Example:
    ```
    from red_utils.ext import time_utils

    now = time_utils.get_ts()
    ```

    or, with `arrow`:
    ```
    from red_utils.ext import time_utils.arrow_utils as arrow_utils

    now = arrow_utils.get_ts()
    ```
     
Common code shared by the `std` and `ext` modules can be imported from `red_utils.core` and `red_utils.domain`. Any code in these modules should be clean of any external dependency. This is because the `std` module imports from `core`, and adding non-stdlib functionality in `red_utils.core` breaks the philosophy of the `stdlib` module. I may introduce a `red_utils.ext.core` at some point.

Some domain objects (`dataclass` or regular Python classes) may be stored in `red_utils.domain`. As of release v0.2.12, this module is empty, but future releases may bring some utilities in the form of a class.

Custom/common exceptions are stored in `red_utils.exc`.

## Dynamic imports

The `red-utils` package makes use of the Python stdlib `pkgutil` module to control imports. Packages in the `ext` module are only imported and available in `red_utils` if the corresponding dependency exists.

For instance, `red_utils.ext.msgpack_utils` will only be available if this check in [red_utiles/ext/__init__.py](https://github.com/redjax/red-utils/blob/main/red_utils/ext/__init__.py) passes:
```
import pkgutil

...

if pkgutil.find_loader("msgpack"):
  from . import msgpack_utils
```

`pkgutil.find_loader()` is used throughout the app to control imports and ensure `red_utils` is stable, by keeping uninstalled module's utilities out of the namespace.

# Installation

This project uses dependencies groups, meaning it can be installed with `pip install red-utils` for the base package, or with dependency groups like `pip install red-utils[all]` (to install all packages with a corresponding red-util module), `pip install red-utils[http]` (to install some helpful packages for HTTP requests, i.e. `httpx` and `diskcache`), and more.

## Dependency groups:

*Note*: I will do my best to update this, but to get an accurate view of available dependency groups and the packages that will be installed, check the [`pyproject.toml`](./pyproject.toml) file. Look for the dependency lists, i.e. `dependencies = [` (the base set of dependencies), `all = [`, `http = [`, etc.

`[all]`: Install all packages that have a corresponding util. This may be a large install, and is generally not recommended.

`[arrow]`: By default, the `pendulum` library is used for `time_utils`. Installing `red_utils[arrow]` allows for importing `arrow` functions from `red_utils.ext.time_utils.arrow`.

`[fastapi]`: Dependencies for `fastapi_utils`

`[http]`: My standard "HTTP toolkit." Comes with a request client (`httpx`), logging (`loguru`), caching (`diskcache`), & more.

## Pip

`pip install red-utils`

## PDM

`pdm add red-utils`

# Modules

Check the [Github page](https://github.com/redjax/red-utils/tree/main/red_utils) to see modules in the [`ext`](https://github.com/redjax/red-utils/tree/main/red_utils/ext) and [`std`](https://github.com/redjax/red-utils/tree/main/red_utils/std) modules (or click one of those words to be taken there).

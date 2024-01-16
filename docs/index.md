# Red-Utils

!!! warning

    This is my first Python package. I'm experimenting with CI/CD and Pypi. This library is most likely not useful to anyone else, may be broken at times, may undergo refactors with little to no notice/documentation, and all that other awful stuff that comes with being an amateur developer doing this in their free time 🙃

My personal collection of Python utilities (modules, functions, etc)

## Description

- 🔗 [Project Home - Github Repository](https://github.com/redjax/red-utils)
- 🐍 [Red Utils on Pypi](https://pypi.org/project/red_utils/)
- 📖 [Red Utils Docs](https://red-utils.readthedocs.io/en/latest/)

A collection of utility scripts/functions that I use frequently. Includes helper functions/default variables for libraries like `loguru`, `diskcache`, and `msgpack`.

The utilities are broken down into 2 modules:

- `std`: Utilities with no external dependencies, only the Python `stdlib`.
- `ext`: Utilities for dependencies like `loguru` and `msgpack`
  - **Note**: It is generally a good practice to import `ext` modules as a whole, instead of importing functions/variables from the module.
  - This is because some of the function names I chose may be common (like `get_ts()` in the `ext.time_utils` module).
  - Example:

```python linenums="1" title="Example: Import time_utils"
from red_utils.ext import time_utils

now = time_utils.get_ts()
```

or, with `pendulum`:
```python linenums="1"
from red_utils.ext.time_utils import pendulum_utils

now = pendulum_utils.get_ts()
```
     
Common code shared by the `std` and `ext` modules can be imported from `red_utils.core` and `red_utils.domain`. Any code in these modules should be clean of any external dependency. This is because the `std` module imports from `core`, and adding non-stdlib functionality in `red_utils.core` breaks the philosophy of the `stdlib` module. I may introduce a `red_utils.ext.core` at some point.

Some domain objects (`dataclass` or regular Python classes) may be stored in `red_utils.domain`. As of release `v0.2.12`, this module is empty, but future releases may bring some utilities in the form of a class.

Custom/common exceptions are stored in `red_utils.exc`.

## Dynamic imports

The `red-utils` package makes use of the Python stdlib `pkgutil` module to control imports. Packages in the `ext` module are only imported and available in `red_utils` if the corresponding dependency exists.

For instance, `red_utils.ext.msgpack_utils` will only be available if this check in [src/red_utils/ext/__init__.py](https://github.com/redjax/red-utils/blob/main/src/red_utils/ext/__init__.py) passes:
```
import pkgutil

...

if pkgutil.find_loader("msgpack"):
  from . import msgpack_utils
```

`pkgutil.find_loader()` is used throughout the app to control imports and ensure `red_utils` is stable, by keeping uninstalled module's utilities out of the namespace.


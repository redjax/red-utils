# red_utils.ext

Utilities for external dependencies. Uses `pkglib.find_loader()` to control imports of utilities. If a module is not installed, the utility that depends on it is not loaded.

# Extending a red-utils module by adding additional utils

**WARNING**: These docs need to be updated after refactoring this repository. It uses [`uv`](https://docs.astral.sh) and workspaces as a monorepo now.

- Create a new directory in `red_utils`
- Initialize with `pdm init`
- Add dependencies
- Add a `src` dir and an `__init__.py` file at the module's root
- Import functions & constants from the `src` dir into `src/__init__.py`
- Finally, import desired functions & constants from `src` in the module's root `__init__.py`

# Setup dev environment

These notes are mostly for me, but I suppose if anyone ever takes an interest in submitting a pull request, the documentation here will help get the local dev environment set up.

**WARNING**: These docs need to be updated after refactoring this repository. It uses [`uv`](https://docs.astral.sh) and workspaces as a monorepo now.

# Requirements

-[Astral `uv`](https://docs.astral.sh/uv)
  - This project is built with `uv`, and much of the monorepo functionality is tied to `uv`'s concept of [workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/).
  - You do not necessarily need to install Python to work on this repository, [`uv` can manage your Python install for you](https://docs.astral.sh/uv/guides/install-python/)
  - Each package is its own isolated `uv`-managed project, with its own dependencies and `pytest` tests.

# Using the VSCode Workspace

If you use Visual Studio Code as your text editor, you can open [the workspace in the `.vscode` directory](../../.vscode/) to have a more focused view of the code.

# Developing new modules

...

## Old notes on modules

The `red-utils` package separates modules into `std` and `ext`, which are respectively modules that require only the modules in the Python stdlib, or extended modules that require external dependencies.

Any modules in the `red_utils.std` package should rely only on Python stdlib packages. In fact, anything outside of the `red_utils.ext` module should rely only on the Python stdlib (i.e. `red_utils.core`, `red_utils.domain`).

If developing a utility for an external dependency (like `sqlalchemy`, `fastapi`, `pandas`/`polars`, etc), add the module to the `red_utils.ext` group and keep all code related to that dependency beneath the `red_utils.ext` module.

You can reference other modules in `red_utils.ext` to learn how to use `pkgutils` to control import flow. There are many `if pkgutil.find_loader("<package-name>")` lines throughout the `red-utils` app; the `.find_loader()` function searches for a package in the global namespace, and if it is not found, that module is not imported. This helps keep `red-utils` stable if, for example, a user installs a dependency group instead of the entirety of `red-utils`.

As an example real-world scenario, if a user installs `red-utils[http]`, they will only have access to the `red_utils.ext` modules for dependencies in the `http` dependency group in the project's `pyproject.toml`. A package like `sqlalchemy` is not installed with this group, and so `red_utils.ext.sqlalchemy_utils` will not be imported or available to the user. Type hinting in an IDE will not suggest `red_utils.ext.sqlalchemy_utils` as an importable module, and `red-utils` will skip any modules looking for `sqlalchemy`.

# Testing with PDM

You can test a new build before pushing a release by creating a new PDM project somewhere else on the system and importing the path to the `red-utils` repository.

For example, if creating a module `pandas_utils` for utility functions related to [`Pandas DataFrames`](https://pandas.pydata.org), and assuming the `red-utils` repository was cloned to `~/git/red-utils`, you would follow a process like the following:

- In the `~/git/red-utils` directory, install `pandas` in the `[all]` and `[data]` dependency groups
  - `pdm add -G all pandas`
  - `pdm add -G data pandas`
- Create a directory at `red_utils.ext.pandas_utils`
  - In this directory, create a file `operations.py` and add some utility functions (such as a function to scan a directory and load all CSV files into a DataFrame).
  - Create `red_utils/ext/pandas_utils/__init__.py`:
    - Contents of `__init__.py`:
    ```
    from .operations import load_files_to_df()
    ```
  - In `red_utils/ext/__init__.py`, add a `pkgutil.find_loader()` line to detect if `pandas` is installed, then load `pandas_utils`
    - Contents of `red_utils/ext/__init__.py`:
    ```
    import pkgutil

    ...

    if pkgutil.find_loader("pandas"):
        from . import pandas_utils
    ```
  - The new `pandas_utils` module should be available if `pandas` is available in the Python path
- Build the app with `pdm build`
- Create a new directory somewhere outside the repository, i.e. `~/testing/red-utils`
  - Initialize the project (example uses `pdm`):
    - `pdm init`
    - Answer the initialization prompts
  - Add `red-utils` from its local path
    - `pdm add ~/git/red-utils`
  - To remove the local dependency, just run `pdm remove ~/git/red-utils`

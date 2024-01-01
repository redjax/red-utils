# Setup dev environment

These notes are mostly for me, but I suppose if anyone ever takes an interest in submitting a pull request, the documentation here will help get the local dev environment set up.

# Requirements

- [PDM](https://pdm-project.org/latest/)
  - `pdm` is used to manage this package and its dependencies
  - Take a look at the project's `pyproject.toml` for available dependency groups. As you develop modules, consider which dependency group they belong in, i.e. most dependencies should *not* be added to the default dependency group.
    - If you are working on a FastAPI module, for example, add new dependencies to the `fastapi` and `all` groups.
      - `pdm add -G fastapi <package>`
      - `pdm add -G all <package>`
  - There are also a number of project scripts configured in the `pyproject.toml` file, which aid in development
    - Scripts are declared in sections that look like `[tool.pdm.scripts.<script-name>]`, and can be called with `pdm run <script-name>`
      - For example, to run the PDM script that calls `black` and `ruff` to format code:
        - `pdm run lint`
      - To run the PDM script that exports a `requirements.txt` file:
        - `pdm run export`
- (Optional) [Pre-commit](https://pre-commit.com)
  - There are some `pre-commit` scripts configured, too, for things like linting/formatting the code during commit.
    - To see configured `pre-commit` steps, check `.pre-commit-config.yaml`
  - To use these `pre-commit` scripts, they need to be installed locally with `pdm run pre-commit install`
  - To disable the pre-commit hooks, run `pdm run pre-commit uninstall`

# Using the VSCode Workspace

If you use Visual Studio Code as your text editor, you can open the workspace in the `.vscode` directory to have a more focused view of the code.

# Developing new modules

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

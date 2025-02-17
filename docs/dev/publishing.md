# Publishing

**WARNING**: These docs need to be updated after refactoring this repository. It uses [`uv`](https://docs.astral.sh) and workspaces as a monorepo now.

- Create a file `~/.pypirc`
``` py linenums="1" title="~/.pypirc"
[distutils]
index-servers=
    pypi
    testpypi

[testpypi]
username = __token__ 
password = <your-testpypi-token>

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = <your-pypi-token>
```
  - Set the file's chmod to `600`

## With PDM scripts:
  - Run `pdm run create-<major|minor|micro>-release`
    - These scripts use `pdm bump` to bump the version number, build the package, & publish to pypi.
    - To see the script, check the `[tool.pdm.scripts.create-<major|minor|micro>-release]` script sections in `../../pyproject.toml`
  - Upload to pypi:
    ```
    ## Test pypi
    pdm run upload-test-pypi

    ## Pypi
    pdm run upload-pypi
    ```

## Without PDM scripts:
  - Run the following commands:
  ```
  pdm bump <major|minor|micro>
  pdm bump tag
  pdm lock
  pdm build
  git push --tags
  ```
  - Upload to pypi:
    ```
    ## Test pypi
    pdm run upload-test-pypi

    ## Pypi
    pdm run upload-pypi
    ```

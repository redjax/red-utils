from __future__ import annotations

from pathlib import Path

import nox

nox.options.default_venv_backend = "venv"
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False
nox.options.error_on_missing_interpreters = False
# nox.options.report = True
nox.sessions = ["lint", "export", "tests"]

PYVER: str = "3.11"
TEST_PYVERS: list[str] = ["3.12", "3.11"]

PDM_VER: str = "2.11"

LINT_PATHS: list[str] = ["red_utils", "tests", "./noxfile.py"]

REQUIREMENTS_OUTPUT_DIR: Path = Path("./requirements")

if not REQUIREMENTS_OUTPUT_DIR.exists():
    try:
        REQUIREMENTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        msg = Exception(
            f"Unable to create requirements export directory: '{REQUIREMENTS_OUTPUT_DIR}'. Details: {exc}"
        )
        print(msg)

        REQUIREMENTS_OUTPUT_DIR: Path = Path(".")


@nox.session(python=TEST_PYVERS, name="build-env")
@nox.parametrize("pdm_ver", [PDM_VER])
def setup_base_testenv(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")

    print("Installing dependencies with PDM")
    session.run("pdm", "sync")
    session.run("pdm", "install")


@nox.session(python=[PYVER], name="lint")
def run_linter(session: nox.Session):
    session.install("ruff", "black")

    for d in LINT_PATHS:
        lint_path: Path = Path(d)
        print(f"Running ruff imports sort on '{d}'")
        session.run(
            "ruff",
            "--select",
            "I",
            "--fix",
            lint_path,
        )

        print(f"Formatting '{d}' with Black")
        session.run(
            "black",
            lint_path,
        )

        print(f"Running ruff checks on '{d}' with --fix")
        session.run(
            "ruff",
            "--config",
            "ruff.ci.toml",
            lint_path,
            "--fix",
        )


@nox.session(python=[PYVER], name="export")
@nox.parametrize("pdm_ver", [PDM_VER])
def export_requirements(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")

    print("Exporting production requirements")
    session.run(
        "pdm",
        "export",
        "--prod",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt",
        "--without-hashes",
    )

    print("Exporting development requirements")
    session.run(
        "pdm",
        "export",
        "-d",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.dev.txt",
        "--without-hashes",
    )

    # print("Exporting CI requirements")
    # session.run(
    #     "pdm",
    #     "export",
    #     "--group",
    #     "ci",
    #     "-o",
    #     f"{REQUIREMENTS_OUTPUT_DIR}/requirements.ci.txt",
    #     "--without-hashes",
    # )


@nox.session(python=TEST_PYVERS, name="tests")
@nox.parametrize("pdm_ver", [PDM_VER])
def run_tests(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")
    session.run("pdm", "install")

    print("Running Pytest tests")
    session.run(
        "pdm",
        "run",
        "pytest",
        "-n",
        "auto",
        "--tb=auto",
        "-v",
        "-rsXxfP",
    )

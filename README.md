# C3PO

> *C3PO*: <u>C</u>ore <u>C</u>ontent Management & <u>C</u>leaning Repository for <u>P</u>ostprocessing and <<u>O</u>rganization

Companion Codebase to [R2D2](https://github.com/AlexanderKhazatsky/R2D2); core codebase for any data management,
cleaning, and postprocessing/annotation for the robot trajectory data collected as part of the large-scale multi-lab 
data collection effort.

Built with Python 3.8, using sane quality defaults (`black`, `ruff`, `pre-commit`).

---

## Installation

With Python 3.8 as your default Python version (e.g., in a virtualenv, Conda environment, or Docker) you can install 
this package locally via an editable installation:

```bash
git clone https://github.com/siddk/c3po
cd c3po
pip install -e .
```

## Usage

Project-specific usage notes...

## Contributing

Before committing to the repository, *make sure to set up your dev environment!*

Here are the basic development environment setup guidelines:

+ Fork/clone the repository, performing an editable installation. Make sure to install with the development dependencies
  (e.g., `pip install -e ".[dev]"`); this will install `black`, `ruff`, and `pre-commit`.

+ Install `pre-commit` hooks (`pre-commit install`).

+ Branch for the specific feature/issue, issuing PR against the upstream repository for review.

Additional Contribution Notes:
- This project has migrated to the recommended
  [`pyproject.toml` based configuration for setuptools](https://setuptools.pypa.io/en/latest/userguide/quickstart.html).
  However, given that several tools have not fully adopted [PEP 660](https://peps.python.org/pep-0660/), we provide a
  [`setup.py` file for backwards compatibility](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html).

- This package follows the [`flat-layout` structure](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#flat-layout)
  described in `setuptools`.

- Make sure to add any new dependencies to the `project.toml` file!

---

## Repository Structure

High-level overview of repository/project file-tree:

+ `docs/` - Package documentation - including key design choices and additional notes.
+ `c3po` - Package source code; has all core utilities for data munging, uploading, cleaning, and postprocessing.
+ `scripts/` - Standalone scripts for various functionality (e.g., uploading data to S3).
+ `.gitignore` - Default Python `.gitignore`.
+ `.pre-commit-config.yaml` - Pre-commit configuration file (sane defaults + `black` + `ruff`).
+ `LICENSE` - By default, research code is made available under the MIT License; if changing, think carefully about why!
+ `Makefile` - Top-level Makefile (by default, supports linting - checking & auto-fix); extend as needed.
+ `pyproject.toml` - Following PEP 621, this file has all project configuration details (including dependencies), as
                     well as tool configurations (for `black` and `ruff`).
+ `README.md` - You are here!

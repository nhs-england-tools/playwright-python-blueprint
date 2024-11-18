# Getting Started #2: Blueprint File Breakdown

This guide outlines the breakdown of this blueprint, and specifically the files of importance for running Playwright Pytest.

## Contents

- [Getting Started #2: Blueprint File Breakdown](#getting-started-2-blueprint-file-breakdown)
  - [Contents](#contents)
  - [Directories \& Files Directly Impacting Tests](#directories--files-directly-impacting-tests)
    - [`requirements.txt`](#requirementstxt)
    - [`pytest.ini`](#pytestini)
    - [`tests/`](#tests)
    - [`pages/`](#pages)
    - [`utils/`](#utils)
  - [Directories \& Files Specific For This Repository](#directories--files-specific-for-this-repository)

## Directories & Files Directly Impacting Tests

The files in this section cover the files that impact your ability to execute tests.

### `requirements.txt`

This file outlines the packages required from the Python Package Index (PyPI) to execute this project. This should be regularly maintained to ensure that we have the most up-to-date versions of any packages we intend to use.

### `pytest.ini`

This file outlines the configuration of pytest, and ultimately how Playwright also executes. A couple of things to note:

- The `log_cli` section covers default logging provided by pytest - we have defaulted this to on at INFO level, but this can be amended as needed.
- The `addopts` section will run any commands you want to run by default for each execution and can be overwritten using the appropriate options via the command line. For example, you can override the `--tracing` level to on by executing pytest using: `pytest --tracing=on`.
- The `markers` section is for organizing any marks (or tags) you want to apply to your tests, for example by a business area or a testing type. If you don't include your marks in this list, pytest will give you a warning until they have either been added here or programmatically within the code.

Any configuration you want to apply to all of your test executions should be placed in this file where possible, to ensure easy maintenance.

### `tests/`

This directory is designed to house all of your tests intended for execution.

Because we want to treat this directory as a [Python package](https://docs.python.org/3/tutorial/modules.html#packages), there is a blank `__init__.py` file present in this directory that should remain present.

### `pages/`

This directory is designed to house all of your [page object model](https://playwright.dev/python/docs/pom) classes, to facilitate reusable code and easy to maintain tests.

We want this directory to be treated as a [Python package](https://docs.python.org/3/tutorial/modules.html#packages), so there is a blank `__init__.py` file present in this directory that should remain present.

### `utils/`

This directory is designed to house any utility classes that would assist in test execution. We provide some utility classes as part of this blueprint, but as you begin testing your own applications you may find that these utilities may need to be expanded or you need something different from what has been provided. For example, you may create a utility class for logging into your application - that code should go in this directory.

We want this directory to be treated as a [Python package](https://docs.python.org/3/tutorial/modules.html#packages), so there is a blank `__init__.py` file present in this directory that should remain present.

> NOTE: If you write a utility class for your own project that you think other projects may benefit from and can be applied in a generic way, please raise a [Feature Request](https://github.com/nhs-england-tools/playwright-python-blueprint/issues/new/choose) as we welcome any contributions of this fashion.

## Directories & Files Specific For This Repository

The following directories and files are specific for this repository, and may require modification or removal if transferring this code into a new repository.

- `.github/`: This directory has the code used to manage our repository and pipelines including CI/CD checks. You may find some useful for your own repository, especially if you are using GitHub to manage your code.
- `.vscode/`: This directory houses the default recommended configuration and settings for VSCode, if you use it as an IDE.
- `docs/`: This directory houses the documentation for this repo (including documents like this one).
- `scripts/`: This directory houses the scripts used by this repo, primarily as part of the CI/CD checks.
- `tests_utils/`: This directory houses the unit tests for the utilities provided by this repository. You may want to copy these over if you want to ensure utilities are behaving as expected.
- `.editorconfig`, `.gitattributes`, `.gitignore`, `.gitleaks.toml`, `.gitleaksignore`: These files are configuration for git, and quality and security checks provided via the CI/CD checks.

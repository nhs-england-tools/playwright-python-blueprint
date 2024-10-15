# Playwright Python Blueprint

[![CI/CD Pull Request](https://github.com/nhs-england-tools/repository-template/actions/workflows/cicd-1-pull-request.yaml/badge.svg)](https://github.com/nhs-england-tools/playwright-python-blueprint/actions/workflows/cicd-1-pull-request.yaml)

This project is designed to provide a blueprint to allow for development teams to start quickly developing UI tests using [Playwright Python](https://playwright.dev/python/), providing the base framework and utilities to allow for initial focus on writing tests, rather than configuration of the framework itself.

NOTE: This project is currently under initial development so isn't finalised, but should work if you want to experiment with Playwright Python.

> **NOTE: When considering this project, please be advised that currently Playwright is a "proposed" tool within the [NHS England Tech Radar](https://radar.engineering.england.nhs.uk/).  Whilst we are taking steps to get Playwright moved to the "mainstream" section of the radar, as it has not yet been formally adopted it is possible that Playwright may not be fully endorsed by NHS England as a standard tool going forward, and using this framework for an NHS England project is currently at your own risk.**

## Table of Contents

- [Playwright Python Blueprint](#playwright-python-blueprint)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Configuration](#configuration)
  - [Getting Started](#getting-started)
  - [Contacts](#contacts)
  - [Licence](#licence)

## Setup

You can clone this whole repository using the code below:

```shell
git clone https://github.com/nhs-england-tools/playwright-python-blueprint.git
```

### Prerequisites

To utilise the blueprint code, you will need to have the following installed:

- [Python](https://www.python.org/downloads/) 3.12 or greater

Whilst not required to get started, you may also want to [configure a Python virtual environment for your project](https://docs.python.org/3/library/venv.html) before proceeding with
the configuration.  If you are using an IDE such as Visual Studio Code or PyCharm, you will normally be prompted to do this automatically.

### Configuration

To get started using Playwright and with the examples provided, use the following commands:

```shell
pip install -r requirements.txt
playwright install --with-deps
```

This will install all the necessary packages for executing Playwright tests, and install Playwright ready for use by the framework.  You can test the configuration
has worked by running our example tests, which can be done using the following command (this will run all tests with tracing reports turned on, and in headed mode
so you can see the browser execution):

```shell
pytest --tracing on --headed
```

## Getting Started

> NOTE: This section is currently under development and requires further work, so links to pages within this repository may not be very useful at this stage.

Once you've confirmed your installation is working, please take a look at the following guides on getting started with Playwright Python.

1. [Understanding Playwright Python](./docs/getting-started/1_Understanding_Playwright_Python.md)
2. [Blueprint File Breakdown](./docs/getting-started/2_Blueprint_File_Breakdown.md)

For additional reading and guidance on writing tests, we also recommend reviewing the [Playwright Python documentation](https://playwright.dev/python/docs/writing-tests).

## Contacts

If you have any queries regarding this blueprint, please contact [dave.harding1@nhs.net](mailto:dave.harding1@nhs.net).

## Licence

> The [LICENCE.md](./LICENCE.md) file will need to be updated with the correct year and owner

Unless stated otherwise, the codebase is released under the MIT License. This covers both the codebase and any sample code in the documentation.

Any HTML or Markdown documentation is [© Crown Copyright](https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/) and available under the terms of the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

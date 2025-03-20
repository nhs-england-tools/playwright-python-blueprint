# Playwright Python Blueprint

[![CI/CD Pull Request](https://github.com/nhs-england-tools/repository-template/actions/workflows/cicd-1-pull-request.yaml/badge.svg)](https://github.com/nhs-england-tools/playwright-python-blueprint/actions/workflows/cicd-1-pull-request.yaml)

This project is designed to provide a blueprint to allow for development teams to start quickly developing UI tests using [Playwright Python](https://playwright.dev/python/), providing the base framework and utilities to allow for initial focus on writing tests, rather than configuration of the framework itself. Playwright is the current mainstream UI testing tool for NHS England, as outlined on the [NHS England Tech Radar](https://radar.engineering.england.nhs.uk/).

> NOTE: This project is currently under initial development so isn't finalised, but should work if you want to experiment with Playwright Python.

## Table of Contents

- [Playwright Python Blueprint](#playwright-python-blueprint)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Configuration](#configuration)
  - [Getting Started](#getting-started)
  - [Utilities](#utilities)
  - [Contributing](#contributing)
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

> NOTE: There are currently known issues with Python 3.13 and Playwright, so if you encounter issues running this project whilst using Python 3.13 it is recommended to downgrade to Python 3.12 in the interim.

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

Alternatively if you are using Visual Studio Code as your IDE, we have pre-configured this project to work with the
[Testing functionality](https://code.visualstudio.com/docs/editor/testing) so the example tests should be discovered automatically.

## Getting Started

> NOTE: This section is currently under development and requires further work, so links to pages within this repository may not be very useful at this stage.

Once you've confirmed your installation is working, please take a look at the following guides on getting started with Playwright Python.

1. [Understanding Playwright Python](./docs/getting-started/1_Understanding_Playwright_Python.md)
2. [Blueprint File Breakdown](./docs/getting-started/2_Blueprint_File_Breakdown.md)

We've also created a [Quick Reference Guide](./docs/getting-started/Quick_Reference_Guide.md) for common commands and actions you may regularly perform using this blueprint.

For additional reading and guidance on writing tests, we also recommend reviewing the [Playwright Python documentation](https://playwright.dev/python/docs/writing-tests).

## Utilities

This blueprint also provides the following utility classes, that can be used to aid in testing:

|Utility|Description|
|-------|-----------|
|[Axe](./docs/utility-guides/Axe.md)|Accessibility scanning using axe-core.|
|[Date Time Utility](./docs/utility-guides/DateTimeUtility.md)|Basic functionality for managing date/times.|
|[NHSNumberTools](./docs/utility-guides/NHSNumberTools.md)|Basic tools for working with NHS numbers.|
|[User Tools](./docs/utility-guides/UserTools.md)|Basic user management tool.|

## Contributing

Further guidance on contributing to this project can be found in our [contribution](./CONTRIBUTING.md) page.

## Contacts

If you have any ideas or require support for this project, please [raise an issue via this repository](https://github.com/nhs-england-tools/playwright-python-blueprint/issues/new/choose) using the appropriate template.

If you have any general queries regarding this blueprint, please contact [dave.harding1@nhs.net](mailto:dave.harding1@nhs.net).

## Licence

Unless stated otherwise, the codebase is released under the [MIT License](LICENCE.md). This covers both the codebase and any sample code in the documentation.

Any HTML or Markdown documentation is [© Crown Copyright](https://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/) and available under the terms of the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

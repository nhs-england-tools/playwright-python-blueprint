# Contributing To This Project

This document outlines the general guidance that should be applied when contributing new code to this project,
to ensure that coding standards and principles remain consistent throughout the project.

## Table of Contents

- [Contributing To This Project](#contributing-to-this-project)
  - [Table of Contents](#table-of-contents)
  - [General Principles](#general-principles)
    - [Use Playwright and pytest documentation as our standard](#use-playwright-and-pytest-documentation-as-our-standard)
    - [Proving tests work before raising a pull request](#proving-tests-work-before-raising-a-pull-request)
    - [Evidencing tests](#evidencing-tests)
      - [Example](#example)
  - [Coding Practices](#coding-practices)
    - [Tests](#tests)
      - [Docstring](#docstring)
        - [Example](#example-1)
    - [Page objects](#page-objects)
      - [Naming Conventions](#naming-conventions)
      - [Docstring](#docstring-1)
        - [Example](#example-2)
    - [Utilities](#utilities)
      - [Docstring](#docstring-2)
        - [Example](#example-3)
    - [Package management](#package-management)
  - [Last Reviewed](#last-reviewed)

## General Principles

### Use Playwright and pytest documentation as our standard

When contributing to this project, we should be following the guidance outlined in the
[Playwright](https://playwright.dev/python/docs/api/class-playwright) and
[pytest](https://docs.pytest.org/en/stable/)
documentation in the first instance to ensure our code remains as close to the recommended standard as possible.
This will allow anyone contributing to this project to follow the code and when we use elements from either
Playwright or pytest, easily reference the implementation from their documentation.

In the event we need to deviate away from this for any reason, we should clearly document the reasons why and explain
this in any pull request raised.

### Proving tests work before raising a pull request

When creating or modifying any code, if tests in the framework have been impacted by the change we should ensure that
we execute the tests prior to raising a pull request (to ensure we are not asking for a code review for code that does
not work as intended). This can either be done locally or via a pipeline/workflow.

### Evidencing tests

When we create new tests, or significantly change the functionality of a test, we should demonstrate these tests work
by [recording the trace using Playwright](https://playwright.dev/python/docs/trace-viewer-intro) and attaching the
generated trace file to the associated ticket within `Jira`.

> NOTE: If the trace file exceeds the maximum file attachment size for `Jira`, we should
> upload the file to a Confluence page instead and link this back to the ticket.

When we modify existing tests (including any page objects or utilities used by these tests) but the behaviour of the test
has not fundamentally changed, we should upload the generated HTML report from the Playwright execution to the
`Jira` ticket.

#### Example

We introduce a new test that covers the send a kit functionality for a single subject using `codegen` in the first instance.
To demonstrate this test has worked as intended, we should turn tracing on and generate a trace file from Playwright and
attach this to the ticket in `Jira`.

We then decide to refactor the test so that it uses a page object model for the send a kit page, but this does not change
the behaviour of the test in any way (just makes the elements reusable). In this instance, we should upload the HTML report
to the `Jira` ticket showing the test passing as the logic of the test has not changed in any way.

We then decide to create a utility that loops through several subjects at once and apply this to the previously created send
a kit test. In this instance, we should turn tracing on again and generate a trace file from Playwright and attach this to the
ticket in `Jira`, because the logic of the test has fundamentally changed.

## Coding Practices

### Tests

The following guidance applies to any files in the /tests directory.

#### Docstring

For any tests in the project, we should add a docstring that explains the test in a non-technical way, outlining the following
points:

- The steps undertaken as part of the test
- References to any applicable acceptance criteria this test covers

This information will be populated on the HTML report provided by the framework, allowing for non-technical stakeholders to
understand the purpose of a test without specifically needing to view the code directly.

This should always be done using a [multi-line docstring](https://peps.python.org/pep-0257/#multi-line-docstrings), even if
the test description is reasonably short.

##### Example

    def test_example_scenario(page: Page) -> None:
        """
        This test covers an example scenario whereby the user navigates to the subject search page,
        selects a subject who is 70 years old and validates their age is correctly displayed on the
        screening subject summary page.

        This test is used for the following acceptance criteria:
        - BCSS-1234 (A/C 1)
        """

### Page objects

The following guidance applies to any files in the /pages directory.

#### Naming Conventions

For any newly created page objects, we should apply the following logic:

- The filename should end with `_page` (Example: `send_a_kit_page.py`)
- The class name should end with `Page` (Example: `SendAKitPage`)

#### Docstring

For any page objects in the project, we need to ensure for any class methods or functions we give a
brief description of the intent of the function for the benefit of anyone reading the project or using
intellisense. This can be done using a [single-line docstring](https://peps.python.org/pep-0257/#one-line-docstrings)
where possible.

##### Example

    class ExamplePage:

        def __init__(page: Page) -> None:
            self.page = page

        def click_on_locator(locator: Locator) -> None:
            """Clicks on the provided locator."""
            locator.click()

        def get_text_from_locator(locator: Locator) -> str:
            """Returns the text from the locator as a string."""
            return locator.inner_text()

### Utilities

The following guidance applies to any files in the /utils directory.

#### Docstring

For any utilities added to the project, we should add docstrings that outline the functionality including
any arguments and returns. These should be formatted as
[multi-line docstrings](https://peps.python.org/pep-0257/#multi-line-docstrings) with a description, Args and
Returns provided.

##### Example

    def example_util(user: str) -> dict:
        """
        Takes the user string and retrieves example information applicable to this user.

        Args:
            user (str): The user details required, using the record key from users.json.

        Returns:
            dict: A Python dictionary with the example details of the user requested.
        """

### Package management

If we need to introduce a new Python package (via requirements.txt) into this project to allow for
appropriate testing, we need to have critically reviewed the package and ensure the following:

- The package we intend to use is actively being maintained (e.g. has had recent updates or has a large active community behind it)
- The package has appropriate documentation that will allow us to easily implement and maintain the dependency in our code

## Last Reviewed

This document was last reviewed on 01/05/2025.

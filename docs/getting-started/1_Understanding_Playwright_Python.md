# Getting Started #1: Understanding Playwright Python

This guide outlines how Playwright works in Python, and how to start writing tests in the format this blueprint recommends.

## Contents

Come back to this

## The Basics

For Python, Playwright is treated as a plugin for a unit testing framework called [pytest](https://docs.pytest.org/en/stable/) and
expands the functionality provided by pytest to allow for interaction with browsers (and allow us to write UI tests using the same logic)
along with other testing utilities. Because of this, in this blueprint you will see references to pytest regularly, as it is the engine
that drives the test execution.

## How Does pytest Work

In the case of this blueprint, pytest works by
[scanning directories within the code base to discover tests](https://docs.pytest.org/en/stable/explanation/goodpractices.html#test-discovery),
where by default it looks for any files in the format of `test_*.py` or `*_test.py`. Once the files have been discovered, it'll check for any
functions in the file starting with `test_` and if found, will execute that function as a test and collect the result.

pytest will spin up any utilities it needs to execute tests (including any we choose to define), which for this framework includes a number of
Playwright-based objects we would likely want to utilise, including:

- `page`: The Playwright page object, which we use to interact with a browser page during tests. You'll likely use this object for every test.
- `browser`: The Playwright browser object, which we use to create and manage the browser directly and create new pages if required. It's unlikely you'll need to include this unless you have a very specific browser test.
- `playwright`: The Playwright object, which we can use to manage the Playwright instance during testing. It's extremely unlikely you'll need this when pytest is the test executor.

For further reading on pytest, it's recommended to read the [full documentation](https://docs.pytest.org/en/stable/).

## Executing Tests

Because pytest is the engine in this blueprint, we use the pytest command to initiate any test exectuion. This can be done as simply by using
the following command in the command line against this blueprint (once the initial setup has been completed):

    pytest

When using this command, it will run any tests with the default configuration provided by pytest and Playwright (which in the case of UI testing,
normally means that it'll run all tests against the [Chromium](#info-what-is-chromium) browser that was installed).

If you want to execute tests with specific settings, such as a specific browser or to specify specific tests to run, these can be passed in on the
command line after the pytest command or via the [pytest.ini](../../pytest.ini) file (using the `addopts` section).

For further reading on the kinds of settings you can apply with pytest, take a look at our [Quick Reference Guide](./Quick_Reference_Guide.md).

## Using pytest Logic

When we use Playwright with pytest, a number of objects that we may want to interact with are automatically generated, but the most pertinant
of these is the `page` object, which represents the browser page object we want to interact with. Because it's provided automatically when we
start a test run, we do not need to do any specific configuration with the test other than add a reference to this page object in the function
arguments for the test like so:

    # Doing an import like this for the page object isn't required, but is considered good practice
    from playwright.sync_api import Page

    # An example call showing how the page object is brought into a test, and how it can be used
    def test_example(page: Page) -> None:
        page.goto("https://github.com/nhs-england-tools/playwright-python-blueprint")

As you can see from the example, the only setup for the `page` object here is in the function arguments, and we can use it as needed in the test.

## Utilising Playwright codegen

If you're new to Playwright, Python or automating tests generally, then Playwright provides a code generation tool that allows you to manually navigate
through a browser to generate the code for a test. You can access the `codegen` tool by using the following command:

    # Load a empty browser window
    playwright codegen

This will bring up a browser window, with the Playwright code generator running in the background, like so:

# TODO - Image for codegen

## Appendix

### Info: What is Chromium

[Chromium](https://www.chromium.org/Home/) is one of the open source browser that comes bundled with Playwright on install (if using the instructions
within the readme of this blueprint) but also more importantly, serves as the base code for both Google Chrome and Microsoft Edge. Whilst this doesn't
replace the need to test in independent browsers as required, Chromium provides the opportunity to do some initial broad testing which should largely be
representative of the user experience with Chrome and Edge respectively.
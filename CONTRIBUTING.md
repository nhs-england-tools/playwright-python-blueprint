# Contributing To This Project

With this project, we actively encourage anyone who may have any ideas or code that could make this repository better to contribute
in any way they can.

## How To Contribute

If you have an idea about something new that could be added, then please raise a
[Feature Request via the Issues tab](https://github.com/nhs-england-tools/playwright-python-blueprint/issues/new/choose) for this
repository. Even if you don't feel you have the technical ability to implement the request, please raise an issue regardless as
the maintainers of this project will frequently review any requests and attempt to implement if deemed suitable for this blueprint.

If you have some code you think could be implemented, please raise a Feature Request and
[create a fork of this repository](https://github.com/nhs-england-tools/playwright-python-blueprint/fork) to experiment and ensure
that the change you want to push back works as intended.

## Contribution Requirements

For any contributions to this project, the following requirements need to be met:

- You must be a member of the [NHS England Tools](https://github.com/nhs-england-tools) organisation on GitHub.
- [Any commits must be signed](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits), so they show as verified once they reach GitHub. This checking serves as part of our CI/CD process, so unsigned commits will prevent a pull request from being merged.
- For any utility methods that are added to this framework in the `utils` directory, the following applies:
  - Unit tests for the utility should be added to the `tests_utils` directory and need to be tagged with the `utils` mark.
  - Documentation for these classes and how to use any methods should also be added to the `docs/utilities-guide` directory.
  - Each method that is intended to be used as part of a class should have a correctly formatted docstring, to allow for developers using Intellisense within their IDE to understand what the code is intended to do.
- All CI/CD checks will need to pass before any code is merged to the `main` branch - this includes ensuring appropriate formatting of code and documentation, security checks and that all unit and example tests pass.

## Things We Want

What we are particularly interested in is:

- Any utility classes that can uniformly applied to any project. This may be something that's been created for your own project and by doing some minor abstraction any other teams working in a similar way could adopt this functionality.
- Any development code that supports executing this project in a CI/CD fashion. This primarily covers any changes that support development principles outlined in the [Software Engineering Quality Framework](https://github.com/NHSDigital/software-engineering-quality-framework), and could include logic around how the test code is containerized.
- Any changes that allow for test reporting in a consistent, reliable, maintainable and interesting format for varying stakeholders. This includes logic that expands on from the reporting we generate, such as example scripts for how to generate dashboards using the data we generate.

Examples:

- Say you've created a utility for generating test patients within your application. Any elements of this code that could be universally applied and other teams are likely to use (e.g. NHS number, patient name) we would want in this blueprint. If there's something business specific to your project that exists as part of this code (e.g. a unique reference number that only applies to your service), then we would advise removing that logic from any code before raising a pull request here.
  - If you do end up adding a utility class in this format in a more generic way to this project, you can subsequently [inherit the utility class](https://docs.python.org/3/tutorial/classes.html#inheritance) to include your additional business-specific requirements within your own version of the class.

# Utility Guide: User Tools

The User Tools utility provided by this blueprint allows for the easy management of test users via a json file included
at the base of the repository.

## Table of Contents

- [Utility Guide: User Tools](#utility-guide-user-tools)
  - [Table of Contents](#table-of-contents)
  - [Using the User Tools class](#using-the-user-tools-class)
  - [Managing Users](#managing-users)
    - [Considering Security](#considering-security)
  - [`retrieve_user()`: Retrieve User Details](#retrieve_user-retrieve-user-details)
    - [Required Arguments](#required-arguments)
    - [Returns](#returns)
    - [Example Usage](#example-usage)

## Using the User Tools class

You can initialise the User Tools class by using the following code in your test file:

    from utils.user_tools import UserTools

This module has been designed as a static class, so you do not need to instantiate it when you want to retrieve any user information.

## Managing Users

For this class, users are managed via the [users.json](../../users.json) file provided with this repository. For any new users you need to
add, the idea is to just add a new record, with any appropriate metadata you need for the user whilst they interact with your application.

For example, adding a record like so (this example shows the entire `users.json` file):

    {
        "Documentation User": {
            "username": "DOC_USER",
            "roles": ["Example Role A"],
            "unique_id": 42
        }
    }

The data you require for these users can be completely customised for what information you need, so whilst the example shows `username`, `roles`
and `unique_id` as possible values we may want to use, this is not an exhaustive list. The key that is used (so in this example, `"Documentation User"`)
is also customisable and should be how you want to easily reference retrieving this user in your tests.

### Considering Security

An important note on managing users in this way is that passwords or security credentials should **never** be stored in the `users.json` file. These
are considered secrets, and whilst it may be convenient to store them in this file, it goes against the
[security principles outlined in the Software Engineering Quality Framework](https://github.com/NHSDigital/software-engineering-quality-framework/blob/main/practices/security.md#application-level-security).

With this in mind, it's recommended to do the following when it comes to managing these types of credentials:

- When running locally, store any secret values in a local configuration file and set this file in `.gitignore` so it is not committed to the codebase.
- When running via a CI/CD process, store any secret values in an appropriate secret store and pass the values into pytest at runtime.

## `retrieve_user()`: Retrieve User Details

The `retrieve_user()` method is designed to easily retrieve the data for a specific user entry from the `users.json` file. This is a static method,
so can be called using the following logic:

    # Retrieving documentation user details from example
    user_details = UserTools.retrieve_user("Documentation User")

### Required Arguments

The following are required for `UserTools.retrieve_user()`:

| Argument | Format | Description                                             |
| -------- | ------ | ------------------------------------------------------- |
| user     | `str`  | The key from `users.json` for the user details required |

### Returns

A Python `dict` object that contains the values associated with the provided user argument.

### Example Usage

When using a `users.json` file as set up in the example above:

    from utils.user_tools import UserTools
    from playwright.sync_api import Page

    def test_login(page: Page) -> None:
        # Retrieving documentation user details from example
        user_details = UserTools.retrieve_user("Documentation User")

        # Use values to populate a form
        page.get_by_role("textbox", name="Username").fill(user_details["username"])
        page.get_by_role("textbox", name="ID").fill(user_details["unique_id"])

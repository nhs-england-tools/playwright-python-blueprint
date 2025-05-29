# Utility Guide: User Tools

The User Tools utility provided by this blueprint allows for the easy management of test users via a `users.json` file included
at the base of the repository.

## Table of Contents

- [Utility Guide: User Tools](#utility-guide-user-tools)
  - [Table of Contents](#table-of-contents)
  - [Using the User Tools class](#using-the-user-tools-class)
  - [Managing Users](#managing-users)
    - [Considering Security](#considering-security)
  - [`user_login()`: Log In as a User](#user_login-log-in-as-a-user)
    - [Required Arguments](#required-arguments)
    - [Example Usage](#example-usage)
  - [`retrieve_user()`: Retrieve User Details](#retrieve_user-retrieve-user-details)
    - [Required Arguments](#required-arguments-1)
    - [Returns](#returns)
    - [Example Usage](#example-usage-1)

## Using the User Tools class

You can use the User Tools class by importing it in your test file:

```python
from utils.user_tools import UserTools
```

This module has been designed as a static class, so you do not need to instantiate it when you want to retrieve any user information.

## Managing Users

For this class, users are managed via the [`users.json`](../../users.json) file provided with this repository. For any new users you need to add, simply add a new record with any appropriate metadata you need for the user whilst they interact with your application.

For example, adding a record like so (this example shows the entire `users.json` file):

```json
{
    "Hub Manager State Registered at BCS01": {
        "username": "BCSS401",
        "roles": [
            "Hub Manager State Registered, Midlands and North West"
        ]
  }
}
```

### Considering Security

An important note on managing users in this way is that passwords or security credentials should **never** be stored in the `users.json` file. These are considered secrets, and whilst it may be convenient to store them in this file, it goes against the
[security principles outlined in the Software Engineering Quality Framework](https://github.com/NHSDigital/software-engineering-quality-framework/blob/main/practices/security.md#application-level-security).

With this in mind, it's recommended to do the following when it comes to managing these types of credentials:

- When running locally, store any secret values in a local configuration file such as `local.env`. This file is created by running the script [`setup_env_file.py`](../../setup_env_file.py) and is included in `.gitignore` so it is not committed to the codebase.
- When running via a CI/CD process, store any secret values in an appropriate secret store and pass the values into pytest at runtime.

## `user_login()`: Log In as a User

The `user_login()` method allows you to log in to the BCSS application as a specified user. It retrieves the username from the `users.json` file and the password from the `local.env` file (using the `BCSS_PASS` environment variable).

### Required Arguments

| Argument  | Format | Description                                                        |
|-----------|--------|--------------------------------------------------------------------|
| page      | `Page` | The Playwright page object to interact with.                       |
| username  | `str`  | The key from `users.json` for the user you want to log in as.      |

### Example Usage

```python
from utils.user_tools import UserTools

def test_login_as_user(page):
    UserTools.user_login(page, "Hub Manager State Registered at BCS01")
```

> **Note:**
> Ensure you have set the `BCSS_PASS` environment variable in your `local.env` file (created by running `setup_env_file.py`) before using this method.

---

## `retrieve_user()`: Retrieve User Details

The `retrieve_user()` method is designed to easily retrieve the data for a specific user entry from the `users.json` file. This is a static method,
so can be called using the following logic:

```python
# Retrieving documentation user details from example
user_details = UserTools.retrieve_user("Hub Manager State Registered at BCS01")
```

### Required Arguments

The following are required for `UserTools.retrieve_user()`:

| Argument | Format | Description                                             |
| -------- | ------ | ------------------------------------------------------- |
| user     | `str`  | The key from `users.json` for the user details required |

### Returns

A Python `dict` object that contains the values associated with the provided user argument.

### Example Usage

When using a `users.json` file as set up in the example above:

```python
from utils.user_tools import UserTools
from playwright.sync_api import Page

def test_login(page: Page) -> None:
    # Retrieving documentation user details from example
    user_details = UserTools.retrieve_user("Hub Manager State Registered at BCS01")

    # Use values to populate a form
    page.get_by_role("textbox", name="Username").fill(user_details["username"])
```

---

For more details on each function's implementation, refer to the source code in `utils/user_tools.py`.

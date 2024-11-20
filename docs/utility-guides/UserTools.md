# Utility Guide: User Tools

The User Tools utility provided by this blueprint allows for the easy management of test users via a json file included
at the base of the repository.

## Table of Contents

- [Utility Guide: User Tools](#utility-guide-user-tools)
  - [Table of Contents](#table-of-contents)
  - [Using the User Tools class](#using-the-user-tools-class)
  - [Managing Users](#managing-users)

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

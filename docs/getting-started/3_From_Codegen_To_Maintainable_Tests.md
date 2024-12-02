# Getting Started #3: From `codegen` To Maintainable Tests

This guide outlines the process of taking a test generated using the `playwright codegen` tool to a state where it
will be easy to maintain going forward.

## Contents

- [Getting Started #3: From `codegen` To Maintainable Tests](#getting-started-3-from-codegen-to-maintainable-tests)
  - [Contents](#contents)
  - [Setting The Scene](#setting-the-scene)
  - [Using `codegen` For A Test](#using-codegen-for-a-test)
  - [Breaking The Test Down](#breaking-the-test-down)
  - [Creating A Sign In Utility](#creating-a-sign-in-utility)

## Setting The Scene

For this guide, we will look at refactoring a test that we've initially generated using the `codegen` utility provided
by Playwright into a format that will make it easy to maintain going forward.

To start, here is our application under test for the purposes of this guide:

- Login Screen: A simple username / password login screen.

<!-- vale off -->
![An image of the example application login screen](./img/3-1_example_login.png "Example login screen with a username and password field")
<!-- vale on -->

- Main Menu: The landing page once logged in.

<!-- vale off -->
![An image of the example application home screen](./img/3-2_example_home.png "Example home screen with a navigation menu, news and alerts section")
<!-- vale on -->

- Search Patient: Some functionality to search for patients in our application.

<!-- vale off -->
![An image of the example application search patient screen](./img/3-2_example_home.png "Example search patient screen with a search field and table")
<!-- vale on -->

- View Patient: A page for viewing the patient we have selected from the search menu.

<!-- vale off -->
![An image of the example application view patient screen](./img/3-2_example_home.png "Example view patient screen showing an example patient")
<!-- vale on -->

## Using `codegen` For A Test

To get our first test, we will use the `codegen` tool by using the following command:

    playwright codegen <link to example application>

We then navigate through the application to do an assertion of the View Patient screen, doing the following actions:

1. Navigate to example application to reach the Sign In screen
2. Click on the Username field and enter a test username ("Test")
3. Click on the Password field and enter a test password ("test")
4. Press the Sign In button to reach the Home / Welcome screen
5. Click on the Search button in the navigation menu to reach the Search screen
6. Click on the Patient Name field and enter a test patient ("Test Patient")
7. Press the Search button to populate the results table
8. Select the top result from the table and press the View button to reach the View Patient screen
9. On the View Patient screen, confirm we've hit the correct screen by asserting the header of this screen is "View Patient"

This generates the following code (when setting `pytest` as the Target):

    import re
    from playwright.sync_api import Page, expect


    def test_example(page: Page) -> None:
        page.goto("https://<example application url>/signin")
        page.get_by_role("textbox", name="Username").click()
        page.get_by_role("textbox", name="Username").fill("Test")
        page.get_by_role("textbox", name="Password").click()
        page.get_by_role("textbox", name="Password").fill("test")
        page.get_by_role("button", name="submit").click()
        page.get_by_role("link", name="Search").click()
        page.get_by_role("textbox", name="Patient Name").click()
        page.get_by_role("textbox", name="Patient Name").fill("Test Patient")
        page.get_by_role("button", name="search").click()
        page.get_by_role("button", name="view").nth(0).click()
        expect(page.get_by_role("heading")).to_contain_text("View Patient")

The immediate thing to notice with this test is that whilst it may work, there are a number of parts with this test
that could easily be refactored or reworked in a way that could be utilised by multiple tests. There is also scope to
add value to this test, and reduce the scope for potential flakiness.

## Breaking The Test Down

Our first step with refining this test is to break down the individual components of the test, to work out logical points
of reuse. The main things to consider with this are:

- Are there any steps that are repeatable or we would want to use many times?
- Are there any consistent elements across the pages we are navigating through?
- When running this test as-is, are there any areas which are prone to failure or flakiness?

The first part is the sign in step, which is likely applicable to every test we may want to run against this UI:

    page.goto("https://<example application url>/signin")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill("Test")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("test")
    page.get_by_role("button", name="submit").click()

The next part is navigating to the Search screen, which is a simple step but one we may wish to reuse many times across multiple tests:

    page.get_by_role("link", name="Search").click()

The third part is the search of the patient on the Search screen itself and selecting the first entry:

    page.get_by_role("textbox", name="Patient Name").click()
    page.get_by_role("textbox", name="Patient Name").fill("Test Patient")
    page.get_by_role("button", name="search").click()
    page.get_by_role("button", name="view").nth(0).click()

The final part is the assertion of the View Patient header once selecting a patient:

    expect(page.get_by_role("heading")).to_contain_text("View Patient")

## Creating A Sign In Utility

To do

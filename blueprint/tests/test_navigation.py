# import pytest
# from playwright.sync_api import Page, expect

# @pytest.mark.skip
# def Login(page: Page) -> None:
#     page.goto('https://www.saucedemo.com/')
#     page.get_by_placeholder("Username").fill("standard_user")
#     page.get_by_placeholder("Password").fill("secret_sauce")
#     page.get_by_role("button", name="Login").click()

# @pytest.mark.only
# def AddItemsToCart(page: Page) -> None:
#     page.locator('#add-to-cart-sauce-labs-backpack').click()

# @pytest.mark.only
# def Checkout(page: Page) -> None:
#     page.locator('.shopping_cart_badge').click()
#     page.get_by_role("button", name="Checkout").click()
#     # Enter name and zip code
#     page.get_by_placeholder("First Name").fill("Andy")
#     page.get_by_placeholder("Last Name").fill("George")
#     page.get_by_placeholder("Zip/Postal Code").fill("AA11 1AA")
#     #Complete checkout
#     page.get_by_role("button", name="Continue").click()
#     page.get_by_role("button", name="Finish").click()
#     expect(page.locator('.complete-header')).to_contain_text("Thank you for your order!")


from playwright.sync_api import Page, expect
class BcssLoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.page.goto("/")
        self.username = page.get_by_role("textbox", name="Username")
        self.password = page.get_by_role("textbox", name="Password")
        self.submit_button = page.get_by_role("button", name="submit")


    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.submit_button.click()

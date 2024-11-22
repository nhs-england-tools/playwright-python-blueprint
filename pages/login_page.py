from playwright.sync_api import Page


class BcssLoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.page.goto("/")
        self.username = page.get_by_role("textbox", name="Username")
        self.password = page.get_by_role("textbox", name="Password")
        self.submit_button = page.get_by_role("button", name="submit")


    def login(self, username, password):
        """Logs in to bcss with specified user credentials
        Args:
            username (str) enter a username
            password (str) enter a password
        """
        self.username.fill(username)
        self.password.fill(password)
        self.submit_button.click()

    def login_as_user_bcss401(self):
        """Logs in to bcss as the test user 'BCSS401'"""
        self.username.fill("BCSS401")
        self.password.fill("changeme")
        self.submit_button.click()

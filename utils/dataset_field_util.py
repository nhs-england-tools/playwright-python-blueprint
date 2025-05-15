from playwright.sync_api import Page, Locator


class DatasetFieldUtil:

    def __init__(self, page: Page):
        self.page = page

    def get_input_locator_for_field(self, text: str) -> Locator:
        """
        Matches input elements that are to the right of any element matching the inner selector, at any vertical position.

        Args:
            text (str): The text of the element you want to get the input locator of

        Returns:
            Locator: the locator of the input
        """
        return self.page.locator(f'input:right-of(:text(\"{text}\"))').first

    def populate_input_locator_for_field(
        self, text: str, value: str
    ) -> None:
        """
        Inputs a value into an input to the right of any element matching the inner selector, at any vertical position.

        Args:
            text (str): The text of the element you want to get the input locator of
            value (str): The value you want to input
        """
        locator = self.get_input_locator_for_field(text)
        locator.fill(value)

    def get_select_locator_for_field(self, text: str) -> Locator:
        """
        Matches select elements that are to the right of any element matching the inner selector, at any vertical position.

        Args:
            text (str): The text of the element you want to get the select locator of

        Returns:
            Locator: the locator of the input
        """
        return self.page.locator(f'select:right-of(:text(\"{text}\"))').first

    def populate_select_locator_for_field(
        self, text: str, option: str
    ) -> None:
        """
        Matches select elements that are to the right of any element matching the inner selector, at any vertical position.

        Args:
            text (str): The text of the element you want to get the select locator of.
            option (str): The option you want to select
        """
        locator = self.get_select_locator_for_field(text)
        locator.select_option(option)

    def get_input_locator_for_field_inside_div(self, text: str, div: str) -> Locator:
        """
        Matches input elements that are to the right of any element matching the inner selector, at any vertical position.

        Args:
            text (str): The text of the element you want to get the input locator of
            div (str): The ID of the DIV the text belongs in

        Returns:
            Locator: the locator of the input
        """
        container = self.page.locator(f"div#{div}")
        return container.locator(f'input:right-of(:text(\"{text}\"))').first

    def populate_input_locator_for_field_inside_div(
        self, text: str, div: str, value: str
    ) -> None:
        """
        Inputs a value into an input to the right of any element matching the inner selector, at any vertical position.

        Args:
            text (str): The text of the element you want to get the input locator of
            div (str): The ID of the DIV the text belongs in
            value (str): The value you want to input
        """
        locator = self.get_input_locator_for_field_inside_div(text, div)
        locator.fill(value)

    def get_select_locator_for_field_inside_div(self, text: str, div: str) -> Locator:
        """
        Matches select elements that are to the right of any element matching the inner selector, at any vertical position.

        Args:
            text (str): The text of the element you want to get the select locator of
            div (str): The ID of the DIV the text belongs in

        Returns:
            Locator: the locator of the input
        """
        container = self.page.locator(f"div#{div}")
        return container.locator(f'select:right-of(:text(\"{text}\"))').first

    def populate_select_locator_for_field_inside_div(
        self, text: str, div: str, option: str
    ) -> None:
        """
        Matches select elements that are to the right of any element matching the inner selector, at any vertical position.

        Args:
            text (str): The text of the element you want to get the select locator of.
            div (str): The ID of the DIV the text belongs in
            option (str): The option you want to select
        """
        locator = self.get_select_locator_for_field_inside_div(text, div)
        locator.select_option(option)

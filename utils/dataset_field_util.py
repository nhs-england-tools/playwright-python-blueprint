from playwright.sync_api import Page, Locator
from typing import Optional, List
import logging


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
        return self.page.locator(f'input:right-of(:text("{text}"))').first

    def populate_input_locator_for_field(self, text: str, value: str) -> None:
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
        return self.page.locator(f'select:right-of(:text("{text}"))').first

    def populate_select_locator_for_field(self, text: str, option: str) -> None:
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
        return container.locator(f'input:right-of(:text("{text}"))').first

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
        return container.locator(f'select:right-of(:text("{text}"))').first

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

    def click_lookup_link_inside_div(self, text: str, div: str) -> None:
        """
        Finds and clicks the 'lookup' link (anchor tag) that is in the same row/section
        as the provided label text within a given div container.
        Args:
            text (str): The label text that appears before the 'lookup' link (e.g., "Pathology Provider")
            div (str): The ID of the outer div container to scope the search within
        """
        container = self.page.locator(f"div#{div}")
        row = container.locator(
            f"xpath=//span[contains(@class,'label') and contains(normalize-space(), '{text}')]/ancestor::div[contains(@class,'noTableRow')]"
        )
        lookup_link = row.locator("a:text('lookup')").first
        lookup_link.click()

    def assert_cell_to_right_has_expected_text(
        self, text: str, expected_text: str, div: Optional[str] = None
    ) -> None:
        """
        Asserts that the first visible field to the right of the cell containing `text` has the expected value,
        ensuring it is in the same row (not just visually to the right).
        Args:
            text (str): The text in the left-hand cell.
            expected_text (str): The expected value in the adjacent right-hand cell.
            div (str, optional): The ID of the container DIV. Defaults to None.
        Raises:
            AssertionError: If the expected text is not found.
        """
        logging.info(f"Checking that the cell next to {text} contains {expected_text}")

        scope = self.page
        if div:
            scope = self.page.locator(f"div#{div}")

        # Locate the parent row containing the label text
        row = scope.locator(f'.noTableRow:has-text("{text}")').first

        # Defensive check
        if not row.is_visible():
            raise AssertionError(f'Could not find a visible row with text "{text}".')

        # Find all children inside this row
        cells = row.locator("xpath=./*").all()

        # Loop through children to find the one with the label text, then check the next one
        for idx, cell in enumerate(cells):
            cell_text = cell.inner_text().strip()
            if text.strip() in cell_text:
                if idx + 1 >= len(cells):
                    raise AssertionError(f'No cell found to the right of "{text}".')
                right_cell = cells[idx + 1]

                # Check <input>
                input_el = right_cell.locator("input")
                if input_el.count() > 0:
                    value = input_el.first.input_value().strip()
                    assert (
                        value == expected_text
                    ), f'Expected "{expected_text}" but found "{value}" in input.'
                    logging.info(f"The cell next to {text} contains {expected_text}")
                    return

                # Check <select>
                select_el = right_cell.locator("select")
                if select_el.count() > 0:
                    selected = select_el.locator("option:checked").inner_text().strip()
                    assert (
                        selected == expected_text
                    ), f'Expected "{expected_text}" but found "{selected}" in select.'
                    logging.info(f"The cell next to {text} contains {expected_text}")
                    return

                # Check <p>, <span>, etc.
                generic_text = right_cell.inner_text().strip()
                assert (
                    generic_text == expected_text
                ), f'Expected "{expected_text}" but found "{generic_text}".'
                logging.info(f"The cell next to {text} contains {expected_text}")
                return

        raise AssertionError(f'Could not locate label "{text}" in any cell.')

    def assert_select_to_right_has_values(
        self, text: str, expected_values: List[str], div: Optional[str] = None
    ) -> None:
        """
        Asserts that the select dropdown to the right of the cell containing `text` includes all expected values.
        Args:
            text (str): The label or text on the left-hand side.
            expected_values (List[str]): List of expected dropdown values.
            div (str, optional): The ID of the container DIV. Defaults to None.
        Raises:
            AssertionError: If the select element is not found or expected values are missing.
        """
        logging.info(
            f"Checking that the dropdown next to {text} contains {expected_values}"
        )
        scope = self.page
        if div:
            scope = self.page.locator(f"div#{div}")

        # Locate the parent row containing the label text
        row = scope.locator(f'.noTableRow:has-text("{text}")').first

        if not row.is_visible():
            raise AssertionError(f'Could not find a visible row with text "{text}".')

        # Find all children of the row
        cells = row.locator("xpath=./*").all()

        for idx, cell in enumerate(cells):
            if text.strip() in cell.inner_text().strip():
                if idx + 1 >= len(cells):
                    raise AssertionError(f'No cell found to the right of "{text}".')

                right_cell = cells[idx + 1]
                select_el = right_cell.locator("select").first

                if not select_el.is_visible():
                    raise AssertionError(
                        f'Select element to right of "{text}" is not visible.'
                    )

                actual_options = select_el.locator("option").all_text_contents()
                missing = [val for val in expected_values if val not in actual_options]

                assert not missing, (
                    f'Missing expected dropdown values in select to right of "{text}": {missing}. '
                    f"Actual options: {actual_options}"
                )
                logging.info(f"The dropdown next to {text} contains {expected_values}")
                return

        raise AssertionError(f'Could not locate label "{text}" in any cell.')

    def assert_checkbox_to_right_is_ticked_or_not(
        self, text: str, expected_state: str, div: Optional[str] = None
    ) -> None:
        """
        Asserts that the checkbox to the right of a given label is either ticked or unticked.
        Args:
            text (str): The label or text on the left-hand side.
            expected_state (str): Either "Ticked" or "Unticked".
            div (Optional[str]): Optional ID of a container DIV.
        Raises:
            AssertionError: If checkbox is not found or its state doesn't match.
        """
        logging.info(f"Checking that the checkbox next to {text} is {expected_state}")
        if expected_state not in ("Ticked", "Unticked"):
            raise ValueError('expected_state must be either "Ticked" or "Unticked"')

        scope = self.page
        if div:
            scope = self.page.locator(f"div#{div}")

        # Use :right-of to locate checkbox right of the label text
        checkbox = scope.locator(
            f'input[type="checkbox"]:right-of(:text("{text}"))'
        ).first

        if not checkbox.is_visible():
            raise AssertionError(f'Checkbox to the right of "{text}" is not visible.')

        is_checked = checkbox.is_checked()
        expected_checked = expected_state == "Ticked"

        assert is_checked == expected_checked, (
            f'Expected checkbox to be {expected_state} to the right of "{text}", '
            f'but it was {"Ticked" if is_checked else "Unticked"}.'
        )
        logging.info(f"The checkbox next to {text} is {expected_state}")

    def assert_radio_to_right_is_selected(
        self, text: str, expected_value: str, div: Optional[str] = None
    ) -> None:
        """
        Asserts that the selected radio button to the right of a label with the given text matches the expected value.
        Args:
            text (str): The label or text on the left-hand side.
            expected_value (str): The expected label/text of the selected radio button.
            div (Optional[str]): Optional ID of a container DIV.
        Raises:
            AssertionError: If no radio button is selected, or the selected one doesn't match expected.
        """
        logging.info(
            f"Checking that the radio select next to {text} is {expected_value}"
        )
        scope = self.page
        if div:
            scope = self.page.locator(f"div#{div}")

        # Find all radio buttons to the right of the label
        radio_buttons = scope.locator(f'input[type="radio"]:right-of(:text("{text}"))')

        if radio_buttons.count() == 0:
            raise AssertionError(f'No radio buttons found to the right of "{text}".')

        found_match = False
        for radio_button_index in range(radio_buttons.count()):
            radio = radio_buttons.nth(radio_button_index)
            if radio.is_checked():
                # Try to find the label next to the radio
                label = radio.evaluate_handle(
                    """
                    (radio) => {
                        const label = radio.closest('label');
                        return label ? label.innerText : radio.nextSibling?.textContent?.trim() || "";
                    }
                """
                )
                label_text = label.json_value()
                found_match = True
                assert label_text.strip() == expected_value, (
                    f'Expected selected radio to be "{expected_value}" to the right of "{text}", '
                    f'but found "{label_text}".'
                )
                break

        if not found_match:
            raise AssertionError(
                f'No radio button is selected to the right of "{text}".'
            )
        logging.info(f"The radio selected next to {text} was {expected_value}")

    def assert_checkbox_to_right_is_enabled(
        self,
        text: str,
        should_be_enabled: bool,
        div: Optional[str] = None,
    ) -> None:
        """
        Asserts that the (first) checkbox immediately to the right of a label with
        the given text is enabled/disabled as expected.
        Args:
            text (str): Visible label or text on the left-hand side.
            should_be_enabled (bool): True if the checkbox is expected to be
                enabled (interactive); False if it is expected to be disabled.
            div (Optional[str]): Optional ID of a container DIV that scopes the
                search. Useful when the same label appears more than once.
        Raises:
            AssertionError: If the checkbox isn’t found, or its enabled/disabled
                state doesn’t match the expectation.
        """
        state_word = "enabled" if should_be_enabled else "disabled"
        logging.info(f'Checking that the checkbox next to "{text}" is {state_word}')

        # Restrict the search to a container if one is supplied
        scope = self.page.locator(f"div#{div}") if div else self.page

        # Playwright’s relational selector: anything :right-of the label text
        checkbox = scope.locator(
            f'input[type="checkbox"]:right-of(:text("{text}"))'
        ).first

        if checkbox.count() == 0:
            raise AssertionError(f'No checkbox found to the right of "{text}".')

        # .is_enabled() returns True iff the element is *not* disabled
        is_enabled = checkbox.is_enabled()

        assert is_enabled == should_be_enabled, (
            f'Expected checkbox to the right of "{text}" to be {state_word}, '
            f'but it is {"enabled" if is_enabled else "disabled"}.'
        )

        logging.info(f'The checkbox next to "{text}" is correctly {state_word}.')

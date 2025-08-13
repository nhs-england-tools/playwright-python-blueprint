from playwright.sync_api import Page, Locator
from typing import Optional, List
import logging
from pages.datasets.investigation_dataset_page import (
    to_enum_name_or_value,
)


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
        logging.info(f"Filling input for field '{text}' with value '{value}'")
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
        logging.info(
            f"Selecting option '{to_enum_name_or_value(option)}' for field '{text}'"
        )
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
        logging.info(f"Filling input for field '{text}' with value '{value}'")
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
        logging.info(
            f"Selecting option '{to_enum_name_or_value(option)}' for field '{text}'"
        )
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
        supporting both table row and span structures.
        Args:
            text (str): The text in the left-hand cell.
            expected_text (str): The expected value in the adjacent right-hand cell.
            div (str, optional): The ID of the container DIV. Defaults to None.
        Raises:
            AssertionError: If the expected text is not found.
        """
        logging.info(f"Checking that the cell next to {text} contains {expected_text}")
        scope = self.page.locator(f"div#{div}") if div else self.page

        if self._check_table_row(scope, text, expected_text):
            return
        if self._check_span_structure(scope, text, expected_text):
            return

        raise AssertionError(
            f'Could not find a visible row or span with text "{text}".'
        )

    def _check_table_row(
        self, scope: Locator | Page, text: str, expected_text: str
    ) -> bool:
        """
        Checks if the expected text is present in the cell to the right of the cell containing `text`
        within a table row structure.
        Args:
            scope (Locator): The Playwright locator to scope the search.
            text (str): The label text to search for.
            expected_text (str): The expected value in the adjacent right-hand cell.
        Returns:
            bool: True if the expected text is found and matches, False otherwise.
        Raises:
            AssertionError: If the actual value does not match the expected value.
        """
        row = scope.locator(f'.noTableRow:has-text("{text}")').first
        if row.count() == 0 or not row.is_visible():
            return False
        cells = row.locator("xpath=./*").all()
        label_cell_index = next(
            (
                cell_index
                for cell_index, cell in enumerate(cells)
                if text.strip() in cell.inner_text().strip()
            ),
            None,
        )
        if label_cell_index is None or label_cell_index + 1 >= len(cells):
            return False
        right_cell = cells[label_cell_index + 1]
        if self._assert_right_cell(right_cell, text, expected_text):
            logging.info(f"The cell next to {text} contains {expected_text}")
            return True
        return False

    def _assert_right_cell(
        self, right_cell: Locator, text: str, expected_text: str
    ) -> bool:
        """
        Asserts that the right cell contains the expected value, checking input, select, or generic text.
        Args:
            right_cell (Locator): The Playwright locator for the cell to the right.
            text (str): The label text for logging and error messages.
            expected_text (str): The expected value to check.
        Returns:
            bool: True if the expected value is found, False otherwise.
        """
        input_locator = right_cell.locator("input")
        if input_locator.count() > 0:
            value = input_locator.first.input_value().strip()
            if value == expected_text:
                logging.info(
                    f'Input to the right of "{text}" contains "{expected_text}"'
                )
                return True
            return False

        select_locator = right_cell.locator("select")
        if select_locator.count() > 0:
            selected = select_locator.locator("option:checked").inner_text().strip()
            if selected == expected_text:
                logging.info(
                    f'Select to the right of "{text}" contains "{expected_text}"'
                )
                return True
            return False

        generic_text = right_cell.inner_text().strip()
        if generic_text == expected_text:
            logging.info(f'Cell to the right of "{text}" contains "{expected_text}"')
            return True
        return False

    def _check_span_structure(
        self, scope: Locator | Page, text: str, expected_text: str
    ) -> bool:
        """
        Checks if the expected text is present in a span structure (label and userInput spans).
        Args:
            scope (Locator): The Playwright locator to scope the search.
            text (str): The label text to search for.
            expected_text (str): The expected value in the adjacent userInput span.
        Returns:
            bool: True if the expected text is found and matches, False otherwise.
        Raises:
            AssertionError: If the actual value does not match the expected value.
        """
        label_span = scope.locator(f'span.label:has-text("{text}")').first
        user_input_span = label_span.locator(
            'xpath=following-sibling::span[contains(@class,"userInput")]'
        ).first
        if (
            label_span.count() > 0
            and label_span.is_visible()
            and user_input_span.count() > 0
            and user_input_span.is_visible()
        ):
            actual_text = user_input_span.inner_text().strip()
            assert (
                actual_text == expected_text
            ), f'Expected "{expected_text}" but found "{actual_text}" in userInput span next to "{text}".'
            logging.info(f"The span next to '{text}' contains '{expected_text}'")
            return True
        return False

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
        Handles both wrapped <label> patterns and label-for patterns.

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

        # Find all radio buttons to the right of the label text
        radio_buttons = scope.locator(f'input[type="radio"]:right-of(:text("{text}"))')

        count = radio_buttons.count()
        if count == 0:
            raise AssertionError(f'No radio buttons found to the right of "{text}".')

        found_match = False

        for radio_index in range(count):
            radio = radio_buttons.nth(radio_index)
            if radio.is_checked():
                # Try both wrapped label and label-for approaches
                label_text = radio.evaluate(
                    """
                    (radio) => {
                        // Case 1: Wrapped inside label
                        let label = radio.closest('label');
                        if (label) {
                            return label.innerText.trim();
                        }
                        // Case 2: label-for pattern
                        const id = radio.id;
                        if (id) {
                            label = document.querySelector(`label[for="${id}"]`);
                            if (label) {
                                return label.innerText.trim();
                            }
                        }
                        // Fallback: Try immediate text sibling
                        return radio.nextSibling?.textContent?.trim() || "";
                    }
                """
                )
                found_match = True
                assert label_text == expected_value, (
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

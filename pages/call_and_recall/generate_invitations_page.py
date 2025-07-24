from playwright.sync_api import Page, expect
from pages.base_page import BasePage
import pytest
import logging
from utils.oracle.oracle import OracleDB
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder
from classes.user import User
from classes.subject import Subject
from utils.table_util import TableUtils

DISPLAY_RS_SELECTOR = "#displayRS"


class GenerateInvitationsPage(BasePage):
    """Generate Invitations page locators, and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Generate Invitations - page links
        self.generate_invitations_button = self.page.get_by_role(
            "button", name="Generate Invitations"
        )
        self.display_rs = self.page.locator(DISPLAY_RS_SELECTOR)
        self.refresh_button = self.page.get_by_role("button", name="Refresh")
        self.planned_invitations_total = self.page.locator("#col8_total")
        self.self_referrals_total = self.page.locator("#col5_total")

    def click_generate_invitations_button(self) -> None:
        """This function is used to click the Generate Invitations button."""
        self.click(self.generate_invitations_button)

    def click_refresh_button(self) -> None:
        """This function is used to click the Refresh button."""
        self.click(self.refresh_button)

    def verify_generate_invitations_title(self) -> None:
        """This function is used to verify the Generate Invitations page title."""
        self.bowel_cancer_screening_page_title_contains_text("Generate Invitations")

    def verify_invitation_generation_progress_title(self) -> None:
        """This function is used to verify the Invitation Generation Progress page title."""
        self.bowel_cancer_screening_page_title_contains_text(
            "Invitation Generation Progress"
        )

    def wait_for_invitation_generation_complete(
        self, number_of_invitations: int
    ) -> bool:
        """
        This function is used to wait for the invitations to be generated.
        Every 5 seconds it refreshes the table and checks to see if the invitations have been generated.
        It also checks that enough invitations were generated and checks to see if self referrals are present
        """
        self.page.wait_for_selector(DISPLAY_RS_SELECTOR, timeout=5000)

        if self.planned_invitations_total == "0":
            pytest.fail("There are no planned invitations to generate")

        # Initially, ensure the table contains "Queued"
        expect(self.display_rs).to_contain_text("Queued")

        # Set timeout parameters
        timeout = 120000  # Total timeout of 120 seconds (in milliseconds)
        wait_interval = 5000  # Wait 5 seconds between refreshes (in milliseconds)
        elapsed = 0

        # Loop until the table no longer contains "Queued"
        logging.info("Waiting for successful generation")
        while (
            elapsed < timeout
        ):  # there may be a stored procedure to speed this process up
            table_text = self.display_rs.text_content()
            if table_text is None:
                pytest.fail("Failed to retrieve table text content")

            if "Failed" in table_text:
                pytest.fail("Invitation has failed to generate")
            elif "Queued" in table_text or "In Progress" in table_text:
                # Click the Refresh button
                self.click_refresh_button()
                self.page.wait_for_timeout(wait_interval)
                elapsed += wait_interval
            else:
                break

        # Final check: ensure that the table now contains "Completed"
        try:
            expect(self.display_rs).to_contain_text("Completed")
            logging.info("Invitations successfully generated")
            logging.info(f"Invitations took {elapsed / 1000} seconds to generate")
        except Exception as e:
            pytest.fail(f"Invitations not generated successfully: {str(e)}")

        value = self.planned_invitations_total.text_content()
        if value is None:
            pytest.fail("Failed to retrieve planned invitations total")
        value = value.strip()  # Get text and remove extra spaces
        if int(value) < number_of_invitations:
            pytest.fail(
                f"Expected {number_of_invitations} invitations generated but got {value}"
            )

        self_referrals_total_text = self.self_referrals_total.text_content()
        if self_referrals_total_text is None:
            pytest.fail("Failed to retrieve self-referrals total")
        self_referrals_total = int(self_referrals_total_text.strip())
        if self_referrals_total >= 1:
            return True
        else:
            logging.warning("No S1 Digital Leaflet batch will be generated")
            return False

    def wait_for_self_referral_invitation_generation_complete(
        self, expected_minimum: int = 1
    ) -> bool:
        """
        Waits until the invitations have been generated and checks that 'Self Referrals Generated' meets the expected threshold.

        Args:
            expected_minimum (int): Minimum number of self-referrals expected to be generated (default is 1)

        Returns:
            bool: True if threshold is met, False otherwise.
        """
        # Reuse the existing table completion logic — consider extracting this into a shared method later
        timeout = 120000
        wait_interval = 5000
        elapsed = 0
        logging.info(
            "[WAIT] Waiting for self-referral invitation generation to complete"
        )

        while elapsed < timeout:
            table_text = self.display_rs.text_content()
            if table_text is None:
                pytest.fail("Failed to retrieve table text content")

            if "Failed" in table_text:
                pytest.fail("Invitation has failed to generate")
            elif "Queued" in table_text or "In Progress" in table_text:
                self.click_refresh_button()
                self.page.wait_for_timeout(wait_interval)
                elapsed += wait_interval
            else:
                break

        try:
            expect(self.display_rs).to_contain_text("Completed")
            logging.info(
                f"[STATUS] Generation finished after {elapsed / 1000:.1f} seconds"
            )
        except Exception as e:
            pytest.fail(f"[ERROR] Invitations not generated successfully: {str(e)}")

        # Dynamically check 'Self Referrals Generated'
        table_utils = TableUtils(self.page, DISPLAY_RS_SELECTOR)

        try:
            value_text = table_utils.get_footer_value_by_header(
                "Self Referrals Generated"
            )
            value = int(value_text.strip())
            logging.info(f"[RESULT] 'Self Referrals Generated' = {value}")
        except Exception as e:
            pytest.fail(f"[ERROR] Unable to read 'Self Referrals Generated': {str(e)}")

        if value >= expected_minimum:
            return True
        else:
            logging.warning(
                f"[ASSERTION] Expected at least {expected_minimum}, but got {value}"
            )
            return False

    def check_self_referral_subjects_ready(
        self, search_scope: str, volume: str
    ) -> None:
        """
        Asserts whether self-referral subjects are ready to invite.

        Args:
            search_scope (str): Either "currently" or "now" to determine when to assert
            volume (str): Either "some" or "no" — expected number of self-referrals

        Raises:
            AssertionError if the count doesn't match expectation and search_scope is "now"
        """
        assert search_scope in (
            "currently",
            "now",
        ), f"Invalid search_scope: '{search_scope}'"
        assert volume in ("some", "no"), f"Invalid volume: '{volume}'"

        # Confirm we're on the Generate Invitations page
        self.verify_generate_invitations_title()

        # Extract and clean the count
        self_referrals_text = self.self_referrals_total.text_content()
        if self_referrals_text is None:
            pytest.fail("Failed to read self-referrals total")
        else:
            self_referrals_text = self_referrals_text.strip()

        self_referrals_count = int(self_referrals_text)

        # Determine if condition is met
        condition_met = (
            self_referrals_count > 0 if volume == "some" else self_referrals_count == 0
        )

        logging.debug(f"[DEBUG] Self-referral subject count = {self_referrals_count}")

        if search_scope == "now":
            assert (
                condition_met
            ), f"Expected {volume.upper()} self-referral subjects, but got {self_referrals_count}"
        logging.info(
            f"[SELF-REFERRAL CHECK] scope='{search_scope}' | expected='{volume}' | actual={self_referrals_count}"
        )

    def get_self_referral_eligible_subject(self, user: User, subject: Subject) -> str:
        criteria = {
            "screening status": "Inactive",
            "subject age": ">= 75",
            "has GP practice": "Yes - active",
            "subject hub code": "BCS02",
        }

        builder = SubjectSelectionQueryBuilder()
        query, bind_vars = builder.build_subject_selection_query(
            criteria, user, subject
        )

        oracle = OracleDB()
        result = oracle.execute_query(query, bind_vars)

        if result.empty:
            raise RuntimeError("No eligible subject found")

        return result.iloc[0]["subject_nhs_number"]

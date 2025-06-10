from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.table_util import TableUtils


class CreateAPlanPage(BasePage):
    """Create a Plan page locators and methods to interact with the page"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Call and Recall - page links
        self.set_all_button = self.page.get_by_role("link", name="Set all")
        self.daily_invitation_rate_field = self.page.get_by_placeholder(
            "Enter daily invitation rate"
        )
        self.weekly_invitation_rate_field = self.page.get_by_placeholder(
            "Enter weekly invitation rate"
        )
        self.update_button = self.page.get_by_role("button", name="Update")
        self.confirm_button = self.page.get_by_role("button", name="Confirm")
        self.save_button = self.page.get_by_role("button", name="Save")
        self.note_field = self.page.get_by_placeholder("Enter note")
        self.save_note_button = self.page.locator("#saveNote").get_by_role(
            "button", name="Save"
        )
        # Create A Plan Table Locators
        self.weekly_invitation_rate_field_on_table = self.page.locator(
            "#invitationPlan > tbody > tr:nth-child(1) > td.input.border-right.dt-type-numeric > input"
        )
        self.invitations_sent_value = self.page.locator(
            "tbody tr:nth-child(1) td:nth-child(8)"
        )

        self.resulting_position_value = self.page.locator(
            "#invitationPlan > tbody > tr:nth-child(1) > td:nth-child(9)"
        )

        # Initialize TableUtils for different tables
        self.create_a_plan_table = TableUtils(page, "#invitationPlan")

    def click_set_all_button(self) -> None:
        """Clicks the Set all button to set all values"""
        self.click(self.set_all_button)

    def fill_daily_invitation_rate_field(self, value: str) -> None:
        """Fills the daily invitation rate field with the given value"""
        self.daily_invitation_rate_field.fill(value)

    def fill_weekly_invitation_rate_field(self, value) -> None:
        """Fills the weekly invitation rate field with the given value"""
        self.weekly_invitation_rate_field.fill(value)

    def click_update_button(self) -> None:
        """Clicks the Update button to save any changes"""
        self.click(self.update_button)

    def click_confirm_button(self) -> None:
        """Clicks the Confirm button"""
        self.click(self.confirm_button)

    def click_save_button(self) -> None:
        """Clicks the Save button"""
        self.click(self.save_button)

    def fill_note_field(self, value) -> None:
        """Fills the note field with the given value"""
        self.note_field.fill(value)

    def click_save_note_button(self) -> None:
        """Clicks the Save note button"""
        self.click(self.save_note_button)

    def verify_create_a_plan_title(self) -> None:
        """Verifies the Create a Plan page title"""
        self.bowel_cancer_screening_page_title_contains_text("View a plan")

    def verify_weekly_invitation_rate_for_weeks(
        self, start_week: int, end_week: int, expected_weekly_rate: str
    ) -> None:
        """
        Verifies that the weekly invitation rate is correctly calculated and displayed for the specified range of weeks.

        Args:
        start_week (int): The starting week of the range.
        end_week (int): The ending week of the range.
        expected_weekly_rate (str): The expected weekly invitation rate.
        """

        # Verify the rate for the starting week
        weekly_invitation_rate_selector = "#invitationPlan > tbody > tr:nth-child(2) > td.input.border-right.dt-type-numeric > input"
        self.page.wait_for_selector(weekly_invitation_rate_selector)
        weekly_invitation_rate = self.page.locator(
            weekly_invitation_rate_selector
        ).input_value()

        assert (
            weekly_invitation_rate == expected_weekly_rate
        ), f"Expected weekly invitation rate '{expected_weekly_rate}' for week {start_week} but got '{weekly_invitation_rate}'"
        # Verify the rate for the specified range of weeks
        for week in range(start_week + 1, end_week + 1):
            weekly_rate_locator = f"#invitationPlan > tbody > tr:nth-child({week + 2}) > td.input.border-right.dt-type-numeric > input"

            # Wait for the element to be available
            self.page.wait_for_selector(weekly_rate_locator)

            # Get the input value safely
            weekly_rate_element = self.page.locator(weekly_rate_locator)
            assert (
                weekly_rate_element.is_visible()
            ), f"Week {week} rate element not visible"

            # Verify the value
            actual_weekly_rate = weekly_rate_element.input_value()
            assert (
                actual_weekly_rate == expected_weekly_rate
            ), f"Week {week} invitation rate should be '{expected_weekly_rate}', but found '{actual_weekly_rate}'"

            # Get the text safely
        # Get the frame first
        frame = self.page.frame(
            url="https://bcss-bcss-18680-ddc-bcss.k8s-nonprod.texasplatform.uk/invitation/plan/23159/23162/create"
        )

        # Ensure the frame is found before proceeding
        assert frame, "Frame not found!"

        # Now locate the input field inside the frame and get its value
        weekly_invitation_rate_selector = "#invitationPlan > tbody > tr:nth-child(2) > td.input.border-right.dt-type-numeric > input"
        weekly_invitation_rate = frame.locator(
            weekly_invitation_rate_selector
        ).input_value()

        # Assert the expected value
        assert (
            weekly_invitation_rate == expected_weekly_rate
        ), f"Week 2 invitation rate should be '{expected_weekly_rate}', but found '{weekly_invitation_rate}'"

    def increment_invitation_rate_and_verify_changes(self) -> None:
        """
        Increments the invitation rate by 1, then verifies that both the
        'Invitations Sent' has increased by 1 and 'Resulting Position' has decreased by 1.
        """
        # Capture initial values before any changes
        initial_invitations_sent = int(self.invitations_sent_value.inner_text().strip())
        initial_resulting_position = int(
            self.resulting_position_value.inner_text().strip()
        )

        # Increment the invitation rate
        current_rate = int(
            self.create_a_plan_table.get_cell_value("Invitation Rate", 1)
        )
        new_rate = str(current_rate + 1)
        self.weekly_invitation_rate_field_on_table.fill(new_rate)
        self.page.keyboard.press("Tab")

        # Wait dynamically for updates
        expect(self.invitations_sent_value).to_have_text(
            str(initial_invitations_sent + 1)
        )
        expect(self.resulting_position_value).to_have_text(
            str(initial_resulting_position + 1)
        )

        # Capture updated values
        updated_invitations_sent = int(self.invitations_sent_value.inner_text().strip())
        updated_resulting_position = int(
            self.resulting_position_value.inner_text().strip()
        )

        # Assert changes
        assert (
            updated_invitations_sent == initial_invitations_sent + 1
        ), f"Expected Invitations Sent to increase by 1. Was {initial_invitations_sent}, now {updated_invitations_sent}."

        assert (
            updated_resulting_position == initial_resulting_position + 1
        ), f"Expected Resulting Position to increase by 1. Was {initial_resulting_position}, now {updated_resulting_position}."

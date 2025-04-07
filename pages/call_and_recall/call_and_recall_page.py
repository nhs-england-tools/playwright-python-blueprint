from playwright.sync_api import Page
from pages.base_page import BasePage


class CallAndRecall(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        # Call and Recall - page links
        self.planning_and_monitoring_page = self.page.get_by_role(
            "link", name="Planning and Monitoring"
        )
        self.generate_invitations_page = self.page.get_by_role(
            "link", name="Generate Invitations"
        )
        self.invitation_generation_progress_page = self.page.get_by_role(
            "link", name="Invitation Generation Progress"
        )
        self.non_invitation_days_page = self.page.get_by_role(
            "link", name="Non Invitation Days"
        )
        self.age_extension_rollout_plans_page = self.page.get_by_role(
            "link", name="Age Extension Rollout Plans"
        )

    def go_to_planning_and_monitoring_page(self) -> None:
        self.click(self.planning_and_monitoring_page)

    def go_to_generate_invitations_page(self) -> None:
        self.click(self.generate_invitations_page)

    def go_to_invitation_generation_progress_page(self) -> None:
        self.click(self.invitation_generation_progress_page)

    def go_to_non_invitation_days_page(self) -> None:
        self.click(self.non_invitation_days_page)

    def go_to_age_extension_rollout_plans_page(self) -> None:
        self.click(self.age_extension_rollout_plans_page)

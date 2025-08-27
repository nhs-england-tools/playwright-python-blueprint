from typing import Optional, List
from datetime import date


class InvitationPlanWeek:
    """
    Represents a week within an invitation plan, including targets and cumulative counts.
    """

    def __init__(
        self,
        plan_id: Optional[int] = None,
        week_number: Optional[int] = None,
        week_start_date: Optional[date] = None,
        invite_days: Optional[int] = None,
        subjects_due: Optional[int] = None,
        invitations_target: Optional[int] = None,
        cumulative_subjects: Optional[int] = None,
        cumulative_invites: Optional[int] = None,
        resulting_position_subjects: Optional[int] = None,
        resulting_position_weeks: Optional[int] = None,
        calculated_target: Optional[int] = None,
    ) -> None:
        self.plan_id: Optional[int] = plan_id
        self.week_number: Optional[int] = week_number
        self.week_start_date: Optional[date] = week_start_date
        self.invite_days: Optional[int] = invite_days
        self.subjects_due: Optional[int] = subjects_due
        self.invitations_target: Optional[int] = invitations_target
        self.cumulative_subjects: Optional[int] = cumulative_subjects
        self.cumulative_invites: Optional[int] = cumulative_invites
        self.resulting_position_subjects: Optional[int] = resulting_position_subjects
        self.resulting_position_weeks: Optional[int] = resulting_position_weeks
        self.calculated_target: Optional[int] = calculated_target

    def __str__(self) -> str:
        """
        Returns a string representation of the invitation plan week.
        """
        return (
            f"Plan ID : {self.plan_id} - Week no :{self.week_number} - "
            f"Week start date : {self.week_start_date} - Subjects due: {self.subjects_due}"
        )

    def get_plan_id(self) -> Optional[int]:
        """Returns the plan ID."""
        return self.plan_id

    def set_plan_id(self, plan_id: int) -> None:
        """Sets the plan ID."""
        self.plan_id = plan_id

    def get_week_number(self) -> Optional[int]:
        """Returns the week number."""
        return self.week_number

    def set_week_number(self, week_number: int) -> None:
        """Sets the week number."""
        self.week_number = week_number

    def get_week_start_date(self) -> Optional[date]:
        """Returns the week start date."""
        return self.week_start_date

    def set_week_start_date(self, week_start_date: date) -> None:
        """Sets the week start date."""
        self.week_start_date = week_start_date

    def get_invite_days(self) -> Optional[int]:
        """Returns the number of invite days."""
        return self.invite_days

    def set_invite_days(self, invite_days: int) -> None:
        """Sets the number of invite days."""
        self.invite_days = invite_days

    def get_subjects_due(self) -> Optional[int]:
        """Returns the number of subjects due."""
        return self.subjects_due

    def set_subjects_due(self, subjects_due: int) -> None:
        """Sets the number of subjects due."""
        self.subjects_due = subjects_due

    def get_invitations_target(self) -> Optional[int]:
        """Returns the invitations target."""
        return self.invitations_target

    def set_invitations_target(self, invitations_target: int) -> None:
        """Sets the invitations target."""
        self.invitations_target = invitations_target

    def get_cumulative_subjects(self) -> Optional[int]:
        """Returns the cumulative subjects."""
        return self.cumulative_subjects

    def set_cumulative_subjects(self, cumulative_subjects: int) -> None:
        """Sets the cumulative subjects."""
        self.cumulative_subjects = cumulative_subjects

    def get_cumulative_invites(self) -> Optional[int]:
        """Returns the cumulative invites."""
        return self.cumulative_invites

    def set_cumulative_invites(self, cumulative_invites: int) -> None:
        """Sets the cumulative invites."""
        self.cumulative_invites = cumulative_invites

    def get_resulting_position_subjects(self) -> Optional[int]:
        """Returns the resulting position subjects."""
        return self.resulting_position_subjects

    def set_resulting_position_subjects(self, resulting_position_subjects: int) -> None:
        """Sets the resulting position subjects."""
        self.resulting_position_subjects = resulting_position_subjects

    def get_resulting_position_weeks(self) -> Optional[int]:
        """Returns the resulting position weeks."""
        return self.resulting_position_weeks

    def set_resulting_position_weeks(self, resulting_position_weeks: int) -> None:
        """Sets the resulting position weeks."""
        self.resulting_position_weeks = resulting_position_weeks

    def get_calculated_target(self) -> Optional[int]:
        """Returns the calculated target."""
        return self.calculated_target

    def set_calculated_target(self, calculated_target: int) -> None:
        """Sets the calculated target."""
        self.calculated_target = calculated_target

    @classmethod
    def from_cursor(cls, rows: List[list]) -> "InvitationPlanWeek":
        """
        Maps the first row of a database cursor to an InvitationPlanWeek instance.
        Expects cursor rows in the order:
            (plan_id, week_number, week_start_date, invite_days, subjects_due,
            invitations_target, cumulative_subjects, cumulative_invites,
            resulting_position_subjects, resulting_position_weeks, calculated_target)
        """
        if not rows:
            return cls()
        row = rows[0]
        return cls(
            plan_id=row[0],
            week_number=row[1],
            week_start_date=row[2],
            invite_days=row[3],
            subjects_due=row[4],
            calculated_target=row[5],
            invitations_target=row[6],
            cumulative_subjects=row[7],
            cumulative_invites=row[8],
            resulting_position_subjects=row[9],
            resulting_position_weeks=row[10],
        )

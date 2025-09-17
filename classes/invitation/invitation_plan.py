from typing import Optional
from datetime import date, datetime
from classes.invitation.invitation_plan_status_type import InvitationPlanStatusType


class InvitationPlan:
    """
    Represents an invitation plan for a screening centre/hub.
    """

    def __init__(
        self,
        plan_id: Optional[int] = None,
        created_date: Optional[date] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        invitations_due: Optional[int] = None,
        invitations_per_week: Optional[int] = None,
        invitations_per_day: Optional[int] = None,
        plan_status: Optional[InvitationPlanStatusType] = None,
        fip_note: Optional[str] = None,
        date_stamp: Optional[datetime] = None,
    ) -> None:
        """
        Initializes an InvitationPlan instance.
        Args:
            plan_id (Optional[int]): The plan ID.
            created_date (Optional[date]): The date the plan was created.
            start_date (Optional[date]): The start date of the plan.
            end_date (Optional[date]): The end date of the plan.
            invitations_due (Optional[int]): The total number of invitations due.
            invitations_per_week (Optional[int]): The number of invitations per week.
            invitations_per_day (Optional[int]): The number of invitations per day.
            plan_status (Optional[InvitationPlanStatusType]): The status of the plan.
            fip_note (Optional[str]): Any notes associated with the plan.
            date_stamp (Optional[datetime]): The timestamp of the last update.
        """
        self.plan_id: Optional[int] = plan_id
        self.created_date: Optional[date] = created_date
        self.start_date: Optional[date] = start_date
        self.end_date: Optional[date] = end_date
        self.invitations_due: Optional[int] = invitations_due
        self.invitations_per_week: Optional[int] = invitations_per_week
        self.invitations_per_day: Optional[int] = invitations_per_day
        self.plan_status: Optional[InvitationPlanStatusType] = plan_status
        self.fip_note: Optional[str] = fip_note
        self.date_stamp: Optional[datetime] = date_stamp

    def __str__(self) -> str:
        """
        Returns a string representation of the invitation plan.
        """
        return (
            f"Plan ID: {self.plan_id} - Created date: {self.created_date} - "
            f"Start date: {self.start_date} - End date: {self.end_date} - "
            f"Invitations due: {self.invitations_due} - Invitations per day: {self.invitations_per_day} - "
            f"Plan status: {self.plan_status}"
        )

    def get_plan_id(self) -> Optional[int]:
        """
        Returns the plan ID.
        """
        return self.plan_id

    def set_plan_id(self, plan_id: int) -> None:
        """
        Sets the plan ID.
        """
        self.plan_id = plan_id

    def get_fip_note(self) -> Optional[str]:
        """
        Returns the FIP note.
        """
        return self.fip_note

    def set_fip_note(self, fip_note: str) -> None:
        """
        Sets the FIP note.
        """
        self.fip_note = fip_note

    def get_created_date(self) -> Optional[date]:
        """
        Returns the created date.
        """
        return self.created_date

    def set_created_date(self, created_date: date) -> None:
        """
        Sets the created date.
        """
        self.created_date = created_date

    def get_start_date(self) -> Optional[date]:
        """
        Returns the start date.
        """
        return self.start_date

    def set_start_date(self, start_date: date) -> None:
        """
        Sets the start date.
        """
        self.start_date = start_date

    def get_end_date(self) -> Optional[date]:
        """
        Returns the end date.
        """
        return self.end_date

    def set_end_date(self, end_date: date) -> None:
        """
        Sets the end date.
        """
        self.end_date = end_date

    def get_invitations_due(self) -> Optional[int]:
        """
        Returns the number of invitations due.
        """
        return self.invitations_due

    def set_invitations_due(self, invitations_due: int) -> None:
        """
        Sets the number of invitations due.
        """
        self.invitations_due = invitations_due

    def get_invitations_per_week(self) -> Optional[int]:
        """
        Returns the number of invitations per week.
        """
        return self.invitations_per_week

    def set_invitations_per_week(self, invitations_per_week: int) -> None:
        """
        Sets the number of invitations per week.
        """
        self.invitations_per_week = invitations_per_week

    def get_invitations_per_day(self) -> Optional[int]:
        """
        Returns the number of invitations per day.
        """
        return self.invitations_per_day

    def set_invitations_per_day(self, invitations_per_day: int) -> None:
        """
        Sets the number of invitations per day.
        """
        self.invitations_per_day = invitations_per_day

    def get_plan_status(self) -> Optional[InvitationPlanStatusType]:
        """
        Returns the plan status.
        """
        return self.plan_status

    def set_plan_status(self, plan_status: InvitationPlanStatusType) -> None:
        """
        Sets the plan status.
        """
        self.plan_status = plan_status

    def get_date_stamp(self) -> Optional[datetime]:
        """
        Returns the date stamp.
        """
        return self.date_stamp

    def set_date_stamp(self, date_stamp: datetime) -> None:
        """
        Sets the date stamp.
        """
        self.date_stamp = date_stamp

    @classmethod
    def from_cursor(cls, rows: list) -> "InvitationPlan":
        """
        Maps the first row of a database cursor to an InvitationPlan instance.
        Expects cursor rows in the order:
            (plan_id, created_date, start_date, end_date, invitations_due,
            invitations_per_week, invitations_per_day, plan_status, fip_note, date_stamp)
        """
        if not rows:
            return cls()
        row = rows[0]
        return cls(
            plan_id=row[0],
            created_date=row[1],
            start_date=row[2],
            end_date=row[3],
            invitations_due=row[4],
            invitations_per_week=row[5],
            invitations_per_day=row[6],
            fip_note=row[7],
            plan_status=row[8],
            date_stamp=row[9],
        )

import logging
from typing import List, Optional, Any
from utils.oracle.oracle import OracleDB
import oracledb
from classes.database.database_error import DatabaseError
from classes.invitation_plan import InvitationPlan
from classes.invitation_plan_week import InvitationPlanWeek
from classes.invitation_plan_status_type import InvitationPlanStatusType


class InvitationRepository:
    """
    Repository class handling database access for invitation planning.
    Uses OracleDB for database operations.
    """

    def __init__(self):
        self.oracle_db = OracleDB()

    def get_plans(
        self,
        hub_id: Optional[int],
        screening_centre_id: Optional[int],
        plan_id: Optional[int],
    ) -> List[Any]:
        """
        Gets a list of invitation plans for the specified screening centre or details of a specific plan.

        Args:
            hub_id (Optional[int]): Hub ID.
            screening_centre_id (Optional[int]): Screening centre ID.
            plan_id (Optional[int]): Plan ID (optional).

        Returns:
            List[Any]: [error, plans, weeks]
        """
        logging.debug(
            f"start: get_plans(hub_id={hub_id}, screening_centre_id={screening_centre_id}, plan_id={plan_id})"
        )
        procedure = "PKG_FOBT_CALL.p_get_plans"
        in_params = [hub_id, screening_centre_id, plan_id]
        out_params = [oracledb.CURSOR, oracledb.CURSOR, oracledb.CURSOR]

        result = self.oracle_db.execute_stored_procedure(
            procedure, in_params, out_params
        )
        if result is None:
            raise RuntimeError("Stored procedure did not return any results.")

        # Map outputs
        logging.debug("map errorCursor")
        error_cursor = result[4]  # OUT param 4
        error = DatabaseError.from_cursor(error_cursor)
        if error.is_error():
            raise RuntimeError(f"Database error: {error.get_return_message()}")

        logging.debug("map plansCursor")
        plans_cursor = result[5]
        plans = InvitationPlan.from_cursor(plans_cursor)

        logging.debug("map weeksCursor")
        week_cursor = result[6]
        weeks = InvitationPlanWeek.from_cursor(week_cursor)

        logging.debug("exit: get_plans()")
        return [error, plans, weeks]

    def get_active_plan(self, hub_id: int, screening_centre_id: int) -> Optional[dict]:
        """
        Gets the ACTIVE invitation plan for a hub / screening centre.

        Args:
            hub_id (int): Hub ID.
            screening_centre_id (int): Screening centre ID.

        Returns:
            Optional[dict]: The active invitation plan, or None if not found.
        """
        logging.debug(
            f"start: get_active_plan(hub_id={hub_id}, screening_centre_id={screening_centre_id})"
        )
        result_list = self.get_plans(hub_id, screening_centre_id, None)
        all_plans = result_list[1]
        if not all_plans:
            logging.debug("exit: get_active_plan(None)")
            return None
        else:
            next(
                (
                    p
                    for p in all_plans
                    if p.get_plan_status() == InvitationPlanStatusType.ACTIVE
                ),
                None,
            )

    def refresh_invitation_shortlist(self) -> None:
        """
        Runs the database procedure to refresh the invitations shortlist.
        Picks up any newly self-referred subjects ready for invite.
        """
        logging.debug("start: InvitationRepository.refresh_invitation_shortlist")
        procedure = "PKG_FOBT_CALL.p_find_next_subjects_to_invite"
        number_of_weeks = 4
        max_number_of_subjects = 2500
        hub_id = None
        screening_centre_id = None
        params = [number_of_weeks, max_number_of_subjects, hub_id, screening_centre_id]
        self.oracle_db.execute_stored_procedure(procedure, params)
        logging.debug("exit: InvitationRepository.refresh_invitation_shortlist")

    def process_next_invitations(self) -> None:
        """
        Runs the database procedure to process the next invitations run waiting to be processed.
        """
        logging.debug("start: InvitationRepository.process_next_invitations")
        procedure = "PKG_FOBT_CALL.p_generate_invitations_next_sc"
        in_params = [None, None, None]
        self.oracle_db.execute_stored_procedure(procedure, in_params)
        logging.debug("exit: InvitationRepository.process_next_invitations")

import logging
from datetime import date, timedelta
from typing import Optional, Dict
from classes.subject.subject import Subject
from classes.user.user import User
from classes.repositories.subject_repository import SubjectRepository
from classes.subject.pi_subject import PISubject
from classes.deduction.deduction_reason_types import DeductionReasonType
from utils.date_time_utils import DateTimeUtils


class SSPIChangeSteps:
    def __init__(self) -> None:
        self.subject_repo = SubjectRepository()

    def sspi_update_to_change_dob_received(
        self, nhs_no: str, age_to_change_to: int
    ) -> None:
        """
        Receives an SSPI update to change the subject's date of birth to the specified age.
        Args:
            nhs_no (str): The NHS number of the subject to update.
            age_to_change_to (int): The age to change the subject's date of birth to.
        """
        logging.debug(
            f"start: sspi_update_to_change_dob_received(age_to_change_to={age_to_change_to})"
        )

        subject = Subject().populate_subject_object_from_nhs_no(nhs_no)
        # Calculate the new birth date
        birth_date = DateTimeUtils.calculate_birth_date_for_age(age_to_change_to)
        logging.debug(f"change date of birth to: {birth_date}")

        # Pass control to handle_update to make the DB changes
        pi_subject = PISubject().from_subject(subject)
        self.handle_update(pi_subject, birth_date)

        logging.debug("exit: sspi_update_to_change_dob_received()")

    def process_sspi_deduction_by_code(self, nhs_no: str, deduction_code: str) -> None:
        """
        Process an SSPI deduction based on the provided deduction code.
        Args:
            nhs_no (str): The subject's NHS Number
            deduction_code (str): The deduction code to process.
        """
        subject = Subject().populate_subject_object_from_nhs_no(nhs_no)
        if DeductionReasonType.by_deduction_code(deduction_code) is None:
            raise ValueError(f"Unknown Deduction Code: {deduction_code}")

        pi_subject = PISubject().from_subject(subject)

        if subject is not None:
            logging.debug(
                f"Set deduction code to {deduction_code}, set related deduction details, and remove GP practice"
            )
            pi_subject.nhais_deduction_reason = deduction_code
            pi_subject.nhais_deduction_date = date.today() - timedelta(days=3)
            pi_subject.gp_practice_code = None
            pi_subject.gnc_code = None
            pi_subject.death_date = None
            pi_subject.removed_to = None
            pi_subject.superseded_by_nhs_number = None

            if deduction_code in ["DEA", "D"]:
                pi_subject.death_date = date.today() - timedelta(days=5)
            elif deduction_code == "R":
                pi_subject.removed_to = "DN"
            elif deduction_code in ["LDN", "R/C"]:
                # Logical deletion requires a "superseded by" NHS number
                subject_criteria: Dict[str, str] = {"Screening Status": "Call"}
                superseded_subject = self.subject_repo.get_matching_subject(
                    subject_criteria, Subject(), User()
                )
                if not superseded_subject:
                    raise RuntimeError(
                        "No subject found to provide superseded NHS number."
                    )
                nhs_number = superseded_subject.nhs_number
                logging.debug(f"Superseding with NHS number: {nhs_number}")
                pi_subject.superseded_by_nhs_number = nhs_number
            else:
                logging.warning(
                    f"Unprocessed Deduction Code in switch statement: {deduction_code}"
                )

            # This is for number changes not deductions
            pi_subject.replaced_nhs_number = None

            self.handle_update(pi_subject)
        else:
            raise ValueError("No subject found to update.")

    def reregister_subject_with_latest_gp_practice(self, nhs_no) -> None:
        """
        For a currently deducted subject this will remove their deduction and re-register them with their last GP practice.
        This also un-ceases a subject ceased by SSPI for death, embarkation or logical deletion.
        For a subject currently registered with a GP practice this will have no effect.
        Args:
            nhs_no (str): The subject's NHS Number
        """
        method_name = "reregister_subject_with_latest_gp_practice"
        logging.debug(f"start: {method_name}()")

        subject = Subject().populate_subject_object_from_nhs_no(nhs_no)
        pi_subject = PISubject().from_subject(subject)

        if subject is not None:
            gp_code = self.subject_repo.get_latest_gp_practice_for_subject(nhs_no)
            logging.debug(f"Set GP code to {gp_code} and remove all deduction details")

            pi_subject.gp_practice_code = gp_code
            pi_subject.gnc_code = gp_code
            pi_subject.nhais_deduction_reason = None
            pi_subject.nhais_deduction_date = None
            pi_subject.death_date = None
            pi_subject.removed_to = None
            pi_subject.replaced_nhs_number = None
            pi_subject.superseded_by_nhs_number = None

            self.handle_update(pi_subject)
        else:
            raise ValueError("No subject found to update.")

    def handle_update(
        self, pi_subject: PISubject, birth_date: Optional[date] = None
    ) -> None:
        """
        Performs the SSPI update to make the changes in the database.
        Args:
            subject (PISubject): The pisubject object to update.
            birth_date (Optional[date]): The new birth date to set.
        """
        logging.debug("start: handle_update(Subject, date)")

        pi_subject.pi_reference = "AUTOMATED TEST"
        # Check if a date of birth change needs to be made first
        if birth_date is not None:
            pi_subject.birth_date = birth_date

        # Run the update into the DB (SSPI updates are always run as automated process user 2)
        self.subject_repo.update_pi_subject(2, pi_subject)

        logging.debug("exit: handle_update()")

    def process_sspi_deduction_by_description(
        self, nhs_no: str, deduction_reason_description: str
    ) -> None:
        """
        Process an SSPI deduction based on the deduction reason description.
        Args:
            nhs_no (str): The subject's NHS Number.
            deduction_reason_description (str): The deduction reason description (case-insensitive).
        """
        logging.debug(
            f"start: process_sspi_deduction_by_description(deduction_reason_description={deduction_reason_description})"
        )
        deduction_type = DeductionReasonType.by_description_case_insensitive(
            deduction_reason_description
        )
        if deduction_type is None:
            raise ValueError(
                f"Unknown Deduction Reason Description: {deduction_reason_description}"
            )
        deduction_code = deduction_type.allowed_value
        self.process_sspi_deduction_by_code(nhs_no, deduction_code)
        logging.debug("exit: process_sspi_deduction_by_description()")

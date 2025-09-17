import logging
from datetime import date
from typing import Optional
from classes.subject.subject import Subject
from classes.repositories.subject_repository import SubjectRepository
from classes.subject.pi_subject import PISubject
from utils.date_time_utils import DateTimeUtils


class SSPIChangeSteps:
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
        self.handle_update(subject, birth_date)

        logging.debug("exit: sspi_update_to_change_dob_received()")

    def handle_update(self, subject: Subject, birth_date: Optional[date]) -> None:
        """
        Performs the SSPI update to make the changes in the database.
        Args:
            subject (Subject): The subject object to update.
            birth_date (Optional[date]): The new birth date to set.
        """
        logging.debug("start: handle_update(Subject, date)")

        subject_repo = SubjectRepository()

        pi_subject = PISubject().from_subject(subject)
        pi_subject.pi_reference = "AUTOMATED TEST"
        # Check if a date of birth change needs to be made first
        if birth_date is not None:
            pi_subject.birth_date = birth_date

        # Run the update into the DB (SSPI updates are always run as automated process user 2)
        subject_repo.update_pi_subject(2, pi_subject)

        logging.debug("exit: handle_update()")

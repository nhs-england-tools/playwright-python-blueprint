import logging
from datetime import date, timedelta
from typing import Optional
import random
from utils.oracle.oracle import OracleDB
from utils.nhs_number_tools import NHSNumberTools
from classes.region_type import RegionType
from classes.repositories.investigation_repository import InvitationRepository
from classes.data.data_creation import DataCreation
from classes.repositories.word_repository import WordRepository
from classes.pi_subject import PISubject
from classes.repositories.subject_repository import SubjectRepository
from classes.repositories.user_repository import UserRepository
from classes.user_role_type import UserRoleType


class CreateSubjectSteps:
    """
    Handles creation, logging, and removal of subjects for test scenarios.
    Uses OracleDB for database operations.
    """

    def __init__(
        self,
    ):
        self.oracle_db = OracleDB()

    def there_were_less_than_x_subjects(
        self, num_subjects: int, sc_org_id: int, hub_org_id: int
    ) -> None:
        """
        Checks if there were fewer than X subjects to invite per day in the active invitation plan.

        Args:
            num_subjects (int): Required number of subjects per day.
            sc_org_id (int): Screening center ID.
            hub_org_id (int): Hub ID.
        """
        logging.debug(
            f"Checking if fewer than {num_subjects} subjects to invite per day for screening center {sc_org_id}, hub {hub_org_id}"
        )

        active_plan = InvitationRepository().get_active_plan(
            hub_org_id,
            sc_org_id,
        )

        if active_plan is None:
            raise RuntimeError(
                f"No active invitation plan for screening centre {sc_org_id}, hub id {hub_org_id}"
            )

        logging.debug(f"Current active plan = {active_plan}")
        invitations_per_day = active_plan["invitations_per_day"]
        logging.debug(
            f"Need to add more subjects? {num_subjects > invitations_per_day} (numRequired={num_subjects}, numAvailable={invitations_per_day})"
        )

    def additional_subjects_are_created(
        self, num_subjects: int, sc_org_id: int, hub_org_id: int, region_str: str
    ) -> None:
        """
        Creates sufficient additional subjects so that there are at least X subjects to invite per day.

        Args:
            num_subjects (int): Required number of subjects per day.
            sc_org_id (int): Screening center ID.
            hub_org_id (int): Hub ID.
            region (str): Region name.
        """
        logging.debug(
            f"Creating additional subjects for {num_subjects} per day, screening center {sc_org_id}, hub {hub_org_id}, region {region_str}"
        )

        region = RegionType.get_region(region_str)
        active_plan = InvitationRepository().get_active_plan(hub_org_id, sc_org_id)

        if active_plan is None:
            raise RuntimeError(
                f"No active invitation plan for screening centre {sc_org_id}, hub id {hub_org_id}"
            )

        logging.debug(f"Current active plan = {active_plan}")

        if num_subjects <= active_plan["invitations_per_day"]:
            logging.debug(
                f"Don't need to add more subjects (numRequired={num_subjects}, numAvailable={active_plan['invitations_per_day']})"
            )
        else:
            logging.debug(
                f"Need to add more subjects (numRequired={num_subjects}, numAvailable={active_plan['invitations_per_day']})"
            )

            total_number_of_new_subjects = (
                num_subjects - active_plan["invitations_per_day"]
            )
            plan_duration_days = (
                active_plan["end_date"] - active_plan["start_date"]
            ).days
            pio_id = self.get_pio_id_for_region(region)

            logging.debug(f"adding {total_number_of_new_subjects} more subjects")
            for _ in range(total_number_of_new_subjects):
                # Generate a random subject
                new_subject = DataCreation().generate_random_subject(
                    WordRepository().get_random_subject_details(),
                    "AUTOMATED TEST",
                    region,
                )
                # Random birth date: start_date + random offset - 60 years
                day_offset = random.randint(0, plan_duration_days)
                birth_date = (
                    active_plan["start_date"]
                    + timedelta(days=day_offset)
                    - timedelta(days=60 * 365)
                )
                new_subject.birth_date = birth_date

                # Ensure NHS number is unique
                attempts = 1
                max_attempts = 20
                while (
                    new_subject.nhs_number is not None
                    and self.subject_exists(new_subject.nhs_number)
                    and attempts <= max_attempts
                ):
                    new_subject.nhs_number = NHSNumberTools.generate_random_nhs_number()
                    attempts += 1

                if attempts > max_attempts:
                    logging.error(
                        f"Failed to create random NHS number for subject: {self.get_subject_details(new_subject)}"
                    )
                else:
                    logging.debug(
                        f"Creating new Subject {self.get_subject_details(new_subject)}"
                    )
                    SubjectRepository().create_pi_subject(pio_id, new_subject)

    def get_pio_id_for_region(self, region: "RegionType") -> int:
        """
        Returns the pio_id for the given region.

        Args:
            region (RegionType): The region object.

        Returns:
            int: The pio_id for the region.
        """
        logging.debug(f"Getting pio_id for region: {region.region_name}")

        if region.region_name == "National" or region.region_name == "Isle of Man":
            return 1
        else:
            return 0

    def subject_exists(self, nhs_number: str) -> bool:
        """
        Checks if a subject with the given NHS number exists.

        Args:
            nhs_number (str): NHS number to check.

        Returns:
            bool: True if subject exists, False otherwise.
        """
        query = "SELECT COUNT(*) AS cnt FROM screening_subject_t WHERE subject_nhs_number = :nhs_number"
        df = self.oracle_db.execute_query(query, {"nhs_number": nhs_number})
        return not df.empty and int(df.iloc[0]["cnt"]) > 0

    def complete_nhs_number(self, incomplete_nhs_number: str) -> str:
        """
        Completes a 9-digit NHS number by calculating and appending the check digit.

        Args:
            incomplete_nhs_number (str): 9-digit NHS number.

        Returns:
            str: 10-digit NHS number.
        """
        if len(incomplete_nhs_number) == 9:
            arr_s_value = [int(c) for c in incomplete_nhs_number]
            i_check_digit_total = sum((10 - idx) * arr_s_value[idx] for idx in range(9))
            i_check_digit_total_mod11 = i_check_digit_total % 11
            i_check_digit = 11 - i_check_digit_total_mod11
            if i_check_digit == 11:
                i_check_digit = 0
            completed_nhs_number = incomplete_nhs_number + str(i_check_digit)
            return completed_nhs_number
        else:
            raise ValueError("The incomplete NHS number provided is not 9 digits.")

    def create_custom_subject(
        self, subject_requirements: dict, user_role: UserRoleType
    ) -> Optional[str]:
        """
        Creates a custom PI subject based on the provided requirements.

        Args:
            subject_requirements (dict): Dictionary of subject criteria.
            user_role (UserRoleType): UseroleType onject for the user you are logged in as

        Returns:
            str: The subject's nhs number.

        Raises:
            ValueError: If an invalid criteria is provided.
        """
        logging.debug("Starting custom subject creation")

        word_repo = WordRepository()
        data_creation = DataCreation()
        subject = data_creation.generate_random_subject(
            word_repo.get_random_subject_details(),
            "AUTOMATED TEST",
            RegionType.get_region("England"),
        )

        subject_repo = SubjectRepository()

        for key, value in subject_requirements.items():
            key_lower = key.lower()
            if key_lower == "nhs number":
                subject.nhs_number = value
                logging.debug(f"nhs number updated = {subject.nhs_number}")
            elif key_lower == "age":
                birth_date = date.today() - timedelta(days=int(value) * 365)
                subject.birth_date = birth_date
                logging.debug(f"date of birth updated = {subject.birth_date}")
            elif key_lower == "age (y/d)":
                years, days = map(int, value.split("/"))
                birth_date = date.today() - timedelta(days=years * 365 + days)
                subject.birth_date = birth_date
                logging.debug(f"date of birth updated = {subject.birth_date}")
            elif key_lower == "gp practice":
                subject.gp_practice_code = value
                logging.debug(f"gp practice updated = {subject.gp_practice_code}")
            elif key_lower == "active gp practice in hub/sc":
                orgs = value.split("/")
                gp_code = subject_repo.get_active_gp_practice_in_hub_and_sc(
                    orgs[0], orgs[1]
                )
                subject.gp_practice_code = gp_code
                logging.debug(f"gp practice set = {subject.gp_practice_code}")
            elif key_lower == "inactive gp practice":
                gp_code = subject_repo.get_inactive_gp_practice()
                subject.gp_practice_code = gp_code
                logging.debug(f"gp practice set = {subject.gp_practice_code}")
            else:
                raise ValueError(f"The criteria provided ({key}) is not valid")

        user_repository = UserRepository()
        pio_id = user_repository.get_pio_id_for_role(user_role)
        subject_repo.create_pi_subject(pio_id, subject)
        logging.debug(f"subject added = {subject.to_string()}")
        return subject.nhs_number

    def safe_string(self, value: Optional[str]) -> str:
        """
        Returns a safe string representation, replacing None with 'null'.

        Args:
            value (Optional[str]): String value.

        Returns:
            str: Safe string.
        """
        return value if value is not None else "null"

    def safe_date(self, value: Optional[date]) -> str:
        """
        Returns a safe date string representation, replacing None with 'null'.

        Args:
            value (Optional[date]): Date value.

        Returns:
            str: Safe date string.
        """
        return value.strftime("%d/%m/%Y") if value is not None else "null"

    def get_subject_details(self, subject: PISubject) -> str:
        """
        Returns a formatted string of subject details.

        Args:
            subject (PISubject): Subject details.

        Returns:
            str: Formatted details.
        """
        return "{} {} {} (DoB = {}, NHS number = {})".format(
            self.safe_string(subject.name_prefix),
            self.safe_string(subject.first_given_names),
            self.safe_string(subject.family_name),
            self.safe_date(subject.birth_date),
            self.safe_string(subject.nhs_number),
        )

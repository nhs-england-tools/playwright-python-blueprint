from typing import Dict, Optional
import logging
from datetime import datetime, date
from classes.bowel_scope.bowel_scope_dd_reason_for_change_type import (
    BowelScopeDDReasonForChangeType,
)
from classes.ceased.ceased_confirmation_details import CeasedConfirmationDetails
from classes.ceased.ceased_confirmation_user_id import CeasedConfirmationUserId
from classes.ceased.clinical_cease_reason_type import ClinicalCeaseReasonType
from classes.date.date_description import DateDescription
from classes.event.event_status_type import EventStatusType
from classes.episode.episode_type import EpisodeType
from classes.screening.has_gp_practice import HasGPPractice
from classes.screening.has_unprocessed_sspi_updates import HasUnprocessedSSPIUpdates
from classes.date.has_user_dob_update import HasUserDobUpdate
from classes.episode.subject_has_episode import SubjectHasEpisode
from classes.ceased.manual_cease_requested import ManualCeaseRequested
from classes.screening.screening_status_type import ScreeningStatusType
from classes.surveillance.sdd_reason_for_change_type import SDDReasonForChangeType
from classes.surveillance.ssdd_reason_for_change_type import SSDDReasonForChangeType
from classes.screening.ss_reason_for_change_type import SSReasonForChangeType
from classes.screening.subject_hub_code import SubjectHubCode
from classes.screening.subject_screening_centre_code import SubjectScreeningCentreCode
from classes.subject_selection_query_builder.subject_selection_criteria_key import (
    SubjectSelectionCriteriaKey,
)
from classes.subject.subject import Subject
from classes.user.user import User
from classes.subject_selection_query_builder.selection_builder_exception import (
    SelectionBuilderException,
)
from classes.appointment.appointment_slot_type import AppointmentSlotType
from classes.appointment.appointment_status_type import AppointmentStatusType
from classes.diagnostic.which_diagnostic_test import WhichDiagnosticTest
from classes.diagnostic.diagnostic_test_type import DiagnosticTestType
from classes.diagnostic.diagnostic_test_is_void import DiagnosticTestIsVoid
from classes.diagnostic.diagnostic_test_has_result import DiagnosticTestHasResult
from classes.diagnostic.diagnostic_test_has_outcome_of_result import (
    DiagnosticTestHasOutcomeOfResult,
)
from classes.datasets.intended_extent_type import IntendedExtentType
from classes.episode.latest_episode_has_dataset import LatestEpisodeHasDataset
from classes.episode.latest_episode_latest_investigation_dataset import (
    LatestEpisodeLatestInvestigationDataset,
)
from classes.surveillance.surveillance_review_status_type import (
    SurveillanceReviewStatusType,
)
from classes.surveillance.does_subject_have_surveillance_review_case import (
    DoesSubjectHaveSurveillanceReviewCase,
)
from classes.surveillance.surveillance_review_case_type import (
    SurveillanceReviewCaseType,
)
from classes.date.has_date_of_death_removal import HasDateOfDeathRemoval
from classes.invitation.invited_since_age_extension import InvitedSinceAgeExtension
from classes.episode.episode_result_type import EpisodeResultType
from classes.datasets.symptomatic_procedure_result_type import (
    SymptomaticProcedureResultType,
)
from classes.screening.screening_referral_type import ScreeningReferralType
from classes.lynch.lynch_sdd_reason_for_change_type import LynchSDDReasonForChangeType
from classes.lynch.lynch_incident_episode_type import (
    LynchIncidentEpisodeType,
)
from classes.episode.prevalent_incident_status_type import PrevalentIncidentStatusType
from classes.yes_no.yes_no_type import YesNoType
from classes.episode.episode_sub_type import EpisodeSubType
from classes.episode.episode_status_type import EpisodeStatusType
from classes.episode.episode_status_reason_type import EpisodeStatusReasonType
from classes.recall.recall_calculation_method_type import RecallCalculationMethodType
from classes.recall.recall_episode_type import RecallEpisodeType
from classes.recall.recall_surveillance_type import RecallSurveillanceType
from classes.event.event_code_type import EventCodeType
from classes.referral.has_referral_date import HasReferralDate
from classes.diagnostic.diagnosis_date_reason_type import DiagnosisDateReasonType
from classes.yes_no.yes_no import YesNo
from classes.diagnostic.diagnostic_test_referral_type import DiagnosticTestReferralType
from classes.referral.reason_for_onward_referral_type import ReasonForOnwardReferralType
from classes.referral.reason_for_symptomatic_referral_type import (
    ReasonForSymptomaticReferralType,
)
from classes.datasets.asa_grade_type import ASAGradeType
from classes.datasets.scan_type import ScanType
from classes.datasets.metastases_present_type import MetastasesPresentType
from classes.datasets.metastases_location_type import MetastasesLocationType
from classes.datasets.final_pretreatment_t_category_type import (
    FinalPretreatmentTCategoryType,
)
from classes.datasets.final_pretreatment_n_category_type import (
    FinalPretreatmentNCategoryType,
)
from classes.datasets.final_pretreatment_m_category_type import (
    FinalPretreatmentMCategoryType,
)
from classes.datasets.reason_no_treatment_received_type import (
    ReasonNoTreatmentReceivedType,
)
from classes.datasets.location_type import LocationType
from classes.datasets.previously_excised_tumour_type import PreviouslyExcisedTumourType
from classes.datasets.treatment_type import TreatmentType
from classes.datasets.treatment_given import TreatmentGiven
from classes.datasets.cancer_treatment_intent import CancerTreatmentIntent
from classes.notify.notify_message_status import NotifyMessageStatus
from classes.notify.notify_message_type import NotifyMessageType


class SubjectSelectionQueryBuilder:
    """
    Builds dynamic SQL queries for selecting screening subjects based on various criteria.
    """

    # -- SQL Fragments --
    _SQL_IS_NULL = " IS NULL "
    _SQL_IS_NOT_NULL = " IS NOT NULL "
    _SQL_NOT_EXISTS = " NOT EXISTS "
    _SQL_AND_NOT_EXISTS = "AND NOT EXISTS"
    _SQL_AND_EXISTS = "AND EXISTS"
    _TRUNC_SYSDATE = "TRUNC(SYSDATE)"

    # -- Semantic Messages --
    _REASON_NO_EXISTING_SUBJECT = "no existing subject"

    def __init__(self):
        """
        Initialise the query builder with empty SQL clause lists and bind variable dictionary.
        """
        self.sql_select = []
        self.sql_from = []
        self.sql_where = []
        self.sql_from_episode = []
        self.sql_from_genetic_condition_diagnosis = []
        self.sql_from_diagnostic_test = []
        self.sql_from_cancer_audit_datasets = []
        self.sql_from_surveillance_review = []
        self.bind_vars = {}
        self.criteria_value_count = 0

        self.xt = "xt"
        self.ap = "ap"
        self.tk = "tk"
        self.ap = "ap"

        # Repeated Strings:
        self.c_dob = "c.date_of_birth"

    def build_subject_selection_query(
        self,
        criteria: Dict[str, str],
        user: "User",
        subject: "Subject",
        subjects_to_retrieve: Optional[int] = None,
        enable_logging: bool = True,
    ) -> tuple[str, dict]:
        """
        This method builds a SQL query string based on the provided selection criteria.
        It combines all of the different sections of the query into one string.
        """
        # Clear previous state to avoid duplicate SQL fragments
        self.sql_select = []
        self.sql_from = []
        self.sql_where = []
        self.sql_from_episode = []
        self.sql_from_genetic_condition_diagnosis = []
        self.sql_from_diagnostic_test = []
        self.sql_from_cancer_audit_datasets = []
        self.sql_from_surveillance_review = []
        self.bind_vars = {}
        self.criteria_value_count = 0

        self.xt = "xt"
        self.ap = "ap"

        self._build_select_clause()
        self._build_main_from_clause()
        self._start_where_clause()
        self._add_variable_selection_criteria(criteria, user, subject)
        if subjects_to_retrieve is not None:
            self._end_where_clause(subjects_to_retrieve)
        else:
            self._end_where_clause(1)

        query = " ".join(
            str(part)
            for part in (
                self.sql_select
                + self.sql_from
                + self.sql_from_episode
                + self.sql_from_diagnostic_test
                + self.sql_from_genetic_condition_diagnosis
                + self.sql_from_cancer_audit_datasets
                + self.sql_from_surveillance_review
                + self.sql_where
            )
        )
        if enable_logging:
            logging.info(f"[SUBJECT SELECTION QUERY BUILDER] Final query: {query}")
        return query, self.bind_vars

    def _build_select_clause(self) -> None:
        """
        This method builds the 'SELECT' section of the SQL query
        """
        columns: list[str] = [
            "ss.screening_subject_id",
            "ss.subject_nhs_number",
            "c.person_family_name",
            "c.person_given_name",
            "ss.datestamp",
            "ss.screening_status_id",
            "ss.ss_reason_for_change_id",
            "ss.screening_status_change_date",
            "ss.screening_due_date",
            "ss.sdd_reason_for_change_id",
            "ss.sdd_change_date",
            "ss.calculated_sdd",
            "ss.surveillance_screen_due_date",
            "ss.calculated_ssdd",
            "ss.surveillance_sdd_rsn_change_id",
            "ss.surveillance_sdd_change_date",
            "ss.lynch_screening_due_date",
            "ss.lynch_sdd_reason_for_change_id",
            "ss.lynch_sdd_change_date",
            "ss.lynch_calculated_sdd",
            self.c_dob,
            "c.date_of_death ",
        ]
        self.sql_select.append("SELECT " + ", ".join(columns))

    def _build_main_from_clause(self) -> None:
        """
        Defines the intital 'FROM' clause
        """
        self.sql_from.append(
            " FROM screening_subject_t ss "
            " INNER JOIN sd_contact_t c ON c.nhs_number = ss.subject_nhs_number "
        )

    def _start_where_clause(self) -> None:
        """
        Starts the intital 'WHERE' clause
        """
        self.sql_where.append(" WHERE 1=1 ")

    def _end_where_clause(self, subject_count: int) -> None:
        """
        End the 'WHERE' clause by fetching x subjects
        """
        self.sql_where.append(f" FETCH FIRST {subject_count} ROWS ONLY ")

    def _preprocess_criteria(self, key: str, value: str, subject: "Subject") -> bool:
        """
        Parses and validates a single selection criterion key-value pair before dispatching.

        This method extracts and sets internal state needed to evaluate a subject selection criterion,
        including the criteria key name, modifier flags, value, and comparator. It also performs initial
        checks such as:
            - Ignoring commented-out criteria (those starting with "#")
            - Rejecting "unchanged" values if no subject is supplied
            - Preventing invalid use of "not" modifiers with NULL values

        Parameters:
            key (str): The criteria key name (e.g. "subject age", "screening status")
            value (str): The corresponding value, possibly with modifiers or comparators
            subject (Subject): The subject context to validate certain special-case logic

        Returns:
            bool: True if the criteria should be processed further; False if it is ignorable

        Raises:
            ValueError: If the criterion references 'unchanged' without a subject
            SelectionBuilderException: For invalid usage of 'not' modifier with NULL
        """
        self.criteria_key_name = key.lower()
        self.criteria_has_not_modifier = self._get_criteria_has_not_comparator(value)
        self.criteria_value = self._get_criteria_value(value)
        self.criteria_comparator = self._get_criteria_comparator()

        if self.criteria_value.startswith("#"):
            self.criteria_value = ""

        if not self.criteria_value:
            return False

        if subject is None and self.criteria_value.lower().startswith("unchanged"):
            raise ValueError(f"{self.criteria_key_name}: No existing subject")

        if self.criteria_value.lower() == "null" and self.criteria_has_not_modifier:
            self._force_not_modifier_is_invalid_for_criteria_value()

        return True

    def _add_variable_selection_criteria(
        self,
        criteria: Dict[str, str],
        user: "User",
        subject: "Subject",
    ):
        """
        Processes each selection criteria from the provided dictionary and builds the SQL clauses accordingly.
        """
        for criterium_key, criterium_value in criteria.items():
            if not self._preprocess_criteria(criterium_key, criterium_value, subject):
                continue

            try:
                self.criteria_key = SubjectSelectionCriteriaKey.by_description(
                    self.criteria_key_name.replace("+", "")
                )
                if self.criteria_key is None:
                    raise ValueError(
                        f"No SubjectSelectionCriteriaKey found for description: {self.criteria_key_name}"
                    )

                self._check_if_more_than_one_criteria_value_is_valid_for_criteria_key()
                self._check_if_not_modifier_is_valid_for_criteria_key()
                self._dispatch_criteria_key(user, subject)

            except Exception:
                raise SelectionBuilderException(
                    f"Invalid subject selection criteria key: {self.criteria_key_name}"
                )

    def _dispatch_criteria_key(self, user: "User", subject: "Subject") -> None:
        """
        Executes the appropriate SQL clause logic based on the resolved SubjectSelectionCriteriaKey.

        This method is called after all preprocessing and validation of a given criterion. It routes
        the request to the correct `_add_criteria_*` or `_add_join_*` method based on the value of
        `self.criteria_key`. All matching logic is encapsulated here, grouped by category for clarity.

        Parameters:
            user (User): The current user performing the subject selection.
            subject (Subject): The subject object used for validations and lookups.

        Raises:
            SelectionBuilderException: If the criteria key is invalid or unrecognized.
        """
        match self.criteria_key:
            # ------------------------------------------------------------------------
            # 👤 Demographics & Subject Identity Criteria
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.NHS_NUMBER:
                self.criteria_value.replace(" ", "")
                self._add_criteria_nhs_number()
            case (
                SubjectSelectionCriteriaKey.SUBJECT_AGE
                | SubjectSelectionCriteriaKey.SUBJECT_AGE_YD
            ):
                self._add_criteria_subject_age()
            case SubjectSelectionCriteriaKey.SUBJECT_HUB_CODE:
                self._add_criteria_subject_hub_code(user)
            case SubjectSelectionCriteriaKey.DEMOGRAPHICS_TEMPORARY_ADDRESS:
                self._add_criteria_has_temporary_address()
            # ------------------------------------------------------------------------
            # 🏥 Screening Centre & GP Linkage Criteria
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.RESPONSIBLE_SCREENING_CENTRE_CODE:
                self._add_criteria_subject_screening_centre_code(user)
            case SubjectSelectionCriteriaKey.HAS_GP_PRACTICE:
                self._add_criteria_has_gp_practice()
            case (
                SubjectSelectionCriteriaKey.HAS_GP_PRACTICE_ASSOCIATED_WITH_SCREENING_CENTRE_CODE
            ):
                self._add_criteria_has_gp_practice_linked_to_sc()
            # ------------------------------------------------------------------------
            # 🩺 Screening Status & Change History Criteria
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.SCREENING_STATUS:
                self._add_criteria_screening_status(subject)
            case SubjectSelectionCriteriaKey.PREVIOUS_SCREENING_STATUS:
                self._add_criteria_previous_screening_status()
            case SubjectSelectionCriteriaKey.SCREENING_STATUS_REASON:
                self._add_criteria_screening_status_reason(subject)
            case SubjectSelectionCriteriaKey.SCREENING_STATUS_DATE_OF_CHANGE:
                self._add_criteria_date_field(
                    subject, "ALL_PATHWAYS", "SCREENING_STATUS_CHANGE_DATE"
                )
            # ------------------------------------------------------------------------
            # ⏰ Due Dates: Screening, Surveillance & Lynch Pathways
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.PREVIOUS_LYNCH_DUE_DATE:
                self._add_criteria_date_field(subject, "LYNCH", "PREVIOUS_DUE_DATE")
            case (
                SubjectSelectionCriteriaKey.PREVIOUS_SCREENING_DUE_DATE
                | SubjectSelectionCriteriaKey.PREVIOUS_SCREENING_DUE_DATE_BIRTHDAY
            ):
                self._add_criteria_date_field(subject, "FOBT", "PREVIOUS_DUE_DATE")
            case SubjectSelectionCriteriaKey.PREVIOUS_SURVEILLANCE_DUE_DATE:
                self._add_criteria_date_field(
                    subject, "SURVEILLANCE", "PREVIOUS_DUE_DATE"
                )
            case (
                SubjectSelectionCriteriaKey.SCREENING_DUE_DATE
                | SubjectSelectionCriteriaKey.SCREENING_DUE_DATE_BIRTHDAY
            ):
                self._add_criteria_date_field(subject, "FOBT", "DUE_DATE")
            case (
                SubjectSelectionCriteriaKey.CALCULATED_SCREENING_DUE_DATE
                | SubjectSelectionCriteriaKey.CALCULATED_SCREENING_DUE_DATE_BIRTHDAY
                | SubjectSelectionCriteriaKey.CALCULATED_FOBT_DUE_DATE
            ):
                self._add_criteria_date_field(subject, "FOBT", "CALCULATED_DUE_DATE")
            case SubjectSelectionCriteriaKey.SCREENING_DUE_DATE_REASON:
                self._add_criteria_screening_due_date_reason(subject)
            case SubjectSelectionCriteriaKey.SCREENING_DUE_DATE_DATE_OF_CHANGE:
                self._add_criteria_date_field(subject, "FOBT", "DUE_DATE_CHANGE_DATE")
            case SubjectSelectionCriteriaKey.SURVEILLANCE_DUE_DATE:
                self._add_criteria_date_field(subject, "SURVEILLANCE", "DUE_DATE")
            case SubjectSelectionCriteriaKey.CALCULATED_SURVEILLANCE_DUE_DATE:
                self._add_criteria_date_field(
                    subject, "SURVEILLANCE", "CALCULATED_DUE_DATE"
                )
            case SubjectSelectionCriteriaKey.SURVEILLANCE_DUE_DATE_REASON:
                self._add_criteria_surveillance_due_date_reason(subject)
            case SubjectSelectionCriteriaKey.SURVEILLANCE_DUE_DATE_DATE_OF_CHANGE:
                self._add_criteria_date_field(
                    subject, "SURVEILLANCE", "DUE_DATE_CHANGE_DATE"
                )
            case SubjectSelectionCriteriaKey.BOWEL_SCOPE_DUE_DATE_REASON:
                self._add_criteria_bowel_scope_due_date_reason()
            # ------------------------------------------------------------------------
            # ⛔ Cease & Manual Override Criteria
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.MANUAL_CEASE_REQUESTED:
                self._add_criteria_manual_cease_requested()
            case SubjectSelectionCriteriaKey.CEASED_CONFIRMATION_DATE:
                self._add_criteria_date_field(
                    subject, "ALL_PATHWAYS", "CEASED_CONFIRMATION_DATE"
                )
            case SubjectSelectionCriteriaKey.CEASED_CONFIRMATION_DETAILS:
                self._add_criteria_ceased_confirmation_details()
            case SubjectSelectionCriteriaKey.CEASED_CONFIRMATION_USER_ID:
                self._add_criteria_ceased_confirmation_user_id(user)
            case SubjectSelectionCriteriaKey.CLINICAL_REASON_FOR_CEASE:
                self._add_criteria_clinical_reason_for_cease()
            # ------------------------------------------------------------------------
            # 📦 Event Status & System Update Flags
            # ------------------------------------------------------------------------
            case (
                SubjectSelectionCriteriaKey.SUBJECT_HAS_EVENT_STATUS
                | SubjectSelectionCriteriaKey.SUBJECT_DOES_NOT_HAVE_EVENT_STATUS
            ):
                self._add_criteria_subject_has_event_status()
            case SubjectSelectionCriteriaKey.SUBJECT_HAS_UNPROCESSED_SSPI_UPDATES:
                self._add_criteria_has_unprocessed_sspi_updates()
            case SubjectSelectionCriteriaKey.SUBJECT_HAS_USER_DOB_UPDATES:
                self._add_criteria_has_user_dob_update()
            # ------------------------------------------------------------------------
            # 📁 Subject Has Episode & Age-Based Criteria
            # ------------------------------------------------------------------------
            case (
                SubjectSelectionCriteriaKey.SUBJECT_HAS_EPISODES
                | SubjectSelectionCriteriaKey.SUBJECT_HAS_AN_OPEN_EPISODE
            ):
                self._add_criteria_subject_has_episodes()
            case SubjectSelectionCriteriaKey.SUBJECT_HAS_FOBT_EPISODES:
                self._add_criteria_subject_has_episodes(EpisodeType.FOBT)
            case SubjectSelectionCriteriaKey.SUBJECT_LOWER_FOBT_AGE:
                self._add_criteria_subject_lower_fobt_age()
            case SubjectSelectionCriteriaKey.SUBJECT_LOWER_LYNCH_AGE:
                self._add_criteria_subject_lower_lynch_age()
            # ------------------------------------------------------------------------
            # 🧱 Latest Episode Attributes
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_TYPE:
                self._add_criteria_latest_episode_type()
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_SUB_TYPE:
                self._add_criteria_latest_episode_sub_type()
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_STATUS:
                self._add_criteria_latest_episode_status()

            case SubjectSelectionCriteriaKey.LATEST_EPISODE_STATUS_REASON:
                self._add_criteria_latest_episode_status_reason()
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_RECALL_CALCULATION_METHOD:
                self._add_criteria_latest_episode_recall_calc_method()
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_RECALL_EPISODE_TYPE:
                self._add_criteria_latest_episode_recall_episode_type()
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_RECALL_SURVEILLANCE_TYPE:
                self._add_criteria_latest_episode_recall_surveillance_type()
            # ------------------------------------------------------------------------
            # 🎯 Event Code & Status Inclusion Criteria
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.LATEST_EVENT_STATUS:
                self._add_criteria_event_status("ep.latest_event_status_id")
            case SubjectSelectionCriteriaKey.PRE_INTERRUPT_EVENT_STATUS:
                self._add_criteria_event_status("ep.pre_interrupt_event_status_id")
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_INCLUDES_EVENT_CODE:
                self._add_criteria_event_code_in_episode(True)
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_DOES_NOT_INCLUDE_EVENT_CODE:
                self._add_criteria_event_code_in_episode(False)
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_INCLUDES_EVENT_STATUS:
                self._add_criteria_event_status_in_episode(True)
            case (
                SubjectSelectionCriteriaKey.LATEST_EPISODE_DOES_NOT_INCLUDE_EVENT_STATUS
            ):
                self._add_criteria_event_status_in_episode(False)
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_STARTED:
                self._add_criteria_date_field(
                    subject, "ALL_PATHWAYS", "LATEST_EPISODE_START_DATE"
                )
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_ENDED:
                self._add_criteria_date_field(
                    subject, "ALL_PATHWAYS", "LATEST_EPISODE_END_DATE"
                )
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_KIT_CLASS:
                self._add_criteria_latest_episode_kit_class()
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_SIGNIFICANT_KIT_RESULT:
                self._add_criteria_has_significant_kit_result()
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_REFERRAL_DATE:
                self._add_criteria_has_referral_date()
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_DIAGNOSIS_DATE:
                self._add_criteria_has_diagnosis_date()
            case SubjectSelectionCriteriaKey.SUBJECT_HAS_DIAGNOSTIC_TESTS:
                self._add_criteria_has_diagnostic_test(False)
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_DIAGNOSTIC_TEST:
                self._add_criteria_has_diagnostic_test(True)
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_DIAGNOSIS_DATE_REASON:
                self._add_criteria_diagnosis_date_reason()
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_COMPLETED_SATISFACTORILY:
                self._add_criteria_latest_episode_completed_satisfactorily()
            case SubjectSelectionCriteriaKey.HAS_DIAGNOSTIC_TEST_CONTAINING_POLYP:
                self._add_criteria_has_diagnostic_test_containing_polyp()
            # ------------------------------------------------------------------------
            # 📦 Kit Metadata & Participation History
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.SUBJECT_HAS_UNLOGGED_KITS:
                self._add_criteria_subject_has_unlogged_kits()
            case SubjectSelectionCriteriaKey.SUBJECT_HAS_LOGGED_FIT_KITS:
                self._add_criteria_subject_has_logged_fit_kits()
            case SubjectSelectionCriteriaKey.SUBJECT_HAS_KIT_NOTES:
                self._add_criteria_subject_has_kit_notes()
            case SubjectSelectionCriteriaKey.SUBJECT_HAS_LYNCH_DIAGNOSIS:
                self._add_criteria_subject_has_lynch_diagnosis()
            case SubjectSelectionCriteriaKey.WHICH_TEST_KIT:
                self._add_join_to_test_kits()
            case SubjectSelectionCriteriaKey.KIT_HAS_BEEN_READ:
                self._add_criteria_kit_has_been_read()
            case SubjectSelectionCriteriaKey.KIT_RESULT:
                self._add_criteria_kit_result()
            case SubjectSelectionCriteriaKey.KIT_HAS_ANALYSER_RESULT_CODE:
                self._add_criteria_kit_has_analyser_result_code()
            case SubjectSelectionCriteriaKey.WHICH_APPOINTMENT:
                self._add_join_to_appointments()
            case SubjectSelectionCriteriaKey.APPOINTMENT_TYPE:
                self._add_criteria_appointment_type()
            case SubjectSelectionCriteriaKey.APPOINTMENT_STATUS:
                self._add_criteria_appointment_status()
            case SubjectSelectionCriteriaKey.APPOINTMENT_DATE:
                self._add_criteria_date_field(
                    subject, "ALL_PATHWAYS", "APPOINTMENT_DATE"
                )
            case SubjectSelectionCriteriaKey.WHICH_DIAGNOSTIC_TEST:
                self._add_join_to_diagnostic_tests()
            case SubjectSelectionCriteriaKey.DIAGNOSTIC_TEST_CONFIRMED_TYPE:
                self._add_criteria_diagnostic_test_type("confirmed")
            case SubjectSelectionCriteriaKey.DIAGNOSTIC_TEST_PROPOSED_TYPE:
                self._add_criteria_diagnostic_test_type("proposed")
            case SubjectSelectionCriteriaKey.DIAGNOSTIC_TEST_IS_VOID:
                self._add_criteria_diagnostic_test_is_void()
            case SubjectSelectionCriteriaKey.DIAGNOSTIC_TEST_HAS_RESULT:
                self._add_criteria_diagnostic_test_has_result()
            case SubjectSelectionCriteriaKey.DIAGNOSTIC_TEST_HAS_OUTCOME:
                self._add_criteria_diagnostic_test_has_outcome_of_result()
            case SubjectSelectionCriteriaKey.DIAGNOSTIC_TEST_FAILED:
                self._add_criteria_diagnostic_test_failed()
            case SubjectSelectionCriteriaKey.DIAGNOSTIC_TEST_INTENDED_EXTENT:
                self._add_criteria_diagnostic_test_intended_extent()
            case (
                SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_CANCER_AUDIT_DATASET
                | SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_COLONOSCOPY_ASSESSMENT_DATASET
                | SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_MDT_DATASET
            ):
                self._add_criteria_latest_episode_has_dataset()
            case (
                SubjectSelectionCriteriaKey.LATEST_EPISODE_LATEST_INVESTIGATION_DATASET
            ):
                self._add_criteria_latest_episode_latest_investigation_dataset()
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_DATASET_INTENDED_EXTENT:
                self._add_criteria_latest_episode_intended_extent()
            # ------------------------------------------------------------------------
            # 📆 Clinical Milestones, Dates & Case History
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.SURVEILLANCE_REVIEW_CASE_TYPE:
                self._add_criteria_surveillance_review_type()
            case SubjectSelectionCriteriaKey.DATE_OF_DEATH:
                self._add_criteria_date_field(subject, "ALL_PATHWAYS", "DATE_OF_DEATH")
            case SubjectSelectionCriteriaKey.HAS_HAD_A_DATE_OF_DEATH_REMOVAL:
                self._add_criteria_has_date_of_death_removal()
            case SubjectSelectionCriteriaKey.INVITED_SINCE_AGE_EXTENSION:
                self._add_criteria_invited_since_age_extension()
            case SubjectSelectionCriteriaKey.NOTE_COUNT:
                self._add_criteria_note_count()
            case SubjectSelectionCriteriaKey.SURVEILLANCE_REVIEW_STATUS:
                self._add_criteria_surveillance_review_status()
            case SubjectSelectionCriteriaKey.HAS_EXISTING_SURVEILLANCE_REVIEW_CASE:
                self._add_criteria_does_subject_have_surveillance_review_case()
            case SubjectSelectionCriteriaKey.SUBJECT_75TH_BIRTHDAY:
                self._add_criteria_date_field(
                    subject, "ALL_PATHWAYS", "SEVENTY_FIFTH_BIRTHDAY"
                )
            # ------------------------------------------------------------------------
            # 🧪 Latest Episode Results & Symptomatic Pathway
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.LATEST_EPISODE_ACCUMULATED_RESULT:
                self._add_criteria_latest_episode_accumulated_episode_result()
            case SubjectSelectionCriteriaKey.SYMPTOMATIC_PROCEDURE_RESULT:
                self._add_criteria_symptomatic_procedure_result()
            case SubjectSelectionCriteriaKey.SYMPTOMATIC_PROCEDURE_DATE:
                self._add_criteria_date_field(
                    subject, "ALL_PATHWAYS", "SYMPTOMATIC_PROCEDURE_DATE"
                )
            case SubjectSelectionCriteriaKey.DIAGNOSTIC_TEST_CONFIRMED_DATE:
                self._add_criteria_date_field(
                    subject,
                    "ALL_PATHWAYS",
                    "DIAGNOSTIC_TEST_CONFIRMED_DATE",
                )
            case SubjectSelectionCriteriaKey.SCREENING_REFERRAL_TYPE:
                self._add_criteria_screening_referral_type()
            # ------------------------------------------------------------------------
            # 🧬 Lynch Pathway Due Dates & Diagnosis Tracking
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.CALCULATED_LYNCH_DUE_DATE:
                self._add_criteria_date_field(subject, "LYNCH", "CALCULATED_DUE_DATE")
            case SubjectSelectionCriteriaKey.LYNCH_DUE_DATE:
                self._add_criteria_date_field(subject, "LYNCH", "DUE_DATE")
            case SubjectSelectionCriteriaKey.LYNCH_DUE_DATE_REASON:
                self._add_criteria_lynch_due_date_reason(subject)
            case SubjectSelectionCriteriaKey.LYNCH_DUE_DATE_DATE_OF_CHANGE:
                self._add_criteria_date_field(subject, "LYNCH", "DUE_DATE_CHANGE_DATE")
            case SubjectSelectionCriteriaKey.LYNCH_INCIDENT_EPISODE:
                self._add_criteria_lynch_incident_episode()
            case SubjectSelectionCriteriaKey.LYNCH_DIAGNOSIS_DATE:
                self._add_criteria_date_field(subject, "LYNCH", "DIAGNOSIS_DATE")
            case SubjectSelectionCriteriaKey.LYNCH_LAST_COLONOSCOPY_DATE:
                self._add_criteria_date_field(subject, "LYNCH", "LAST_COLONOSCOPY_DATE")
            # ------------------------------------------------------------------------
            # 🧬 CADS Clinical Dataset Filters
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.CADS_ASA_GRADE:
                self._add_criteria_cads_asa_grade()
            case SubjectSelectionCriteriaKey.CADS_STAGING_SCANS:
                self._add_criteria_cads_staging_scans()
            case SubjectSelectionCriteriaKey.CADS_TYPE_OF_SCAN:
                self._add_criteria_cads_type_of_scan()
            case SubjectSelectionCriteriaKey.CADS_METASTASES_PRESENT:
                self._add_criteria_cads_metastases_present()
            case SubjectSelectionCriteriaKey.CADS_METASTASES_LOCATION:
                self._add_criteria_cads_metastases_location()
            case SubjectSelectionCriteriaKey.CADS_METASTASES_OTHER_LOCATION:
                self._add_criteria_cads_metastases_other_location(self.criteria_value)
            case SubjectSelectionCriteriaKey.CADS_FINAL_PRE_TREATMENT_T_CATEGORY:
                self._add_criteria_cads_final_pre_treatment_t_category()
            case SubjectSelectionCriteriaKey.CADS_FINAL_PRE_TREATMENT_N_CATEGORY:
                self._add_criteria_cads_final_pre_treatment_n_category()
            case SubjectSelectionCriteriaKey.CADS_FINAL_PRETREATMENT_M_CATEGORY:
                self._add_criteria_cads_final_pre_treatment_m_category()
            case SubjectSelectionCriteriaKey.CADS_TREATMENT_RECEIVED:
                self._add_criteria_cads_treatment_received()
            case SubjectSelectionCriteriaKey.CADS_REASON_NO_TREATMENT_RECEIVED:
                self._add_criteria_cads_reason_no_treatment_received()
            case SubjectSelectionCriteriaKey.CADS_TUMOUR_DATE_OF_DIAGNOSIS:
                self._add_criteria_date_field(
                    subject, "ALL_PATHWAYS", "CADS_TUMOUR_DATE_OF_DIAGNOSIS"
                )
            case SubjectSelectionCriteriaKey.CADS_TUMOUR_LOCATION:
                self._add_criteria_cads_tumour_location()
            case (
                SubjectSelectionCriteriaKey.CADS_TUMOUR_HEIGHT_OF_TUMOUR_ABOVE_ANAL_VERGE
            ):
                self._add_criteria_cads_tumour_height_of_tumour_above_anal_verge()
            case SubjectSelectionCriteriaKey.CADS_TUMOUR_PREVIOUSLY_EXCISED_TUMOUR:
                self._add_criteria_cads_tumour_previously_excised_tumour()
            case SubjectSelectionCriteriaKey.CADS_TREATMENT_START_DATE:
                self._add_criteria_date_field(
                    subject, "ALL_PATHWAYS", "CADS_TREATMENT_START_DATE"
                )
            case SubjectSelectionCriteriaKey.CADS_TREATMENT_TYPE:
                self._add_criteria_cads_treatment_type()
            case SubjectSelectionCriteriaKey.CADS_TREATMENT_GIVEN:
                self._add_criteria_cads_treatment_given()
            case SubjectSelectionCriteriaKey.CADS_CANCER_TREATMENT_INTENT:
                self._add_criteria_cads_cancer_treatment_intent()
            case SubjectSelectionCriteriaKey.HAS_PREVIOUSLY_HAD_CANCER:
                self._add_criteria_has_previously_had_cancer()
            # ------------------------------------------------------------------------
            # 🧪 Screening Flow & Pathway Classification
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.FOBT_PREVALENT_INCIDENT_STATUS:
                self._add_criteria_fobt_prevalent_incident_status()
            # ------------------------------------------------------------------------
            # 📨 Notify Message Status Filters
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.NOTIFY_QUEUED_MESSAGE_STATUS:
                self._add_criteria_notify_queued_message_status()
            case SubjectSelectionCriteriaKey.NOTIFY_ARCHIVED_MESSAGE_STATUS:
                self._add_criteria_notify_archived_message_status()
            # ------------------------------------------------------------------------
            # 📝 Referrals
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.REASON_FOR_ONWARD_REFERRAL:
                self._add_criteria_onward_referral_reason("complete_reason_id")
            case SubjectSelectionCriteriaKey.REFER_FROM_SYMPTOMATIC_REASON:
                self._add_criteria_onward_referral_reason(
                    "refer_from_surgery_reason_id"
                )
            case SubjectSelectionCriteriaKey.REFER_ANOTHER_DIAGNOSTIC_TEST_TYPE:
                self._add_criteria_onward_referral_type("referral_procedure_group_id")
            case SubjectSelectionCriteriaKey.REFER_FROM_SYMPTOMATIC_TYPE:
                self._add_criteria_onward_referral_type("refer_from_surgery_type_id")
            case SubjectSelectionCriteriaKey.REASON_FOR_SYMPTOMATIC_REFERRAL:
                self._add_criteria_symptomatic_referral_reason()
            # ------------------------------------------------------------------------
            # 🔘 Other non criteria
            # ------------------------------------------------------------------------
            case SubjectSelectionCriteriaKey.ADD_COLUMN_TO_SELECT_STATEMENT:
                self._add_extra_column_to_select_statement()
            # ------------------------------------------------------------------------
            # 🛑 Fallback: Unmatched Criteria Key
            # ------------------------------------------------------------------------
            case _:
                raise SelectionBuilderException(
                    f"Invalid subject selection criteria key: {self.criteria_key_name}"
                )

    def _get_criteria_has_not_comparator(self, original_criteria_value: str) -> bool:
        """
        Determines if the criteria value has a 'NOT:' modifier.
        """
        return original_criteria_value.startswith("NOT:")

    def _get_criteria_value(self, original_criteria_value: str) -> str:
        """
        Extracts the actual criteria value from the original string, removing any 'NOT:' prefix if present.
        """
        if self.criteria_has_not_modifier:
            return original_criteria_value[4:].strip()
        else:
            return original_criteria_value

    def _get_criteria_comparator(self) -> str:
        """
        Determines the SQL comparator to use based on whether the criteria has a 'NOT:' modifier.
        If 'NOT:' is present, it uses '!='; otherwise, it uses '='.
        """
        if self.criteria_has_not_modifier:
            return " != "
        else:
            return " = "

    def _force_not_modifier_is_invalid_for_criteria_value(self) -> None:
        """
        Raises an exception if the 'NOT:' modifier is used with a criteria value that is NULL.
        This is to prevent logical inconsistencies in the query.
        """
        if self.criteria_has_not_modifier:
            raise ValueError(
                f"The 'NOT:' qualifier cannot be used with criteria key: {self.criteria_key_name}, value: {self.criteria_value}"
            )

    def _check_if_more_than_one_criteria_value_is_valid_for_criteria_key(self) -> None:
        """
        Validates that the number of criteria values does not exceed the allowed limit for the given criteria key.
        Raises an exception if the criteria key does not allow multiple values and more than one value is
        """
        if self.criteria_key is None:
            raise ValueError(f"criteria_key: {self.criteria_key} is None")
        if (
            not self.criteria_key.allow_more_than_one_value
            and self.criteria_value_count > 1
        ):
            raise ValueError(
                f"It is only valid to enter one selection value for criteria key: {self.criteria_key_name}"
            )

    def _check_if_not_modifier_is_valid_for_criteria_key(self) -> None:
        """
        Validates that the 'NOT:' modifier is allowed for the given criteria key.
        Raises an exception if the criteria key does not allow the 'NOT:' modifier and it is used.
        """
        if self.criteria_key is None:
            raise ValueError("criteria_key is None")
        if not self.criteria_key.allow_not_modifier and self.criteria_has_not_modifier:
            raise ValueError(
                f"The 'NOT:' qualifier cannot be used with criteria key: {self.criteria_key_name}"
            )

    def _add_extra_column_to_select_statement(self) -> None:
        """
        Adds an extra column to the SELECT statement.
        """
        self.sql_select.append(f", {self.criteria_value}")

    def _add_criteria_nhs_number(self) -> None:
        """
        Adds a check for the subject's NHS number
        """
        self.sql_where.append(" AND c.nhs_number = :nhs_number ")
        self.bind_vars["nhs_number"] = self.criteria_value

    def _add_criteria_subject_age(self) -> None:
        """
        Adds a check for the subject's age
        """
        if "y/d" in self.criteria_key_name and "/" in self.criteria_value:
            age_criteria = self.criteria_value.split("/")
            self.sql_where.append(" AND c.date_of_birth = ")
            self.sql_where.append(
                self._subtract_years_from_oracle_date(
                    self._TRUNC_SYSDATE, age_criteria[0]
                )
            )
            self.sql_where.append(" - ")
            self.sql_where.append(age_criteria[1])
        else:
            self.sql_where.append(
                " AND FLOOR(MONTHS_BETWEEN(TRUNC(SYSDATE), c.date_of_birth)/12) "
            )
            if self.criteria_value[0] in "0123456789":
                self.sql_where.append("= ")
            self.sql_where.append(self.criteria_value)

    def _add_criteria_subject_lower_fobt_age(self) -> None:
        """
        Adds a SQL constraint that compares a subject's lower FOBT age eligibility
        using a comparator and a value (e.g. '>= 55' or '>= default').

        If value is 'default', it's replaced with a national parameter lookup:
        pkg_parameters.f_get_national_param_val(10)
        """
        try:
            value = self.criteria_value
            comparator = self.criteria_comparator

            if value.lower() == "default":
                value = "pkg_parameters.f_get_national_param_val (10)"

            self.sql_where.append(
                f" AND pkg_bcss_common.f_get_ss_lower_age_limit (ss.screening_subject_id) "
                f" {comparator} {value} "
            )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_subject_lower_lynch_age(self) -> None:
        """
        Adds a SQL constraint for Lynch syndrome lower-age eligibility.

        If value is 'default', it's replaced with '35'.
        Uses comparator to build the WHERE clause.
        """
        try:
            value = self.criteria_value
            comparator = self.criteria_comparator

            if value.lower() == "default":
                value = "35"

            self.sql_where.append(
                f" AND pkg_bcss_common.f_get_lynch_lower_age_limit (ss.screening_subject_id) "
                f" {comparator} {value} "
            )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_type(self) -> None:
        """
        Adds a SQL condition that restricts subjects based on the episode_type_id of their latest episode.

        Translates a human-readable episode type string into an internal numeric ID.
        """
        try:
            episode_type = EpisodeType.by_description_case_insensitive(
                self.criteria_value
            )
            if episode_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self._add_join_to_latest_episode()
            self.sql_where.append(
                f" AND ep.episode_type_id {self.criteria_comparator} {episode_type.valid_value_id} "
            )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_sub_type(self) -> None:
        """
        Adds a SQL condition that filters based on the episode_subtype_id of a subject's latest episode.

        Translates a human-readable episode sub-type string into an internal numeric ID.
        """
        try:
            episode_sub_type = EpisodeSubType.by_description_case_insensitive(
                self.criteria_value
            )
            if episode_sub_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            self._add_join_to_latest_episode()
            self.sql_where.append(
                f" AND ep.episode_subtype_id {self.criteria_comparator}{episode_sub_type.get_id()}"
            )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_status(self) -> None:
        """
        Adds a SQL condition that filters based on the episode_status_id of a subject's latest episode.

        Translates a human-readable episode status into an internal numeric ID.
        """
        try:
            episode_status = EpisodeStatusType.by_description_case_insensitive(
                self.criteria_value
            )
            if episode_status is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            self._add_join_to_latest_episode()
            self.sql_where.append(
                f" AND ep.episode_status_id {self.criteria_comparator}{episode_status.get_id()} "
            )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_status_reason(self) -> None:
        """
        Adds a SQL condition that filters based on the episode_status_reason_id of the subject's latest episode.

        Allows for explicit mapping or handling of NULL where no status reason is recorded.
        """
        try:
            episode_status_reason = (
                EpisodeStatusReasonType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            if episode_status_reason is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            self._add_join_to_latest_episode()
            self.sql_where.append(" AND ep.episode_status_reason_id ")
            if episode_status_reason == EpisodeStatusReasonType.NULL:
                self.sql_where.append(self._SQL_IS_NULL)
            else:
                self.sql_where.append(
                    f" {self.criteria_comparator} {episode_status_reason.get_id()} "
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_recall_calc_method(self) -> None:
        """
        Adds a SQL condition filtering on recall_calculation_method_id from the latest episode.

        Handles mapped descriptions or nulls for closed episodes with no recall method.
        """
        try:
            recall_calc_method = (
                RecallCalculationMethodType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            if recall_calc_method is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            self._add_join_to_latest_episode()
            self.sql_where.append(" AND ep.recall_calculation_method_id ")
            if recall_calc_method == RecallCalculationMethodType.NULL:
                self.sql_where.append(self._SQL_IS_NULL)
            else:
                self.sql_where.append(
                    f"{self.criteria_comparator}{recall_calc_method.get_id()}"
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_recall_episode_type(self) -> None:
        """
        Adds a filter for recall_episode_type_id based on the type of episode that triggered the recall.
        Supports mapped descriptions and IS NULL.
        """
        try:
            recall_episode_type = RecallEpisodeType.by_description_case_insensitive(
                self.criteria_value
            )
            if recall_episode_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            self._add_join_to_latest_episode()
            self.sql_where.append(" AND ep.recall_episode_type_id ")
            if recall_episode_type == RecallEpisodeType.NULL:
                self.sql_where.append(self._SQL_IS_NULL)
            else:
                self.sql_where.append(
                    f"{self.criteria_comparator}{recall_episode_type.get_id()}"
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_recall_surveillance_type(self) -> None:
        """
        Adds a filter for recall_polyp_surv_type_id based on the type of surveillance used during recall.
        Supports mapped descriptions and null values.
        """
        try:
            recall_surveillance_type = (
                RecallSurveillanceType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            if recall_surveillance_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            self._add_join_to_latest_episode()
            self.sql_where.append(" AND ep.recall_polyp_surv_type_id ")
            if recall_surveillance_type == RecallSurveillanceType.NULL:
                self.sql_where.append(
                    f"IS {recall_surveillance_type.get_description()}"
                )
            else:
                self.sql_where.append(
                    f"{self.criteria_comparator}{recall_surveillance_type.get_id()}"
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_event_status(self, column_name: str) -> None:
        """
        Filters based on the event status code found in the specified column.

        Extracts a code from the criteria value (e.g. "ES01 - Invitation Received"),
        and injects its corresponding event_status_id into SQL.
        """
        try:
            self._add_join_to_latest_episode()
            criteria_words = self.criteria_value.split(" ")
            event_status = EventStatusType.get_by_code(criteria_words[0].upper())
            if event_status is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(
                f" AND {column_name} {self.criteria_comparator} {int(event_status.id) }"
            )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_event_code_in_episode(self, event_is_included: bool) -> None:
        """
        Adds a filter checking whether the given event code appears in the latest episode's event list.
        Uses EXISTS or NOT EXISTS depending on the flag.
        """
        self._add_join_to_latest_episode()
        criteria_words = self.criteria_value.split(" ")
        try:
            event_code = EventCodeType.by_code(criteria_words[0].upper())
            if event_code is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            if event_is_included:
                self.sql_where.append(" AND EXISTS ( SELECT 'evc' ")
            else:
                self.sql_where.append(" AND NOT EXISTS ( SELECT 'evc' ")
            self.sql_where.append(
                f"   FROM ep_events_t evc "
                f"   WHERE evc.event_code_id = {event_code.get_id()} "
                f"   AND evc.subject_epis_id = ep.subject_epis_id) "
            )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_event_status_in_episode(self, event_is_included: bool) -> None:
        """
        Adds a filter that checks whether the specified event status is present
        in the latest episode. Uses EXISTS or NOT EXISTS depending on the flag.
        """
        self._add_join_to_latest_episode()
        criteria_words = self.criteria_value.split(" ")
        try:
            event_status = EventStatusType.get_by_code(criteria_words[0].upper())
            if event_status is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            if event_is_included:
                self.sql_where.append(" AND EXISTS ( SELECT 'ev' ")
            else:
                self.sql_where.append(" AND NOT EXISTS ( SELECT 'ev' ")
            self.sql_where.append(
                f"   FROM ep_events_t ev "
                f"   WHERE ev.event_status_id = {event_status.id} "
                f"   AND ev.subject_epis_id = ep.subject_epis_id) "
            )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_kit_class(self) -> None:
        """
        Filters based on the test kit class of the latest episode using a nested IN clause.
        Resolves from symbolic class name (e.g. 'FIT') to test class ID.
        """
        try:
            self._add_join_to_latest_episode()
            value = self.criteria_value.upper()
            comparator = self.criteria_comparator

            # Simulated TestKitClass enum
            test_kit_class_map = {
                "GFOBT": 208098,
                "FIT": 208099,
                # Extend as needed
            }

            if value not in test_kit_class_map:
                raise ValueError(f"Unknown test kit class: {value}")

            kit_class_id = test_kit_class_map[value]

            self.sql_where.append(
                " AND ep.tk_type_id IN ( "
                " SELECT tkt.tk_type_id"
                " FROM tk_type_t tkt "
                f" WHERE tkt.tk_test_class_id {comparator} {kit_class_id} "
                " ) "
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_has_significant_kit_result(self) -> None:
        """
        Adds a filter to check if the latest episode has a significant kit result.
        Significant values: NORMAL, ABNORMAL, WEAK_POSITIVE.
        Accepts criteriaValue: "yes" or "no".
        """
        try:
            value = self.criteria_value.strip().lower()

            if value == "yes":
                exists_clause = "EXISTS"
            elif value == "no":
                exists_clause = self._SQL_NOT_EXISTS
            else:
                raise ValueError(
                    f"Unknown response for significant kit result: {value}"
                )

            self.sql_where.append(
                f"""AND {exists_clause} (
        SELECT 'tks'
        FROM tk_items_t tks
        WHERE tks.screening_subject_id = ss.screening_subject_id
        AND tks.logged_subject_epis_id = ep.subject_epis_id
        AND tks.test_results IN ('NORMAL', 'ABNORMAL', 'WEAK_POSITIVE')
    )"""
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_has_referral_date(self) -> None:
        """
        Adds a filter for the presence or timing of referral_date in the latest episode.
        Accepts values: yes, no, past, more_than_28_days_ago, within_the_last_28_days.
        """
        self._add_join_to_latest_episode()
        try:
            criteria = HasReferralDate.by_description(self.criteria_value.lower())
            if criteria == HasReferralDate.PAST:
                self.sql_where.append(" AND ep.referral_date < trunc(sysdate)  ")
            elif criteria == HasReferralDate.MORE_THAN_28_DAYS_AGO:
                self.sql_where.append(" AND (ep.referral_date + 28) < trunc(sysdate)  ")
            elif criteria == HasReferralDate.WITHIN_THE_LAST_28_DAYS:
                self.sql_where.append(" AND (ep.referral_date + 28) > trunc(sysdate)  ")
            elif criteria == HasReferralDate.YES:
                self.sql_where.append(" AND ep.referral_date IS NOT NULL ")
            elif criteria == HasReferralDate.NO:
                self.sql_where.append(" AND ep.referral_date IS NULL ")
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_has_diagnosis_date(self) -> None:
        """
        Adds a filter to check if the latest episode has a diagnosis_date set,
        and whether it matches the subject's date of death if specified.
        Accepts values: yes, no, yes_date_of_death
        """
        try:
            value = self.criteria_value.strip().lower()

            if value == "yes":
                self.sql_where.append(" AND ep.diagnosis_date IS NOT NULL ")
            elif value == "no":
                self.sql_where.append(" AND ep.diagnosis_date IS NULL ")
            elif value == "yes - date of death":
                self.sql_where.append(" AND ep.diagnosis_date IS NOT NULL ")
                self.sql_where.append(" AND ep.diagnosis_date = c.date_of_death ")
            else:
                raise ValueError(f"Unknown condition for diagnosis date: {value}")

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_has_diagnostic_test(self, latest_episode_only: bool) -> None:
        """
        Adds a filter checking if the subject has (or doesn't have) a diagnostic test.
        Void tests are excluded. The `latest_episode_only` flag limits scope to the latest episode.
        Accepts criteria value: "yes" or "no".
        """
        try:
            value = self.criteria_value.strip().lower()

            if value == "no":
                prefix = "AND NOT "
            elif value == "yes":
                prefix = "AND "
            else:
                raise ValueError(f"Invalid diagnostic test condition: {value}")

            subquery = [
                "EXISTS (",
                "  SELECT 1",
                "  FROM external_tests_t lesxt",
                "  WHERE lesxt.screening_subject_id = ss.screening_subject_id",
                "    AND lesxt.void = 'N'",
            ]
            if latest_episode_only:
                subquery.append("    AND lesxt.subject_epis_id = ep.subject_epis_id")
            subquery.append(")")

            self.sql_where.append(prefix + "\n".join(subquery))

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_diagnosis_date_reason(self) -> None:
        """
        Adds a filter on ep.diagnosis_date_reason_id.
        Supports symbolic matches (via ID) and special values: NULL, NOT_NULL.
        """
        try:
            diagnosis_date_reason = (
                DiagnosisDateReasonType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            if diagnosis_date_reason is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            self._add_join_to_latest_episode()
            self.sql_where.append(" AND ep.diagnosis_date_reason_id ")
            if diagnosis_date_reason in (
                DiagnosisDateReasonType.NULL,
                DiagnosisDateReasonType.NOT_NULL,
            ):
                self.sql_where.append(f"IS {diagnosis_date_reason.get_description()}")
            else:
                self.sql_where.append(
                    f"{self.criteria_comparator}{diagnosis_date_reason.get_valid_value_id()}"
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_completed_satisfactorily(self) -> None:
        """
        Adds a filter to check whether the latest episode completed satisfactorily or not.
        Checks for presence/absence of interruption events or disqualifying result codes.
        """
        try:
            value = self.criteria_value.strip().lower()

            if value == "yes":
                exists_prefix = self._SQL_AND_NOT_EXISTS
            elif value == "no":
                exists_prefix = self._SQL_AND_EXISTS
            else:
                raise ValueError(f"Invalid completion flag: {value}")

            self.sql_where.append(
                f"""{exists_prefix} (
        SELECT 'ev'
        FROM ep_events_t ev
        WHERE ev.subject_epis_id = ep.subject_epis_id
        AND (
            ev.event_status_id IN (11237, 20188)
            OR ep.episode_result_id IN (605002, 605003, 605004, 605007)
        )
    )"""
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_diagnostic_test_failed(self) -> None:
        """
        Adds a SQL WHERE clause for diagnostic tests that have failed or not, based on self.criteria_value.
        Uses self.sql_where.append() to build the clause.
        """
        try:
            test_failed = YesNo.by_description_case_insensitive(self.criteria_value)
            no_result_comparator = " = "
            failure_reasons_comparator = "OR EXISTS"
            if test_failed == YesNo.NO:
                no_result_comparator = " != "
                failure_reasons_comparator = "AND NOT EXISTS"
            self.sql_where.append(
                f" AND ({self.xt}{self.criteria_value_count}.result_id {no_result_comparator} 20311 "
            )
            self.sql_where.append(
                f"{failure_reasons_comparator} (SELECT 1 FROM ds_failure_reason_t xtfr "
            )
            self.sql_where.append(
                f" WHERE xtfr.ext_test_id = {self.xt}{self.criteria_value_count}.ext_test_id "
            )
            self.sql_where.append(" AND xtfr.deleted_flag = 'N' ")
            self.sql_where.append(" AND xtfr.failure_reason_id != 18500)) ")
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_has_diagnostic_test_containing_polyp(self) -> None:
        """
        Adds logic to filter based on whether a diagnostic test has a recorded polyp.
        'Yes' joins polyp tables; 'No' checks for absence via NOT EXISTS.
        """
        try:
            value = self.criteria_value.strip().lower()

            if value == "yes":
                self.sql_from.append(
                    "INNER JOIN external_tests_t ext ON ep.subject_epis_id = ext.subject_epis_id\n"
                    "INNER JOIN ds_colonoscopy_t dsc ON ext.ext_test_id = dsc.ext_test_id\n"
                    "INNER JOIN ds_polyp_t dst ON ext.ext_test_id = dst.ext_test_id"
                )
                self.sql_where.append(
                    """AND ext.void = 'N'\n" "AND dst.deleted_flag = 'N'"""
                )
            elif value == "no":
                self.sql_where.append(
                    """AND NOT EXISTS (
        SELECT 'ext'
        FROM external_tests_t ext
        LEFT JOIN ds_polyp_t dst ON ext.ext_test_id = dst.ext_test_id
        WHERE ext.subject_epis_id = ep.subject_epis_id
    )"""
                )
            else:
                raise ValueError(
                    f"Unknown value for diagnostic test containing polyp: {value}"
                )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_subject_has_unlogged_kits(self) -> None:
        """
        Adds a filter to check for unlogged kits across subject history,
        or scoped to the latest episode. Accepts:
        - "yes"
        - "yes - latest episode"
        - "no"
        """
        try:
            value = self.criteria_value.strip().lower()

            if value in ("yes", "yes - latest episode"):
                prefix = self._SQL_AND_EXISTS
            elif value == "no":
                prefix = self._SQL_AND_NOT_EXISTS
            else:
                raise ValueError(f"Unknown value for unlogged kits: {value}")

            subquery = [
                f"{prefix} (",
                "  SELECT 'tku' ",
                "  FROM tk_items_t tku ",
                "  WHERE tku.screening_subject_id = ss.screening_subject_id ",
            ]

            if value == "yes - latest episode":
                self._add_join_to_latest_episode()
                subquery.append("    AND tku.subject_epis_id = ep.subject_epis_id ")

            subquery.append("    AND tku.logged_in_flag = 'N' ")
            subquery.append(" ) ")

            self.sql_where.append("\n".join(subquery))

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_subject_has_logged_fit_kits(self) -> None:
        """
        Adds a filter to check if the subject has logged FIT kits (tk_type_id > 1 and logged_in_flag = 'Y').
        Accepts values: 'yes' or 'no'.
        """
        try:
            value = self.criteria_value.strip().lower()

            if value == "yes":
                prefix = self._SQL_AND_EXISTS
            elif value == "no":
                prefix = self._SQL_AND_NOT_EXISTS
            else:
                raise ValueError(f"Invalid value for logged FIT kits: {value}")

            self.sql_where.append(
                f"""{prefix} (
    SELECT 'tkl'
    FROM tk_items_t tkl
    WHERE tkl.screening_subject_id = ss.screening_subject_id
        AND tkl.tk_type_id > 1
        AND tkl.logged_in_flag = 'Y'
    )"""
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_subject_has_kit_notes(self) -> None:
        """
        Filters subjects based on presence of active kit-related notes.
        Accepts values: 'yes' or 'no'.
        """
        try:
            value = self.criteria_value.strip().lower()

            if value == "yes":
                prefix = self._SQL_AND_EXISTS
            elif value == "no":
                prefix = self._SQL_AND_NOT_EXISTS
            else:
                raise ValueError(f"Invalid value for kit notes: {value}")

            self.sql_where.append(
                f"""{prefix} (
        SELECT 1
        FROM supporting_notes_t sn
        WHERE sn.screening_subject_id = ss.screening_subject_id
            AND (
            sn.type_id = '308015'
            OR sn.promote_pio_id IS NOT NULL
            )
            AND sn.status_id = 4100
        )
        AND ss.number_of_invitations > 0
        AND rownum = 1"""
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_subject_has_lynch_diagnosis(self) -> None:
        """
        Adds a filter to check if a subject has an active Lynch diagnosis.
        Accepts:
            - "yes" → subject must have active diagnosis ('Y')
            - "no"  → subject must not have active diagnosis ('N')
        """
        try:
            value = self.criteria_value.strip().lower()

            if value == "yes":
                self.sql_where.append(
                    "AND pkg_lynch.f_subject_has_active_lynch_diagnosis (ss.screening_subject_id) = 'Y'"
                )
            elif value == "no":
                self.sql_where.append(
                    "AND pkg_lynch.f_subject_has_active_lynch_diagnosis (ss.screening_subject_id) = 'N'"
                )
            else:
                raise ValueError(f"Invalid value for Lynch diagnosis: {value}")

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_join_to_test_kits(self) -> None:
        """
        Adds joins to the tk_items_t table based on test kit selection criteria.
        Handles whether any kit is considered, or a specific one from the latest episode.

        Expected values (case-insensitive):
            - "any_kit_in_any_episode"
            - "only_kit_issued_in_latest_episode"
            - "first_kit_issued_in_latest_episode"
            - "latest_kit_issued_in_latest_episode"
            - "only_kit_logged_in_latest_episode"
            - "first_kit_logged_in_latest_episode"
            - "latest_kit_logged_in_latest_episode"
        """
        try:
            value = self.criteria_value.strip().lower()
            tk_alias = "tk"  # You can extend this if you need multiple joins

            # Base join for all paths (only FIT kits)
            self.sql_from.append(
                f" INNER JOIN tk_items_t {tk_alias} ON {tk_alias}.screening_subject_id = ss.screening_subject_id "
                f" AND {tk_alias}.tk_type_id > 1 "
            )

            if value == "any kit in any episode":
                return

            if "issued in latest episode" in value:
                self._add_join_to_latest_episode()
                self.sql_from.append(
                    f" AND {tk_alias}.subject_epis_id = ep.subject_epis_id "
                    f" AND NOT EXISTS ("
                    f" SELECT 'tko1' FROM tk_items_t tko "
                    f" WHERE tko.screening_subject_id = ss.screening_subject_id "
                    f" AND tko.subject_epis_id = ep.subject_epis_id "
                )
                if value.startswith("only"):
                    comparator = "!="
                elif value.startswith("first"):
                    comparator = "<"
                else:  # latest
                    comparator = ">"
                self.sql_from.append(f" AND tko.kitid {comparator} {tk_alias}.kitid) ")

            elif "logged in latest episode" in value:
                self._add_join_to_latest_episode()
                self.sql_from.append(
                    f" AND {tk_alias}.logged_subject_epis_id = ep.subject_epis_id "
                    f" AND NOT EXISTS ( "
                    f" SELECT 'tko2' FROM tk_items_t tko "
                    f" WHERE tko.screening_subject_id = ss.screening_subject_id "
                    f" AND tko.logged_subject_epis_id = ep.subject_epis_id "
                )
                if value.startswith("only"):
                    self.sql_from.append(f" AND tko.kitid != {tk_alias}.kitid ")
                elif value.startswith("first"):
                    self.sql_from.append(
                        f" AND tko.logged_in_on < {tk_alias}.logged_in_on "
                    )
                else:  # latest
                    self.sql_from.append(
                        f" AND tko.logged_in_on > {tk_alias}.logged_in_on "
                    )
                self.sql_from.append(")")

            else:
                raise ValueError(f"Invalid test kit selection value: {value}")

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_kit_has_been_read(self) -> None:
        """
        Filters test kits based on whether they have been read.
        Requires prior join to tk_items_t as alias 'tk' (via WHICH_TEST_KIT).

        Accepts values:
            - "yes" → reading_flag = 'Y'
            - "no"  → reading_flag = 'N'
        """
        try:
            value = self.criteria_value.strip().lower()
            if value == "yes":
                self.sql_where.append(f" AND /*rf*/ {self.tk}.reading_flag = 'Y' ")
            elif value == "no":
                self.sql_where.append(f" AND /*rf*/ {self.tk}.reading_flag = 'N' ")
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_kit_result(self) -> None:
        """
        Filters based on the result associated with the selected test kit.
        Requires prior join to tk_items_t as alias 'tk' (via WHICH_TEST_KIT).
        Uses comparator and uppercase value.
        """
        try:
            comparator = self.criteria_comparator
            value = self.criteria_value.strip().upper()
            self.sql_where.append(f"AND tk.test_results {comparator} '{value}'")
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_kit_has_analyser_result_code(self) -> None:
        """
        Filters kits based on whether they have an analyser error code.
        Requires prior join to tk_items_t as alias 'tk' (via WHICH_TEST_KIT).

        Accepts values:
            - "yes" → analyser_error_code IS NOT NULL
            - "no"  → analyser_error_code IS NULL
        """
        try:
            value = self.criteria_value.strip().lower()

            if value == "yes":
                self.sql_where.append(
                    f" AND /*aec*/ {self.tk}.analyser_error_code IS NOT NULL "
                )
            elif value == "no":
                self.sql_where.append(
                    " AND /*aec*/ {self.tk}.analyser_error_code IS NULL "
                )
            else:
                raise ValueError(
                    f"Invalid value for analyser result code presence: {value}"
                )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_join_to_appointments(self) -> None:
        """
        Adds join to appointment_t table based on appointment selection strategy.
        Requires prior join to latest episode (ep). Aliases the appointment table as 'ap'.

        Accepts values:
            - "any_appointment_in_latest_episode"
            - "latest_appointment_in_latest_episode"
            - "earlier_appointment_in_latest_episode"
            - "later_appointment_in_latest_episode"
        """
        try:
            value = self.criteria_value.strip().lower()
            ap_alias = "ap"
            apr_alias = "ap_prev"  # Simulated prior alias for test support

            self._add_join_to_latest_episode()
            self.sql_from.append(
                f" INNER JOIN appointment_t {ap_alias} ON {ap_alias}.subject_epis_id = ep.subject_epis_id "
            )

            if value == "any_appointment_in_latest_episode":
                return
            elif value == "latest appointment in latest episode":
                self.sql_from.append(
                    f" AND {ap_alias}.appointment_id = ( "
                    f" SELECT MAX(apx.appointment_id) "
                    f" FROM appointment_t apx "
                    f" WHERE apx.subject_epis_id = ep.subject_epis_id "
                    f" AND apx.void = 'N') "
                )
            elif value == "earlier appointment in latest episode":
                self.sql_from.append(
                    f" AND {ap_alias}.appointment_id < {apr_alias}.appointment_id "
                )
            elif value == "later appointment in latest episode":
                self.sql_from.append(
                    f" AND {ap_alias}.appointment_id > {apr_alias}.appointment_id "
                )
            else:
                raise ValueError(f"Invalid appointment selection value: {value}")

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_appointment_type(self) -> None:
        """
        Filters appointments by slot type (e.g. clinic, phone).
        Requires prior join to appointment_t as alias 'ap' (via WHICH_APPOINTMENT).

        Uses comparator and resolves slot type label to ID via AppointmentSlotType.
        """
        try:
            comparator = self.criteria_comparator
            appointment_slot_type = AppointmentSlotType.by_description_case_insensitive(
                self.criteria_value
            )
            if appointment_slot_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(
                f" AND /*ast*/ {self.ap}.appointment_slot_type_id {comparator} {appointment_slot_type.valid_value_id} "
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_appointment_status(self) -> None:
        """
        Filters appointments by status (e.g. booked, attended).
        Requires prior join to appointment_t as alias 'ap'.

        Uses comparator and resolves status label to ID via AppointmentStatusType.
        """
        try:
            comparator = self.criteria_comparator
            appointment_status_type = (
                AppointmentStatusType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            if appointment_status_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(
                f" AND /*as*/ {self.ap}.appointment_status_id {comparator} {appointment_status_type.valid_value_id} "
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_join_to_diagnostic_tests(self) -> None:
        """
        Adds joins to external_tests_t table for diagnostic test selection criteria.
        Handles various test types and conditions based on the criteria value.
        """
        try:
            which_test = WhichDiagnosticTest.by_description_case_insensitive(
                self.criteria_value
            )
            if which_test is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            idx = self.criteria_value_count
            xt = f"xt{idx}"
            xtp = f"xt{idx - 1}"

            # Ensure the join is only added once
            self.sql_from_diagnostic_test.append(
                f" INNER JOIN external_tests_t {xt} ON {xt}.screening_subject_id = ss.screening_subject_id "
            )

            match which_test:
                case WhichDiagnosticTest.ANY_TEST_IN_ANY_EPISODE:
                    # No further restriction required
                    return

                case WhichDiagnosticTest.ANY_TEST_IN_LATEST_EPISODE:
                    self._add_join_to_latest_episode()
                    self.sql_from_diagnostic_test.append(
                        f" AND /*any*/ {xt}.subject_epis_id = ep.subject_epis_id /*any*/ "
                    )
                    return

                case (
                    WhichDiagnosticTest.ONLY_TEST_IN_LATEST_EPISODE
                    | WhichDiagnosticTest.ONLY_NOT_VOID_TEST_IN_LATEST_EPISODE
                ):
                    self._add_join_to_latest_episode()
                    self.sql_from_diagnostic_test.append(
                        f" AND /*only*/ {xt}.subject_epis_id = ep.subject_epis_id "
                    )
                    if (
                        which_test
                        == WhichDiagnosticTest.ONLY_NOT_VOID_TEST_IN_LATEST_EPISODE
                    ):
                        self.sql_from_diagnostic_test.append(
                            f" AND /*only*/ {xt}.void = 'N' "
                        )
                    self.sql_from_diagnostic_test.append(
                        " AND NOT EXISTS ( SELECT 'xto' "
                        " FROM external_tests_t xto "
                        " WHERE xto.screening_subject_id = ss.screening_subject_id "
                    )
                    if (
                        which_test
                        == WhichDiagnosticTest.ONLY_NOT_VOID_TEST_IN_LATEST_EPISODE
                    ):
                        self.sql_from_diagnostic_test.append(" AND xto.void = 'N' ")
                    self.sql_from_diagnostic_test.append(
                        f" AND xto.subject_epis_id = ep.subject_epis_id "
                        f" AND xto.ext_test_id != {xt}.ext_test_id ) "
                    )
                    return

                case (
                    WhichDiagnosticTest.LATEST_TEST_IN_LATEST_EPISODE
                    | WhichDiagnosticTest.LATEST_NOT_VOID_TEST_IN_LATEST_EPISODE
                ):
                    self._add_join_to_latest_episode()
                    self.sql_from_diagnostic_test.append(
                        f" AND /*xtx*/ {xt}.ext_test_id = ( "
                        " SELECT MAX(xtx.ext_test_id) "
                        " FROM external_tests_t xtx "
                        " WHERE xtx.screening_subject_id = ss.screening_subject_id "
                    )
                    if (
                        which_test
                        == WhichDiagnosticTest.LATEST_NOT_VOID_TEST_IN_LATEST_EPISODE
                    ):
                        self.sql_from_diagnostic_test.append(" AND xtx.void = 'N' ")
                    self.sql_from_diagnostic_test.append(
                        " AND xtx.subject_epis_id = ep.subject_epis_id ) "
                    )
                    return

                case WhichDiagnosticTest.EARLIEST_NOT_VOID_TEST_IN_LATEST_EPISODE:
                    self._add_join_to_latest_episode()
                    self.sql_from_diagnostic_test.append(
                        f" AND /*xtn*/ {xt}.ext_test_id = ( "
                        " SELECT MIN(xtn.ext_test_id) "
                        " FROM external_tests_t xtn "
                        " WHERE xtn.screening_subject_id = ss.screening_subject_id "
                        " AND xtn.void = 'N' "
                        " AND xtn.subject_epis_id = ep.subject_epis_id ) "
                    )
                    return

                case (
                    WhichDiagnosticTest.EARLIER_TEST_IN_LATEST_EPISODE
                    | WhichDiagnosticTest.LATER_TEST_IN_LATEST_EPISODE
                ):
                    comparator = (
                        "<"
                        if which_test
                        == WhichDiagnosticTest.EARLIER_TEST_IN_LATEST_EPISODE
                        else ">"
                    )
                    if idx == 0:
                        raise SelectionBuilderException(
                            f"Diagnostic test selection value {self.single_quoted(self.criteria_value)} is not valid in the first line of the table of criteria"
                        )
                    else:
                        self._add_join_to_latest_episode()
                        self.sql_from_diagnostic_test.append(
                            f" AND /*xt*/ {xt}.ext_test_id {comparator} {xtp}.ext_test_id "
                        )
                    return

                case _ if hasattr(which_test, "get_test_number"):
                    self._add_join_to_latest_episode()
                    test_number = which_test.test_number
                    self.sql_from_diagnostic_test.append(
                        f" AND {xt}.subject_epis_id = ep.subject_epis_id "
                        f" AND {xt}.ext_test_id = ( "
                        "   SELECT xtr.ext_test_id "
                        "   FROM ("
                        "     SELECT rnk.ext_test_id, RANK() OVER (ORDER BY rnk.ext_test_id ASC) AS test_number "
                        "     FROM external_tests_t rnk "
                        f"     WHERE rnk.subject_epis_id = {xt}.subject_epis_id "
                        "     ) xtr "
                        f"   WHERE xtr.test_number = {test_number}"
                        " )"
                    )
                    return

                case _:
                    raise SelectionBuilderException(
                        f"Invalid diagnostic test selection value: {self.criteria_value}"
                    )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_diagnostic_test_type(self, proposed_or_confirmed: str) -> None:
        """
        Filters diagnostic tests by type—proposed or confirmed.
        Requires prior join to external_tests_t (xt aliasing assumed).
        """
        try:
            idx = getattr(self, "criteria_index", 0)
            xt = f"xt{idx}"

            if proposed_or_confirmed == "proposed":
                column = f"{xt}.proposed_type_id"
            elif proposed_or_confirmed == "confirmed":
                column = f"{xt}.confirmed_type_id"
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(f"AND {column} ")

            value = self.criteria_value.strip().lower()
            if value == "null":
                self.sql_where.append(self._SQL_IS_NULL)
            elif value == "not null":
                self.sql_where.append(self._SQL_IS_NOT_NULL)
            else:
                comparator = self.criteria_comparator
                diagnostic_test_type = (
                    DiagnosticTestType.by_description_case_insensitive(
                        self.criteria_value
                    )
                )
                if diagnostic_test_type is None:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )
                self.sql_where.append(
                    f" {comparator} {diagnostic_test_type.valid_value_id} "
                )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_diagnostic_test_is_void(self) -> None:
        """
        Adds WHERE clause to check whether diagnostic test is voided ('Y' or 'N').
        Requires prior join to external_tests_t using alias xtN.
        """
        try:
            idx = getattr(self, "criteria_index", 0)
            xt = f"xt{idx}"
            value = DiagnosticTestIsVoid.from_description(self.criteria_value)

            if value == DiagnosticTestIsVoid.YES:
                self.sql_where.append(f"AND {xt}.void = 'Y'")
            elif value == DiagnosticTestIsVoid.NO:
                self.sql_where.append(f"AND {xt}.void = 'N'")
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_diagnostic_test_has_result(self) -> None:
        """
        Adds WHERE clause to check whether a diagnostic test has a result (IS NULL / NOT NULL / = result_id).
        """
        try:
            idx = getattr(self, "criteria_index", 0)
            xt = f"xt{idx}"
            value = self.criteria_value.strip().lower()
            result = DiagnosticTestHasResult.by_description_case_insensitive(value)
            if result is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(f"AND {xt}.result_id ")

            if result == DiagnosticTestHasResult.YES:
                self.sql_where.append(self._SQL_IS_NOT_NULL)
            elif result == DiagnosticTestHasResult.NO:
                self.sql_where.append(self._SQL_IS_NULL)
            else:
                result_id = result.valid_value_id
                self.sql_where.append(f"= {result_id}")

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_diagnostic_test_has_outcome_of_result(self) -> None:
        """
        Adds WHERE clause filtering on whether the diagnostic test has an outcome-of-result.
        """
        try:
            idx = getattr(self, "criteria_index", 0)
            xt = f"xt{idx}"
            value = self.criteria_value.strip().lower()
            outcome = DiagnosticTestHasOutcomeOfResult.by_description_case_insensitive(
                value
            )
            if outcome is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(f"AND {xt}.outcome_of_result_id ")

            if outcome == DiagnosticTestHasOutcomeOfResult.YES:
                self.sql_where.append(self._SQL_IS_NOT_NULL)
            elif outcome == DiagnosticTestHasOutcomeOfResult.NO:
                self.sql_where.append(self._SQL_IS_NULL)
            else:
                outcome_id = outcome.valid_value_id
                self.sql_where.append(f" = {outcome_id} ")

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_diagnostic_test_intended_extent(self) -> None:
        """
        Adds WHERE clause filtering diagnostic tests by intended_extent_id.
        Supports null checks and value comparisons.
        """
        try:
            idx = getattr(self, "criteria_index", 0)
            xt = f"xt{idx}"
            extent = IntendedExtentType.by_description_case_insensitive(
                self.criteria_value
            )
            if extent is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(f"AND {xt}.intended_extent_id ")

            if extent in (IntendedExtentType.NULL, IntendedExtentType.NOT_NULL):
                self.sql_where.append(f"IS {extent.description}")
            else:
                self.sql_where.append(
                    f"{self.criteria_comparator} {extent.valid_value_id}"
                )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_has_dataset(self) -> None:
        """
        Filters based on presence or completion status of a dataset in the latest episode.
        """
        try:
            self._add_join_to_latest_episode()

            dataset_info = self._dataset_source_for_criteria_key()
            dataset_table = dataset_info["table"]
            alias = dataset_info["alias"]

            clause = "AND EXISTS ( "
            value = self.criteria_value.strip().lower()
            status = LatestEpisodeHasDataset.from_description(value)
            filter_clause = ""

            if status == LatestEpisodeHasDataset.NO:
                clause = " AND NOT EXISTS ( "
            elif status == LatestEpisodeHasDataset.YES_INCOMPLETE:
                filter_clause = f" AND {alias}.dataset_completed_date IS NULL "
            elif status == LatestEpisodeHasDataset.YES_COMPLETE:
                filter_clause = f" AND {alias}.dataset_completed_date IS NOT NULL "
            elif status == LatestEpisodeHasDataset.PAST:
                filter_clause = (
                    f" AND TRUNC({alias}.dataset_completed_date) < TRUNC(SYSDATE) "
                )
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(
                "".join(
                    [
                        clause,
                        f" SELECT 1 FROM {dataset_table} {alias} ",
                        f" WHERE {alias}.episode_id = ep.subject_epis_id ",
                        f" AND {alias}.deleted_flag = 'N' ",
                        filter_clause,
                        " ) ",
                    ]
                )
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _dataset_source_for_criteria_key(self) -> dict:
        """
        Internal helper method.
        Maps LATEST_EPISODE_HAS_* criteria keys to their corresponding dataset tables and aliases.
        Used by _add_criteria_latest_episode_has_dataset().
        """
        key = self.criteria_key
        if key == SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_CANCER_AUDIT_DATASET:
            return {"table": "ds_cancer_audit_t", "alias": "cads"}
        if (
            key
            == SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_COLONOSCOPY_ASSESSMENT_DATASET
        ):
            return {"table": "ds_patient_assessment_t", "alias": "dspa"}
        if key == SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_MDT_DATASET:
            return {"table": "ds_mdt_t", "alias": "mdt"}
        raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_latest_investigation_dataset(self) -> None:
        """
        Filters subjects based on their latest investigation dataset in their latest episode.
        Supports colonoscopy and radiology variations.
        """
        try:
            self._add_join_to_latest_episode()
            value = LatestEpisodeLatestInvestigationDataset.from_description(
                self.criteria_value
            ).lower()

            if value == "none":
                self.sql_where.append(
                    " AND NOT EXISTS (SELECT 'dsc1' FROM v_ds_colonoscopy dsc1 "
                    " WHERE dsc1.episode_id = ep.subject_epis_id "
                    " AND dsc1.confirmed_type_id = 16002) "
                )
            elif value == "colonoscopy - new":
                self.sql_where.append(
                    " AND EXISTS (SELECT 'dsc2' FROM v_ds_colonoscopy dsc2 "
                    " WHERE dsc2.episode_id = ep.subject_epis_id "
                    " AND dsc2.confirmed_type_id = 16002 "
                    " AND dsc2.deleted_flag = 'N' "
                    " AND dsc2.dataset_new_flag = 'Y') "
                )
            elif value == "limited colonoscopy - new":
                self.sql_where.append(
                    " AND EXISTS (SELECT 'dsc3' FROM v_ds_colonoscopy dsc3 "
                    " WHERE dsc3.episode_id = ep.subject_epis_id "
                    " AND dsc3.confirmed_type_id = 17996 "
                    " AND dsc3.deleted_flag = 'N' "
                    " AND dsc3.dataset_new_flag = 'Y') "
                )
            elif value == "flexible sigmoidoscopy - new":
                self.sql_where.append(
                    " AND EXISTS (SELECT 'dsc4' FROM v_ds_colonoscopy dsc4 "
                    " WHERE dsc4.episode_id = ep.subject_epis_id "
                    " AND dsc4.confirmed_type_id = 16004 "
                    " AND dsc4.deleted_flag = 'N' "
                    " AND dsc4.dataset_new_flag = 'Y') "
                )
            elif value == "ct colonography - new":
                self.sql_where.append(
                    " AND EXISTS (SELECT 'dsr1' FROM v_ds_radiology dsr1 "
                    " WHERE dsr1.episode_id = ep.subject_epis_id "
                    " AND dsr1.confirmed_type_id = 16087 "
                    " AND dsr1.deleted_flag = 'N' "
                    " AND dsr1.dataset_new_flag = 'Y') "
                )
            elif value == "endoscopy - incomplete":
                self.sql_where.append(
                    " AND EXISTS (SELECT 'dsei' FROM v_ds_colonoscopy dsei "
                    " WHERE dsei.episode_id = ep.subject_epis_id "
                    " AND dsei.deleted_flag = 'N' "
                    " AND dsei.dataset_completed_flag = 'N' "
                    " AND dsei.dataset_new_flag = 'N' "
                    " AND dsei.confirmed_test_date >= TO_DATE('01/01/2020','dd/mm/yyyy')) "
                )
            elif value == "radiology - incomplete":
                self.sql_where.append(
                    " AND EXISTS (SELECT 'dsri' FROM v_ds_radiology dsri "
                    " WHERE dsri.episode_id = ep.subject_epis_id "
                    " AND dsri.deleted_flag = 'N' "
                    " AND dsri.dataset_completed_flag = 'N' "
                    " AND dsri.dataset_new_flag = 'N' "
                    " AND dsri.confirmed_test_date >= TO_DATE('01/01/2020','dd/mm/yyyy')) "
                )
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_intended_extent(self) -> None:
        """
        Filters subjects based on presence of a colonoscopy dataset with a specific intended_extent_id
        in their latest episode.
        """
        try:
            self._add_join_to_latest_episode()
            extent = IntendedExtentType.by_description_case_insensitive(
                self.criteria_value
            )
            if extent is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            extent_id = extent.valid_value_id

            self.sql_where.append(
                " AND EXISTS (SELECT 'dsc' FROM v_ds_colonoscopy dsc "
                " WHERE dsc.episode_id = ep.subject_epis_id "
                f" AND dsc.intended_extent_id = {extent_id})"
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_surveillance_review_status(self) -> None:
        """
        Filters subjects based on the review_status_id in their surveillance review dataset.
        """
        try:
            self._add_join_to_surveillance_review()
            surveillance_review_status_type = (
                SurveillanceReviewStatusType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            if surveillance_review_status_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(
                f"AND sr.review_status_id {self.criteria_comparator} {surveillance_review_status_type.valid_value_id}"
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_join_to_surveillance_review(self) -> None:
        """
        Internal helper. Adds the necessary join to the surveillance review dataset for filtering.
        """
        if not self.sql_from_surveillance_review:
            self.sql_from_surveillance_review.append(
                " INNER JOIN surveillance_review sr ON sr.subject_id = ss.screening_subject_id "
            )

    def _add_criteria_does_subject_have_surveillance_review_case(self) -> None:
        """
        Filters subjects based on presence or absence of a surveillance review case.
        """
        try:
            value = DoesSubjectHaveSurveillanceReviewCase.from_description(
                self.criteria_value
            )

            clause = (
                self._SQL_AND_EXISTS if value == "yes" else self._SQL_AND_NOT_EXISTS
            )

            self.sql_where.append(
                f"{clause} (SELECT 'sr' FROM surveillance_review sr "
                "WHERE sr.subject_id = ss.screening_subject_id)"
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_surveillance_review_type(self) -> None:
        """
        Filters subjects based on review_case_type_id in the surveillance review dataset.
        """
        try:
            self._add_join_to_surveillance_review()
            surveillance_review_case_type = (
                SurveillanceReviewCaseType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            if surveillance_review_case_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(
                f" AND sr.review_case_type_id {self.criteria_comparator} {surveillance_review_case_type.valid_value_id} "
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_has_date_of_death_removal(self) -> None:
        """
        Filters subjects based on presence or absence of a date-of-death removal record.
        """
        try:
            value = HasDateOfDeathRemoval.from_description(self.criteria_value)
            clause = "EXISTS" if value == "Yes" else self._SQL_NOT_EXISTS

            self.sql_where.append(
                f" AND {clause} (SELECT 'dodr' FROM report_additional_data_t dodr "
                " WHERE dodr.rad_type_id = 15901 "
                " AND dodr.entity_id = c.contact_id) "
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_invited_since_age_extension(self) -> None:
        """
        Filters subjects based on whether they were invited since age extension began.
        """
        try:
            self._add_join_to_latest_episode()
            value = InvitedSinceAgeExtension.from_description(self.criteria_value)
            clause = "EXISTS" if value == "yes" else self._SQL_NOT_EXISTS

            self.sql_where.append(
                f"AND {clause} (SELECT 'sagex' FROM screening_subject_attribute_t sagex "
                "INNER JOIN valid_values vvagex ON vvagex.valid_value_id = sagex.attribute_id "
                "AND vvagex.domain = 'FOBT_AGEX_LOWER_AGE' "
                "WHERE sagex.screening_subject_id = ep.screening_subject_id "
                "AND sagex.start_date < ep.episode_start_date)"
            )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_note_count(self) -> None:
        """
        Filters subjects based on the count of associated supporting notes.
        """
        try:
            # Assumes criteriaValue contains both comparator and numeric literal, e.g., '>= 2'
            criteria_value = self.criteria_value.strip()

            self.sql_where.append(
                "AND (SELECT COUNT(*) FROM SUPPORTING_NOTES_T snt "
                "WHERE snt.screening_subject_id = ss.screening_subject_id) "
                f"{criteria_value} "
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_latest_episode_accumulated_episode_result(self) -> None:
        """
        Filters subjects based on the result of their latest episode.
        """
        self._add_join_to_latest_episode()

        self.sql_where.append(" AND ep.episode_result_id ")
        try:
            episode_result_type = EpisodeResultType.by_description_case_insensitive(
                self.criteria_value
            )
            if episode_result_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            if episode_result_type == EpisodeResultType.NULL:
                self.sql_where.append(self._SQL_IS_NULL)
            elif episode_result_type == EpisodeResultType.NOT_NULL:
                self.sql_where.append(self._SQL_IS_NOT_NULL)
            elif (
                episode_result_type
                == EpisodeResultType.ANY_SURVEILLANCE_NON_PARTICIPATION
            ):
                self.sql_where.append(
                    " IN (SELECT snp.valid_value_id FROM valid_values snp "
                    "WHERE snp.domain = 'OTHER_EPISODE_RESULT' "
                    "AND LOWER(snp.description) LIKE '%surveillance non-participation') "
                )
            else:
                self.sql_where.append(
                    f" {self.criteria_comparator} {episode_result_type.id} "
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_symptomatic_procedure_result(self) -> None:
        """
        Filters based on symptomatic surgery result value or presence.
        """
        try:
            column = f"{self.xt}{self.criteria_value_count}.surgery_result_id"

            result_type = (
                SymptomaticProcedureResultType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            if result_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            if result_type == SymptomaticProcedureResultType.NULL:
                self.sql_where.append(f" AND {column} IS NULL ")
            else:
                result_id = result_type.valid_value_id
                self.sql_where.append(
                    f" AND {column} {self.criteria_comparator} {result_id} "
                )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_screening_referral_type(self) -> None:
        """
        Filters based on screening referral type ID or null presence.
        """
        try:
            column = f"{self.xt}{self.criteria_value_count}.screening_referral_type_id"
            value = self.criteria_value.strip().lower()

            if value == "null":
                self.sql_where.append(f"AND {column} IS NULL")
            else:
                referral_type = ScreeningReferralType.by_description_case_insensitive(
                    self.criteria_value
                )
                if referral_type is None:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )
                self.sql_where.append(
                    f" AND {column} {self.criteria_comparator} {referral_type.valid_value_id} "
                )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_lynch_due_date_reason(
        self, subject: Optional[Subject] = None
    ) -> None:
        """
        Filters based on Lynch due date change reason. Supports symbolic types and subject comparison.
        """
        try:
            column = "ss.lynch_sdd_reason_for_change_id"
            reason = LynchSDDReasonForChangeType.by_description_case_insensitive(
                self.criteria_value
            )
            if reason is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            if reason == LynchSDDReasonForChangeType.NULL:
                self.sql_where.append(f" AND {column} IS NULL ")

            elif reason == LynchSDDReasonForChangeType.NOT_NULL:
                self.sql_where.append(f" AND {column} IS NOT NULL ")

            elif reason == LynchSDDReasonForChangeType.UNCHANGED:
                self._force_not_modifier_is_invalid_for_criteria_value()
                if subject is None:
                    raise SelectionBuilderException(
                        self.criteria_key_name,
                        "No subject provided for 'unchanged' logic",
                    )
                elif subject.lynch_due_date_change_reason_id is None:
                    self.sql_where.append(f"AND {column} IS NULL")
                else:
                    self.sql_where.append(
                        f"AND {column} = {subject.lynch_due_date_change_reason_id}"
                    )

            else:
                self.sql_where.append(
                    f"AND {column} {self.criteria_comparator} {reason.valid_value_id}"
                )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_lynch_incident_episode(self) -> None:
        """
        Filters based on linkage to a Lynch incident episode.
        """
        try:
            self._add_join_to_latest_episode()
            column = "ss.lynch_incident_subject_epis_id"
            value = LynchIncidentEpisodeType.from_description(self.criteria_value)

            if value == LynchIncidentEpisodeType.NULL:
                self.sql_where.append(f"AND {column} IS NULL")

            elif value == LynchIncidentEpisodeType.NOT_NULL:
                self.sql_where.append(f"AND {column} IS NOT NULL")

            elif value == LynchIncidentEpisodeType.LATEST_EPISODE:
                self.sql_where.append(f"AND {column} = ep.subject_epis_id")

            elif value == LynchIncidentEpisodeType.EARLIER_EPISODE:
                self.sql_where.append(f"AND {column} < ep.subject_epis_id")

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_fobt_prevalent_incident_status(self) -> None:
        """
        Filters subjects by whether their FOBT episode is prevalent or incident.
        """
        try:
            value = PrevalentIncidentStatusType.from_description(self.criteria_value)
            column = "ss.fobt_incident_subject_epis_id"

            if value == PrevalentIncidentStatusType.PREVALENT:
                self.sql_where.append(f"AND {column} IS NULL")
            elif value == PrevalentIncidentStatusType.INCIDENT:
                self.sql_where.append(f"AND {column} IS NOT NULL")

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_notify_queued_message_status(self) -> None:
        """
        Filters subjects based on Notify queued message status.
        """
        try:
            notify_message_event_status_id = (
                self._get_notify_message_event_status_id_from_criteria()
            )
            notify_message_code = self._get_notify_message_code_from_criteria()
            notify_message_status = self._get_notify_message_status_from_criteria()

            if notify_message_status == NotifyMessageStatus.NONE:
                self.sql_where.append(" AND NOT EXISTS (")
            else:
                self.sql_where.append(" AND EXISTS (")

            self.sql_where.append(
                " SELECT 1 FROM notify_message_queue nmq "
                " INNER JOIN notify_message_definition nmd ON nmd.message_definition_id = nmq.message_definition_id "
                " WHERE nmq.nhs_number = c.nhs_number "
                f" AND nmd.event_status_id = {notify_message_event_status_id} "
            )
            if (
                notify_message_status != NotifyMessageStatus.NONE
                and notify_message_status is not None
            ):
                self.sql_where.append(
                    f" AND nmq.message_status = '{notify_message_status.description}'"
                )
            if notify_message_code is not None:
                self.sql_where.append(
                    f" AND nmd.message_code = '{notify_message_code}'"
                )
            self.sql_where.append(")")

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_notify_archived_message_status(self) -> None:
        """
        Filters subjects based on archived Notify message criteria.
        """
        try:
            notify_message_event_status_id = (
                self._get_notify_message_event_status_id_from_criteria()
            )
            notify_message_code = self._get_notify_message_code_from_criteria()
            notify_message_status = self._get_notify_message_status_from_criteria()

            if notify_message_status == NotifyMessageStatus.NONE:
                self.sql_where.append(" AND NOT EXISTS (")
            else:
                self.sql_where.append(" AND EXISTS (")

            self.sql_where.append(
                " SELECT 1 FROM notify_message_record nmr "
                "INNER JOIN notify_message_batch nmb ON nmb.batch_id = nmr.batch_id "
                "INNER JOIN notify_message_definition nmd ON nmd.message_definition_id = nmb.message_definition_id "
                "WHERE nmr.subject_id = ss.screening_subject_id "
                f"AND nmd.event_status_id = {notify_message_event_status_id}"
            )
            if notify_message_code is not None:
                self.sql_where.append(
                    f" AND nmd.message_code = '{notify_message_code}'"
                )
            if (
                notify_message_status != NotifyMessageStatus.NONE
                and notify_message_status is not None
            ):
                self.sql_where.append(
                    f" AND nmr.message_status = '{notify_message_status.description}'"
                )
            self.sql_where.append(")")

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_has_previously_had_cancer(self) -> None:
        """
        Filters based on whether the subject previously had cancer.
        """
        try:
            answer = YesNoType.by_description_case_insensitive(self.criteria_value)
            condition = "'Y'" if answer == YesNoType.YES else "'N'"

            self.sql_where.append(
                f"AND pkg_letters.f_subj_prev_diagnosed_cancer(pi_subject_id => ss.screening_subject_id) = {condition}"
            )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_has_temporary_address(self) -> None:
        """
        Filters subjects based on whether they have a temporary address on record.
        """
        try:
            answer = YesNoType.by_description_case_insensitive(self.criteria_value)

            if answer == YesNoType.YES:
                self.sql_from.append(
                    " INNER JOIN sd_address_t adds ON adds.contact_id = c.contact_id "
                    " AND adds.ADDRESS_TYPE = 13043 "
                    " AND adds.EFFECTIVE_FROM IS NOT NULL "
                )
            elif answer == YesNoType.NO:
                self.sql_from.append(
                    " LEFT JOIN sd_address_t  adds ON adds.contact_id = c.contact_id "
                )
                self.sql_where.append(
                    " AND NOT EXISTS ("
                    " SELECT 1 "
                    " FROM sd_address_t x "
                    " WHERE x.contact_id  = c.contact_id "
                    " AND x.address_type = 13043"
                    " AND x.effective_from is not null) "
                )
            else:
                raise ValueError()
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    # ------------------------------------------------------------------------
    # 🧬 CADS Clinical Dataset Filters
    # ------------------------------------------------------------------------

    def _add_criteria_cads_asa_grade(self) -> None:
        """
        Filters subjects based on their ASA grade in the cancer audit dataset.
        Requires prior join to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the ASA grade is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        asa_grade = ASAGradeType.by_description_case_insensitive(self.criteria_value)
        if asa_grade is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND cads.asa_grade_id = {asa_grade.get_valid_value_id()} "
        )

    def _add_criteria_cads_staging_scans(self) -> None:
        """
        Filters subjects based on whether staging scans have been done in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the criteria value is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        self._add_join_to_cancer_audit_dataset_staging_scan()
        yes_no = YesNoType.by_description_case_insensitive(self.criteria_value)
        if yes_no is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(f" AND cads.staging_scans_done_id = {yes_no.get_id()} ")

    def _add_criteria_cads_type_of_scan(self) -> None:
        """
        Filters subjects based on the type of scan in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the scan type is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        self._add_join_to_cancer_audit_dataset_staging_scan()
        scan_type = ScanType.by_description_case_insensitive(self.criteria_value)
        if scan_type is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(f" AND dcss.type_of_scan_id = {scan_type.get_id()} ")

    def _add_criteria_cads_metastases_present(self) -> None:
        """
        Filters subjects based on whether metastases are present in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the metastases present type is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        metastases_present_type = MetastasesPresentType.by_description_case_insensitive(
            self.criteria_value
        )
        if metastases_present_type is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND cads.metastases_found_id = {metastases_present_type.get_id()} "
        )

    def _add_criteria_cads_metastases_location(self) -> None:
        """
        Filters subjects based on the location of metastases in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the metastases location is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        self._add_join_to_cancer_audit_dataset_metastasis()
        metastases_location = MetastasesLocationType.by_description_case_insensitive(
            self.criteria_value
        )
        if metastases_location is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND dcm.location_of_metastasis_id = {metastases_location.get_id()} "
        )

    def _add_criteria_cads_metastases_other_location(self, other_location: str) -> None:
        """
        Filters subjects based on the 'other' location of metastases in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the other location is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        self._add_join_to_cancer_audit_dataset_metastasis()
        self.sql_where.append(
            f" AND dcm.other_location_of_metastasis = '{other_location}' "
        )

    def _add_criteria_cads_final_pre_treatment_t_category(self) -> None:
        """
        Filters subjects based on their final pre-treatment T category in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the T category is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        final_pretreatment_t_category = (
            FinalPretreatmentTCategoryType.by_description_case_insensitive(
                self.criteria_value
            )
        )
        if final_pretreatment_t_category is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND cads.final_pre_treat_t_category_id = {final_pretreatment_t_category.get_id()} "
        )

    def _add_criteria_cads_final_pre_treatment_n_category(self) -> None:
        """
        Filters subjects based on their final pre-treatment N category in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the N category is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        final_pretreatment_n_category = (
            FinalPretreatmentNCategoryType.by_description_case_insensitive(
                self.criteria_value
            )
        )
        if final_pretreatment_n_category is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND cads.final_pre_treat_n_category_id = {final_pretreatment_n_category.get_id()} "
        )

    def _add_criteria_cads_final_pre_treatment_m_category(self) -> None:
        """
        Filters subjects based on their final pre-treatment M category in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the M category is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        final_pretreatment_m_category = (
            FinalPretreatmentMCategoryType.by_description_case_insensitive(
                self.criteria_value
            )
        )
        if final_pretreatment_m_category is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND cads.final_pre_treat_m_category_id = {final_pretreatment_m_category.get_id()} "
        )

    def _add_criteria_cads_treatment_received(self) -> None:
        """
        Filters subjects based on whether they received treatment in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the treatment received value is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        yes_no = YesNoType.by_description_case_insensitive(self.criteria_value)
        if yes_no is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(f" AND cads.treatment_received_id = {yes_no.get_id()} ")

    def _add_criteria_cads_reason_no_treatment_received(self) -> None:
        """
        Filters subjects based on the reason for not receiving treatment in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the reason is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        reason_no_treatment_recieved = (
            ReasonNoTreatmentReceivedType.by_description_case_insensitive(
                self.criteria_value
            )
        )
        if reason_no_treatment_recieved is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND cads.reason_no_treatment_id = {reason_no_treatment_recieved.get_id()} "
        )

    def _add_criteria_cads_tumour_location(self) -> None:
        """
        Filters subjects based on the location of the tumour in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the location is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        self._add_join_to_cancer_audit_dataset_tumour()
        location = LocationType.by_description_case_insensitive(self.criteria_value)
        if location is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(f" AND dctu.location_id = {location.get_id()} ")

    def _add_criteria_cads_tumour_height_of_tumour_above_anal_verge(self) -> None:
        """
        Filters subjects based on the height of the tumour above the anal verge in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the height is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        self._add_join_to_cancer_audit_dataset_tumour()
        self.sql_where.append(
            " AND dctu.height_above_anal_verge = {self.criteria_value} "
        )

    def _add_criteria_cads_tumour_previously_excised_tumour(self) -> None:
        """
        Filters subjects based on whether the tumour was previously excised in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the tumour type is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        self._add_join_to_cancer_audit_dataset_tumour()
        previously_excised_tumor = (
            PreviouslyExcisedTumourType.by_description_case_insensitive(
                self.criteria_value
            )
        )
        if previously_excised_tumor is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND dctu.recurrence_id = {previously_excised_tumor.get_id()} "
        )

    def _add_criteria_cads_treatment_type(self) -> None:
        """
        Filters subjects based on the type of treatment in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the treatment type is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        self._add_join_to_cancer_audit_dataset_treatment()
        treatment = TreatmentType.by_description_case_insensitive(self.criteria_value)
        if treatment is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND dctr.treatment_category_id = {treatment.get_id()} "
        )

    def _add_criteria_cads_treatment_given(self) -> None:
        """
        Filters subjects based on the specific treatment given in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the treatment is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        self._add_join_to_cancer_audit_dataset_treatment()
        treatment = TreatmentGiven.by_description_case_insensitive(self.criteria_value)
        if treatment is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND dctr.treatment_procedure_id = {treatment.get_id()} "
        )

    def _add_criteria_cads_cancer_treatment_intent(self) -> None:
        """
        Filters subjects based on the cancer treatment intent in the cancer audit dataset.
        Requires prior joins to the latest episode and cancer audit dataset.
        Raises SelectionBuilderException if the treatment intent is invalid.
        """
        self._add_join_to_latest_episode()
        self._add_join_to_cancer_audit_dataset()
        self._add_join_to_cancer_audit_dataset_treatment()
        cancer_treatment_intent = CancerTreatmentIntent.by_description_case_insensitive(
            self.criteria_value
        )
        if cancer_treatment_intent is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        self.sql_where.append(
            f" AND dctr.treatment_intent_id = {cancer_treatment_intent.get_id()} "
        )

    def _add_join_to_cancer_audit_dataset_staging_scan(self) -> None:
        """
        Internal helper. Adds the necessary join to the cancer audit dataset staging scan table.
        This is used to filter subjects based on their staging scans.
        """
        self.sql_from.append(
            "INNER JOIN data_cancer_audit_dataset_staging_scan dcss ON dcss.cancer_audit_dataset_id = cads.cancer_audit_dataset_id"
        )

    def _add_join_to_cancer_audit_dataset_metastasis(self) -> None:
        """
        Internal helper. Adds the necessary join to the cancer audit dataset metastasis table.
        This is used to filter subjects based on their metastasis information.
        """
        self.sql_from.append(
            "INNER JOIN data_cancer_audit_dataset_metastasis dcm ON dcm.cancer_audit_dataset_id = cads.cancer_audit_dataset_id"
        )

    def _add_join_to_cancer_audit_dataset_tumour(self) -> None:
        """
        Internal helper. Adds the necessary join to the cancer audit dataset tumour table.
        This is used to filter subjects based on their tumour information.
        """
        self.sql_from.append(
            "INNER JOIN data_cancer_audit_dataset_tumour dctu ON dctu.cancer_audit_dataset_id = cads.cancer_audit_dataset_id"
        )

    def _add_criteria_subject_hub_code(self, user: "User") -> None:
        """
        Adds criteria for filtering subjects based on their hub code.
        This method checks if the criteria value corresponds to a valid hub code,
        and if it does, it constructs the SQL WHERE clause to filter subjects by their hub ID.
        If the criteria value is not a valid hub code, it raises a SelectionBuilderException.
        """
        hub_code = None
        try:
            hub_enum = SubjectHubCode.by_description(self.criteria_value.lower())
            if hub_enum in [SubjectHubCode.USER_HUB, SubjectHubCode.USER_ORGANISATION]:
                if user.organisation is None or user.organisation.id is None:
                    raise ValueError("User organisation or organisation_id is None")
                hub_code = user.organisation.id
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
        except Exception:
            # If not in the enum it must be an actual hub code
            hub_code = self.criteria_value

        hub_code_str = str(hub_code).upper()
        self.sql_where.append(" AND c.hub_id ")
        self.sql_where.append(self.criteria_comparator)
        self.sql_where.append(" (")
        self.sql_where.append("   SELECT hub.org_id ")
        self.sql_where.append("   FROM org hub ")
        self.sql_where.append("   WHERE hub.org_code = ")
        self.sql_where.append(self.single_quoted(hub_code_str))
        self.sql_where.append(") ")

    def _add_criteria_subject_screening_centre_code(self, user: "User"):
        """
        Adds criteria for filtering subjects based on their screening centre code.
        This method checks if the criteria value corresponds to a valid screening centre code,
        and if it does, it constructs the SQL WHERE clause to filter subjects by their responsible screening centre ID.
        If the criteria value is not a valid screening centre code, it raises a SelectionBuilderException.
        If the user is associated with an organisation, it uses that organisation's ID as the screening centre code.
        If the criteria value is 'none' or 'not null', it constructs the appropriate SQL conditions for null or not null screening centre IDs.
        If the criteria value is 'user screening centre', 'user sc', or 'user organisation', it uses the user's organisation ID as the screening centre code.
        If the criteria value is not recognized, it raises a SelectionBuilderException.
        If the criteria value is not in the enum, it treats it as an actual screening centre code and constructs the SQL condition accordingly.
        Raises:
            SelectionBuilderException: If the criteria value is not recognized or if the user organisation is None or organisation_id is None.
        """
        sc_code = None

        try:
            option = SubjectScreeningCentreCode.by_description(
                self.criteria_value.lower()
            )
            match option:
                case SubjectScreeningCentreCode.NONE | SubjectScreeningCentreCode.NULL:
                    self.sql_where.append(" AND c.responsible_sc_id IS NULL ")
                case SubjectScreeningCentreCode.NOT_NULL:
                    self.sql_where.append(" AND c.responsible_sc_id IS NOT NULL ")
                case (
                    SubjectScreeningCentreCode.USER_SCREENING_CENTRE
                    | SubjectScreeningCentreCode.USER_SC
                    | SubjectScreeningCentreCode.USER_ORGANISATION
                ):
                    if user.organisation is None or user.organisation.id is None:
                        raise ValueError("User organisation or organisation_id is None")
                    sc_code = user.organisation.id
                case _:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )
        except SelectionBuilderException as ssbe:
            raise ssbe
        except Exception:
            # If not in enum, treat as an actual SC code
            sc_code = self.criteria_value

        if sc_code is not None:
            sc_code_str = str(sc_code).upper()
            self.sql_where.append(
                f" AND c.responsible_sc_id {self.criteria_comparator} ("
                "   SELECT sc.org_id "
                "   FROM org sc "
                f"   WHERE sc.org_code = {self.single_quoted(sc_code_str)}"
                ") "
            )

    def _add_criteria_has_gp_practice(self):
        """
        Adds criteria for filtering subjects based on whether they have a GP practice linked.
        This method checks the criteria value against predefined options in the HasGPPractice enum.
        Depending on the value, it constructs the appropriate SQL JOIN or WHERE clause to filter subjects accordingly.
        Raises:
            SelectionBuilderException: If the criteria value does not match any predefined options in the HasGPPractice enum.
            SelectionBuilderException: If an unexpected error occurs while processing the criteria value.
        """
        try:
            option = HasGPPractice.by_description(self.criteria_value.lower())

            match option:
                case HasGPPractice.YES_ACTIVE:
                    self.sql_from.append(
                        " INNER JOIN gp_practice_current_links gpl "
                        "   ON gpl.gp_practice_id = c.gp_practice_id "
                    )
                case HasGPPractice.YES_INACTIVE:
                    self.sql_where.append(
                        " AND c.gp_practice_id IS NOT NULL "
                        " AND c.gp_practice_id NOT IN ( "
                        "   SELECT gpl.gp_practice_id "
                        "   FROM gp_practice_current_links gpl ) "
                    )
                case HasGPPractice.NO:
                    self.sql_where.append(" AND c.gp_practice_id IS NULL ")
                case _:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_has_gp_practice_linked_to_sc(self) -> None:
        """
        Adds criteria for filtering subjects based on whether their GP practice is linked to a specific screening centre.
        This method constructs the SQL WHERE clause to filter subjects whose GP practice is linked to the screening centre specified by the criteria value.
        It uses a subquery to check if the GP practice ID is associated with the screening centre ID derived from the criteria value.
        """
        self.sql_where.append(
            " AND c.gp_practice_id IN ( "
            " SELECT o.org_id FROM gp_practice_current_links gpcl "
            " INNER JOIN org o ON gpcl.gp_practice_id = o.org_id "
            " WHERE gpcl.sc_id = ( "
            f" SELECT org_id FROM org WHERE org_code = {self.single_quoted(self.criteria_value)})) "
        )

    def _add_criteria_screening_status(self, subject: "Subject"):
        """
        Adds criteria for filtering subjects based on their screening status.
        This method constructs the SQL WHERE clause to filter subjects by their screening status ID.
        If the criteria value is 'unchanged', it checks if a subject is provided and uses the subject's existing screening status ID.
        If the criteria value is not 'unchanged', it attempts to resolve the screening status type from the criteria value.
        If the screening status type is not found, it raises a SelectionBuilderException.
        If the criteria value is 'unchanged' but no subject is provided, it raises an exception indicating that the subject must exist.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid screening status type.
            SelectionBuilderException: If the criteria value is 'unchanged' but no subject is provided.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a screening status type.
        """
        self.sql_where.append(" AND ss.screening_status_id ")

        if self.criteria_value.lower() == "unchanged":
            self._force_not_modifier_is_invalid_for_criteria_value()
            if subject is None:
                raise self.invalid_use_of_unchanged_exception(
                    self.criteria_key_name, self._REASON_NO_EXISTING_SUBJECT
                )
            self.sql_where.append(" = ")
            self.sql_where.append(subject.get_screening_status_id())
        else:
            try:
                screening_status_type = (
                    ScreeningStatusType.by_description_case_insensitive(
                        self.criteria_value
                    )
                )
                if screening_status_type is None:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )
                self.sql_where.append(self.criteria_comparator)
                self.sql_where.append(screening_status_type.valid_value_id)
            except Exception:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

    def _add_criteria_previous_screening_status(self):
        """
        Adds criteria for filtering subjects based on their previous screening status.
        This method constructs the SQL WHERE clause to filter subjects by their previous screening status ID.
        It resolves the screening status type from the criteria value and appends the appropriate SQL condition.
        If the screening status type is not found, it raises a SelectionBuilderException.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid screening status type.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a screening status type.
        """
        screening_status_type = ScreeningStatusType.by_description_case_insensitive(
            self.criteria_value
        )
        if screening_status_type is None:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

        self.sql_where.append(" AND ss.previous_screening_status_id ")

        match screening_status_type:
            case ScreeningStatusType.NULL:
                self.sql_where.append(self._SQL_IS_NULL)
            case ScreeningStatusType.NOT_NULL:
                self.sql_where.append(self._SQL_IS_NOT_NULL)
            case _:
                self.sql_where.append(
                    f"{self.criteria_comparator}{screening_status_type.valid_value_id}"
                )

    def _add_criteria_screening_status_reason(self, subject: "Subject"):
        """
        Adds criteria for filtering subjects based on their screening status change reason.
        This method constructs the SQL WHERE clause to filter subjects by their screening status change reason ID.
        If the criteria value is 'unchanged', it checks if a subject is provided and uses the subject's existing screening status change reason ID.
        If the criteria value is not 'unchanged', it attempts to resolve the screening status change reason type from the criteria value.
        If the screening status change reason type is not found, it raises a SelectionBuilderException.
        If the criteria value is 'unchanged' but no subject is provided, it raises an exception indicating that the subject must exist.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid screening status change reason type.
            SelectionBuilderException: If the criteria value is 'unchanged' but no subject is provided.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a screening status change reason type.
        """
        if self.criteria_value.lower() == "unchanged":
            self._force_not_modifier_is_invalid_for_criteria_value()
            if subject is None:
                raise self.invalid_use_of_unchanged_exception(
                    self.criteria_key_name, self._REASON_NO_EXISTING_SUBJECT
                )
            elif subject.get_screening_status_change_reason_id() is None:
                self.sql_where.append(" AND ss.ss_reason_for_change_id IS NULL")
            else:
                self.sql_where.append(
                    f" AND ss.ss_reason_for_change_id = {subject.get_screening_status_change_reason_id()}"
                )
        else:
            try:
                screening_status_change_reason_type = (
                    SSReasonForChangeType.by_description_case_insensitive(
                        self.criteria_value
                    )
                )
                if screening_status_change_reason_type is None:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )
                self.sql_where.append(
                    f" AND ss.ss_reason_for_change_id {self.criteria_comparator}{screening_status_change_reason_type.valid_value_id}"
                )
            except Exception:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

    def _add_criteria_date_field(
        self, subject: "Subject", pathway: str, date_type: str
    ) -> None:
        """
        Adds criteria for filtering subjects based on a date field.
        This method constructs the SQL WHERE clause to filter subjects by a specific date field,
        such as the date of birth, screening date, or other relevant dates.
        It handles various formats and conditions for the date field, including exact dates, relative dates,
        and special cases like 'last birthday'.
        """
        date_column_name = self._get_date_field_column_name(pathway, date_type)
        self._add_date_field_required_joins(date_column_name)

        criteria_words = self.criteria_value.split(" ")

        if self.criteria_value.isdigit():
            self._add_check_comparing_one_date_with_another(
                date_column_name,
                " = ",
                self._add_years_to_oracle_date(self.c_dob, self.criteria_value),
                False,
            )
        elif (
            self.criteria_value.lower() != "last birthday"
            and self.criteria_value.lower().endswith(" birthday")
            and len(criteria_words) == 2
        ):
            self._add_check_comparing_one_date_with_another(
                date_column_name,
                " = ",
                self._add_years_to_oracle_date(self.c_dob, criteria_words[0][:-2]),
                False,
            )
        elif self._is_valid_date(self.criteria_value):
            self._add_check_comparing_one_date_with_another(
                date_column_name,
                " = ",
                self._oracle_to_date_method(self.criteria_value, "yyyy-mm-dd"),
                False,
            )
        elif self._is_valid_date(self.criteria_value, "%d/%m/%Y"):
            self._add_check_comparing_one_date_with_another(
                date_column_name,
                " = ",
                self._oracle_to_date_method(self.criteria_value, "dd/mm/yyyy"),
                False,
            )
        elif (
            self.criteria_value.endswith(" ago")
            or self.criteria_value.endswith(" later")
        ) and (
            len(criteria_words) == 3
            or (
                len(criteria_words) == 4
                and self.criteria_value.startswith(("> ", "< ", "<= ", ">="))
            )
            or (
                len(criteria_words) == 5
                and self.criteria_value.lower().startswith(("more than ", "less than "))
            )
        ):
            self._add_check_date_is_a_period_ago_or_later(
                date_column_name, self.criteria_value
            )
        else:
            self._add_criteria_date_field_special_cases(
                self.criteria_value, subject, pathway, date_type, date_column_name
            )

    def _add_date_field_required_joins(self, column: str) -> None:
        """Used by: _add_criteria_date_field
        Determines which joins are needed based on the resolved date_column_name.
        Keeps the main method focused on value handling, not join logic.
        """
        if column.startswith("TRUNC(ep."):
            self._add_join_to_latest_episode()
        elif column.startswith("TRUNC(gcd."):
            self._add_join_to_genetic_condition_diagnosis()
        elif column.startswith("TRUNC(dctu."):
            self._add_join_to_latest_episode()
            self._add_join_to_cancer_audit_dataset()
            self._add_join_to_cancer_audit_dataset_tumor()
        elif column.startswith("TRUNC(dctr."):
            self._add_join_to_latest_episode()
            self._add_join_to_cancer_audit_dataset()
            self._add_join_to_cancer_audit_dataset_treatment()

    def _add_criteria_screening_due_date_reason(self, subject: "Subject"):
        """
        Adds criteria for filtering subjects based on their screening due date change reason.
        This method constructs the SQL WHERE clause to filter subjects by their screening due date change reason ID.
        If the criteria value is 'unchanged', it checks if a subject is provided and uses the subject's existing screening due date change reason ID.
        If the criteria value is not 'unchanged', it attempts to resolve the screening due date change reason type from the criteria value.
        If the screening due date change reason type is not found, it raises a SelectionBuilderException.
        If the criteria value is 'unchanged' but no subject is provided, it raises an exception indicating that the subject must exist.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid screening due date change reason type.
            SelectionBuilderException: If the criteria value is 'unchanged' but no subject is provided.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a screening due date change reason type.
        """
        due_date_reason = "ss.sdd_reason_for_change_id"
        try:
            screening_due_date_change_reason_type = (
                SDDReasonForChangeType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            self.sql_where.append(" AND ")

            if screening_due_date_change_reason_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            match screening_due_date_change_reason_type:
                case SDDReasonForChangeType.NULL:
                    self.sql_where.append(f"{due_date_reason}_SQL_IS_NULL")
                case SDDReasonForChangeType.NOT_NULL:
                    self.sql_where.append(f"{due_date_reason}_SQL_IS_NOT_NULL")
                case SDDReasonForChangeType.UNCHANGED:
                    self._force_not_modifier_is_invalid_for_criteria_value()
                    if subject is None:
                        raise self.invalid_use_of_unchanged_exception(
                            self.criteria_key_name, self._REASON_NO_EXISTING_SUBJECT
                        )
                    elif subject.get_screening_due_date_change_reason_id() is None:
                        self.sql_where.append(f"{due_date_reason}_SQL_IS_NULL")
                    else:
                        self.sql_where.append(
                            f"{due_date_reason}{" = "}{subject.get_screening_due_date_change_reason_id()}"
                        )
                case _:
                    self.sql_where.append(
                        f"{due_date_reason}{self.criteria_comparator}{screening_due_date_change_reason_type.valid_value_id}"
                    )
        except SelectionBuilderException as ssbe:
            raise ssbe
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_surveillance_due_date_reason(self, subject: "Subject"):
        """
        Adds criteria for filtering subjects based on their surveillance due date change reason.
        This method constructs the SQL WHERE clause to filter subjects by their surveillance due date change reason ID.
        If the criteria value is 'unchanged', it checks if a subject is provided and uses the subject's existing surveillance due date change reason ID.
        If the criteria value is not 'unchanged', it attempts to resolve the surveillance due date change reason type from the criteria value.
        If the surveillance due date change reason type is not found, it raises a SelectionBuilderException.
        If the criteria value is 'unchanged' but no subject is provided, it raises an exception indicating that the subject must exist.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid surveillance due date change reason type.
            SelectionBuilderException: If the criteria value is 'unchanged' but no subject is provided.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a surveillance due date change reason type.
        """
        try:
            surveillance_due_date_change_reason = (
                SSDDReasonForChangeType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            self.sql_where.append(" AND ss.surveillance_sdd_rsn_change_id ")

            if surveillance_due_date_change_reason is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            match surveillance_due_date_change_reason:
                case SSDDReasonForChangeType.NULL | SSDDReasonForChangeType.NOT_NULL:
                    self.sql_where.append(
                        f" IS {surveillance_due_date_change_reason.description}"
                    )
                case SSDDReasonForChangeType.UNCHANGED:
                    self._force_not_modifier_is_invalid_for_criteria_value()
                    if subject is None:
                        raise self.invalid_use_of_unchanged_exception(
                            self.criteria_key_name, self._REASON_NO_EXISTING_SUBJECT
                        )
                    elif subject.get_surveillance_due_date_change_reason_id() is None:
                        self.sql_where.append(self._SQL_IS_NULL)
                    else:
                        self.sql_where.append(
                            f" = {subject.get_surveillance_due_date_change_reason_id()}"
                        )
                case _:
                    self.sql_where.append(
                        f"{self.criteria_comparator}{surveillance_due_date_change_reason.valid_value_id}"
                    )
        except SelectionBuilderException as ssbe:
            raise ssbe
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_bowel_scope_due_date_reason(self):
        """
        Adds criteria for filtering subjects based on their bowel scope due date change reason.
        This method constructs the SQL WHERE clause to filter subjects by their bowel scope due date change reason ID.
        It resolves the bowel scope due date change reason type from the criteria value and appends the appropriate SQL condition.
        If the bowel scope due date change reason type is not found, it raises a SelectionBuilderException.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid bowel scope due date change reason type.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a bowel scope due date change reason type.
        """
        try:
            bowel_scope_due_date_change_reason_type = (
                BowelScopeDDReasonForChangeType.by_description(self.criteria_value)
            )

            if bowel_scope_due_date_change_reason_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(" AND ss.fs_sdd_reason_for_change_id ")
            self.sql_where.append(
                f"{self.criteria_comparator}{bowel_scope_due_date_change_reason_type.valid_value_id}"
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_manual_cease_requested(self) -> None:
        """
        Adds criteria for filtering subjects based on the manual cease requested status.
        This method constructs the SQL WHERE clause to filter subjects by their manual cease requested status ID.
        It resolves the manual cease requested status from the criteria value and appends the appropriate SQL condition.
        If the manual cease requested status is not found, it raises a SelectionBuilderException.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid manual cease requested status.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a manual cease requested status.
        """
        try:
            self.sql_where.append(" AND ss.cease_requested_status_id ")

            criterion = ManualCeaseRequested.by_description_case_insensitive(
                self.criteria_value
            )
            if criterion is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            match criterion:
                case ManualCeaseRequested.NO:
                    self.sql_where.append(self._SQL_IS_NULL)
                case ManualCeaseRequested.YES:
                    self.sql_where.append(self._SQL_IS_NOT_NULL)
                case ManualCeaseRequested.DISCLAIMER_LETTER_REQUIRED:
                    self.sql_where.append("= 35")  # C1
                case ManualCeaseRequested.DISCLAIMER_LETTER_SENT:
                    self.sql_where.append("= 36")  # C2
                case _:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_ceased_confirmation_details(self):
        """
        Adds criteria for filtering subjects based on ceased confirmation details.
        This method constructs the SQL WHERE clause to filter subjects by their ceased confirmation details.
        It resolves the ceased confirmation details from the criteria value and appends the appropriate SQL condition.
        If the ceased confirmation details are not found, it raises a SelectionBuilderException.
        If the criteria value is not recognized, it falls back to string matching.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid ceased confirmation details.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to ceased confirmation details.
        """
        self.sql_where.append(" AND LOWER(ss.ceased_confirmation_details) ")

        try:
            ccd = CeasedConfirmationDetails.by_description(self.criteria_value.lower())
            if ccd in (
                CeasedConfirmationDetails.NULL,
                CeasedConfirmationDetails.NOT_NULL,
            ):
                self.sql_where.append(f" IS {ccd.get_description()} ")
            else:
                raise ValueError("Unrecognized enum value")
        except Exception:
            # Fall back to string matching
            value_quoted = f"'{self.criteria_value.lower()}'"
            self.sql_where.append(f"{self.criteria_comparator} {value_quoted} ")

    def _add_criteria_ceased_confirmation_user_id(self, user: "User") -> None:
        """
        Adds criteria for filtering subjects based on the ceased confirmation PIO ID.
        This method constructs the SQL WHERE clause to filter subjects by their ceased confirmation PIO ID.
        It resolves the ceased confirmation user ID from the criteria value and appends the appropriate SQL condition.
        If the criteria value is numeric, it treats it as an actual PIO ID.
        If the criteria value is not numeric, it attempts to resolve it from the CeasedConfirmationUserId enum.
        If the enum value is not recognized, it raises a SelectionBuilderException.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid ceased confirmation user ID.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a ceased confirmation user ID.
            SelectionBuilderException: If the user organisation is None or organisation_id is None when required.
        """
        self.sql_where.append(" AND ss.ceased_confirmation_pio_id ")

        if self.criteria_value.isnumeric():  # actual PIO ID
            self.sql_where.append(self.criteria_comparator)
            self.sql_where.append(self.criteria_value)
            self.sql_where.append(" ")
        else:
            try:
                enum_value = CeasedConfirmationUserId.by_description(
                    self.criteria_value.lower()
                )
                if enum_value == CeasedConfirmationUserId.AUTOMATED_PROCESS_ID:
                    self.sql_where.append(self.criteria_comparator)
                    self.sql_where.append(" 2 ")
                elif enum_value == CeasedConfirmationUserId.NOT_NULL:
                    self.sql_where.append(self._SQL_IS_NOT_NULL)
                elif enum_value == CeasedConfirmationUserId.NULL:
                    self.sql_where.append(self._SQL_IS_NULL)
                elif enum_value == CeasedConfirmationUserId.USER_ID:
                    self.sql_where.append(self.criteria_comparator)
                    self.sql_where.append(str(user.user_id) + " ")
                else:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )
            except Exception:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

    def _add_criteria_clinical_reason_for_cease(self) -> None:
        """
        Adds criteria for filtering subjects based on their clinical reason for cease.
        This method constructs the SQL WHERE clause to filter subjects by their clinical reason for cease ID.
        It resolves the clinical cease reason type from the criteria value and appends the appropriate SQL condition.
        If the clinical cease reason type is not found, it raises a SelectionBuilderException.
        If the criteria value is 'null' or 'not null', it constructs the appropriate SQL condition for null or not null clinical cease reason IDs.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid clinical cease reason type.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a clinical cease reason type.
            SelectionBuilderException: If an unexpected error occurs while processing the criteria value.
        """
        try:
            clinical_cease_reason = (
                ClinicalCeaseReasonType.by_description_case_insensitive(
                    self.criteria_value
                )
            )
            self.sql_where.append(" AND ss.clinical_reason_for_cease_id ")

            if clinical_cease_reason is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            if clinical_cease_reason in {
                ClinicalCeaseReasonType.NULL,
                ClinicalCeaseReasonType.NOT_NULL,
            }:
                self.sql_where.append(f" IS {clinical_cease_reason.description}")
            else:
                self.sql_where.append(
                    f"{self.criteria_comparator}{clinical_cease_reason.valid_value_id}"
                )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_subject_has_event_status(self) -> None:
        """
        Adds criteria for filtering subjects based on their event status.
        This method constructs the SQL WHERE clause to filter subjects by their event status ID.
        It resolves the event status type from the criteria value and appends the appropriate SQL condition.
        If the event status type is not found, it raises a SelectionBuilderException.
        If the criteria value is 'not null', it constructs the appropriate SQL condition for not null event status IDs.
        If the criteria value is 'null', it constructs the appropriate SQL condition for null event status IDs.
        If the criteria value is 'exists', it constructs a subquery to check for the existence of an event status.
        If the criteria value is 'not exists', it constructs a subquery to check for the non-existence of an event status.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid event status type.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to an event status type.
            SelectionBuilderException: If an unexpected error occurs while processing the criteria value.
        """
        event_exists = (
            self.criteria_key == SubjectSelectionCriteriaKey.SUBJECT_HAS_EVENT_STATUS
        )

        try:
            event_status = EventStatusType.get_by_code(self.criteria_value.upper())

            if event_status is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

            self.sql_where.append(" AND")

            if not event_exists:
                self.sql_where.append(" NOT")

            self.sql_where.append(
                f" EXISTS ("
                f" SELECT 1"
                f" FROM ep_events_t sev"
                f" WHERE sev.screening_subject_id = ss.screening_subject_id"
                f" AND sev.event_status_id = {event_status.id}"
                f") "
            )

        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_criteria_has_unprocessed_sspi_updates(self) -> None:
        """
        Adds criteria for filtering subjects based on whether they have unprocessed SSPI updates.
        This method constructs the SQL WHERE clause to filter subjects based on the existence of unprocessed SSPI updates.
        It resolves the unprocessed SSPI updates status from the criteria value and appends the appropriate SQL condition.
        If the unprocessed SSPI updates status is not found, it raises a SelectionBuilderException.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid unprocessed SSPI updates status.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to an unprocessed SSPI updates status.
            SelectionBuilderException: If an unexpected error occurs while processing the criteria value.
        """
        try:
            value = HasUnprocessedSSPIUpdates.by_description(
                self.criteria_value.lower()
            )
            if value == HasUnprocessedSSPIUpdates.YES:
                self.sql_where.append(" AND EXISTS ( SELECT 'sdfp' ")
            elif value == HasUnprocessedSSPIUpdates.NO:
                self.sql_where.append(" AND NOT EXISTS ( SELECT 'sdfp' ")
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

        self.sql_where.append("   FROM sd_feed_processing_t sdfp ")
        self.sql_where.append("   WHERE sdfp.contact_id = c.contact_id ")
        self.sql_where.append("   AND sdfp.awaiting_manual_intervention = 'Y' ) ")

    def _add_criteria_has_user_dob_update(self) -> None:
        """
        Adds criteria for filtering subjects based on whether they have a user DOB update.
        This method constructs the SQL WHERE clause to filter subjects based on the existence of a user DOB update.
        It resolves the user DOB update status from the criteria value and appends the appropriate SQL condition.
        If the user DOB update status is not found, it raises a SelectionBuilderException.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid user DOB update status.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a user DOB update status.
            SelectionBuilderException: If an unexpected error occurs while processing the criteria value.
        """
        try:
            value = HasUserDobUpdate.by_description(self.criteria_value.lower())
            if value == HasUserDobUpdate.YES:
                self.sql_where.append(" AND EXISTS ( SELECT 'div' ")
            elif value == HasUserDobUpdate.NO:
                self.sql_where.append(" AND NOT EXISTS ( SELECT 'div' ")
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

        self.sql_where.append("   from mpi.sd_data_item_value_t div ")
        self.sql_where.append("   WHERE div.contact_id = c.contact_id ")
        self.sql_where.append("   AND div.data_item_id = 4 ) ")

    def _add_criteria_subject_has_episodes(
        self, episode_type: Optional["EpisodeType"] = None
    ) -> None:
        """
        Adds criteria for filtering subjects based on whether they have episodes.
        This method constructs the SQL WHERE clause to filter subjects based on the existence of episodes.
        It resolves the subject has episode status from the criteria value and appends the appropriate SQL condition.
        If the subject has episode status is not found, it raises a SelectionBuilderException.
        If the criteria value is 'yes', it constructs a subquery to check for the existence of episodes.
        If the criteria value is 'no', it constructs a subquery to check for the non-existence of episodes.
        If the criteria key is SUBJECT_HAS_AN_OPEN_EPISODE, it adds an additional condition to check for open episodes.
        Raises:
            SelectionBuilderException: If the criteria value does not correspond to a valid subject has episode status.
            SelectionBuilderException: If the criteria value is invalid or cannot be resolved to a subject has episode status.
            SelectionBuilderException: If an unexpected error occurs while processing the criteria value.
        """
        try:
            value = SubjectHasEpisode.by_description(self.criteria_value)
            if value == SubjectHasEpisode.YES:
                self.sql_where.append(" AND EXISTS ( SELECT 'ep' ")
            elif value == SubjectHasEpisode.NO:
                self.sql_where.append(" AND NOT EXISTS ( SELECT 'ep' ")
            else:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
        except Exception:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

        self.sql_where.append("   FROM ep_subject_episode_t ep ")
        self.sql_where.append(
            "   WHERE ep.screening_subject_id = ss.screening_subject_id "
        )

        if episode_type is not None:
            self.sql_where.append(
                f"   AND ep.episode_type_id = {episode_type.valid_value_id} "
            )

        if self.criteria_key == SubjectSelectionCriteriaKey.SUBJECT_HAS_AN_OPEN_EPISODE:
            self.sql_where.append("   AND ep.episode_end_date IS NULL ")

        self.sql_where.append(" )")

    def _get_date_field_column_name(self, pathway: str, date_type: str) -> str:
        """
        Map pathway and date_type to the correct Oracle column name.
        xt and ap are optional table aliases for diagnostic test and appointment joins.
        """

        concat_key = (pathway + date_type).upper()

        mapping = {
            "ALL_PATHWAYSSCREENING_STATUS_CHANGE_DATE": "TRUNC(ss.screening_status_change_date)",
            "ALL_PATHWAYSLATEST_EPISODE_START_DATE": "TRUNC(ep.episode_start_date)",
            "ALL_PATHWAYSLATEST_EPISODE_END_DATE": "TRUNC(ep.episode_end_date)",
            "ALL_PATHWAYSCEASED_CONFIRMATION_DATE": "TRUNC(ss.ceased_confirmation_recd_date)",
            "ALL_PATHWAYSDATE_OF_DEATH": "TRUNC(c.date_of_death)",
            "ALL_PATHWAYSSYMPTOMATIC_PROCEDURE_DATE": f"TRUNC({self.xt}{self.criteria_value_count}.surgery_date)",
            "ALL_PATHWAYSAPPOINTMENT_DATE": f"TRUNC({self.ap}.appointment_date)",
            "FOBTDUE_DATE": "TRUNC(ss.screening_due_date)",
            "FOBTCALCULATED_DUE_DATE": "TRUNC(ss.calculated_sdd)",
            "FOBTDUE_DATE_CHANGE_DATE": "TRUNC(ss.sdd_change_date)",
            "FOBTPREVIOUS_DUE_DATE": "TRUNC(ss.previous_sdd)",
            "SURVEILLANCEDUE_DATE": "TRUNC(ss.surveillance_screen_due_date)",
            "SURVEILLANCECALCULATED_DUE_DATE": "TRUNC(ss.calculated_ssdd)",
            "SURVEILLANCEDUE_DATE_CHANGE_DATE": "TRUNC(ss.surveillance_sdd_change_date)",
            "SURVEILLANCEPREVIOUS_DUE_DATE": "TRUNC(ss.previous_surveillance_sdd)",
            "LYNCHDUE_DATE": "TRUNC(ss.lynch_screening_due_date)",
            "LYNCHCALCULATED_DUE_DATE": "TRUNC(ss.lynch_calculated_sdd)",
            "LYNCHDUE_DATE_CHANGE_DATE": "TRUNC(ss.lynch_sdd_change_date)",
            "LYNCHDIAGNOSIS_DATE": "TRUNC(gcd.diagnosis_date)",
            "LYNCHLAST_COLONOSCOPY_DATE": "TRUNC(gcd.last_colonoscopy_date)",
            "LYNCHPREVIOUS_DUE_DATE": "TRUNC(ss.previous_lynch_sdd)",
            "LYNCHLOWER_LYNCH_AGE": "pkg_bcss_common.f_get_lynch_lower_age_limit (ss.screening_subject_id)",
            "ALL_PATHWAYSSEVENTY_FIFTH_BIRTHDAY": "ADD_MONTHS(TRUNC(c.date_of_birth), 12*75)",
            "ALL_PATHWAYSCADS TUMOUR_DATE_OF_DIAGNOSIS": "TRUNC(dctu.date_of_diagnosis)",
            "ALL_PATHWAYSCADS TREATMENT_START_DATE": "TRUNC(dctr.treatment_start_date)",
            "ALL_PATHWAYSDIAGNOSTIC_TEST_CONFIRMED_DATE": f"TRUNC({self.xt}{self.criteria_value_count}.confirmed_date)",
        }
        if concat_key not in mapping:
            raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)
        return mapping[concat_key]

    def _add_join_to_latest_episode(self) -> None:
        """
        Adds a join to the latest episode for the screening subject.
        This method constructs the SQL JOIN clause to link the screening subject with their latest episode.
        It ensures that the join is only added once to avoid duplication.
        The join is based on the screening subject's ID and the latest episode's subject episode ID.
        The join condition ensures that the latest episode is selected by using a subquery to get the maximum subject episode ID for each screening subject.
        This method is used to ensure that the latest episode is included in the SQL query for filtering subjects based on their latest episode information.
        """
        if not self.sql_from_episode:
            self.sql_from_episode.append(
                " INNER JOIN ep_subject_episode_t ep "
                " ON ep.screening_subject_id = ss.screening_subject_id "
                " AND ep.subject_epis_id = ( "
                " SELECT MAX(epx.subject_epis_id) "
                " FROM ep_subject_episode_t epx "
                " WHERE epx.screening_subject_id = ss.screening_subject_id ) "
            )

    def _add_join_to_genetic_condition_diagnosis(self) -> None:
        """
        Adds a join to the genetic condition diagnosis for the screening subject.
        This method constructs the SQL JOIN clause to link the screening subject with their genetic condition diagnosis.
        It ensures that the join is only added once to avoid duplication.
        The join condition is based on the screening subject's ID and the genetic condition diagnosis's screening subject ID.
        The join also checks that the genetic condition diagnosis is not marked as deleted.
        This method is used to ensure that the genetic condition diagnosis is included in the SQL query for filtering subjects based on their genetic condition diagnosis information.
        """
        if not self.sql_from_genetic_condition_diagnosis:
            self.sql_from_genetic_condition_diagnosis.append(
                " INNER JOIN genetic_condition_diagnosis gcd "
                " ON gcd.screening_subject_id = ss.screening_subject_id "
                " AND gcd.deleted_flag = 'N' "
            )

    def _add_join_to_cancer_audit_dataset(self) -> None:
        """
        Adds a join to the cancer audit datasets for the screening subject.
        This method constructs the SQL JOIN clause to link the screening subject with their cancer audit datasets.
        It ensures that the join is only added once to avoid duplication.
        The join condition is based on the screening subject's episode ID and the cancer audit dataset's episode ID.
        The join also checks that the cancer audit dataset is not marked as deleted.
        This method is used to ensure that the cancer audit datasets are included in the SQL query for filtering subjects based on their cancer audit information.
        """
        if (
            " INNER JOIN ds_cancer_audit_t cads ON cads.episode_id = ep.subject_epis_id AND cads.deleted_flag = 'N' "
            not in self.sql_from_cancer_audit_datasets
        ):
            self.sql_from_cancer_audit_datasets.append(
                " INNER JOIN ds_cancer_audit_t cads ON cads.episode_id = ep.subject_epis_id AND cads.deleted_flag = 'N' "
            )

    def _add_join_to_cancer_audit_dataset_tumor(self) -> None:
        """
        Adds a join to the cancer audit dataset tumor for the screening subject.
        This method constructs the SQL JOIN clause to link the screening subject with their cancer audit dataset tumor.
        It ensures that the join is only added once to avoid duplication.
        The join condition is based on the cancer audit dataset's cancer audit ID and the cancer audit dataset tumor's cancer audit ID.
        The join also checks that the cancer audit dataset tumor is not marked as deleted.
        This method is used to ensure that the cancer audit dataset tumor information is included in the SQL query for filtering subjects based on their cancer audit tumor information.
        """
        if (
            " INNER JOIN DS_CA2_TUMOUR dctu ON dctu.CANCER_AUDIT_ID =cads.CANCER_AUDIT_ID AND dctu.deleted_flag = 'N' "
            not in self.sql_from_cancer_audit_datasets
        ):
            self.sql_from_cancer_audit_datasets.append(
                " INNER JOIN DS_CA2_TUMOUR dctu ON dctu.CANCER_AUDIT_ID =cads.CANCER_AUDIT_ID AND dctu.deleted_flag = 'N' "
            )

    def _add_join_to_cancer_audit_dataset_treatment(self) -> None:
        """
        Adds a join to the cancer audit dataset treatment for the screening subject.
        This method constructs the SQL JOIN clause to link the screening subject with their cancer audit dataset treatment.
        It ensures that the join is only added once to avoid duplication.
        The join condition is based on the cancer audit dataset's cancer audit ID and the cancer audit dataset treatment's cancer audit ID.
        The join also checks that the cancer audit dataset treatment is not marked as deleted.
        This method is used to ensure that the cancer audit dataset treatment information is included in the SQL query for filtering subjects based on their cancer audit treatment information.
        """
        if (
            " INNER JOIN DS_CA2_TREATMENT dctr ON dctr.CANCER_AUDIT_ID = cads.CANCER_AUDIT_ID AND dctr.deleted_flag = 'N' "
            not in self.sql_from_cancer_audit_datasets
        ):
            self.sql_from_cancer_audit_datasets.append(
                " INNER JOIN DS_CA2_TREATMENT dctr ON dctr.CANCER_AUDIT_ID = cads.CANCER_AUDIT_ID AND dctr.deleted_flag = 'N' "
            )

    def _add_check_comparing_one_date_with_another(
        self,
        column_to_check: str,
        comparator: str,
        date_to_check_against: str,
        allow_nulls: bool,
    ) -> None:
        """
        Adds a condition to the SQL WHERE clause to compare one date column with another date.
        This method constructs the SQL condition to check if the specified date column is either greater than,
        less than, or equal to the specified date to check against.
        If allow_nulls is True, it uses the NVL function to handle null values in the date columns.
        The comparator can be one of the following: '=', '!=', '<', '>', '<=', '>='.
        Args:
            column_to_check (str): The name of the date column to check.
            comparator (str): The comparator to use for the date comparison.
            date_to_check_against (str): The date to check against, formatted as an Oracle date string.
            allow_nulls (bool): Whether to allow null values in the date columns.
        """
        if allow_nulls:
            column_to_check = self._nvl_date(column_to_check)
            date_to_check_against = self._nvl_date(date_to_check_against)
        self.sql_where.append(
            f" AND {column_to_check}  {comparator}  {date_to_check_against} "
        )

    def _add_days_to_oracle_date(self, column_name: str, number_of_days: str) -> str:
        """
        Adds a specified number of days to an Oracle date column.
        This method constructs the SQL expression to add days to a date column in Oracle.
        Args:
            column_name (str): The name of the date column to which days will be added.
            number_of_days (str): The number of days to add, as a string.
        Returns:
            str: The SQL expression to add days to the date column.
        """
        return f" TRUNC({column_name}) + {number_of_days} "

    def _add_months_to_oracle_date(
        self, column_name: str, number_of_months: str
    ) -> str:
        """
        Adds a specified number of months to an Oracle date column.
        This method constructs the SQL expression to add months to a date column in Oracle.
        Args:
            column_name (str): The name of the date column to which months will be added.
            number_of_months (str): The number of months to add, as a string.
        Returns:
            str: The SQL expression to add months to the date column.
        """
        return self._add_months_or_years_to_oracle_date(
            column_name, False, number_of_months
        )

    def _add_years_to_oracle_date(self, column_name: str, number_of_years) -> str:
        """
        Adds a specified number of years to an Oracle date column.
        This method constructs the SQL expression to add years to a date column in Oracle.
        Args:
            column_name (str): The name of the date column to which years will be added.
            number_of_years (str): The number of years to add, as a string.
        Returns:
            str: The SQL expression to add years to the date column.
        """
        return self._add_months_or_years_to_oracle_date(
            column_name, True, number_of_years
        )

    def _add_months_or_years_to_oracle_date(
        self, column_name: str, years: bool, number_to_add_or_subtract: str
    ) -> str:
        """
        Adds or subtracts months or years to/from an Oracle date column.
        This method constructs the SQL expression to add or subtract months or years from a date column in Oracle.
        Args:
            column_name (str): The name of the date column to which months or years will be added or subtracted.
            years (bool): If True, adds or subtracts years; if False, adds or subtracts months.
            number_to_add_or_subtract (str): The number of months or years to add or subtract, as a string.
        Returns:
            str: The SQL expression to add or subtract months or years from the date column.
        """
        if years:
            number_to_add_or_subtract += " * 12 "
        return f" ADD_MONTHS(TRUNC({column_name}), {number_to_add_or_subtract}) "

    def _subtract_days_from_oracle_date(
        self, column_name: str, number_of_days: str
    ) -> str:
        """
        Subtracts a specified number of days to an Oracle date column.
        This method constructs the SQL expression to subtract days to a date column in Oracle.
        Args:
            column_name (str): The name of the date column to which days will be subtracted.
            number_of_days (str): The number of days to subtract, as a string.
        Returns:
            str: The SQL expression to subtract days to the date column.
        """
        return f" TRUNC({column_name}) - {number_of_days} "

    def _subtract_months_from_oracle_date(
        self, column_name: str, number_of_months: str
    ) -> str:
        """
        Subtracts a specified number of months to an Oracle date column.
        This method constructs the SQL expression to subtract months to a date column in Oracle.
        Args:
            column_name (str): The name of the date column to which months will be subtracted.
            number_of_months (str): The number of months to subtract, as a string.
        Returns:
            str: The SQL expression to subtract months to the date column.
        """
        return self._add_months_or_years_to_oracle_date(
            column_name, False, "-" + number_of_months
        )

    def _subtract_years_from_oracle_date(
        self, column_name: str, number_of_years: str
    ) -> str:
        """
        Subtracts a specified number of years to an Oracle date column.
        This method constructs the SQL expression to subtract years to a date column in Oracle.
        Args:
            column_name (str): The name of the date column to which years will be subtracted.
            number_of_years (str): The number of years to subtract, as a string.
        Returns:
            str: The SQL expression to subtract years to the date column.
        """
        return self._add_months_or_years_to_oracle_date(
            column_name, True, "-" + number_of_years
        )

    def _oracle_to_date_method(self, date: str, format: str) -> str:
        """
        Constructs an Oracle TO_DATE function to convert a string to a date.
        This method formats the date string according to the specified format.
        Args:
            date (str): The date string to be converted.
            format (str): The format in which the date string is provided.
        Returns:
            str: The SQL expression for the Oracle TO_DATE function.
        """
        return f" TO_DATE( '{date}', '{format}') "

    def _add_check_date_is_a_period_ago_or_later(
        self, date_column_name: str, value: str
    ) -> None:
        """
        Adds a condition to the SQL WHERE clause to check if a date column is a certain period ago or later.
        This method constructs the SQL condition to check if the specified date column is a certain number of
        years, months, or days ago or later compared to the current date.
        It extracts the comparator, numerator, denominator, and ago/later from the value string.
        The value string should be in the format of "X years ago", "X months later", etc.
        Args:
            date_column_name (str): The name of the date column to check.
            value (str): The value string specifying the period and direction (ago/later).
        Raises:
            SelectionBuilderException: If the value string does not conform to the expected format.
        """
        criteria_words = value.strip().lower().split()
        comparator, numerator, denominator, ago_or_later = (
            self._extract_date_comparison_components(criteria_words)
        )

        compound = f"{denominator} {ago_or_later}"

        getter_map = {
            "year ago": self._get_x_years_ago,
            "years ago": self._get_x_years_ago,
            "year later": self._get_x_years_later,
            "years later": self._get_x_years_later,
            "month ago": self._get_x_months_ago,
            "months ago": self._get_x_months_ago,
            "month later": self._get_x_months_later,
            "months later": self._get_x_months_later,
            "day ago": self._get_x_days_ago,
            "days ago": self._get_x_days_ago,
            "day later": self._get_x_days_later,
            "days later": self._get_x_days_later,
        }

        if compound in getter_map:
            getter_map[compound](date_column_name, comparator, numerator)

        if comparator == " > ":
            post_condition = " <= " if ago_or_later == "ago" else " > "
            self._add_check_comparing_one_date_with_another(
                date_column_name, post_condition, self._TRUNC_SYSDATE, False
            )

    def _extract_date_comparison_components(
        self, words: list[str]
    ) -> tuple[str, str, str, str]:
        """
        Extracts the comparator, numerator, denominator, and direction (ago/later) from a list of words.
        This method processes the list of words to identify the date comparison components.
        It looks for specific keywords that indicate the direction (ago/later) and the comparison operators (>, <, =, etc.).
        The expected format is "X years ago", "X months later", etc.
        Args:
            words (list[str]): A list of words representing the date comparison criteria.
        Returns:
            tuple[str, str, str, str]: A tuple containing the comparator, numerator, denominator, and direction (ago/later).
        Raises:
            SelectionBuilderException: If the words do not conform to the expected format or if the direction is not recognized.
        """
        value = " ".join(words)
        default_comp = " = "
        mappings = {
            "ago": {
                ">": (" < ", 1),
                ">=": (" <= ", 1),
                "more than": (" < ", 2),
                "<": (" > ", 1),
                "<=": (" >= ", 1),
                "less than": (" > ", 2),
            },
            "later": {
                ">": (" > ", 1),
                ">=": (" >= ", 1),
                "more than": (" > ", 2),
                "<": (" < ", 1),
                "<=": (" <= ", 1),
                "less than": (" < ", 2),
            },
        }

        for direction in ("ago", "later"):
            if words[-1] == direction:
                for prefix, (comp, offset) in mappings[direction].items():
                    if value.startswith(prefix):
                        return comp, words[offset], words[offset + 1], direction
                return default_comp, words[0], words[1], direction

        return default_comp, words[0], words[1], words[-1]

    def _add_criteria_date_field_special_cases(
        self,
        value: str,
        subject: "Subject",
        pathway: str,
        date_type: str,
        date_column_name: str,
    ) -> None:
        """
        Adds criteria for filtering subjects based on specific date fields.
        This method constructs the SQL WHERE clause to filter subjects based on various date fields.
        It resolves the date description from the criteria value and appends the appropriate SQL condition.
        If the date description is not found, it raises a ValueError.
        It handles various date descriptions such as NOT_NULL, NULL, TODAY, TOMORROW,
        YESTERDAY, LAST_BIRTHDAY, CSDD, CSSDD, LAST_BIRTHDAY, and others.
        It also handles date comparisons such as less than, greater than, equal to,
        and within a certain number of months or years.
        Args:
            value (str): The criteria value representing the date description.
            subject (Subject): The subject for which the date criteria is being applied.
            pathway (str): The pathway for which the date criteria is being applied.
            date_type (str): The type of date field being checked (e.g., "FOBTDUE_DATE").
            date_column_name (str): The name of the date column in the SQL query.
        Raises:
            ValueError: If the date description is not found for the given value.
            SelectionBuilderException: If the criteria value does not correspond to a valid date description.
            SelectionBuilderException: If an unexpected error occurs while processing the criteria value.
        """
        try:
            date_to_use = DateDescription.by_description_case_insensitive(value)
            if date_to_use is None:
                raise ValueError(f"No DateDescription found for value: {value}")
            number_of_months = str(date_to_use.number_of_months)

            match date_to_use:
                case DateDescription.NOT_NULL:
                    self._add_check_column_is_null_or_not(date_column_name, False)
                case DateDescription.NULL | DateDescription.UNCHANGED_NULL:
                    self._add_check_column_is_null_or_not(date_column_name, True)
                case DateDescription.LAST_BIRTHDAY:
                    self._add_check_comparing_one_date_with_another(
                        date_column_name,
                        " = ",
                        "pkg_bcss_common.f_get_last_birthday(c.date_of_birth)",
                        False,
                    )
                case (
                    DateDescription.CSDD
                    | DateDescription.CALCULATED_FOBT_DUE_DATE
                    | DateDescription.CALCULATED_SCREENING_DUE_DATE
                ):
                    self._add_check_comparing_one_date_with_another(
                        date_column_name, " = ", "TRUNC(ss.calculated_sdd)", True
                    )
                case DateDescription.CALCULATED_LYNCH_DUE_DATE:
                    self._add_check_comparing_one_date_with_another(
                        date_column_name, " = ", "TRUNC(ss.lynch_calculated_sdd)", True
                    )
                case (
                    DateDescription.CALCULATED_SURVEILLANCE_DUE_DATE
                    | DateDescription.CSSDD
                ):
                    self._add_check_comparing_one_date_with_another(
                        date_column_name, " = ", "TRUNC(ss.calculated_ssdd)", True
                    )
                case DateDescription.LESS_THAN_TODAY | DateDescription.BEFORE_TODAY:
                    self._add_check_comparing_one_date_with_another(
                        date_column_name, " < ", self._TRUNC_SYSDATE, False
                    )
                case DateDescription.GREATER_THAN_TODAY | DateDescription.AFTER_TODAY:
                    self._add_check_comparing_one_date_with_another(
                        date_column_name, " > ", self._TRUNC_SYSDATE, False
                    )
                case DateDescription.TODAY:
                    self._add_check_comparing_one_date_with_another(
                        date_column_name, " = ", self._TRUNC_SYSDATE, False
                    )
                case DateDescription.TOMORROW:
                    self._add_check_comparing_one_date_with_another(
                        date_column_name,
                        " = ",
                        self._add_days_to_oracle_date("SYSDATE", "1"),
                        False,
                    )
                case DateDescription.YESTERDAY:
                    self._add_check_comparing_one_date_with_another(
                        date_column_name,
                        " = ",
                        self._subtract_days_from_oracle_date("SYSDATE", "1"),
                        False,
                    )
                case (
                    DateDescription.LESS_THAN_OR_EQUAL_TO_6_MONTHS_AGO
                    | DateDescription.WITHIN_THE_LAST_2_YEARS
                    | DateDescription.WITHIN_THE_LAST_4_YEARS
                    | DateDescription.WITHIN_THE_LAST_6_MONTHS
                ):
                    self._add_check_comparing_one_date_with_another(
                        self._subtract_months_from_oracle_date(
                            "SYSDATE", number_of_months
                        ),
                        " <= ",
                        date_column_name,
                        False,
                    )
                    self._add_check_comparing_one_date_with_another(
                        date_column_name, " <= ", self._TRUNC_SYSDATE, False
                    )
                case DateDescription.LYNCH_DIAGNOSIS_DATE:
                    self._add_join_to_genetic_condition_diagnosis()
                    self._add_check_comparing_one_date_with_another(
                        date_column_name, " = ", "TRUNC(gcd.diagnosis_date)", True
                    )
                case DateDescription.TWO_YEARS_FROM_LAST_LYNCH_COLONOSCOPY_DATE:
                    self._add_join_to_genetic_condition_diagnosis()
                    self._add_check_comparing_one_date_with_another(
                        date_column_name,
                        " = ",
                        self._add_months_to_oracle_date(
                            "gcd.last_colonoscopy_date", number_of_months
                        ),
                        False,
                    )
                case (
                    DateDescription.ONE_YEAR_FROM_EPISODE_END
                    | DateDescription.TWO_YEARS_FROM_EPISODE_END
                    | DateDescription.THREE_YEARS_FROM_EPISODE_END
                ):
                    self._add_check_comparing_one_date_with_another(
                        date_column_name,
                        " = ",
                        self._add_months_to_oracle_date(
                            "ep.episode_end_date", number_of_months
                        ),
                        False,
                    )
                case (
                    DateDescription.ONE_YEAR_FROM_DIAGNOSTIC_TEST
                    | DateDescription.TWO_YEARS_FROM_DIAGNOSTIC_TEST
                    | DateDescription.THREE_YEARS_FROM_DIAGNOSTIC_TEST
                ):
                    self._add_check_comparing_one_date_with_another(
                        date_column_name,
                        " = ",
                        self._add_months_to_oracle_date(
                            self.xt
                            + str(self.criteria_value_count)
                            + ".confirmed_date",
                            number_of_months,
                        ),
                        False,
                    )
                case (
                    DateDescription.ONE_YEAR_FROM_SYMPTOMATIC_PROCEDURE
                    | DateDescription.TWO_YEARS_FROM_SYMPTOMATIC_PROCEDURE
                    | DateDescription.THREE_YEARS_FROM_SYMPTOMATIC_PROCEDURE
                ):
                    self._add_check_comparing_one_date_with_another(
                        date_column_name,
                        " = ",
                        self._add_months_to_oracle_date(
                            self.xt + str(self.criteria_value_count) + ".surgery_date",
                            number_of_months,
                        ),
                        False,
                    )
                case DateDescription.TWO_YEARS_FROM_EARLIEST_S10_EVENT:
                    self._add_check_comparing_date_with_earliest_or_latest_event_date(
                        date_column_name,
                        " = ",
                        "MIN",
                        EventStatusType.S10,
                        number_of_months,
                    )
                case DateDescription.TWO_YEARS_FROM_LATEST_A37_EVENT:
                    self._add_check_comparing_date_with_earliest_or_latest_event_date(
                        date_column_name,
                        " = ",
                        "MAX",
                        EventStatusType.A37,
                        number_of_months,
                    )
                case DateDescription.TWO_YEARS_FROM_LATEST_J8_EVENT:
                    self._add_check_comparing_date_with_earliest_or_latest_event_date(
                        date_column_name,
                        " = ",
                        "MAX",
                        EventStatusType.J8,
                        number_of_months,
                    )
                case DateDescription.TWO_YEARS_FROM_LATEST_J15_EVENT:
                    self._add_check_comparing_date_with_earliest_or_latest_event_date(
                        date_column_name,
                        " = ",
                        "MAX",
                        EventStatusType.J15,
                        number_of_months,
                    )
                case DateDescription.TWO_YEARS_FROM_LATEST_J16_EVENT:
                    self._add_check_comparing_date_with_earliest_or_latest_event_date(
                        date_column_name,
                        " = ",
                        "MAX",
                        EventStatusType.J16,
                        number_of_months,
                    )
                case DateDescription.TWO_YEARS_FROM_LATEST_J25_EVENT:
                    self._add_check_comparing_date_with_earliest_or_latest_event_date(
                        date_column_name,
                        " = ",
                        "MAX",
                        EventStatusType.J25,
                        number_of_months,
                    )
                case DateDescription.TWO_YEARS_FROM_LATEST_S158_EVENT:
                    self._add_check_comparing_date_with_earliest_or_latest_event_date(
                        date_column_name,
                        " = ",
                        "MAX",
                        EventStatusType.S158,
                        number_of_months,
                    )
                case DateDescription.AS_AT_EPISODE_START:
                    self._add_join_to_latest_episode()
                    self._add_check_comparing_one_date_with_another(
                        date_column_name, " = ", "TRUNC(ep.episode_start_dd)", False
                    )
                case DateDescription.UNCHANGED:
                    existing_due_date_value = self._get_date_field_existing_value(
                        subject, pathway, date_type
                    )
                    if subject is None:
                        raise ValueError("Subject is None")
                    elif existing_due_date_value is None:
                        self._add_check_column_is_null_or_not(date_column_name, True)
                    elif existing_due_date_value == date(1066, 1, 1):
                        raise ValueError(f"{value} date doesn't support 'unchanged'")
                    else:
                        self._add_check_comparing_one_date_with_another(
                            date_column_name,
                            " = ",
                            self._oracle_to_date_method(
                                existing_due_date_value.strftime("%Y-%m-%d"),
                                "yyyy-mm-dd",
                            ),
                            False,
                        )

        except Exception as e:
            raise SelectionBuilderException(
                self.criteria_key_name, self.criteria_value
            ) from e

    def _add_criteria_onward_referral_type(
        self, onward_referral_type_field_name: str
    ) -> None:
        """
        Adds a SQL WHERE clause for the specified onward referral type field based on the criteria value.
        """
        self.sql_where.append(
            f" AND {self.xt}{self.criteria_value_count}.{onward_referral_type_field_name} "
        )
        if self.criteria_value.lower() == "null":
            self.sql_where.append(self._SQL_IS_NULL)
        else:
            try:
                referral_type = (
                    DiagnosticTestReferralType.by_description_case_insensitive(
                        self.criteria_value
                    )
                )
                if referral_type is None:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )
                self.sql_where.append(
                    f" {self.criteria_comparator} {referral_type.get_id()} "
                )
            except Exception:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

    def _add_criteria_onward_referral_reason(
        self, onward_referral_reason_field_name: str
    ) -> None:
        """
        Adds a SQL WHERE clause for the specified onward referral reason field based on the criteria value.
        Appends the clause to self.sql_where. If the criteria value is 'null', checks for NULL in the field.
        Otherwise, matches the field against the valid value ID for the reason.
        """
        self.sql_where.append(
            f" AND {self.xt}{self.criteria_value_count}.{onward_referral_reason_field_name} "
        )
        if self.criteria_value.lower() == "null":
            self.sql_where.append("IS NULL")
        else:
            try:
                referral_reason = (
                    ReasonForOnwardReferralType.by_description_case_insensitive(
                        self.criteria_value
                    )
                )
                if referral_reason is None:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )
                self.sql_where.append(
                    f"{self.criteria_comparator}{referral_reason.get_id()}"
                )
            except Exception:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

    def _add_criteria_symptomatic_referral_reason(self) -> None:
        """
        Adds a SQL WHERE clause for the symptomatic referral reason in the diagnostic test table.
        Appends the clause to self.sql_where. If the criteria value is 'null', checks for NULL in the field.
        Otherwise, matches the field against the valid value ID for the reason.
        """
        self.sql_where.append(
            f" AND {self.xt}{self.criteria_value_count}.complete_reason_id "
        )
        if self.criteria_value.lower() == "null":
            self.sql_where.append("IS NULL")
        else:
            try:
                referral_reason = (
                    ReasonForSymptomaticReferralType.by_description_case_insensitive(
                        self.criteria_value
                    )
                )
                if referral_reason is None:
                    raise SelectionBuilderException(
                        self.criteria_key_name, self.criteria_value
                    )
                self.sql_where.append(
                    f"{self.criteria_comparator}{referral_reason.get_id()}"
                )
            except Exception:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )

    def _add_check_comparing_date_with_earliest_or_latest_event_date(
        self,
        date_column_name: str,
        comparator: str,
        min_or_max: str,
        event: EventStatusType,
        number_of_months: str,
    ) -> None:
        """
        Adds a condition to the SQL WHERE clause to compare a date column with the earliest or latest event date.
        This method constructs the SQL condition to check if the specified date column is either greater than,
        less than, or equal to the earliest or latest event date for a specific event type.
        It uses a subquery to retrieve the earliest or latest event date for the specified event type
        and compares it with the date column.
        Args:
            date_column_name (str): The name of the date column to check.
            comparator (str): The comparator to use for the date comparison (e.g., '=', '!=', '<', '>', '<=', '>=').
            min_or_max (str): Specifies whether to use the minimum or maximum event date ('MIN' or 'MAX').
            event (EventStatusType): The event type for which the earliest or latest date is being checked.
            number_of_months (str): The number of months to add or subtract from the event date.
        Raises:
            SelectionBuilderException: If the event type is not recognized or if an error occurs while constructing the SQL condition.
        This method is used to filter subjects based on their event dates, such as
        checking if a subject's date column is within a certain period relative to the earliest or latest event date.
        It ensures that the SQL query is constructed correctly to retrieve subjects based on their event dates.
        It also handles the addition of months to the event date to allow for flexible date comparisons.
        """

        self._add_join_to_latest_episode()

        alias = event.code.lower()
        subquery = (
            f"(SELECT {self._add_months_to_oracle_date(f'{min_or_max}({alias}.datestamp)', number_of_months)} "
            f"FROM ep_events_t {alias} "
            f"WHERE {alias}.subject_epis_id = ep.subject_epis_id "
            f"AND {alias}.event_status_id = {event.id})"
        )

        self.sql_where.append(f"AND {date_column_name} {comparator} {subquery}")

    def _add_check_column_is_null_or_not(self, column_name: str, is_null: bool) -> None:
        """
        Adds a condition to the SQL WHERE clause to check if a column is NULL or NOT NULL.
        This method constructs the SQL condition to check if the specified column is either NULL or NOT NULL.
        It appends the condition to the SQL WHERE clause based on the is_null parameter.
        Args:
            column_name (str): The name of the column to check for NULL or NOT NULL.
            is_null (bool): If True, checks if the column is NULL; if False, checks if the column is NOT NULL.
        Raises:
            SelectionBuilderException: If an error occurs while constructing the SQL condition.
        This method is used to filter subjects based on whether a specific column has a NULL or NOT NULL value.
        It ensures that the SQL query is constructed correctly to retrieve subjects based on the presence or absence of values in the specified column.
        It appends the appropriate SQL condition to the sql_where list.
        """
        self.sql_where.append(f" AND {column_name} ")
        if is_null:
            self.sql_where.append(self._SQL_IS_NULL)
        else:
            self.sql_where.append(self._SQL_IS_NOT_NULL)

    def _get_date_field_existing_value(
        self, subject: "Subject", pathway: str, date_type: str
    ) -> Optional[date]:
        """
        Returns the existing value of a date field for a subject based on the pathway and date type.
        This method retrieves the date field value from the subject object based on the specified pathway and date type.
        It checks the combination of pathway and date type to determine which date field to return.
        If the combination is not recognized, it returns a default date (1066-01-01).
        Args:
            subject (Subject): The subject object containing the date fields.
            pathway (str): The pathway for which the date field is being checked (e.g., "FOBT", "SURVEILLANCE", "LYNCH").
            date_type (str): The type of date field being checked (e.g., "DUE_DATE", "CALCULATED_DUE_DATE", "DUE_DATE_CHANGE_DATE").
        Returns:
            Optional[date]: The existing date value for the specified pathway and date type, or a default date if the combination is not recognized.
        """
        key = pathway + date_type

        if key == "ALL_PATHWAYS" + "SCREENING_STATUS_CHANGE_DATE":
            return subject.screening_status_change_date
        elif key == "ALL_PATHWAYS" + "DATE_OF_DEATH":
            return subject.date_of_death
        elif key == "FOBT" + "DUE_DATE":
            return subject.screening_due_date
        elif key == "FOBT" + "CALCULATED_DUE_DATE":
            return subject.calculated_screening_due_date
        elif key == "FOBT" + "DUE_DATE_CHANGE_DATE":
            return subject.screening_due_date_change_date
        elif key == "SURVEILLANCE" + "DUE_DATE":
            return subject.surveillance_screening_due_date
        elif key == "SURVEILLANCE" + "CALCULATED_DUE_DATE":
            return subject.calculated_surveillance_due_date
        elif key == "SURVEILLANCE" + "DUE_DATE_CHANGE_DATE":
            return subject.surveillance_due_date_change_date
        elif key == "LYNCH" + "DUE_DATE":
            return subject.lynch_due_date
        elif key == "LYNCH" + "CALCULATED_DUE_DATE":
            return subject.calculated_lynch_due_date
        elif key == "LYNCH" + "DUE_DATE_CHANGE_DATE":
            return subject.lynch_due_date_change_date
        else:
            return date(1066, 1, 1)

    def _get_x_years_ago(
        self, date_column_name: str, comparator: str, numerator: str
    ) -> None:
        """
        Adds a condition to the SQL WHERE clause to check if a date column is a certain number of years ago.
        This method constructs the SQL condition to check if the specified date column is a certain number of
        years ago compared to the current date (SYSDATE).
        Args:
            date_column_name (str): The name of the date column to check.
            comparator (str): The comparator to use for the date comparison (e.g., '=', '!=', '<', '>', '<=', '>=').
            numerator (str): The number of years to check against, as a string.
        Raises:
            SelectionBuilderException: If an error occurs while constructing the SQL condition.
        """
        self._add_check_comparing_one_date_with_another(
            date_column_name,
            comparator,
            self._subtract_years_from_oracle_date("SYSDATE", numerator),
            False,
        )

    def _get_x_months_ago(
        self, date_column_name: str, comparator: str, numerator: str
    ) -> None:
        """
        Adds a condition to the SQL WHERE clause to check if a date column is a certain number of months ago.
        This method constructs the SQL condition to check if the specified date column is a certain number of
        months ago compared to the current date (SYSDATE).
        Args:
            date_column_name (str): The name of the date column to check.
            comparator (str): The comparator to use for the date comparison (e.g., '=', '!=', '<', '>', '<=', '>=').
            numerator (str): The number of months to check against, as a string.
        Raises:
            SelectionBuilderException: If an error occurs while constructing the SQL condition.
        """
        self._add_check_comparing_one_date_with_another(
            date_column_name,
            comparator,
            self._subtract_months_from_oracle_date("SYSDATE", numerator),
            False,
        )

    def _get_x_days_ago(
        self, date_column_name: str, comparator: str, numerator: str
    ) -> None:
        """
        Adds a condition to the SQL WHERE clause to check if a date column is a certain number of days ago.
        This method constructs the SQL condition to check if the specified date column is a certain number of
        days ago compared to the current date (SYSDATE).
        Args:
            date_column_name (str): The name of the date column to check.
            comparator (str): The comparator to use for the date comparison (e.g., '=', '!=', '<', '>', '<=', '>=').
            numerator (str): The number of days to check against, as a string.
        Raises:
            SelectionBuilderException: If an error occurs while constructing the SQL condition.
        """
        self._add_check_comparing_one_date_with_another(
            date_column_name,
            comparator,
            self._subtract_days_from_oracle_date("SYSDATE", numerator),
            False,
        )

    def _get_x_years_later(
        self, date_column_name: str, comparator: str, numerator: str
    ) -> None:
        """
        Adds a condition to the SQL WHERE clause to check if a date column is a certain number of years later.
        This method constructs the SQL condition to check if the specified date column is a certain number of
        years later compared to the current date (SYSDATE).
        Args:
            date_column_name (str): The name of the date column to check.
            comparator (str): The comparator to use for the date comparison (e.g., '=', '!=', '<', '>', '<=', '>=').
            numerator (str): The number of years to check against, as a string.
        Raises:
            SelectionBuilderException: If an error occurs while constructing the SQL condition.
        """
        self._add_check_comparing_one_date_with_another(
            date_column_name,
            comparator,
            self._add_years_to_oracle_date("SYSDATE", numerator),
            False,
        )

    def _get_x_months_later(
        self, date_column_name: str, comparator: str, numerator: str
    ) -> None:
        """
        Adds a condition to the SQL WHERE clause to check if a date column is a certain number of months later.
        This method constructs the SQL condition to check if the specified date column is a certain number of
        months later compared to the current date (SYSDATE).
        Args:
            date_column_name (str): The name of the date column to check.
            comparator (str): The comparator to use for the date comparison (e.g., '=', '!=', '<', '>', '<=', '>=').
            numerator (str): The number of months to check against, as a string.
        Raises:
            SelectionBuilderException: If an error occurs while constructing the SQL condition.
        """
        self._add_check_comparing_one_date_with_another(
            date_column_name,
            comparator,
            self._add_months_to_oracle_date("SYSDATE", numerator),
            False,
        )

    def _get_x_days_later(
        self, date_column_name: str, comparator: str, numerator: str
    ) -> None:
        """
        Adds a condition to the SQL WHERE clause to check if a date column is a certain number of days later.
        This method constructs the SQL condition to check if the specified date column is a certain number of
        days later compared to the current date (SYSDATE).
        Args:
            date_column_name (str): The name of the date column to check.
            comparator (str): The comparator to use for the date comparison (e.g., '=', '!=', '<', '>', '<=', '>=').
            numerator (str): The number of days to check against, as a string.
        Raises:
            SelectionBuilderException: If an error occurs while constructing the SQL condition.
        """
        self._add_check_comparing_one_date_with_another(
            date_column_name,
            comparator,
            self._add_days_to_oracle_date("SYSDATE", numerator),
            False,
        )

    def _nvl_date(self, column_name: str) -> str:
        """
        Returns a SQL NVL expression for a date column.
        This method constructs a SQL NVL expression for the specified date column.
        """
        if "SYSDATE" in column_name.upper():
            return_value = " " + column_name + " "
        else:
            return_value = (
                " NVL(" + column_name + ", TO_DATE('01/01/1066', 'dd/mm/yyyy')) "
            )
        return return_value

    def _is_valid_date(self, value: str, date_format: str = "%Y-%m-%d") -> bool:
        """
        Checks if the date is valid.
        Args:
            value (str): The date as a tring
            date_format (str): The format of the date. Default is "%Y-%m-%d"
        Returns
            bool: True is the date is valid, False if it is not
        """
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            return False

    def _get_notify_message_event_status_id_from_criteria(self) -> Optional[int]:
        """
        Get the event status ID from the notify message criteria.
        Returns:
            Optional[int]: The event status ID if found, None otherwise.
        """
        if " " in self.criteria_value:
            notify_message_criteria = self.criteria_value.split(" ")
            message_type = NotifyMessageType.by_description_case_insensitive(
                notify_message_criteria[0]
            )
            if message_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            return message_type.event_status_id
        return None

    def _get_notify_message_code_from_criteria(self) -> Optional[str]:
        """
        Get the message code from the notify message criteria.
        Returns:
            Optional[str]: The message code if found, None otherwise.
        """
        if "(" in self.criteria_value:
            notify_message_criteria = self.criteria_value.split("(")
            notify_message_codes = notify_message_criteria[1].split(")")
            message_type = NotifyMessageType.by_description_case_insensitive(
                notify_message_codes[0]
            )
            if message_type is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            return message_type.description
        return None

    def _get_notify_message_status_from_criteria(self) -> Optional[NotifyMessageStatus]:
        """
        Get the message status from the notify message criteria.
        Returns:
            Optional[NotifyMessageStatus]: The message status if found, None otherwise.
        """
        if " - " in self.criteria_value:
            notify_message_criteria = self.criteria_value.split(" - ")
            message_status = NotifyMessageStatus.by_description_case_insensitive(
                notify_message_criteria[1]
            )
            if message_status is None:
                raise SelectionBuilderException(
                    self.criteria_key_name, self.criteria_value
                )
            return message_status
        return None

    @staticmethod
    def single_quoted(value: str) -> str:
        """
        Returns the value surrounded by single quotes
        """
        return f"'{value}'"

    @staticmethod
    def invalid_use_of_unchanged_exception(criteria_key_name: str, reason: str):
        """
        Raises a SelectionBuilderException
        """
        return SelectionBuilderException(
            f"Invalid use of 'unchanged' criteria value ({reason}) for: {criteria_key_name}"
        )

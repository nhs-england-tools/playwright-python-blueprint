from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from datetime import datetime
from classes.kits.kit_service_management_record import KitServiceManagementRecord


@dataclass
class KitServiceManagementEntity:
    """
    Data class representing a kit service management entity (KIT_QUEUE table).
    """

    device_id: Optional[str] = None
    test_kit_type: Optional[str] = None
    test_kit_name: Optional[str] = None
    test_kit_status: Optional[str] = None
    logged_by_hub: Optional[str] = None
    date_time_logged: Optional[datetime] = None
    test_result: Optional[Decimal] = None
    calculated_result: Optional[str] = None
    error_code: Optional[int] = None
    analyser_code: Optional[str] = None
    date_time_authorised: Optional[datetime] = None
    authoriser_user_code: Optional[str] = None
    datestamp: Optional[datetime] = None
    bcss_error_id: Optional[int] = None
    post_response: Optional[int] = None
    post_attempts: Optional[int] = None
    put_response: Optional[int] = None
    put_attempts: Optional[int] = None
    date_time_error_archived: Optional[datetime] = None
    error_archived_user_code: Optional[str] = None
    issue_date: Optional[datetime] = None
    issued_by_hub: Optional[str] = None
    nhs_number: Optional[str] = None
    analyser_error_description: Optional[str] = None
    error_type: Optional[str] = None
    screening_test_result: Optional[str] = None

    @staticmethod
    def from_record(
        record: "KitServiceManagementRecord",
    ) -> "KitServiceManagementEntity":
        """
        Converts a KitServiceManagementRecord object into a KitServiceManagementEntity object.

        Args:
            record (KitServiceManagementRecord): The record to convert.

        Returns:
            KitServiceManagementEntity: The converted entity.
        """
        return KitServiceManagementEntity(
            device_id=record.device_id,
            test_kit_type=(
                str(record.test_kit_type) if record.test_kit_type is not None else None
            ),  # test_kit_type is converted to a string as this is what is required in the database
            test_kit_name=record.test_kit_name,
            test_kit_status=record.test_kit_status,
            logged_by_hub=record.logged_by_hub,
            date_time_logged=record.date_time_logged,
            test_result=record.test_result,
            calculated_result=record.calculated_result,
            error_code=record.error_code,
            analyser_code=record.analyser_code,
            date_time_authorised=record.date_time_authorised,
            authoriser_user_code=record.authoriser_user_code,
            datestamp=record.datestamp,
            bcss_error_id=record.bcss_error_id,
            post_response=record.post_response,
            post_attempts=record.post_attempts,
            put_response=record.put_response,
            put_attempts=record.put_attempts,
            date_time_error_archived=record.date_time_error_archived,
            error_archived_user_code=record.error_archived_user_code,
            issue_date=record.date_time_issued,
            issued_by_hub=record.issued_by_hub,
            nhs_number=record.nhs_number,
            analyser_error_description=record.analyser_error_description,
            error_type=record.error_type,
            screening_test_result=record.screening_test_result,
        )

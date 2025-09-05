import logging
from typing import Optional
from utils.oracle.oracle import OracleDB
from classes.kit_service_management_record import KitServiceManagementRecord
from classes.entities.kit_service_management_entity import KitServiceManagementEntity


class KitServiceManagementRepository:
    """
    Repository for managing kit service management records.
    """

    def __init__(self):
        self.oracle_db = OracleDB()

    def _device_filter(self, device_id: Optional[str]) -> list[str]:
        """
        Adds a filter on device ID for the 'get_service_management_sql' method
        Args:
            device_id (str): The device ID of the subject
        Returns:
            list[str]: A filter for device_id if it is provided, otherwise it returns an empty list
        """
        return ["AND kq.device_id = :device_id"] if device_id else []

    def _archived_filter(self, archived: Optional[bool]) -> list[str]:
        """
        Adds a filter on date_time_error_archived for the 'get_service_management_sql' method
        Args:
            archived (bool): Whether to include archived records
        Returns:
            list[str]: An SQL filter clause to include or exclude archived records based on the archived flag.
        """
        if archived is None:
            return []
        return [f"AND kq.date_time_error_archived IS {'NOT ' if archived else ''}NULL"]

    def _hub_filter(self, issuing_hub_id: int, logged_hub_id: int) -> list[str]:
        """
        Adds a filter on hubs for the 'get_service_management_sql' method
        Args:
            issuing_hub_id (int): The ID of the issuing hub
            logged_hub_id (int): The ID of the logged hub
        Returns:
            list[str]: An SQL filter clause for the hubs
        """
        hub_conditions = []
        if logged_hub_id > -1:
            hub_conditions.append("lo.org_id = :logged_hub_id")
        if issuing_hub_id > -1:
            hub_conditions.append("ep.start_hub_id = :issuing_hub_id")
        return [f"AND ({' OR '.join(hub_conditions)})"] if hub_conditions else []

    def _status_filter(
        self, status: Optional[str], if_error_has_id: Optional[bool]
    ) -> list[str]:
        """
        Adds a filter on statuses for the 'get_service_management_sql' method
        Args:
            status (str): The status of the test kit
            if_error_has_id (bool): Whether to include records with an error ID
        Returns:
            list[str]: An SQL filter clause for the statuses
        """
        if not status:
            error_status = [
                "AND (kq.test_kit_status = 'COMPLETE' OR (kq.test_kit_status = 'ERROR'"
            ]
            if if_error_has_id is not None:
                error_status.append(
                    f"AND kq.bcss_error_id IS {'NOT ' if if_error_has_id else ''}NULL"
                )
            error_status.append("))")
            return [" ".join(error_status)]
        status_upper = status.upper()
        if status_upper == "ERROR":
            filters = ["AND kq.test_kit_status = 'ERROR'"]
            if if_error_has_id is not None:
                filters.append(
                    f"AND kq.bcss_error_id IS {'NOT ' if if_error_has_id else ''}NULL"
                )
            return filters
        return [f"AND kq.test_kit_status = '{status_upper}'"]

    def _order_by(self, device_id: Optional[str], order_by_column: str) -> list[str]:
        """
        Returns an order by for the column specified
        Args:
            device_id (str): The device ID of the subject
            order_by_column (str): The column to order by
        Returns:
            list[str]: An order by clause for the specified column
        """
        return [f"ORDER BY {order_by_column} DESC NULLS LAST"] if not device_id else []

    def get_service_management_sql(
        self,
        device_id: Optional[str],
        archived: Optional[bool],
        issuing_hub_id: int,
        logged_hub_id: int,
        status: Optional[str],
        if_error_has_id: Optional[bool],
        order_by_column: str,
    ) -> str:
        """
        Constructs the SQL query for kit service management records.
        Args:
            device_id (str): The device ID of the subject
            archived (bool): Whether to include archived records
            issuing_hub_id (int): The ID of the issuing hub
            logged_hub_id (int): The ID of the logged hub
            status (str): The status of the test kit
            if_error_has_id (bool): Whether to include records with an error ID
            order_by_column (str): The column to order by
        Returns:
            str: The SQL query for kit service management records
        """
        base_sql = """
        SELECT kq.device_id, kq.test_kit_name, kq.test_kit_type, kq.test_kit_status,
            CASE WHEN tki.logged_in_flag = 'Y' THEN kq.logged_by_hub END as logged_by_hub,
            CASE WHEN tki.logged_in_flag = 'Y' THEN kq.date_time_logged END as date_time_logged,
            tki.logged_in_on AS tk_logged_date_time,
            kq.test_result, kq.calculated_result, kq.error_code,
            (SELECT vvt.description FROM tk_analyser_t tka INNER JOIN tk_analyser_type_error tkate ON tkate.tk_analyser_type_id = tka.tk_analyser_type_id INNER JOIN valid_values vvt ON tkate.tk_analyser_error_type_id = vvt.valid_value_id WHERE tka.analyser_code = kq.analyser_code AND tkate.error_code = kq.error_code) AS analyser_error_description,
            kq.analyser_code, kq.date_time_authorised, kq.authoriser_user_code, kq.datestamp, kq.bcss_error_id,
            REPLACE (mt.description, 'ERROR - ', '') AS error_type, NVL(mta.allowed_value, 'N') AS error_ok_to_archive,
            kq.post_response, kq.post_attempts, kq.put_response, kq.put_attempts, kq.date_time_error_archived, kq.error_archived_user_code,
            sst.screening_subject_id, sst.subject_nhs_number, tki.test_results, tki.issue_date, o.org_code AS issued_by_hub
        FROM kit_queue kq
        LEFT OUTER JOIN tk_items_t tki ON tki.device_id = kq.device_id OR (tki.device_id IS NULL AND tki.kitid = pkg_test_kit.f_get_kit_id_from_device_id (kq.device_id))
        LEFT OUTER JOIN screening_subject_t sst ON sst.screening_subject_id = tki.screening_subject_id
        LEFT OUTER JOIN ep_subject_episode_t ep ON ep.subject_epis_id = tki.subject_epis_id
        LEFT OUTER JOIN message_types mt ON kq.bcss_error_id = mt.message_type_id
        LEFT OUTER JOIN valid_values mta ON mta.valid_value_id = mt.message_attribute_id AND mta.valid_value_id = 305482
        LEFT OUTER JOIN ORG o ON ep.start_hub_id = o.org_id
        LEFT OUTER JOIN ORG lo ON lo.org_code = kq.logged_by_hub
        WHERE kq.test_kit_type = 'FIT'
        """

        filters = []
        filters += self._device_filter(device_id)
        if not device_id:
            filters += self._archived_filter(archived)
            filters += self._hub_filter(issuing_hub_id, logged_hub_id)
            filters += self._status_filter(status, if_error_has_id)
            filters += self._order_by(device_id, order_by_column)

        return base_sql + "\n" + "\n".join(filters)

    def get_service_management(
        self,
        device_id: Optional[str],
        issuing_hub_id: int,
        logged_hub_id: int,
        status: Optional[str],
        archived: Optional[bool],
        if_error_has_id: Optional[bool],
        order_by_column: str,
    ) -> KitServiceManagementRecord:
        """
        Gets kit service management records based on the provided filters.
        Args:
            device_id (str): The device ID of the subject
            issuing_hub_id (int): The ID of the issuing hub
            logged_hub_id (int): The ID of the logged hub
            status (str): The status of the test kit
            archived (bool): Whether to include archived records
            if_error_has_id (bool): Whether to include records with an error ID
            order_by_column (str): The column to order by
        Returns:
            KitServiceManagementRecord: The populated kit service management record object
        """
        logging.debug("begin KitServiceManagementRepository.get_service_management")
        sql = self.get_service_management_sql(
            device_id,
            archived,
            issuing_hub_id,
            logged_hub_id,
            status,
            if_error_has_id,
            order_by_column,
        )
        params = {}
        if device_id:
            params["device_id"] = device_id
        else:
            if issuing_hub_id > -1:
                params["issuing_hub_id"] = issuing_hub_id
            if logged_hub_id > -1:
                params["logged_hub_id"] = logged_hub_id
        df = self.oracle_db.execute_query(sql, params)
        return KitServiceManagementRecord().from_dataframe_row(df.iloc[0])

    def get_service_management_by_device_id(
        self, device_id: str
    ) -> KitServiceManagementRecord:
        """
        Gets the kit service management record for the specified device ID.
        Args:
            device_id (str): The device ID of the subject
        Returns:
            KitServiceManagementRecord: The populated kit service management record object
        """
        logging.debug(
            "start: KitServiceManagementRepository.get_service_management_by_device_id"
        )
        kit_queue_record = self.get_service_management(
            device_id=device_id,
            issuing_hub_id=-1,
            logged_hub_id=-1,
            status="",
            archived=None,
            if_error_has_id=None,
            order_by_column="date_time_logged",
        )
        logging.debug(
            "exit: KitServiceManagementRepository.get_service_management_by_device_id"
        )
        return kit_queue_record

    def update_kit_service_management_record(
        self, record: KitServiceManagementRecord
    ) -> None:
        """
        Updates a kit service management record in the database.
        Args:
            record (KitServiceManagementRecord): The record to update.
        """
        entity = KitServiceManagementEntity().from_record(record)
        self.update_kit_service_management_entity(entity)

    def update_kit_service_management_entity(
        self, entity: KitServiceManagementEntity
    ) -> None:
        """
        Updates a kit service management entity in the database.
        Args:
            entity (KitServiceManagementEntity): The entity to update.
        """

        try:
            sql_query = f"""
            UPDATE kit_queue kq SET
                kq.test_kit_name = :test_kit_name,
                kq.test_kit_type = :test_kit_type,
                kq.test_kit_status = :test_kit_status,
                kq.logged_by_hub = :logged_by_hub,
                kq.date_time_logged = :date_time_logged,
                kq.test_result = {'null' if entity.test_result is None else ':test_result'},
                kq.error_code = {'null' if entity.error_code is None else ':error_code'},
                kq.analyser_code = :analyser_code,
                kq.date_time_authorised = :date_time_authorised,
                kq.authoriser_user_code = :authoriser_user_code,
                kq.post_response = {'null' if entity.post_response is None else ':post_response'},
                kq.post_attempts = {'null' if entity.post_attempts is None else ':post_attempts'},
                kq.put_response = {'null' if entity.put_response is None else ':put_response'},
                kq.put_attempts = {'null' if entity.put_attempts is None else ':put_attempts'},
                kq.datestamp = SYSTIMESTAMP
            WHERE kq.device_id = :device_id
            """

            params = {
                "device_id": entity.device_id,
                "test_kit_name": entity.test_kit_name,
                "test_kit_type": entity.test_kit_type,
                "test_kit_status": entity.test_kit_status,
                "logged_by_hub": entity.logged_by_hub,
                "date_time_logged": entity.date_time_logged,
                "analyser_code": entity.analyser_code,
                "date_time_authorised": entity.date_time_authorised,
                "authoriser_user_code": entity.authoriser_user_code,
            }
            if entity.test_result is not None:
                params["test_result"] = entity.test_result
            if entity.error_code is not None:
                params["error_code"] = entity.error_code
            if entity.post_response is not None:
                params["post_response"] = entity.post_response
            if entity.post_attempts is not None:
                params["post_attempts"] = entity.post_attempts
            if entity.put_response is not None:
                params["put_response"] = entity.put_response
            if entity.put_attempts is not None:
                params["put_attempts"] = entity.put_attempts

            self.oracle_db.update_or_insert_data_to_table(sql_query, params)
        except Exception as ex:
            raise RuntimeError(f"Error updating KIT_QUEUE record: {ex}")

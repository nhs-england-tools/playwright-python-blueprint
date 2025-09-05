import logging
from utils.oracle.oracle import OracleDB
from classes.user_role_type import UserRoleType
import pandas as pd


class UserRepository:
    """
    Repository class handling database access for users.
    """

    def __init__(self):
        self.oracle_db = OracleDB()
        self.empty_dataframe_string = (
            "Error executing database transition, dataframe is empty"
        )

    def general_query(self, role: "UserRoleType") -> pd.DataFrame:
        """
        Gets the pio_id, org_id, role_id and org_code of a user
        Args:
            role (UserRoleType): A UserRoleType object containing the necessary information to run the query
        Returns:
            pd.DataFrame: A dataframe containing the pio_id, org_id, role_id and org_code of a user
        Raises:
            ValueError: If no user data is returned from the query / the dataframe is empty
        """
        sql = """
            SELECT
                pio.pio_id,
                pio.org_id,
                pio.role_id,
                pio.org_code
            FROM person_in_org pio
            INNER JOIN person prs ON prs.prs_id = pio.prs_id
            INNER JOIN org ON org.org_id = pio.org_id
            WHERE prs.oe_user_code = :user_code
            AND org.org_code = :org_code
            AND pio.role_id = :role_id
            AND pio.is_bcss_user = 1
            AND TRUNC(SYSDATE) BETWEEN TRUNC(pio.start_date) AND NVL(pio.end_date, SYSDATE)
        """
        params = {
            "user_code": role.user_code,
            "org_code": role.org_code,
            "role_id": role.role_id,
        }
        df = self.oracle_db.execute_query(sql, params)
        if df.empty:
            raise ValueError(self.empty_dataframe_string)
        return df

    def get_pio_id_for_role(self, role: "UserRoleType") -> int:
        """
        Get the PIO ID for the role.

        Args:
            role (UserRoleType): A UserRoleType object containing the necessary information to run the query

        Returns:
            int: The pio_id of the user
        """
        logging.debug(f"Getting PIO ID for role: {role.user_code}")

        df = self.general_query(role)
        return int(df["pio_id"].iloc[0])

    def get_org_id_for_role(self, role: "UserRoleType") -> int:
        """
        Get the ORG ID for the role.

        Args:
            role (UserRoleType): A UserRoleType object containing the necessary information to run the query

        Returns:
            int: The org_id of the user
        """
        logging.debug(f"Getting ORG ID for role: {role.user_code}")

        df = self.general_query(role)
        return int(df["org_id"].iloc[0])

    def get_role_id_for_role(self, role: "UserRoleType") -> int:
        """
        Get the ROLE ID for the role.

        Args:
            role (UserRoleType): A UserRoleType object containing the necessary information to run the query

        Returns:
            int: The role_id of the user
        """
        logging.debug(f"Getting ROLE ID for role: {role.user_code}")

        df = self.general_query(role)
        return int(df["role_id"].iloc[0])

    def get_org_code_for_role(self, role: "UserRoleType") -> int:
        """
        Get the ORG CODE for the role.

        Args:
            role (UserRoleType): A UserRoleType object containing the necessary information to run the query

        Returns:
            int: The org_code of the user
        """
        logging.debug(f"Getting ORG CODE for role: {role.user_code}")

        df = self.general_query(role)
        return int(df["org_code"].iloc[0])

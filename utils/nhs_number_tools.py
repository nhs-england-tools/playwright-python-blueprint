import logging
import random

logger = logging.getLogger(__name__)


class NHSNumberTools:
    """
    A utility class providing functionality around NHS numbers.
    """

    @staticmethod
    def _nhs_number_checks(nhs_number: str) -> None:
        """
        This will validate that the provided NHS number is numeric and exactly 10 digits long.

        Args:
            nhs_number (str): The NHS number to validate.

        Raises:
            NHSNumberToolsException: If the NHS number is not numeric or not 10 digits long.

        Returns:
            None
        """
        if not nhs_number.isnumeric():
            raise NHSNumberToolsException(
                "The NHS number provided ({}) is not numeric.".format(nhs_number)
            )
        if len(nhs_number) != 10:
            raise NHSNumberToolsException(
                "The NHS number provided ({}) is not 10 digits.".format(nhs_number)
            )

    @staticmethod
    def spaced_nhs_number(nhs_number: int | str) -> str:
        """
        This will space out a provided NHS number in the format: nnn nnn nnnn.

        Args:
            nhs_number (int | str): The NHS number to space out.

        Returns:
            str: The NHS number in "nnn nnn nnnn" format.
        """
        formatted_nhs_number = str(nhs_number).replace(" ", "")
        NHSNumberTools._nhs_number_checks(formatted_nhs_number)

        return f"{formatted_nhs_number[:3]} {formatted_nhs_number[3:6]} {formatted_nhs_number[6:]}"

    @staticmethod
    def generate_random_nhs_number() -> str:
        """
        Generates a random NHS number
        Returns:
            str: The generated NHS number
        """
        logging.info("generateRandomNHSNumber: start")
        nhs_number_base = 900000000
        nhs_number_range = 100000000
        while True:
            nhs_number = str(
                nhs_number_base + random.Random().randint(0, nhs_number_range - 1)
            )
            if NHSNumberTools.is_valid_nhs_number(nhs_number):
                break
        nhs_number += str(NHSNumberTools.calculate_nhs_number_checksum(nhs_number))
        logging.info("generateRandomNHSNumber: end")
        return nhs_number

    @staticmethod
    def is_valid_nhs_number(nhs_number: str) -> bool:
        """
        Checks if the NHS number is valid
        Returns:
            bool: True if it is valid, False if it is not
        """
        return len(nhs_number) == 9 and nhs_number.isdigit()

    @staticmethod
    def calculate_nhs_number_checksum(nhs_number: str) -> int:
        """
        Calculates the NHS number checksum
        Returns:
            int: the checksum of the NHS number
        """
        digits = [int(d) for d in nhs_number]
        total = sum((10 - i) * digits[i] for i in range(9))
        remainder = total % 11
        checksum = 11 - remainder
        if checksum == 11:
            checksum = 0
        return checksum


class NHSNumberToolsException(Exception):
    pass

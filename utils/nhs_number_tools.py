import logging

logger = logging.getLogger(__name__)


class NHSNumberTools:
    """
    A utility class providing functionality around NHS numbers.
    """

    @staticmethod
    def _nhs_number_checks(nhs_number: str) -> None:
        """
        This does basic checks on NHS number values provided and raises an exception if the number is not valid.

        Args:
            nhs_number (str): The NHS number to check.
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


class NHSNumberToolsException(Exception):
    pass

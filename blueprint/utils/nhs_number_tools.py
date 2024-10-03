import logging
logger = logging.getLogger(__name__)

class NHSNumberTools:
    """
    A utility class providing functionality around NHS numbers.
    """
    def _nhs_number_checks(self, nhs_number: str) -> None:
        """
        This does basic checks on NHS number values provided and outputs information or exceptions if applicable.

        Args:
            nhs_number (str): The NHS number to check.
        """
        if not nhs_number.isnumeric():
            raise Exception("The NHS number provided ({}) is not numeric.".format(nhs_number))


    def spaced_nhs_number(self, nhs_number: int | str) -> str:
        """
        This will space out a provided NHS number in the format nnn nnn nnnn.

        Args:
            nhs_number (int | str): The NHS number to space out.

        Returns:
            str: The NHS number in "nnn nnn nnnn" format.
        """
        self._nhs_number_checks(str(nhs_number))
        return "{} {} {}".format(str(nhs_number)[:3], str(nhs_number)[3:6], str(nhs_number)[6:])

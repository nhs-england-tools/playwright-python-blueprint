class NHSNumberTools:
    """
    A utility class providing functionality around NHS numbers.
    """

    def spaced_nhs_number(self, nhs_number: int | str) -> str:
        """
        This will space out a provided NHS number in the format nnn nnn nnnn.

        Args:
            nhs_number (int | str): The NHS number to space out.
        
        Returns:
            str: The NHS number in "nnn nnn nnnn" format.
        """
        return "{} {} {}".format(str(nhs_number)[:3], str(nhs_number)[3:6], str(nhs_number)[6:])

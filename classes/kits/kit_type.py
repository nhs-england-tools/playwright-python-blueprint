from enum import Enum


class KitType(Enum):
    """
    Enum representing kit types.
    """

    ANY = 0
    GFOBT = 1
    FIT = 2
    QC = 999

    @property
    def id(self) -> int:
        """
        Returns the kit type ID.
        """
        return self.value

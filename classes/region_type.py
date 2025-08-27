from typing import Optional


class RegionType:
    """
    Represents a region type for BCSS, such as England, Isle of Man, Middleware, or Undefined.
    Each region has a display name and a persistence unit name.
    """

    ENGLAND = ("National", "bcss-england")
    ISLE_OF_MAN = ("Isle of Man", "bcss-iom")
    MIDDLEWARE = ("H2 Middleware", "h2-middleware")
    UNDEFINED = ("Undefined", None)

    def __init__(self, region_name: str, persistence_unit_name: Optional[str]) -> None:
        self._region_name = region_name
        self._persistence_unit_name = persistence_unit_name

    @property
    def region_name(self) -> str:
        """
        Returns the display name of the region.
        """
        return self._region_name

    @property
    def persistence_unit_name(self) -> Optional[str]:
        """
        Returns the persistence unit name for the region.
        """
        return self._persistence_unit_name

    @classmethod
    def get_region(cls, region: str) -> "RegionType":
        """
        Factory method to get a RegionType instance by region string.
        Returns:
            RegionType: The corresponding RegionType instance. By default returns UNDEFINED.
        """
        mapping = {
            "England": cls(*cls.ENGLAND),
            "IsleOfMan": cls(*cls.ISLE_OF_MAN),
            "Middleware": cls(*cls.MIDDLEWARE),
            "Undefined": cls(*cls.UNDEFINED),
        }
        return mapping.get(region, cls(*cls.UNDEFINED))

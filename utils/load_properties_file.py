from jproperties import Properties
import os


class PropertiesFile:
    def __init__(self):
        self.smokescreen_properties_file = (
            "tests/smokescreen/bcss_smokescreen_tests.properties"
        )
        self.general_properties_file = "tests/bcss_tests.properties"

    def get_properties(self, type_of_properties_file: str | None = None) -> dict:
        """
        Reads the 'bcss_smokescreen_tests.properties' file or 'bcss_tests.properties' and populates a 'Properties' object depending on whether "smokescreen" is given
        Returns a dictionary of properties for use in tests.

        Args:
            type_of_properties_file (str): The type of properties file you want to load. e.g. 'smokescreen' or 'general'

        Returns:
            dict: A dictionary containing the values loaded from the 'bcss_smokescreen_tests.properties' file.
        """
        configs = Properties()
        path = f"{os.getcwd()}/{self.smokescreen_properties_file if type_of_properties_file == "smokescreen" else self.general_properties_file}"
        with open(path, "rb") as read_prop:
            configs.load(read_prop)
        return configs.properties

    def get_smokescreen_properties(self) -> dict:
        """
        This is used to get the `tests/smokescreen/bcss_smokescreen_tests.properties` file

        Returns:
            dict: A dictionary containing the values loaded from the 'bcss_smokescreen_tests.properties' file.
        """
        return self.get_properties("smokescreen")

    def get_general_properties(self) -> dict:
        """
        This is used to get the `tests/bcss_tests.properties` file

        Returns:
            dict: A dictionary containing the values loaded from the 'bcss_smokescreen_tests.properties' file.
        """
        return self.get_properties()

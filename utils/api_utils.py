import logging
import json

logger = logging.getLogger(__name__)
from playwright.sync_api import BrowserContext, Page, expect


class ApiUtils:
    """
    A utility class providing functionality for making API requests.
    """

    def __init__(self, api_session: BrowserContext, api_to_call: str) -> None:
        self.api_session = api_session
        self.api_to_call = api_to_call

    def get_request(self, parameters: dict, result_ok: bool = True) -> dict | int:
        """
        This will send a Get request using the parameters specified.

        Args:
            parameters (dict): The parameters to give to the Get request.
            result_ok (bool): Expect the result to be successful, if True.

        Returns:
            dict or int: A dictionary representation of the API response or the error code if response is not okay.

        """
        result = self.api_session.request.get(self.api_to_call, params=parameters)
        assert result.ok == result_ok
        return json.loads(result.body()) if result.ok else result.status

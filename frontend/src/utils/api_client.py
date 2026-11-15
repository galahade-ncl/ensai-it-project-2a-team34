import logging
import os

import requests
import streamlit as st

DEFAULT_TIMEOUT = int(os.getenv("BACKEND_TIMEOUT", 5))
API_URL = os.getenv("BACKEND_URL", "http://localhost:5000")


class APIClient:
    """A client for making authenticated HTTP requests to a backend API.

    Attributes:
        base_url (str): The base URL of the API.
        timeout (int): Default timeout for requests in seconds.
        session (requests.Session): The requests session used for connection pooling.
    """

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _get_headers(self) -> dict:
        """Generates headers, including the authentication token if present.

        Returns:
            dict: A dictionary containing the request headers.
        """
        headers = {}
        # Retrieve the token stored in Streamlit's session_state
        token = st.session_state.get("access_token")
        if token:
            headers["X-Auth-Token"] = token
        return headers

    def _request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        logger = st.session_state.get("logger") or logging.getLogger(__name__)
        logger.info(f"  {method} {url}")

        sensitive = kwargs.pop("sensitive", False)  # True: do not log the response body
        headers = kwargs.pop("headers", {})
        headers.update(self._get_headers())
        timeout = kwargs.pop("timeout", self.timeout)

        try:
            response = self.session.request(
                method=method, url=url, timeout=timeout, headers=headers, **kwargs
            )

            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                data = response.json()
            elif content_type.startswith(("application/pdf", "application/octet-stream")):
                data = None  # binary content: use "content"
            else:
                data = response.text

            return {"status_code": response.status_code, "data": data, "content": response.content}

        except requests.exceptions.Timeout:
            return {"status_code": 0, "data": "Timeout", "content": b""}
        except requests.exceptions.ConnectionError:
            return {"status_code": 0, "data": "Connection error", "content": b""}
        except requests.exceptions.RequestException as e:
            return {"status_code": 0, "data": str(e), "content": b""}
        finally:
            if "response" in locals():
                logger.info(f"  {response.status_code} {response.reason}")
                if not sensitive:
                    logger.debug(f"  {data}")

    def get(self, path: str, params=None, **kwargs):
        """Sends a GET request.
        Args:
            path (str): The endpoint path.
            params (dict, optional): Query parameters.
            **kwargs: Additional arguments for requests.request.
        Returns:
            dict: The response dictionary.
        """
        return self._request(method="GET", path=path, params=params, **kwargs)

    def post(self, path: str, json=None, data=None, **kwargs):
        """Sends a POST request.
        Args:
            path (str): The endpoint path.
            json (dict, optional): JSON body for the request.
            data (dict/bytes, optional): Form data or raw body.
            **kwargs: Additional arguments for requests.request.
        Returns:
            dict: The response dictionary.
        """
        return self._request(method="POST", path=path, json=json, data=data, **kwargs)

    def put(self, path: str, json=None, data=None, **kwargs):
        """Sends a PUT request.
        Args:
            path (str): The endpoint path.
            json (dict, optional): JSON body for the request.
            data (dict/bytes, optional): Form data or raw body.
            **kwargs: Additional arguments for requests.request.
        Returns:
            dict: The response dictionary.
        """
        return self._request(method="PUT", path=path, json=json, data=data, **kwargs)

    def delete(self, path: str, **kwargs):
        """Sends a DELETE request.
        Args:
            path (str): The endpoint path.
            **kwargs: Additional arguments for requests.request.
        Returns:
            dict: The response dictionary.
        """
        return self._request(method="DELETE", path=path, **kwargs)


api_client = APIClient(API_URL)

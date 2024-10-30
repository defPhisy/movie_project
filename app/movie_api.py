import os

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()
API_KEY = os.getenv("API_KEY")


def request_for_movie(title: str):
    """
    Send a GET request with a movie title to www.omdbapi.com with authorization
    and retry logic.

    Args:
        title (str): The movie to search for.

    Returns:
        dict: The JSON response from the server.

    Raises:
        HTTPError: If an HTTP error occurs and retries are exhausted.
        Timeout: If the request times out and retries are exhausted.
    """

    url = "http://www.omdbapi.com/?"
    headers = {"Content-Type": "application/json"}
    params = {"apikey": API_KEY, "t": title}
    timeout = 5

    # Configure retries with exponential backoff
    retries = Retry(
        total=3,  # Total number of retries
        backoff_factor=1,  # Wait time between retries: 1 second, 2 seconds, 4 seconds
        status_forcelist=[
            429,
            500,
            502,
            503,
            504,
        ],  # Retry on specific status codes
    )

    # Set up the HTTPAdapter with retry configuration
    adapter = HTTPAdapter(max_retries=retries)

    # Use requests.Session() to apply retries
    with requests.Session() as session:
        session.mount("https://", adapter)
        response = session.get(
            url, headers=headers, params=params, timeout=timeout
        )
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return response.json()

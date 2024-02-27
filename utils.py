import requests
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout
from typing import Optional
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class UtilRequests:
    def __init__(self):
        # Chrome configuration
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )
        self.driver = None

    def open(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options,
        )

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_page_selenium(self, url: str) -> requests.Response:

        try:
            self.driver.get(url)
        except (RequestException, ConnectionError, HTTPError, Timeout):
            return None
    def get_response(self,url):
        return requests.get(url)
    def read_response(self, response: requests.Response) -> str:
        """Obtain html from a response object.

        Args:
            response (requests.Response): Response object.

        Returns:
            str: Raw html.
        """
        return response.content

    def get_request_url(self, request: requests.Request) -> str:
        """Obtain url by a request object.

        Args:
            request (requests.Request): Reques object.

        Returns:
            str: Url made by the request object.
        """
        return requests.__url__


class UtilURL:
    def __init__(self):
        self.request_service = UtilRequests()

    def is_absolute_url(self, url: str) -> bool:
        """Validate if url is absolute or not

        Args:
            url (str): Url to be validated.

        Returns:
            bool: True if is absolute, False if not.
        """
        if "http" in url or "https" in url:
            return True
        return False

    def convert_if_relative_url(self, url1: str, url2: str) -> Optional[str]:
        """Convert relative url if it is a relative path.

        Args:
            url1 (str): Absolute path.
            url2 (str): Relative path.

        Returns:
            Optional[str]: Absolute path if it works, or None if not.
        """
        if self.is_absolute_url(url2):
            return url2
        else:
            return f"https://{url1}{url2}".replace(" ","")
        # return None

    def is_url_ok_to_follow(self, url: str, domain: str) -> bool:
        """Validate if a url is valid.

        Args:
            url (str): Url to be checked.
            domain (str): Domain of the url.

        Returns:
            bool: True if is a valid url, False if not.
        """
        if not self.is_absolute_url(url):
            return False
        if not domain in url:
            return False
        if "@" in url or "mailto:" in url:
            return False
        pattern = r"^(.*?)(?:\.html)?$"
        if not re.match(pattern, url):
            return False
        return True

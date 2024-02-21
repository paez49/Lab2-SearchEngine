import requests
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout
from typing import Optional
import re
class UtilRequests:
    def get_request(url: str) -> requests.Response:
        """Validate url by making a GET request to this one

        Args:
            url (str): url to be requested.

        Returns:
            requests.Response: Response object.
        """
        try:
            response = requests.get(url)
            return response
        except (RequestException, ConnectionError, HTTPError, Timeout):
            return None

    def read_response(response: requests.Response) -> str:
        """Obtain html from a response object.

        Args:
            response (requests.Response): Response object.

        Returns:
            str: Raw html.
        """
        return response.text
    
    def get_request_url(request:requests.Request) -> str:
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
    def is_absolute_url(self, url:str) -> bool:
        """Validate if url is absolute or not

        Args:
            url (str): Url to be validated.

        Returns:
            bool: True if is absolute, False if not.
        """
        if "http" in url or "https" in url:
            return True
        return False

    def convert_if_relative_url(self, url1:str, url2:str)-> Optional[str]:
        """Convert relative url if it is a relative path.

        Args:
            url1 (str): Absolute path.
            url2 (str): Relative path.

        Returns:
            Optional[str]: Absolute path if it works, or None if not.
        """
        if self.is_absolute_url(url2):
            return url2
        elif self.request_service.get_request(url1+url2):
            return url1+url2
        return None
    
    def is_url_ok_to_follow(self,url:str,domain:str)->bool:
        """Validate if a url is valid.

        Args:
            url (str): Url to be checked.
            domain (str): Domain of the url.

        Returns:
            bool: True if is a valid url, False if not.
        """
        if not self.is_absolute_url(url):
            return False
        if not url in domain:
            return False
        if "@" in url or "mailto:" in url:
            return False
        pattern =  r'^[\w-]+\.(html)?$'
        if not re.match(pattern,url):
            return False
        return True
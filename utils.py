import requests
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout
from typing import Optional, List, Set
import re
import json

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
        """Open the webdriver with the chrome configuration.
        """
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options,
        )

    def close(self):
        """Close the webdriver.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_page_selenium(self, url: str):
        """Get the page with the webdriver.

        Args:
            url (str): Url to be requested.

        Raises:
            Exception: Error requesting the page.
        """
        try:
            self.driver.get(url)
        except (RequestException, ConnectionError, HTTPError, Timeout):
            raise Exception("Error requesting the page.")

    def get_response(self, url:str) -> requests.Response:
        """Get the response of a request.

        Args:
            url (str): Url to be requested.

        Returns:
            requests.Response: Response object.
        """
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
            url_res = ""
            if "/" in url2:
                url_res = f"{url1}{url2}"
            else:
                url_res = f"{url1}/{url2}"

        return f"https://{url_res}".replace(" ", "")

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


class UtilText:
    def get_useful_words(self, text: str) -> List[str]:
        """Get useful words from a text, ommits words with less than 4 characters and punctuation.

        Args:
            text (str): Text to be cleaned.

        Returns:
            List[str]: List of useful words.
        """
        words = re.split(r"\s+", text)

        cleaned_words = []
        for word in words:
            cleaned_word = re.sub(r"[!.,:]+$", "", word)
            if (
                re.match(r"^[A-Za-z][A-Za-z0-9_]+$", cleaned_word)
                and len(cleaned_word) > 4
            ):
                cleaned_words.append(cleaned_word.lower())
        return cleaned_words

    def most_frequent_words(self, words: List[str]):
        """Get the most frequent words from a list of words and save it in a json file.

        Args:
            words (List[str]): List of words to be analyzed.
        """
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        sorted_word_count = dict(
            sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        )
        with open("example_files/frequences.json", "w") as file:
            json.dump(sorted_word_count, file, indent=2)

    def get_useless_words(self) -> List[str]:
        """Get the most frequent words from a json file and return the words that are more frequent than 100.

        Returns:
            List[str]: List of useless words.
        """
        with open("example_files/frequences.json", "r") as file:
            dict_useless = json.load(file)
        return [key for key, value in dict_useless.items() if value > 100]


class UtilSimiliraty:
    def jaccard_similarity(set1: Set, set2: Set) -> float:
        """
        This function calculates the Jaccard similarity between two sets.
        Jaccard similarity is calculated as the size of the intersection
        of the two sets divided by the size of the union of the two sets.

        Args:
            set1 (Set): The first set to compare.
            set2 (Set): The second set to compare.

        Returns:
            float: The Jaccard similarity between the two sets.
        """
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)

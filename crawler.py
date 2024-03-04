from typing import Dict
import json
from bs4 import BeautifulSoup
from utils import UtilURL, UtilRequests, UtilText
import pandas as pd

class Crawler:
    def __init__(self, start_url: str, domain: str):
        self.start_url = start_url
        self.domain = domain
        self.util_url = UtilURL()
        self.util_requests = UtilRequests()

    def get_links(self, url: str, n: int) -> Dict[str, str]:
        self.util_requests.open()
        self.util_requests.get_page_selenium(url)
        html = self.util_requests.driver.page_source
        self.util_requests.close()

        soup = BeautifulSoup(html, "html.parser")
        results_list = soup.find("ol", id="list-search-results")

        dict_courses = {}
        i = 0
        for res in results_list:
            if i < n:
                course_link = res.find("a")["href"]
                dict_courses[course_link.split("/")[-1]] = (
                    self.util_url.convert_if_relative_url(self.domain, course_link)
                )
                i += 1
            else:
                break

        return dict_courses

    def go(self, n: int, json_file_name: str, output_file_name: str):
        """Crawl the web and build the index."""
        courses = self.get_links(self.start_url, n)

        util_text = UtilText()
        all_words = []
        columns = ["course_id", "word"]
        df = pd.DataFrame(columns=columns)

        for course_id, url_course in courses.items():
            res = self.util_requests.get_response(url_course)

            soup = BeautifulSoup(res.content, "html.parser")

            title_wrapper = soup.find("div", class_="subtitle")

            course_wrapper = soup.find(
                "div",
                class_="course-wrapper-content col-12 col-md-8",  # Tag with all text of the course
            )
            if not course_wrapper:
                course_wrapper = soup.find(
                    "div",
                    class_="course-wrapper-content course-wrapper-content---top col-12 col-md-8",
                )
            text = course_wrapper.get_text()
            text = text + title_wrapper.get_text()

            useful_words = util_text.get_useful_words(text)
            useless_words = util_text.get_useless_words()

            useful_words = list(set(useful_words))  # Drop duplicated
            for word in useful_words:
                if not word in useless_words:
                    df = pd.concat(
                        [df, pd.DataFrame({"course_id": [course_id], "word": [word]})],
                        ignore_index=True,
                    )

            # all_words = all_words + useful_words
        # util_text.most_frequent_words(all_words)

        with open(json_file_name, "w") as file:
            json.dump(courses, file, indent=2)

        df.to_csv(output_file_name, index=False, sep="|")

        return df, courses

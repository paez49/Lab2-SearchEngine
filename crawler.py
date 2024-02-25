from queue import Queue
from typing import Dict
import json
import csv
from bs4 import BeautifulSoup
from utils import UtilURL, UtilRequests


DOMAIN = "educacionvirtual.javeriana.edu.co"
URL_COURSES = "https://educacionvirtual.javeriana.edu.co/nuestros-programas-nuevo"


class Crawler:
    def __init__(self, start_url: str, domain: str):
        self.start_url = start_url
        self.domain = domain
        self.visited_urls = set()
        self.url_queue = Queue()
        self.index = {}
        self.util_url = UtilURL()
        self.util_requests = UtilRequests()

    def get_links(self, url: str, n: int) -> Dict[str, str]:
        self.util_requests.open()
        self.util_requests.get_response(url)
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
                    self.util_url.convert_if_relative_url(DOMAIN, course_link)
                )
                i += 1
            else:
                break

        return dict_courses

    def go(self, n: int, json_file_name: str, output: str):
        """Crawl the web and build the index."""
        self.url_queue.put(self.start_url)

        url = self.url_queue.get()

        """if url in self.visited_urls:
            continue"""
        try:
            courses = self.get_links(url, n)
            # TODO:Get more information of each course to build the search engine
            # ...
        except Exception as e:
            print(f"Error processing {url}: {e}")

        with open(json_file_name, "w") as file:
            json.dump(courses, file, indent=2)

        with open(output, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["word", "course_ids"])
            for word, course_ids in self.index.items():
                csv_writer.writerow([word, ", ".join(course_ids)])


# Ejemplo de uso
crawler = Crawler(URL_COURSES, DOMAIN)
crawler.go(100, "courses.json", "index.csv")

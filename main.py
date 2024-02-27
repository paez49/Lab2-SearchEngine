from crawler import Crawler
DOMAIN ="educacionvirtual.javeriana.edu.co"
URL_COURSES = "https://educacionvirtual.javeriana.edu.co/nuestros-programas-nuevo"

if __name__ == "__main__":
    crawler = Crawler(URL_COURSES, DOMAIN)
    crawler.go(10, "courses.json", "index.csv")
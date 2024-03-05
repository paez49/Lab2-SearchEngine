from crawler import Crawler
from search import search
from compare import compare


DOMAIN = "educacionvirtual.javeriana.edu.co"
URL_COURSES = "https://educacionvirtual.javeriana.edu.co/nuestros-programas-nuevo"

if __name__ == "__main__":
    crawler = Crawler(URL_COURSES, DOMAIN)
    while True:
        try:
            num_pages = int(input("Enter the number of courses to search: "))
            json_file = (
                input("Enter the name of the JSON file (without extension): ") + ".json"
            )
            csv_file = (
                input("Enter the name of the CSV file (without extension): ") + ".csv"
            )
            break
        except ValueError:
            print("Invalid input. Please enter a valid number of courses.")

    df, dict_courses = crawler.go(num_pages, json_file, csv_file)

    keywords = input("Enter the keywords separated by commas (,): ")
    keywords = keywords.split()

    print("The 5 most relevant courses are:")
    for course in search(keywords, df, dict_courses)[:5]:
        print(f"*   {course}")

    course_1 = input("Enter the ID of the first course to compare: ")
    course_2 = input("Enter the ID of the second course to compare: ")
    similarity = compare(course_1, course_2, df)
    print(f"The similarity between {course_1} and {course_2} is {similarity}")

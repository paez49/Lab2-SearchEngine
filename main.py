from crawler import Crawler
import sys
DOMAIN ="educacionvirtual.javeriana.edu.co"
URL_COURSES = "https://educacionvirtual.javeriana.edu.co/nuestros-programas-nuevo"

if __name__ == "__main__":
    crawler = Crawler(URL_COURSES, DOMAIN)
    crawler.go(10, "courses.json", "index.csv")
    while True:
        try:
            num_pages = int(input("Enter the number of pages: "))
            json_file = input("Enter the name of the JSON file (without extension): ")
            csv_file = input("Enter the name of the CSV file (without extension): ")
            break
        except ValueError:
            print("Invalid input. Please enter a valid number of pages.")
            
    num_pages = int(input("Enter the number of pages: "))
    json_file = input("Enter the name of the JSON file: ")
    csv_file = input("Enter the name of the CSV file: ")
    crawler.go(num_pages, json_file, csv_file)
    
    keywords = input("Enter the keywords separated by commas (,): ")
    keywords = keywords.split()
    
    
    

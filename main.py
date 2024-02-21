import util

DOMAIN ="educacionvirtual.javeriana.edu.co"
URL_COURSES = "https://educacionvirtual.javeriana.edu.co/nuestros-programas-nuevo"

if __name__ == "__main__":
    util.get_request(URL_COURSES)
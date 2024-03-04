import pandas as pd
import numpy as np

"""--------------------Funciones--------------------"""


# funcion de la metrica de similutd de Jaccard
def jaccard_similarity(set1, set2):
    """
    Esta función calcula la similitud de Jaccard entre dos conjuntos.
    La similitud de Jaccard es calculada como el tamaño de la intersección de los dos conjuntos 
    dividido por el tamaño de la unión de los dos conjuntos.

    args:
    set1 (set): El primer conjunto a comparar.
    set2 (set): El segundo conjunto a comparar.

    return:
    float: La similitud de Jaccard entre los dos conjuntos.
    """
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)


def find_similar_courses(words, df):
    """
    Esta función busca los cursos más similares a una lista de palabras proporcionadas.
    La similitud se calcula utilizando la métrica de similitud de Jaccard.

    args:
    words (list): Una lista de palabras a comparar con los cursos.
    df (DataFrame): Un DataFrame que contiene los cursos y sus palabras asociadas.

    return:
    list: Una lista de IDs de cursos similares a las palabras proporcionadas.
    """
    words_set = set(words)
    courses = df.groupby("course_id")["word"].apply(set).reset_index()
    courses["similarity"] = courses["word"].apply(
        lambda x: jaccard_similarity(words_set, x)
    )
    similar_courses = courses.sort_values(by="similarity", ascending=False)
    return similar_courses["course_id"].tolist()


def search(keywords):
    """
    Esta función busca los cursos más similares a una lista de palabras proporcionadas.
    La similitud se calcula utilizando la métrica de similitud de Jaccard.

    args:
    keywords (list): Una lista de palabras a comparar con los cursos.

    return:
    list: Una lista de url de cursos similares a las palabras proporcionadas.
    """
    # crear dataframe del archivo index.csv
    df_index = pd.read_csv("index.csv")

    similar_courses = find_similar_courses(keywords, df_index)
    """
 codigo para devolvers los urls
 """

    return similar_courses

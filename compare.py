import pandas as pd
import numpy as np

"""--------------------Funciones--------------------"""


# funcion de la metrica de similutd de Jaccard
def jaccard_similarity(set1, set2):
    """
    Esta función calcula la similitud de Jaccard entre dos conjuntos.
    La similitud de Jaccard es calculada como el tamaño de la intersección de los dos conjuntos dividido por el tamaño de la unión de los dos conjuntos.

    args:
    set1 (set): El primer conjunto a comparar.
    set2 (set): El segundo conjunto a comparar.

    return:
    float: La similitud de Jaccard entre los dos conjuntos.
    """
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)


def find_similar_two_courses(curso1, curso2, df):
    # buscar los cursos en el dataframe
    curso1 = df[df["course_id"] == curso1]
    curso2 = df[df["course_id"] == curso2]
    # obtener los vectores de palabras
    vec1 = curso1["word"].values[0]
    vec2 = curso2["word"].values[0]

    jaccard_sim = jaccard_similarity(set(vec1), set(vec2))
    # retornar el resultado
    return jaccard_sim


def compare(curso1, curso2):
    """
    Esta función busca los cursos más similares a una lista de palabras proporcionadas.
    La similitud se calcula utilizando la métrica de similitud de Jaccard.

    args:
    curso1 (int): El id del primer curso a comparar.
    curso2 (int): El id del segundo curso a comparar.

    return:
    float: La similitud de Jaccard entre los dos cursos.
    """
    # crear dataframe del archivo index.csv
    df_index = pd.read_csv("index.csv")
    courses = df_index.groupby("course_id")["word"].apply(set).reset_index()
    similarity = find_similar_two_courses(curso1, curso2, courses)
    return similarity

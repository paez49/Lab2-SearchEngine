import pandas as pd
from typing import List,Dict
from utils import UtilSimiliraty


def find_similar_courses(words: List[str], df: pd.DataFrame) -> List[str]:
    """This function searches for the courses most similar to a provided list of words.
    Similarity is calculated using the Jaccard similarity metric.

        Args:
            words (List[str]): A list of words to compare with the courses.
            df (pd.DataFrame): Dataframe with the index of courses and words.

        Returns:
            List[str]: A list of course IDs that are similar to the provided words.
    """
    words_set = set(words)
    courses = df.groupby("course_id")["word"].apply(set).reset_index()
    courses["similarity"] = courses["word"].apply(
        lambda x: UtilSimiliraty.jaccard_similarity(words_set, x)
    )
    similar_courses = courses.sort_values(by="similarity", ascending=False)
    return similar_courses["course_id"].tolist()


def search(keywords: List[str], df_index: pd.DataFrame, dict_courses: Dict[str,str]) -> List[str]:
    """This function searches for the courses most similar to a provided list of words.
    Similarity is calculated using the Jaccard similarity metric.

        Args:
            keywords (List[str]): A list of words to compare with the courses.
            df_index (pd.DataFrame): Dataframe with the index of courses and words.
            dict_courses (Dict[str,str]): A dictionary with the course_id as key and the url as value.

        Returns:
            List[str]: A list of urls that the course are similar to the provided words.
    """

    similar_courses = find_similar_courses(keywords, df_index)
    url_courses = []
    for course in similar_courses:
        url_courses.append(dict_courses[course])
    return url_courses

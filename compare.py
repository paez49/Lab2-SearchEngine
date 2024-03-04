import pandas as pd
from utils import UtilSimiliraty

def find_similar_two_courses(course_1: str, course_2: str, df: pd.DataFrame) -> float:
    """This function searches for the courses most similar to a provided list of words.

    Args:
        course_1 (str): The ID of the first course to compare.
        course_2 (str): The ID of the second course to compare.
        df (pd.DataFrame): Dataframe with the index of courses and words.

    Returns:
        float: Jaccard similarity.
    """
    course_1 = df[df["course_id"] == course_1]
    course_2 = df[df["course_id"] == course_2]

    vec1 = course_1["word"].values[0]
    vec2 = course_2["word"].values[0]

    jaccard_sim = UtilSimiliraty.jaccard_similarity(set(vec1), set(vec2))
    return jaccard_sim


def compare(course_1: str, course_2: str, df_index: pd.DataFrame) -> float:
    """This function searches for the courses most similar to a provided list of words.
    Similarity is calculated using the Jaccard similarity metric.

        Args:
            course_1 (str): The ID of the first course to compare.
            course_2 (str): The ID of the second course to compare.
            df_index (pd.Dataframe): Dataframe with the index of courses and words.

        Returns:
            float: The Jaccard similarity between the two courses.
    """
    courses = df_index.groupby("course_id")["word"].apply(set).reset_index()
    similarity = find_similar_two_courses(course_1, course_2, courses)
    return similarity

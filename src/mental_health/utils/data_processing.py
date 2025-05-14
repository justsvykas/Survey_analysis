"""Module for data processing utilities."""

import pandas as pd


def add_question_answers_proportions_by_group(
    df: pd.DataFrame, questions: str | list[str], group_by: str
) -> pd.DataFrame:
    """Calculates proportions of answers for given questions grouped by a column.

    For each question, groups answers and calculates counts. Groups by the specified column
    to get total counts per group. Divides each answer count by the group total to get
    proportions.

    Args:
        df: Input dataframe containing question and answer data.
        questions: Question text or list of question texts to filter by.
        group_by: Column name to group results by.

    Returns:
        DataFrame with Count and Proportion columns for each answer within groups.
    """
    if type(questions) is list:
        mask = df["questiontext"].isin(questions)
    else:
        mask = df["questiontext"] == questions

    df_processed = df[mask].groupby([group_by, "AnswerText"]).size().reset_index(name="Count")
    total_per_question = df_processed.groupby(group_by)["Count"].sum()
    df_processed["Proportion"] = df_processed.apply(
        lambda row: row["Count"] / total_per_question[row[group_by]], axis=1
    )
    return df_processed


def calculate_counts(group: pd.DataFrame) -> pd.Series:
    """Calculates counts and proportions of null vs non-null answers for a group.

    Args:
        group: DataFrame group containing answer counts with 'AnswerText' and 'count' columns.

    Returns:
        pd.Series: Series containing the following metrics:
            null_count (int): Count of null (-1) answers
            other_count (int): Count of non-null answers
            total_count (int): Total count of all answers
            null_proportion (float): Proportion of null answers (0-1)
    """
    null_count = group.loc[group["AnswerText"] == "-1", "count"].sum()
    other_count = group.loc[group["AnswerText"] != "-1", "count"].sum()
    total_count = null_count + other_count
    null_proportion = null_count / total_count if total_count > 0 else 0
    return pd.Series(
        {
            "null_count": null_count,
            "other_count": other_count,
            "total_count": total_count,
            "null_proportion": null_proportion,
        }
    )

"""Module for data quality logs.

This module provides functions to check for missing values and duplicate
entries in a pandas DataFrame. It uses logging to report findings.
"""

import logging

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.getLogger("seaborn").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logger = logging.getLogger("project_logger")


def check_for_null_and_duplicates(df: pd.DataFrame) -> None:
    """Checks for null values and duplicates in the dataframe.

    Args:
        df: The dataframe to check for null values and duplicates.

    Logs:
        Whether there are any null values in the dataframe.
        Whether there are any -1 values in AnswerText collumn
        Whether there are any duplicate columns in the dataframe.
        Whether there are any duplicate rows in the dataframe.
    """
    logger.info("Any Null values: %s", df.isna().to_numpy().any())
    logger.info("Any -1 answers: %s", (df["AnswerText"] == "-1").any())
    logger.info("Any duplicate columns: %s", df.columns.duplicated().any())
    logger.info("Any duplicate rows: %s", df.duplicated().any())

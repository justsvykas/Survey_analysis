"""Module for calculating prevalence rate and confidence intervals."""  # noqa: N999

import logging

import numpy as np
import pandas as pd
from utils.logs import logger


def calculate_prevalence_rate(
    population: int,
    diagnosed_cases: int,
    total_condition_reports: int,
    specific_condition_count: int,
) -> float:
    """Calculate the prevalence rate for a specific mental health condition.

    This function calculates the prevalence rate by combining diagnosis rate,
    response rate, and condition-specific rate. It includes data validation
    and logging of intermediate calculations.

    Args:
        population: Total number of people in the survey population.
        diagnosed_cases: Number of people diagnosed with any mental health condition.
        follow_up_responses: Number of people who provided follow-up condition details.
        total_condition_reports: Total number of condition reports across all types.
        specific_condition_count: Number of reports for the specific condition.

    Returns:
        float: The calculated prevalence rate as a decimal between 0 and 1.

    Raises:
        None: Returns 0.0 if population is zero instead of raising exception.
    """
    logger.info("Calculating prevalence rate for a specific mental health condition.")

    if population == 0:
        logger.error("Population cannot be zero.")
        return 0.0

    if diagnosed_cases > population:
        logger.warning("Diagnosed cases exceed the total population. Check data.")

    diagnosis_rate = diagnosed_cases / population
    condition_rate = (
        specific_condition_count / total_condition_reports if total_condition_reports > 0 else 0
    )

    prevalence_rate = diagnosis_rate * condition_rate
    logger.info("Diagnosis Rate: %.5f", diagnosis_rate)
    logger.info("Condition Rate: %.5f", condition_rate)
    logger.info("Prevalence Rate: %.5f", prevalence_rate)

    return prevalence_rate


def calculate_disorder_prevalence(df: pd.DataFrame, disorder_name: str) -> float:
    """Calculate the prevalence rate for any specified mental health disorder.

    Args:
        df (pd.DataFrame): DataFrame containing survey responses
        disorder_name (str): Name of the disorder to calculate prevalence for
        (e.g., "Mood Disorder (Depression, Bipolar Disorder, etc)")

    Returns:
        float: Prevalence rate for the specified disorder
    """
    df_2016 = df[df["SurveyID"] == 2016]  # noqa: PLR2004

    population = len(
        df_2016[df_2016["questiontext"] == "Do you currently have a mental health disorder?"]
    )
    logger.info(f"Total Population: {population}")

    diagnosed_cases = len(
        df_2016[
            (df_2016["questiontext"] == "Do you currently have a mental health disorder?")
            & (df_2016["AnswerText"] == "Yes")
        ]
    )
    logger.info(f"Diagnosed Cases: {diagnosed_cases}")

    total_condition_reports = len(
        df_2016[
            df_2016["questiontext"] == "If yes, what condition(s) have you been diagnosed with?"
        ]
    )
    logger.info(f"Total Condition Reports: {total_condition_reports}")

    disorder_reports = len(
        df_2016[
            (df_2016["questiontext"] == "If yes, what condition(s) have you been diagnosed with?")
            & (df_2016["AnswerText"] == disorder_name)
        ]
    )
    logger.info(f"{disorder_name} Reports: {disorder_reports}")

    prevalence_rate = calculate_prevalence_rate(
        population=population,
        diagnosed_cases=diagnosed_cases,
        total_condition_reports=total_condition_reports,
        specific_condition_count=disorder_reports,
    )

    logger.info(f"Final Prevalence Rate: {prevalence_rate:.2f}")
    return prevalence_rate


def bootstrap_prevalence_rate(
    df: pd.DataFrame,
    disorder_name: str,
    n_iterations: int = 1000,
    sample_size: int | None = None,
    random_state: int = 42,
) -> tuple[float, list[float]]:
    """Calculate bootstrap confidence intervals for disorder prevalence rate.

    This function performs bootstrap resampling to estimate the confidence interval
    of the prevalence rate for a specified mental health disorder.

    Args:
        df (pd.DataFrame): DataFrame containing survey responses
        disorder_name (str): Name of the disorder to calculate prevalence for
        n_iterations (int, optional): Number of bootstrap iterations. Defaults to 1000.
        sample_size (int, optional): Size of each bootstrap sample. If None, uses original size.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.

    Returns:
        tuple[float, list[float]]: Tuple containing:
            - Original prevalence rate
            - List of bootstrap prevalence rates
    """
    original_rate = calculate_disorder_prevalence(df, disorder_name)

    df_2016 = df[df["SurveyID"] == 2016]  # noqa: PLR2004

    main_question_df = df_2016[
        df_2016["questiontext"] == "Do you currently have a mental health disorder?"
    ]

    follow_up_df = df_2016[
        df_2016["questiontext"] == "If yes, what condition(s) have you been diagnosed with?"
    ]

    bootstrap_rates = []
    rng = np.random.RandomState(random_state)
    for _ in range(n_iterations):
        bootstrap_main = main_question_df.sample(
            n=sample_size if sample_size else len(main_question_df), replace=True, random_state=rng
        )
        bootstrap_follow_up = follow_up_df.sample(
            n=sample_size if sample_size else len(follow_up_df), replace=True, random_state=rng
        )
        logger.info(f"Bootstrap Main length: {len(bootstrap_main)}")
        logger.info(f"Bootstrap Follow-up length: {len(bootstrap_follow_up)}")
        temp_df = pd.concat([bootstrap_main, bootstrap_follow_up])
        bootstrap_rate = calculate_disorder_prevalence(temp_df, disorder_name)
        bootstrap_rates.append(bootstrap_rate)

    return original_rate, bootstrap_rates


def calculate_confidence_interval(
    bootstrap_rates: list[float], confidence_level: float = 0.95
) -> tuple[float, float]:
    """Calculate confidence interval from bootstrap rates.

    Args:
        bootstrap_rates (list[float]): List of bootstrap prevalence rates
        confidence_level (float, optional): Confidence level (0-1). Defaults to 0.95.

    Returns:
        tuple[float, float]: Lower and upper bounds of the confidence interval
    """
    lower_percentile = (1 - confidence_level) / 2
    upper_percentile = 1 - lower_percentile
    lower_bound = np.percentile(bootstrap_rates, lower_percentile * 100)
    upper_bound = np.percentile(bootstrap_rates, upper_percentile * 100)
    return lower_bound, upper_bound


def analyze_disorder_prevalence(
    df: pd.DataFrame,
    disorder_name: str,
    n_iterations: int = 1000,
    confidence_level: float = 0.95,
    random_state: int = 42,
) -> dict:
    """Perform complete prevalence analysis including confidence intervals.

    Args:
        df (pd.DataFrame): DataFrame containing survey responses
        disorder_name (str): Name of the disorder to analyze
        n_iterations (int, optional): Number of bootstrap iterations. Defaults to 1000.
        confidence_level (float, optional): Confidence level (0-1). Defaults to 0.95.
        random_state (int, optional): Random seed for reproducibility. Defaults to 42.

    Returns:
        dict: Dictionary containing:
            - original_rate: Original prevalence rate
            - confidence_interval: Tuple of (lower_bound, upper_bound)
            - bootstrap_rates: List of bootstrap prevalence rates
            - standard_error: Standard error of the bootstrap estimates
    """
    logging.disable(logging.INFO)
    original_rate, bootstrap_rates = bootstrap_prevalence_rate(
        df, disorder_name, n_iterations, random_state=random_state
    )
    lower_bound, upper_bound = calculate_confidence_interval(bootstrap_rates, confidence_level)
    standard_error = np.std(bootstrap_rates)

    logging.disable(logging.NOTSET)
    logger.info("Original Prevalence Rate: %.2f", original_rate)
    logger.info("95%% Confidence Interval: (%.2f, %.2f)", lower_bound, upper_bound)
    logger.info("Standard Error: %.2f", standard_error)
    return {
        "original_rate": original_rate,
        "confidence_interval": (lower_bound, upper_bound),
        "bootstrap_rates": bootstrap_rates,
        "standard_error": standard_error,
    }

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utils.data_processing import add_question_answers_proportions_by_group

sequential_palette = "Blues"
categorical_palette = "pastel"

sns.set_theme(
    style="white",
    palette=sequential_palette,
    rc={
        "text.color": "black",
        "axes.labelcolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
    },
)


def analyze_null_values(df: pd.DataFrame) -> pd.DataFrame:
    """Analyzes null values (represented as "-1") in the dataset.

    Parameters:
        df (pandas.DataFrame): Input dataframe containing question and answer data

    Returns:
        pandas.DataFrame: DataFrame with null value analysis containing:
            - questiontext: The question being asked
            - null_count: Number of "-1" responses
            - other_count: Number of non-null responses
            - total_count: Total number of responses
            - null_proportion: Proportion of null values
    """
    response_counts = df.groupby(["questiontext", "AnswerText"]).size().reset_index(name="count")

    null_analysis = []
    for question in response_counts["questiontext"].unique():
        question_data = response_counts[response_counts["questiontext"] == question]
        null_count = question_data[question_data["AnswerText"] == "-1"]["count"].sum()
        other_count = question_data[question_data["AnswerText"] != "-1"]["count"].sum()
        total_count = null_count + other_count

        null_analysis.append(
            {
                "questiontext": question,
                "null_count": null_count,
                "other_count": other_count,
                "total_count": total_count,
                "null_proportion": null_count / total_count if total_count > 0 else 0,
            }
        )

    result_df = pd.DataFrame(null_analysis)
    return result_df.sort_values("null_proportion", ascending=False)


def plot_question_grouped_by_years(
    raw_df: pd.DataFrame, question: str, title: str, question_name: str | None = None
) -> None:
    """Creates a bar plot showing question responses grouped by survey years.

    Args:
        raw_df: DataFrame containing the survey data.
        question: Question text to analyze.
        title: Title for the plot.
        question_name: Optional alternative name for x-axis label. If None, uses question text.
    """
    df_question_over_years = add_question_answers_proportions_by_group(
        raw_df, question, "SurveyID"
    )
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        data=df_question_over_years,
        x="SurveyID",
        y="Proportion",
        hue="AnswerText",
        palette=categorical_palette,
        alpha=0.8,
    )
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f")
    plt.ylim(0, 1)

    plt.title(title)
    if question_name is not None:
        plt.xlabel(question_name)
    else:
        plt.xlabel(question)
    plt.ylabel("Proportion of Responses")
    plt.legend(title="Survey Year", loc="upper right")
    sns.despine()
    plt.show()


def plot_question_grouped_by_answers(
    raw_df: pd.DataFrame, question: str, title: str, question_name: str | None = None
) -> None:
    """Creates a bar plot showing question responses grouped by answer options.

    Args:
        raw_df: DataFrame containing the survey data.
        question: Question text to analyze.
        title: Title for the plot.
        question_name: Optional alternative name for x-axis label. If None, uses question text.
    """
    df_question_over_years = add_question_answers_proportions_by_group(
        raw_df, question, "SurveyID"
    )
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        data=df_question_over_years,
        x="AnswerText",
        y="Proportion",
        hue="SurveyID",
        palette=categorical_palette,
        alpha=0.8,
    )
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f")
    plt.ylim(0, 1)

    plt.title(title)
    plt.xlabel(question_name) if question_name is not None else plt.xlabel(question)
    plt.ylabel("Proportion of Responses")
    plt.legend(title="Survey Year", loc="upper right")
    sns.despine()
    plt.show()


def plot_multiple_disorders_distribution(
    results_dict: dict[str, dict],
    disorder_names: list[str],
    colors: list[str] = ["#2ecc71", "#3498db", "#e74c3c"],  # Green, Blue, Red  # noqa: B006
) -> None:
    """Plot multiple disorder distributions with their confidence intervals on the same graph.

    Args:
        results_dict (dict): Dictionary of results from analyze_disorder_prevalence for each
        disorder
        disorder_names (list): List of disorder names
        colors (list): List of colors for each disorder
    """
    _, ax = plt.subplots(figsize=(12, 6))

    for i, (_, results) in enumerate(results_dict.items()):
        sns.kdeplot(
            data=results["bootstrap_rates"], color=colors[i], linewidth=2, label=disorder_names[i]
        )
        ax.axvline(x=results["original_rate"], color=colors[i], linestyle="--", alpha=0.5)
        ci_lower, ci_upper = results["confidence_interval"]
        ax.axvline(x=ci_lower, color=colors[i], linestyle=":", alpha=0.5)
        ax.axvline(x=ci_upper, color=colors[i], linestyle=":", alpha=0.5)
        ax.axvspan(ci_lower, ci_upper, color=colors[i], alpha=0.07)

    ax.set_title("Bootstrap Distributions of Top 3 Mental Health Disorders")
    ax.set_xlabel("Prevalence Rate")
    ax.set_ylabel("Density")
    ax.legend()
    sns.despine()
    plt.tight_layout()
    plt.show()

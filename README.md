# Mental Health in Tech Industry

This project is analysis of mental health issues in tech industry using data from OSMI (Open Soure Mental Illness) survey. In this project I have used bootsraping method to estimate confidence intervals of prevelance rate of mental health disorders in tech industry.

![Confidence Intervals](src/mental_health/wordc_cloud.png)

# Main findings

All in all mental issuses in tech industry are quite common with 50% of respondents having or had a mental health disorder diagnosis. While employees 14% have rated support in tech companies being excellent or good. This shows that it is important to be aware of mental health issues and there is lack for good support.

To improve mental health support for employees I advice:
- Make mental health awareness campaign about most prevelant disorders what they are and how to support people with them. Most prevelant are Mood Disorder between 12% and 15%, Anxiety Disorder between 10% and 13%, ADHD between 3% and 5% with 95% confidence level.
- Remind on available resources and help with mental health issues as 65% of target population does not know of or is not sure of any resources available in the company. One of the reasons why this is such a hight number might be that there is 67% of respondents saying companies haven't talked about mental health when considering employee wellness.
- People are generally willing to be open as 80% of target population has some coworkers and 70% has some supervisors to whom they are willing to open up. It is important to highlight that people are willing to open up, which means they might require some compassionate asking or different ways for others to actually get people talking.
- To have people open up about mental health issues policy should make it crystal clear that opening up  wont result in negative career impact as 39% of target population think openning up would hurt their career and for 7% more it has.
- Another way get people open up about mental health issues is to improve responses of coworkers/empyees as around 13% of population have experienced and around 19% have observed unsupportive response from coworkers/employees.
- There is evidence people are becoming more open about mental health issues in interviews as at the start of the survey in 2014 there were 80% categorically closed respondents while in 2019 there were 68%. So there is possibility to be open with one third of employees from the start of their career at the company.

# Dependencies
Below are dependencies required to have to install project into your local machine. However, there is **main.html** file in the root of the project that can be used to view the analysis without installing the project.

- Python 3.12
- poetry

For managing Python versions consider using [pyenv](https://github.com/pyenv/pyenv).
For using poetry take a look at [poetry installation](https://python-poetry.org/docs/#installation).

# Installation
This analysis is structured to be easily continued by another developer, with dependency management handled via the Poetry library. It follows consistent coding standards, enforced using Ruff for linting and the pre-commit library. To further ease distribution, this project is packaged for ease of use.

After placing yourself in your desired directory, run this command in your terminal to copy this repo.
```bash
git clone https://github.com/justsvykas/Survey_analysis
```
Go to project directory.
```bash
cd Survey_analysis/
```
install package
```bash
poetry install
```

# Usage

Go to directory
```bash
cd src/mental_health/
```
Open main analysis file
```bash
code main.ipynb
```
Run the notebook cells sequentially or review the precomputed outputs. Notice when running the notebook code will query and store data in data/ directory with.

To have pre-commit run some basic tests to ensure the code is up to standard before commits - run:
```bash
pre-commit install
```

# Structure

```bash
.
├── 215.md                        # Documentation file for the task given by TC
├── .gitignore                    # Specifies files to ignore in Git version control
├── .pre-commit-config.yaml       # Configuration for pre-commit hooks
├── README.md                     # Project documentation
├── main.html                     # HTML file for viewing analysis without installation
├── pyproject.toml                # Python project configuration (Poetry)
├── ruff.toml                     # Formatter and linter configuration (Ruff)
├── src                           # Source code directory
│    └── mental_health           # Package directory
│       ├── __init__.py          # Marks this directory as a package
│       ├── main.ipynb           # Main analysis notebook
│       ├── CI.png               # Confidence intervals visualization
│       └── utils/               # Directory for utility files
│           ├── __init__.py
│           ├── data/
│           │   ├── database.sqlite         # Sqlite databse
│           │   ├── raw_mental_health.csv   # raw data from kaggle
│           │   └── processed_data_mental_health.csv
│           ├── data_processing.py/         # Data processing utilities
│           │   └── add_question_answers_proportions_by_group()
│           ├── logs.py                     # Logging utilities
│           │   └── check_for_null_and_duplicates()
│           ├── plots.py                    # Visualization utilities
│           │   ├── analyze_null_values()
│           │   ├── plot_question_grouped_by_years()
│           │   ├── plot_question_grouped_by_answers()
│           │   └── plot_multiple_disorders_distribution()
│           └── prevelance_rate_CI.py       # Prevalence rate calculation utilities
│               ├── calculate_prevalence_rate()
│               ├── calculate_disorder_prevalence()
│               ├── bootstrap_prevalence_rate()
│               ├── calculate_confidence_interval()
│               └── analyze_disorder_prevalence()
└── .vscode                       # Directory for VS-specific settings
    ├── extensions.json           # Recommended VS Code extensions
    └── settings.json             # VS Code workspace settings
```


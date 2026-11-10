# CogniStream: Developer Flow-State & Cognitive Load Analytics

An end-to-end Python data analytics project that explores synthetic developer activity data to understand focus patterns, interruptions, task switching, cognitive-load ratings, task completion, and productivity trends.

The project includes a data-generation and cleaning pipeline, exploratory and statistical analysis, advanced analytics modules, generated reports and visualizations, and an interactive Streamlit dashboard.

> **Data note:** This project uses synthetic/mock developer activity data for demonstration and learning. It does not contain real employee records. Cognitive-load ratings are illustrative values, not medical or psychological measurements. Productivity categories are analytical labels based on the project's scoring logic, not definitive assessments of individual developers.

---

## Project Objectives

- Generate a structured dataset of developer work sessions.
- Clean and validate the dataset before analysis.
- Explore focus duration, interruptions, task switching, task complexity, and task types.
- Examine descriptive relationships between activity metrics.
- Calculate developer productivity metrics and classify sessions.
- Produce reusable CSV/TXT reports and interactive visualizations.
- Present the results through an interactive Streamlit dashboard.

## Dataset Overview

The generated dataset contains **500 synthetic work-session records**, covering **10 developer IDs** and **5 task types**.

The dataset contains 12 columns:

| Column | Description |
|---|---|
| `session_id` | Unique work-session identifier |
| `developer_id` | Synthetic developer identifier |
| `date` | Session date |
| `start_hour` | Session start hour |
| `task_type` | Coding, Debugging, Code Review, Testing, or Documentation |
| `session_duration_min` | Total session duration in minutes |
| `focus_duration_min` | Focus duration in minutes |
| `interruptions` | Number of interruptions during the session |
| `task_switches` | Number of task switches during the session |
| `task_complexity` | Low, Medium, or High |
| `cognitive_load_rating` | Illustrative rating on a 1–5 scale |
| `tasks_completed` | Number of tasks completed in the session |

The data-generation script uses a fixed random seed to make the generated sample reproducible.

## Technology Stack

- **Programming Language:** Python
- **Data Processing:** Pandas, NumPy
- **Statistical Analysis:** SciPy
- **Data Visualization:** Matplotlib, Seaborn, Plotly
- **Dashboard:** Streamlit
- **Development Tools:** VS Code, Git, GitHub

## Project Structure

```text
CogniStream-Developer-Flow-State-Analytics/
│
├── data/
│   ├── raw/
│   │   └── developer_activity.csv
│   │
│   └── processed/
│       ├── developer_activity_cleaned.csv
│       ├── developer_productivity_metrics.csv
│       ├── developer_productivity_classified.csv
│       ├── focus_efficiency_summary.csv
│       ├── focus_session_summary.csv
│       ├── productivity_by_cognitive_load.csv
│       ├── productivity_by_task_type_and_load.csv
│       ├── task_complexity_distribution.csv
│       ├── task_complexity_summary.csv
│       ├── task_switching_summary.csv
│       └── task_type_productivity_summary.csv
│
├── src/
│   ├── data_generation.py
│   ├── data_cleaning.py
│   ├── data_quality_report.py
│   ├── eda_analysis.py
│   ├── statistical_analysis.py
│   ├── productivity_metrics.py
│   ├── focus_efficiency_analysis.py
│   ├── focus_interruption_analysis.py
│   ├── focus_session_analysis.py
│   ├── cognitive_load_analysis.py
│   ├── productivity_classification.py
│   ├── productivity_insights.py
│   ├── developer_productivity_distribution.py
│   ├── time_based_productivity_analysis.py
│   ├── developer_workload_analysis.py
│   ├── session_duration_variability_analysis.py
│   ├── task_complexity_analysis.py
│   ├── task_complexity_completion_analysis.py
│   ├── task_switching_analysis.py
│   ├── task_switching_completion_analysis.py
│   ├── interruption_completion_analysis.py
│   ├── task_type_productivity_analysis.py
│   ├── productivity_cognitive_load_analysis.py
│   ├── developer_work_insights.py
│   └── work_pattern_visualization.py
│
├── dashboard/
│   └── app.py
│
├── reports/
├── figures/
├── notebooks/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

*The `reports/` and `figures/` folders contain generated reports and visualizations. Exact output files depend on which analysis scripts have been executed.*

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/amalms-ai/CogniStream-Developer-Flow-State-Analytics.git
cd CogniStream-Developer-Flow-State-Analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Check Dependencies

```bash
python -m pip check
```

## Running the Project

Run the following commands from the project root directory with the virtual environment activated.

### Step 1: Generate the Dataset

```bash
python src/data_generation.py
```

This generates the raw synthetic dataset:

`data/raw/developer_activity.csv`

### Step 2: Clean the Dataset

```bash
python src/data_cleaning.py
```

This validates and cleans the raw dataset and generates:

`data/processed/developer_activity_cleaned.csv`

### Step 3: Generate the Data Quality Report

```bash
python src/data_quality_report.py
```

### Step 4: Run Core Analytics

```bash
python src/eda_analysis.py
python src/statistical_analysis.py
python src/productivity_metrics.py
```

### Step 5: Run Focus, Cognitive Load, and Advanced Analytics

```bash
python src/focus_efficiency_analysis.py
python src/focus_interruption_analysis.py
python src/focus_session_analysis.py
python src/cognitive_load_analysis.py
python src/productivity_classification.py
python src/productivity_insights.py
python src/developer_productivity_distribution.py
python src/time_based_productivity_analysis.py
python src/developer_workload_analysis.py
python src/session_duration_variability_analysis.py
python src/task_complexity_analysis.py
python src/task_complexity_completion_analysis.py
python src/task_switching_analysis.py
python src/task_switching_completion_analysis.py
python src/interruption_completion_analysis.py
```

Additional analysis scripts available in the source folder:

```bash
python src/task_type_productivity_analysis.py
python src/productivity_cognitive_load_analysis.py
python src/developer_work_insights.py
python src/work_pattern_visualization.py
```

Run these additional scripts after their required input files have been generated. If a script reports a missing input file, run its prerequisite analysis first.

### Step 6: Launch the Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

Open the local address displayed in the terminal, normally:

`http://localhost:8501`

## Dashboard Features

The interactive Streamlit dashboard includes:

1. **Developer Activity Overview** – Displays total sessions, average focus duration, average cognitive load, and total interruptions.
2. **Focus Duration by Task Type** – Compares average focus duration across task categories.
3. **Cognitive Load by Task Type** – Compares average cognitive-load ratings by task type.
4. **Completed Tasks by Task Type** – Displays completed task totals for each task category.
5. **Developer Performance Comparison** – Presents developer-level metrics in a comparison table.
6. **Developer-wise Analytics** – Compares completed tasks, focus duration, interruptions, and cognitive-load ratings by developer.
7. **Productivity Classification** – Displays High, Moderate, and Low Productivity session counts and their distribution.
8. **Productivity Performance Summary** – Compares focus duration, tasks completed, interruptions, and cognitive load across productivity categories.
9. **Filtered Dataset Preview and CSV Download** – Allows users to inspect and download filtered records.

The dashboard provides a task-type filter in the sidebar and uses interactive Plotly visualizations.

## Project Results

The following results were observed when the project scripts were executed using the generated 500-session dataset.

| Metric | Result |
|---|---:|
| Total Sessions | 500 |
| Unique Developers | 10 |
| Average Session Duration | 76.33 minutes |
| Average Focus Duration | 43.63 minutes |
| Average Focus Efficiency | 57.77% |
| Average Interruptions | 5.14 |
| Average Task Switches | 4.11 |
| Average Cognitive Load | 3.13 / 5 |
| Average Tasks Completed | 2.38 |
| Average Tasks per Hour | 2.14 |

### Productivity Classification Results

| Productivity Category | Sessions |
|---|---:|
| High Productivity | 94 |
| Moderate Productivity | 317 |
| Low Productivity | 89 |
| **Total** | **500** |

### Productivity Performance Summary

| Category | Average Focus Duration (min) | Average Tasks Completed | Average Interruptions | Average Cognitive Load |
|---|---:|---:|---:|---:|
| High Productivity | 68.22 | 4.09 | 3.74 | 3.03 |
| Moderate Productivity | 42.50 | 2.35 | 5.26 | 3.13 |
| Low Productivity | 21.69 | 0.70 | 6.21 | 3.22 |

### Key Analytical Observations

- Code Review had an average focus duration of approximately 45.76 minutes.
- Debugging had an average focus duration of approximately 46.60 minutes.
- The observed correlation between interruptions and focus duration was approximately 0.010.
- The observed correlation between task switches and focus duration was approximately -0.090.

These are descriptive results from one synthetic dataset. Correlation does not establish causation, and the results should not be interpreted as universal developer-work patterns.

## Generated Outputs

Depending on the analysis script, the project generates:

- Cleaned and derived CSV datasets in `data/processed/`.
- Text summaries and CSV reports in `reports/`.
- Static chart images and interactive Plotly HTML charts in `figures/`.
- An interactive Streamlit dashboard in `dashboard/app.py`.

## Limitations

- The dataset is synthetic and does not represent actual developer activity.
- Cognitive-load ratings are illustrative numeric values, not clinical or validated psychological assessments.
- Productivity classification depends on the project's scoring formula and thresholds.
- Results describe the generated sample only.
- The results should not be used to rank real employees or make employment decisions.
- Correlation shows association, not cause and effect.

## Future Improvements

- Add date-range and developer-level dashboard filters.
- Add task-switching, interruption, and time-based productivity charts directly to the dashboard.
- Add automated tests for data validation and analysis functions.
- Add dashboard screenshots and a project demonstration video.
- Explore additional statistical methods with clearly stated assumptions.

## Author

**Amal M S**

- GitHub: https://github.com/amalms-ai

---

**Project:** CogniStream – Developer Flow-State & Cognitive Load Analytics

**Purpose:** A data analytics learning project using synthetic developer activity data.

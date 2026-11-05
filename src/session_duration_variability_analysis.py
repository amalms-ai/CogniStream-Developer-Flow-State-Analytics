from pathlib import Path
import pandas as pd
import plotly.express as px

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

REPORT_DIR = BASE_DIR / "reports"
FIGURE_DIR = BASE_DIR / "figures"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


# Step 1: Load dataset
print("Loading developer activity dataset...")

df = pd.read_csv(DATA_FILE)

required_columns = [
    "developer_id",
    "task_type",
    "session_duration_min"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# Step 2: Clean data
df["session_duration_min"] = pd.to_numeric(
    df["session_duration_min"],
    errors="coerce"
)

df = df.dropna(
    subset=[
        "developer_id",
        "task_type",
        "session_duration_min"
    ]
)

df = df[
    df["session_duration_min"] > 0
].copy()

if df.empty:
    raise ValueError("No valid session records found.")

print(f"Valid sessions: {len(df)}")


# Step 3: Create a reusable variability analysis function
def calculate_variability(data, group_column):

    results = []

    for group_name, group in data.groupby(group_column):

        durations = group["session_duration_min"]

        mean_duration = durations.mean()
        std_duration = durations.std()

        q1 = durations.quantile(0.25)
        q3 = durations.quantile(0.75)

        iqr = q3 - q1

        lower_limit = q1 - (1.5 * iqr)
        upper_limit = q3 + (1.5 * iqr)

        outlier_count = (
            (durations < lower_limit) |
            (durations > upper_limit)
        ).sum()

        cv = (
            (std_duration / mean_duration) * 100
            if mean_duration != 0 and pd.notna(std_duration)
            else 0
        )

        results.append({
            group_column: group_name,
            "session_count": len(durations),
            "mean_duration": mean_duration,
            "median_duration": durations.median(),
            "std_duration": std_duration,
            "minimum_duration": durations.min(),
            "maximum_duration": durations.max(),
            "q1_duration": q1,
            "q3_duration": q3,
            "iqr_duration": iqr,
            "coefficient_of_variation": cv,
            "outlier_count": outlier_count
        })

    return pd.DataFrame(results)


# Step 4: Analyze developers
print("\nAnalyzing session duration by developer...")

developer_analysis = calculate_variability(
    df,
    "developer_id"
)

developer_analysis = developer_analysis.sort_values(
    "coefficient_of_variation",
    ascending=False
)

developer_analysis.to_csv(
    REPORT_DIR / "developer_session_variability.csv",
    index=False
)


# Step 5: Analyze task types
print("Analyzing session duration by task type...")

task_analysis = calculate_variability(
    df,
    "task_type"
)

task_analysis = task_analysis.sort_values(
    "coefficient_of_variation",
    ascending=False
)

task_analysis.to_csv(
    REPORT_DIR / "task_session_variability.csv",
    index=False
)


# Step 6: Developer session duration boxplot
fig1 = px.box(
    df,
    x="developer_id",
    y="session_duration_min",
    color="developer_id",
    title="Session Duration Variability Across Developers",
    labels={
        "developer_id": "Developer",
        "session_duration_min": "Session Duration (Minutes)"
    },
    points="outliers"
)

fig1.update_layout(
    template="plotly_white",
    showlegend=False
)

fig1.write_html(
    FIGURE_DIR / "developer_session_variability.html"
)


# Step 7: Task type session duration boxplot
fig2 = px.box(
    df,
    x="task_type",
    y="session_duration_min",
    color="task_type",
    title="Session Duration Variability Across Task Types",
    labels={
        "task_type": "Task Type",
        "session_duration_min": "Session Duration (Minutes)"
    },
    points="outliers"
)

fig2.update_layout(
    template="plotly_white",
    showlegend=False
)

fig2.write_html(
    FIGURE_DIR / "task_session_variability.html"
)


# Step 8: Generate text report
report = []

report.append("COGNISTREAM - SESSION DURATION VARIABILITY ANALYSIS")
report.append("=" * 60)

report.append(f"Total valid sessions: {len(df)}")

report.append(
    f"Overall average duration: "
    f"{df['session_duration_min'].mean():.2f} minutes"
)

report.append(
    f"Overall median duration: "
    f"{df['session_duration_min'].median():.2f} minutes"
)

report.append("\nDEVELOPER SESSION VARIABILITY")
report.append("-" * 60)

for _, row in developer_analysis.iterrows():

    report.append(
        f"\nDeveloper: {row['developer_id']}"
    )

    report.append(
        f"Sessions: {row['session_count']}"
    )

    report.append(
        f"Average Duration: {row['mean_duration']:.2f} minutes"
    )

    report.append(
        f"Median Duration: {row['median_duration']:.2f} minutes"
    )

    report.append(
        f"Duration Variation (CV): "
        f"{row['coefficient_of_variation']:.2f}%"
    )

    report.append(
        f"Outlier Sessions: {row['outlier_count']}"
    )


report.append("\nTASK TYPE SESSION VARIABILITY")
report.append("-" * 60)

for _, row in task_analysis.iterrows():

    report.append(
        f"\nTask Type: {row['task_type']}"
    )

    report.append(
        f"Average Duration: {row['mean_duration']:.2f} minutes"
    )

    report.append(
        f"Median Duration: {row['median_duration']:.2f} minutes"
    )

    report.append(
        f"Duration Variation (CV): "
        f"{row['coefficient_of_variation']:.2f}%"
    )

    report.append(
        f"Outlier Sessions: {row['outlier_count']}"
    )


report.append(
    "\nNote: High session duration variation indicates less "
    "consistency in recorded session lengths. Outliers are "
    "statistical observations and do not automatically indicate errors."
)

with open(
    REPORT_DIR / "session_duration_variability_report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write("\n".join(report))


# Step 9: Completion message
print("\nDAY 23 ANALYSIS COMPLETED SUCCESSFULLY!")

print("\nGenerated files:")
print("- reports/developer_session_variability.csv")
print("- reports/task_session_variability.csv")
print("- reports/session_duration_variability_report.txt")
print("- figures/developer_session_variability.html")
print("- figures/task_session_variability.html")
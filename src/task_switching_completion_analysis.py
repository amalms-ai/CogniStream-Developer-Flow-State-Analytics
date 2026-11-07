import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------------
# 1. Project paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed"
    / "developer_activity_cleaned.csv"
)

REPORT_DIR = BASE_DIR / "reports"
FIGURE_DIR = BASE_DIR / "figures"

REPORT_DIR.mkdir(exist_ok=True)
FIGURE_DIR.mkdir(exist_ok=True)

# -----------------------------------
# 2. Load dataset
# -----------------------------------

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully!")
print("Total records:", len(df))

# -----------------------------------
# 3. Check required columns
# -----------------------------------

required_columns = [
    "task_switches",
    "tasks_completed",
    "session_duration_min",
    "focus_duration_min"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )

# -----------------------------------
# 4. Data preparation
# -----------------------------------

numeric_columns = [
    "task_switches",
    "tasks_completed",
    "session_duration_min",
    "focus_duration_min"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(
        df[col], errors="coerce"
    )

df = df.dropna(subset=required_columns)

df = df[
    (df["task_switches"] >= 0) &
    (df["tasks_completed"] >= 0) &
    (df["session_duration_min"] > 0) &
    (df["focus_duration_min"] >= 0)
]

# -----------------------------------
# 5. Calculate completion rate
# -----------------------------------

df["tasks_completed_per_hour"] = (
    df["tasks_completed"] /
    df["session_duration_min"]
) * 60

# -----------------------------------
# 6. Group by task switches
# -----------------------------------

switching_summary = (
    df.groupby("task_switches")
    .agg(
        total_sessions=("task_switches", "count"),
        avg_tasks_completed=("tasks_completed", "mean"),
        avg_focus_duration=("focus_duration_min", "mean"),
        avg_session_duration=("session_duration_min", "mean"),
        avg_completion_rate=("tasks_completed_per_hour", "mean")
    )
    .reset_index()
    .sort_values("task_switches")
)

print("\nTask Switching Analysis:")
print(switching_summary.round(2))

# -----------------------------------
# 7. Task type comparison
# -----------------------------------

if "task_type" in df.columns:

    task_type_summary = (
        df.groupby("task_type")
        .agg(
            total_sessions=("task_type", "count"),
            avg_task_switches=("task_switches", "mean"),
            avg_tasks_completed=("tasks_completed", "mean"),
            avg_completion_rate=("tasks_completed_per_hour", "mean")
        )
        .reset_index()
    )

    task_type_summary.to_csv(
        REPORT_DIR / "task_switching_by_task_type.csv",
        index=False
    )

# -----------------------------------
# 8. Save CSV report
# -----------------------------------

switching_summary.to_csv(
    REPORT_DIR / "task_switching_completion_summary.csv",
    index=False
)

# -----------------------------------
# 9. Generate text report
# -----------------------------------

report = []

report.append(
    "COGNISTREAM - TASK SWITCHING AND COMPLETION ANALYSIS"
)

report.append("=" * 60)

report.append(
    f"\nTotal sessions analyzed: {len(df)}"
)

report.append(
    f"Average task switches: {df['task_switches'].mean():.2f}"
)

report.append(
    f"Average tasks completed: {df['tasks_completed'].mean():.2f}"
)

report.append(
    f"Average completion rate: {df['tasks_completed_per_hour'].mean():.2f}"
)

report.append("\nCOMPARISON BY TASK SWITCH COUNT")
report.append("-" * 60)

for _, row in switching_summary.iterrows():

    report.append(
        f"\nTask switches: {row['task_switches']}"
    )

    report.append(
        f"Sessions: {row['total_sessions']}"
    )

    report.append(
        f"Average tasks completed: {row['avg_tasks_completed']:.2f}"
    )

    report.append(
        f"Average completion rate: {row['avg_completion_rate']:.2f}"
    )

report.append("\nNote: Results describe synthetic developer activity data.")

with open(
    REPORT_DIR / "task_switching_completion_report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write("\n".join(report))

# -----------------------------------
# 10. Plotly chart 1
# -----------------------------------

fig1 = px.bar(
    switching_summary,
    x="task_switches",
    y="avg_tasks_completed",
    title="Average Tasks Completed by Task Switch Count",
    labels={
        "task_switches": "Number of Task Switches",
        "avg_tasks_completed": "Average Tasks Completed"
    },
    text_auto=".2f"
)

fig1.write_html(
    FIGURE_DIR / "task_switching_vs_tasks_completed.html"
)

# -----------------------------------
# 11. Plotly chart 2
# -----------------------------------

fig2 = px.line(
    switching_summary,
    x="task_switches",
    y="avg_completion_rate",
    markers=True,
    title="Task Completion Rate by Task Switch Count",
    labels={
        "task_switches": "Number of Task Switches",
        "avg_completion_rate": "Tasks Completed Per Hour"
    }
)

fig2.write_html(
    FIGURE_DIR / "task_switching_completion_rate.html"
)

# -----------------------------------
# 12. Final output
# -----------------------------------

print("\nDay 25 analysis completed!")

print("\nGenerated files:")
print("1. task_switching_completion_summary.csv")
print("2. task_switching_by_task_type.csv")
print("3. task_switching_completion_report.txt")
print("4. task_switching_vs_tasks_completed.html")
print("5. task_switching_completion_rate.html")
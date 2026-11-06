import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

# -----------------------------------------
# 1. Project paths
# -----------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "developer_activity_cleaned.csv"

REPORT_DIR = BASE_DIR / "reports"
FIGURE_DIR = BASE_DIR / "figures"

REPORT_DIR.mkdir(exist_ok=True)
FIGURE_DIR.mkdir(exist_ok=True)

# -----------------------------------------
# 2. Load dataset
# -----------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully!")
print("Total records:", len(df))

# -----------------------------------------
# 3. Check required columns
# -----------------------------------------

required_columns = [
    "task_complexity",
    "tasks_completed",
    "session_duration_min",
    "focus_duration_min"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# -----------------------------------------
# 4. Data preparation
# -----------------------------------------

df["task_complexity"] = (
    df["task_complexity"].astype(str).str.strip().str.title()
)

numeric_columns = [
    "tasks_completed",
    "session_duration_min",
    "focus_duration_min"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=required_columns)

df = df[df["session_duration_min"] > 0]

# -----------------------------------------
# 5. Calculate completion rate
# -----------------------------------------

df["tasks_completed_per_hour"] = (
    df["tasks_completed"] /
    df["session_duration_min"]
) * 60

# -----------------------------------------
# 6. Group by task complexity
# -----------------------------------------

complexity_summary = (
    df.groupby("task_complexity")
    .agg(
        total_sessions=("task_complexity", "count"),
        total_tasks_completed=("tasks_completed", "sum"),
        avg_tasks_completed=("tasks_completed", "mean"),
        avg_session_duration=("session_duration_min", "mean"),
        avg_focus_duration=("focus_duration_min", "mean"),
        avg_completion_rate=("tasks_completed_per_hour", "mean")
    )
    .reset_index()
)

print("\nTask Complexity Analysis:")
print(complexity_summary.round(2))

# -----------------------------------------
# 7. Group by task type and complexity
# -----------------------------------------

if "task_type" in df.columns:

    task_type_summary = (
        df.groupby(["task_complexity", "task_type"])
        .agg(
            total_sessions=("task_type", "count"),
            avg_tasks_completed=("tasks_completed", "mean"),
            avg_focus_duration=("focus_duration_min", "mean"),
            avg_session_duration=("session_duration_min", "mean")
        )
        .reset_index()
    )

    task_type_summary.to_csv(
        REPORT_DIR / "complexity_task_type_summary.csv",
        index=False
    )

# -----------------------------------------
# 8. Save CSV report
# -----------------------------------------

complexity_summary.to_csv(
    REPORT_DIR / "task_complexity_completion_summary.csv",
    index=False
)

# -----------------------------------------
# 9. Generate text report
# -----------------------------------------

report_lines = []

report_lines.append(
    "COGNISTREAM - TASK COMPLEXITY AND COMPLETION ANALYSIS"
)

report_lines.append("=" * 60)

report_lines.append(
    f"\nTotal valid sessions analyzed: {len(df)}"
)

for _, row in complexity_summary.iterrows():

    report_lines.append(
        f"\nTask Complexity: {row['task_complexity']}"
    )

    report_lines.append(
        f"Total Sessions: {row['total_sessions']}"
    )

    report_lines.append(
        f"Total Tasks Completed: {row['total_tasks_completed']}"
    )

    report_lines.append(
        f"Average Tasks Completed: {row['avg_tasks_completed']:.2f}"
    )

    report_lines.append(
        f"Average Session Duration: {row['avg_session_duration']:.2f} minutes"
    )

    report_lines.append(
        f"Average Focus Duration: {row['avg_focus_duration']:.2f} minutes"
    )

    report_lines.append(
        f"Average Tasks Completed Per Hour: {row['avg_completion_rate']:.2f}"
    )

report_lines.append("\n" + "=" * 60)

report_lines.append(
    "\nNote: These results describe patterns in synthetic developer activity data."
)

report_path = REPORT_DIR / "task_complexity_completion_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write("\n".join(report_lines))

# -----------------------------------------
# 10. Create interactive Plotly chart
# -----------------------------------------

fig = px.bar(
    complexity_summary,
    x="task_complexity",
    y="avg_tasks_completed",
    color="task_complexity",
    title="Average Tasks Completed by Task Complexity",
    labels={
        "task_complexity": "Task Complexity",
        "avg_tasks_completed": "Average Tasks Completed"
    },
    text_auto=".2f"
)

fig.write_html(
    FIGURE_DIR / "complexity_vs_task_completion.html"
)

# -----------------------------------------
# 11. Create second visualization
# -----------------------------------------

fig2 = px.bar(
    complexity_summary,
    x="task_complexity",
    y="avg_completion_rate",
    color="task_complexity",
    title="Task Completion Rate by Complexity",
    labels={
        "task_complexity": "Task Complexity",
        "avg_completion_rate": "Tasks Completed Per Hour"
    },
    text_auto=".2f"
)

fig2.write_html(
    FIGURE_DIR / "complexity_completion_rate.html"
)

# -----------------------------------------
# 12. Final output
# -----------------------------------------

print("\nAnalysis completed successfully!")

print("\nGenerated files:")
print("1. task_complexity_completion_summary.csv")
print("2. complexity_task_type_summary.csv")
print("3. task_complexity_completion_report.txt")
print("4. complexity_vs_task_completion.html")
print("5. complexity_completion_rate.html")
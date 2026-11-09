import pandas as pd
import plotly.express as px
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "developer_activity_cleaned.csv"
REPORT_DIR = BASE_DIR / "reports"
FIGURE_DIR = BASE_DIR / "figures"

REPORT_DIR.mkdir(exist_ok=True)
FIGURE_DIR.mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)

# Required columns
required_columns = [
    "interruptions",
    "tasks_completed",
    "session_duration_min",
    "task_type"
]

# Check columns
missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

# Convert columns to numeric
numeric_columns = [
    "interruptions",
    "tasks_completed",
    "session_duration_min"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Clean data
df = df.dropna(subset=required_columns)

df = df[
    (df["interruptions"] >= 0) &
    (df["tasks_completed"] >= 0) &
    (df["session_duration_min"] > 0)
].copy()

if df.empty:
    raise ValueError("No valid records available for analysis.")

# Calculate task completion efficiency
df["tasks_completed_per_hour"] = (
    df["tasks_completed"] / df["session_duration_min"]
) * 60

# Group by interruption count
interruption_summary = (
    df.groupby("interruptions")
    .agg(
        total_sessions=("tasks_completed", "count"),
        avg_tasks_completed=("tasks_completed", "mean"),
        avg_session_duration=("session_duration_min", "mean"),
        avg_completion_rate=("tasks_completed_per_hour", "mean")
    )
    .reset_index()
)

# Round numerical values
interruption_summary = interruption_summary.round(2)

# Save summary CSV
interruption_summary.to_csv(
    REPORT_DIR / "interruption_completion_summary.csv",
    index=False
)

# Task-type comparison
task_type_summary = (
    df.groupby("task_type")
    .agg(
        total_sessions=("tasks_completed", "count"),
        avg_interruptions=("interruptions", "mean"),
        avg_tasks_completed=("tasks_completed", "mean"),
        avg_completion_rate=("tasks_completed_per_hour", "mean")
    )
    .reset_index()
    .round(2)
)

task_type_summary.to_csv(
    REPORT_DIR / "interruption_by_task_type.csv",
    index=False
)

# Generate text report
report_path = REPORT_DIR / "interruption_completion_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write("INTERRUPTION VS TASK COMPLETION ANALYSIS\n")
    file.write("=" * 45 + "\n\n")

    file.write(f"Total sessions analyzed: {len(df)}\n\n")

    file.write("Overall Average Metrics:\n")
    file.write(
        f"Average interruptions: {df['interruptions'].mean():.2f}\n"
    )
    file.write(
        f"Average tasks completed: {df['tasks_completed'].mean():.2f}\n"
    )
    file.write(
        f"Average completion rate: "
        f"{df['tasks_completed_per_hour'].mean():.2f} tasks/hour\n\n"
    )

    file.write("Interruption Level Summary:\n")
    file.write(interruption_summary.to_string(index=False))

    file.write("\n\nTask Type Summary:\n")
    file.write(task_type_summary.to_string(index=False))

# Chart 1: Interruptions vs tasks completed
fig1 = px.bar(
    interruption_summary,
    x="interruptions",
    y="avg_tasks_completed",
    title="Interruptions vs Average Tasks Completed",
    labels={
        "interruptions": "Number of Interruptions",
        "avg_tasks_completed": "Average Tasks Completed"
    },
    hover_data=["total_sessions"]
)

fig1.write_html(
    FIGURE_DIR / "interruptions_vs_tasks_completed.html"
)

# Chart 2: Interruptions vs completion rate
fig2 = px.line(
    interruption_summary,
    x="interruptions",
    y="avg_completion_rate",
    markers=True,
    title="Interruptions vs Task Completion Rate",
    labels={
        "interruptions": "Number of Interruptions",
        "avg_completion_rate": "Tasks Completed per Hour"
    }
)

fig2.write_html(
    FIGURE_DIR / "interruptions_vs_completion_rate.html"
)

print("Day 26 analysis completed successfully!")
print("Total valid sessions:", len(df))
print("CSV reports generated.")
print("Text report generated.")
print("Interactive Plotly charts generated.")
from pathlib import Path
import pandas as pd
import plotly.express as px

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "processed" / "developer_activity_cleaned.csv"

REPORT_DIR = BASE_DIR / "reports"
FIGURE_DIR = BASE_DIR / "figures"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


# Step 1: Load dataset
print("Loading developer activity dataset...")

df = pd.read_csv(DATA_FILE)

# Required columns
required_columns = [
    "developer_id",
    "task_type",
    "session_duration_min"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")


# Step 2: Clean data
df["session_duration_min"] = pd.to_numeric(
    df["session_duration_min"], errors="coerce"
)

df = df.dropna(
    subset=["developer_id", "task_type", "session_duration_min"]
)

df = df[df["session_duration_min"] >= 0].copy()

if df.empty:
    raise ValueError("No valid records available for analysis.")

print(f"Valid records: {len(df)}")


# Step 3: Calculate developer workload
workload = (
    df.groupby("developer_id")
    .agg(
        total_sessions=("developer_id", "size"),
        total_work_duration=("session_duration_min", "sum"),
        average_session_duration=("session_duration_min", "mean"),
        task_type_count=("task_type", "nunique")
    )
    .reset_index()
)

# Calculate workload percentage
total_sessions = workload["total_sessions"].sum()

workload["workload_percentage"] = (
    workload["total_sessions"] / total_sessions
) * 100

# Step 4: Categorize workload using relative session counts
median_sessions = workload["total_sessions"].median()

workload["workload_category"] = workload[
    "total_sessions"
].apply(
    lambda count:
    "Low" if count < median_sessions * 0.8
    else "High" if count > median_sessions * 1.2
    else "Moderate"
)

workload = workload.sort_values(
    "total_sessions", ascending=False
)

workload.to_csv(
    REPORT_DIR / "developer_workload_summary.csv",
    index=False
)

print("\nDeveloper workload summary generated.")


# Step 5: Analyze task distribution by developer
task_distribution = (
    df.groupby(["developer_id", "task_type"])
    .size()
    .reset_index(name="session_count")
)

task_distribution.to_csv(
    REPORT_DIR / "developer_task_distribution.csv",
    index=False
)

print("Developer task distribution generated.")


# Step 6: Create workload distribution chart
fig1 = px.bar(
    workload,
    x="developer_id",
    y="total_sessions",
    color="workload_category",
    text="total_sessions",
    title="Developer Workload Distribution",
    labels={
        "developer_id": "Developer",
        "total_sessions": "Total Sessions",
        "workload_category": "Workload Category"
    },
    hover_data=[
        "total_work_duration",
        "average_session_duration",
        "workload_percentage"
    ]
)

fig1.update_layout(
    xaxis_title="Developer ID",
    yaxis_title="Total Sessions",
    template="plotly_white"
)

fig1.write_html(
    FIGURE_DIR / "developer_workload_distribution.html"
)


# Step 7: Create task distribution chart
fig2 = px.bar(
    task_distribution,
    x="developer_id",
    y="session_count",
    color="task_type",
    title="Task Distribution Across Developers",
    labels={
        "developer_id": "Developer",
        "session_count": "Number of Sessions",
        "task_type": "Task Type"
    },
    barmode="stack"
)

fig2.update_layout(
    xaxis_title="Developer ID",
    yaxis_title="Number of Sessions",
    template="plotly_white"
)

fig2.write_html(
    FIGURE_DIR / "developer_task_distribution.html"
)


# Step 8: Generate text report
top_developer = workload.iloc[0]

report = []

report.append("COGNISTREAM - DEVELOPER WORKLOAD ANALYSIS")
report.append("=" * 50)

report.append(f"Total valid sessions: {len(df)}")
report.append(f"Total developers: {workload['developer_id'].nunique()}")

report.append("\nDEVELOPER WORKLOAD SUMMARY")
report.append("-" * 50)

for _, row in workload.iterrows():

    report.append(
        f"\nDeveloper: {row['developer_id']}"
    )

    report.append(
        f"Total Sessions: {row['total_sessions']}"
    )

    report.append(
        f"Total Work Duration: {row['total_work_duration']:.2f} minutes"
    )

    report.append(
        f"Average Session Duration: {row['average_session_duration']:.2f} minutes"
    )

    report.append(
        f"Workload Percentage: {row['workload_percentage']:.2f}%"
    )

    report.append(
        f"Workload Category: {row['workload_category']}"
    )

report.append("\nHIGHEST SESSION VOLUME")
report.append("-" * 50)

report.append(
    f"Developer: {top_developer['developer_id']}"
)

report.append(
    f"Total Sessions: {top_developer['total_sessions']}"
)

report.append(
    "\nNote: Workload categories are based on relative session counts. "
    "They indicate recorded workload volume, not employee performance "
    "or individual effort."
)

report_path = REPORT_DIR / "developer_workload_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write("\n".join(report))


# Step 9: Completion message
print("\nDAY 22 ANALYSIS COMPLETED SUCCESSFULLY!")

print("\nGenerated files:")
print("- reports/developer_workload_summary.csv")
print("- reports/developer_task_distribution.csv")
print("- reports/developer_workload_report.txt")
print("- figures/developer_workload_distribution.html")
print("- figures/developer_task_distribution.html")
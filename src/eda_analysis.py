"""
CogniStream: Developer Flow-State & Cognitive Load Analytics

Day 3:
Exploratory Data Analysis (EDA)
"""

from pathlib import Path

import pandas as pd


# Locate project folders.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

REPORT_FILE = PROJECT_ROOT / "reports" / "eda_summary.txt"


def perform_eda():
    """Explore and summarize the cleaned developer dataset."""

    # Load cleaned data.
    df = pd.read_csv(DATA_FILE)

    # Convert date to datetime.
    df["date"] = pd.to_datetime(df["date"])

    print("=" * 55)
    print("COGNISTREAM - EXPLORATORY DATA ANALYSIS")
    print("=" * 55)

    # 1. Dataset overview.
    print("\n1. DATASET OVERVIEW")
    print("-" * 30)
    print(f"Total sessions: {len(df)}")
    print(f"Unique developers: {df['developer_id'].nunique()}")
    print(f"Total columns: {len(df.columns)}")
    print(
        f"Date range: {df['date'].min().date()} "
        f"to {df['date'].max().date()}"
    )

    # 2. Numerical summary.
    numerical_columns = [
        "session_duration_min",
        "focus_duration_min",
        "interruptions",
        "task_switches",
        "cognitive_load_rating",
        "tasks_completed",
    ]

    print("\n2. NUMERICAL SUMMARY")
    print("-" * 30)

    numerical_summary = df[numerical_columns].describe().round(2)
    print(numerical_summary)

    # 3. Average metrics.
    print("\n3. KEY METRICS")
    print("-" * 30)

    average_session = df["session_duration_min"].mean()
    average_focus = df["focus_duration_min"].mean()
    average_interruptions = df["interruptions"].mean()
    average_switches = df["task_switches"].mean()
    average_workload = df["cognitive_load_rating"].mean()

    print(f"Average session duration: {average_session:.2f} minutes")
    print(f"Average focus duration: {average_focus:.2f} minutes")
    print(f"Average interruptions: {average_interruptions:.2f}")
    print(f"Average task switches: {average_switches:.2f}")
    print(f"Average cognitive workload rating: {average_workload:.2f}/5")

    # 4. Task type analysis.
    print("\n4. ANALYSIS BY TASK TYPE")
    print("-" * 30)

    task_summary = (
        df.groupby("task_type")
        .agg(
            session_count=("session_id", "count"),
            average_focus_min=("focus_duration_min", "mean"),
            average_interruptions=("interruptions", "mean"),
            average_workload=("cognitive_load_rating", "mean"),
        )
        .round(2)
    )

    print(task_summary)

    # 5. Interruption and focus relationship.
    print("\n5. INTERRUPTIONS AND FOCUS")
    print("-" * 30)

    correlation = df[
        ["interruptions", "focus_duration_min"]
    ].corr().iloc[0, 1]

    print(f"Correlation: {correlation:.3f}")

    # 6. Save the summary report.
    report = [
        "COGNISTREAM - EDA SUMMARY",
        "=" * 40,
        f"Total sessions: {len(df)}",
        f"Unique developers: {df['developer_id'].nunique()}",
        f"Average session duration: {average_session:.2f} minutes",
        f"Average focus duration: {average_focus:.2f} minutes",
        f"Average interruptions: {average_interruptions:.2f}",
        f"Average task switches: {average_switches:.2f}",
        f"Average cognitive workload: {average_workload:.2f}/5",
        f"Interruption-focus correlation: {correlation:.3f}",
        "",
        "Task type summary:",
        task_summary.to_string(),
        "",
        "Numerical summary:",
        numerical_summary.to_string(),
    ]

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print(f"\nEDA summary saved to: {REPORT_FILE}")


if __name__ == "__main__":
    perform_eda()
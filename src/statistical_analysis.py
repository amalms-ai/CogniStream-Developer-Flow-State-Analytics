"""
CogniStream - Day 4
Statistical Analysis of Developer Activity
"""

import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset and report paths
DATA_PATH = BASE_DIR / "data" / "processed" / "developer_activity_cleaned.csv"
REPORT_PATH = BASE_DIR / "reports" / "statistical_analysis.txt"


def perform_statistical_analysis():
    # Load cleaned dataset
    df = pd.read_csv(DATA_PATH)

    # Columns for statistical analysis
    metrics = [
        "session_duration_min",
        "focus_duration_min",
        "interruptions",
        "task_switches",
        "cognitive_load_rating",
        "tasks_completed",
    ]

    # Calculate statistical summary
    summary = df[metrics].describe().round(2)

    # Calculate correlation between numeric metrics
    correlation = df[metrics].corr().round(2)

    # Compare focus duration across task types
    task_analysis = (
        df.groupby("task_type")["focus_duration_min"]
        .agg(["mean", "min", "max", "count"])
        .round(2)
    )

    # Create report
    report = []

    report.append("COGNISTREAM - STATISTICAL ANALYSIS REPORT")
    report.append("=" * 50)

    report.append("\n1. STATISTICAL SUMMARY")
    report.append(summary.to_string())

    report.append("\n2. CORRELATION BETWEEN METRICS")
    report.append(correlation.to_string())

    report.append("\n3. FOCUS DURATION BY TASK TYPE")
    report.append(task_analysis.to_string())

    report_text = "\n".join(report)

    # Save report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report_text, encoding="utf-8")

    print(report_text)
    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    perform_statistical_analysis()
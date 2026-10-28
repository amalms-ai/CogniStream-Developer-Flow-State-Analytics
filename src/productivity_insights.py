from pathlib import Path

import pandas as pd


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

REPORT_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORT_DIR / "productivity_insights.txt"


def main():
    # Check whether the dataset exists
    if not DATA_FILE.exists():
        print(f"Dataset not found: {DATA_FILE}")
        return

    # Load the cleaned dataset
    df = pd.read_csv(DATA_FILE)

    # Required columns
    required_columns = [
        "developer_id",
        "task_type",
        "focus_duration_min",
        "interruptions",
        "task_switches",
        "cognitive_load_rating",
        "tasks_completed",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Missing columns:", ", ".join(missing_columns))
        return

    # Convert required metrics to numeric values
    numeric_columns = [
        "focus_duration_min",
        "interruptions",
        "task_switches",
        "cognitive_load_rating",
        "tasks_completed",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove rows missing essential analysis values
    df = df.dropna(
        subset=[
            "developer_id",
            "focus_duration_min",
            "interruptions",
            "task_switches",
            "cognitive_load_rating",
            "tasks_completed",
        ]
    )

    if df.empty:
        print("No valid records are available for analysis.")
        return

    # Calculate overall productivity metrics
    overall = {
        "Total valid sessions": len(df),
        "Average focus duration": df["focus_duration_min"].mean(),
        "Average interruptions": df["interruptions"].mean(),
        "Average task switches": df["task_switches"].mean(),
        "Average cognitive load": df["cognitive_load_rating"].mean(),
        "Average tasks completed": df["tasks_completed"].mean(),
    }

    # Summarize performance by developer
    developer_summary = (
        df.groupby("developer_id")
        .agg(
            total_sessions=("developer_id", "size"),
            average_focus_duration=("focus_duration_min", "mean"),
            average_interruptions=("interruptions", "mean"),
            average_task_switches=("task_switches", "mean"),
            average_cognitive_load=("cognitive_load_rating", "mean"),
            total_tasks_completed=("tasks_completed", "sum"),
        )
        .reset_index()
    )

    # Summarize performance by task type
    task_summary = (
        df.groupby("task_type")
        .agg(
            average_focus_duration=("focus_duration_min", "mean"),
            average_interruptions=("interruptions", "mean"),
            average_task_switches=("task_switches", "mean"),
            average_cognitive_load=("cognitive_load_rating", "mean"),
            total_tasks_completed=("tasks_completed", "sum"),
        )
        .reset_index()
    )

    # Identify notable patterns
    lowest_focus_task = task_summary.loc[
        task_summary["average_focus_duration"].idxmin()
    ]

    highest_focus_task = task_summary.loc[
        task_summary["average_focus_duration"].idxmax()
    ]

    highest_interruptions_task = task_summary.loc[
        task_summary["average_interruptions"].idxmax()
    ]

    highest_cognitive_load_task = task_summary.loc[
        task_summary["average_cognitive_load"].idxmax()
    ]

    # Create practical recommendations based on the observed data
    recommendations = [
        (
            "Review tasks with the lowest average focus duration "
            f"({lowest_focus_task['task_type']}). Investigate possible "
            "causes before changing the workflow."
        ),
        (
            "Review interruption patterns for "
            f"{highest_interruptions_task['task_type']}, which has "
            "the highest average interruptions."
        ),
        (
            "Examine the workload and complexity of "
            f"{highest_cognitive_load_task['task_type']}, which has "
            "the highest average cognitive load."
        ),
        (
            "Compare task switching with focus duration to identify "
            "patterns that may be worth investigating."
        ),
        (
            "Use these results as exploratory insights rather than "
            "proof of cause and effect."
        ),
    ]

    # Prepare the text report
    lines = [
        "=" * 65,
        "COGNISTREAM: PRODUCTIVITY INSIGHTS REPORT",
        "=" * 65,
        "",
        "DATASET OVERVIEW",
        "-" * 65,
        f"Valid sessions analyzed: {len(df)}",
        f"Unique developers: {df['developer_id'].nunique()}",
        f"Task types analyzed: {df['task_type'].nunique()}",
        "",
        "OVERALL PRODUCTIVITY METRICS",
        "-" * 65,
    ]

    for metric, value in overall.items():
        if isinstance(value, (int,)):
            lines.append(f"{metric}: {value}")
        else:
            lines.append(f"{metric}: {value:.2f}")

    lines.extend([
        "",
        "TASK-TYPE COMPARISON",
        "-" * 65,
        task_summary.round(2).to_string(index=False),
        "",
        "KEY FINDINGS",
        "-" * 65,
        (
            f"Lowest average focus duration: "
            f"{lowest_focus_task['task_type']} "
            f"({lowest_focus_task['average_focus_duration']:.2f} minutes)"
        ),
        (
            f"Highest average focus duration: "
            f"{highest_focus_task['task_type']} "
            f"({highest_focus_task['average_focus_duration']:.2f} minutes)"
        ),
        (
            f"Highest average interruptions: "
            f"{highest_interruptions_task['task_type']} "
            f"({highest_interruptions_task['average_interruptions']:.2f})"
        ),
        (
            f"Highest average cognitive load: "
            f"{highest_cognitive_load_task['task_type']} "
            f"({highest_cognitive_load_task['average_cognitive_load']:.2f})"
        ),
        "",
        "DEVELOPER PERFORMANCE SUMMARY",
        "-" * 65,
        developer_summary.round(2).to_string(index=False),
        "",
        "RECOMMENDATIONS",
        "-" * 65,
    ])

    for number, recommendation in enumerate(
        recommendations,
        start=1
    ):
        lines.append(f"{number}. {recommendation}")

    lines.extend([
        "",
        "NOTE",
        "-" * 65,
        (
            "Interpret these results in the context of the dataset. "
            "If the records are synthetic, they demonstrate the analysis "
            "workflow and do not represent verified real-world behavior."
        ),
        "",
    ])

    # Save the report
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print("Productivity insights report generated successfully.")
    print(f"Report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
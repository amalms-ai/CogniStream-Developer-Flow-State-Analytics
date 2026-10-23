from pathlib import Path

import pandas as pd


# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

OUTPUT_CSV = (
    BASE_DIR
    / "data"
    / "processed"
    / "task_type_productivity_summary.csv"
)

OUTPUT_REPORT = (
    BASE_DIR
    / "reports"
    / "task_type_productivity_analysis.txt"
)


def main():
    # Check whether the input file exists
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "Cleaned dataset not found. "
            "Run src/data_cleaning.py first."
        )

    # Load cleaned data
    df = pd.read_csv(INPUT_FILE)

    # Group data by task type
    summary = (
        df.groupby("task_type")
        .agg(
            session_count=("session_id", "count"),
            average_session_duration_min=(
                "session_duration_min",
                "mean",
            ),
            average_focus_duration_min=(
                "focus_duration_min",
                "mean",
            ),
            average_interruptions=("interruptions", "mean"),
            average_task_switches=("task_switches", "mean"),
            average_cognitive_load=(
                "cognitive_load_rating",
                "mean",
            ),
            average_tasks_completed=("tasks_completed", "mean"),
        )
        .round(2)
        .reset_index()
    )

    # Calculate average focus percentage
    summary["average_focus_percentage"] = (
        summary["average_focus_duration_min"]
        / summary["average_session_duration_min"]
        * 100
    ).round(2)

    # Sort task types by average focus duration
    summary = summary.sort_values(
        by="average_focus_duration_min",
        ascending=False,
    )

    # Identify task types with highest and lowest average focus
    highest_focus_task = summary.iloc[0]
    lowest_focus_task = summary.iloc[-1]

    # Save CSV summary
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_CSV, index=False)

    # Create text report
    report_lines = [
        "COGNISTREAM: TASK-TYPE PRODUCTIVITY ANALYSIS",
        "=" * 50,
        "",
        f"Total sessions analyzed: {len(df)}",
        f"Unique task types: {df['task_type'].nunique()}",
        "",
        "TASK-TYPE SUMMARY",
        "-" * 50,
        summary.to_string(index=False),
        "",
        "KEY FINDINGS",
        "-" * 50,
        (
            "Highest average focus duration: "
            f"{highest_focus_task['task_type']} "
            f"({highest_focus_task['average_focus_duration_min']:.2f} minutes)"
        ),
        (
            "Lowest average focus duration: "
            f"{lowest_focus_task['task_type']} "
            f"({lowest_focus_task['average_focus_duration_min']:.2f} minutes)"
        ),
        "",
        "INTERPRETATION",
        "-" * 50,
        (
            "This report compares work-session metrics across task types. "
            "Higher average focus duration does not automatically mean "
            "higher productivity."
        ),
        (
            "Tasks differ in complexity and purpose. The number of tasks "
            "completed should also be interpreted in context."
        ),
        (
            "This analysis uses synthetic data and does not measure "
            "real developers' performance or mental state."
        ),
    ]

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    # Display results
    print("\nTASK-TYPE PRODUCTIVITY ANALYSIS")
    print("=" * 45)
    print(f"Total sessions: {len(df)}")
    print(f"Unique task types: {df['task_type'].nunique()}")

    print("\nSummary by task type:")
    print(summary.to_string(index=False))

    print("\nKey findings:")
    print(
        f"Highest average focus: {highest_focus_task['task_type']} "
        f"({highest_focus_task['average_focus_duration_min']:.2f} min)"
    )
    print(
        f"Lowest average focus: {lowest_focus_task['task_type']} "
        f"({lowest_focus_task['average_focus_duration_min']:.2f} min)"
    )

    print("\nGenerated files:")
    print(OUTPUT_CSV.relative_to(BASE_DIR))
    print(OUTPUT_REPORT.relative_to(BASE_DIR))


if __name__ == "__main__":
    main()
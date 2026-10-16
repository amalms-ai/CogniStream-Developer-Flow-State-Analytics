import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output paths
INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_productivity_metrics.csv"
)

REPORT_FILE = (
    BASE_DIR
    / "reports"
    / "productivity_metrics.txt"
)


def main():

    # Load cleaned dataset
    df = pd.read_csv(INPUT_FILE)

    print("=" * 55)
    print("COGNISTREAM - PRODUCTIVITY METRICS ANALYSIS")
    print("=" * 55)

    print(f"\nTotal sessions analyzed: {len(df)}")

    # Calculate focus percentage
    df["focus_percentage"] = (
        df["focus_duration_min"]
        / df["session_duration_min"]
    ) * 100

    # Calculate completed tasks per hour
    df["tasks_per_hour"] = (
        df["tasks_completed"]
        / df["session_duration_min"]
    ) * 60

    # Calculate interruptions per hour
    df["interruptions_per_hour"] = (
        df["interruptions"]
        / df["session_duration_min"]
    ) * 60

    # Calculate developer-level metrics
    developer_metrics = (
        df.groupby("developer_id")
        .agg(
            total_sessions=("session_id", "count"),
            avg_session_duration=(
                "session_duration_min", "mean"
            ),
            avg_focus_duration=(
                "focus_duration_min", "mean"
            ),
            avg_focus_percentage=(
                "focus_percentage", "mean"
            ),
            avg_tasks_completed=(
                "tasks_completed", "mean"
            ),
            avg_tasks_per_hour=(
                "tasks_per_hour", "mean"
            ),
            avg_interruptions_per_hour=(
                "interruptions_per_hour", "mean"
            ),
            avg_cognitive_load=(
                "cognitive_load_rating", "mean"
            )
        )
        .round(2)
        .reset_index()
    )

    # Calculate task-type metrics
    task_metrics = (
        df.groupby("task_type")
        .agg(
            total_sessions=("session_id", "count"),
            avg_focus_percentage=(
                "focus_percentage", "mean"
            ),
            avg_tasks_completed=(
                "tasks_completed", "mean"
            ),
            avg_interruptions=(
                "interruptions", "mean"
            ),
            avg_cognitive_load=(
                "cognitive_load_rating", "mean"
            )
        )
        .round(2)
    )

    # Save developer-level metrics
    developer_metrics.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # Prepare report
    report = []

    report.append(
        "COGNISTREAM - PRODUCTIVITY METRICS REPORT"
    )
    report.append("=" * 50)

    report.append(
        f"\nTotal sessions analyzed: {len(df)}"
    )
    report.append(
        f"Unique developers: {df['developer_id'].nunique()}"
    )

    report.append(
        f"\nOverall average focus percentage: "
        f"{df['focus_percentage'].mean():.2f}%"
    )

    report.append(
        f"Average tasks completed per session: "
        f"{df['tasks_completed'].mean():.2f}"
    )

    report.append(
        f"Average tasks per hour: "
        f"{df['tasks_per_hour'].mean():.2f}"
    )

    report.append(
        f"Average interruptions per hour: "
        f"{df['interruptions_per_hour'].mean():.2f}"
    )

    report.append(
        f"Average cognitive load: "
        f"{df['cognitive_load_rating'].mean():.2f}/5"
    )

    report.append(
        "\n\nDEVELOPER-LEVEL METRICS"
    )
    report.append("-" * 50)
    report.append(
        developer_metrics.to_string(index=False)
    )

    report.append(
        "\n\nTASK-TYPE METRICS"
    )
    report.append("-" * 50)
    report.append(task_metrics.to_string())

    # Save text report
    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\nProductivity analysis completed!")

    print(
        f"\nAverage focus percentage: "
        f"{df['focus_percentage'].mean():.2f}%"
    )

    print(
        f"Average tasks per hour: "
        f"{df['tasks_per_hour'].mean():.2f}"
    )

    print(
        f"Average interruptions per hour: "
        f"{df['interruptions_per_hour'].mean():.2f}"
    )

    print(f"\nDeveloper metrics saved to:\n{OUTPUT_FILE}")
    print(f"\nReport saved to:\n{REPORT_FILE}")


if __name__ == "__main__":
    main()
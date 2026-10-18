import pandas as pd
from pathlib import Path

# Locate the project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output files
INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

REPORT_FILE = (
    BASE_DIR
    / "reports"
    / "cognitive_load_analysis.txt"
)


def main():

    # Load cleaned developer activity data
    df = pd.read_csv(INPUT_FILE)

    print("=" * 55)
    print("COGNISTREAM - COGNITIVE LOAD ANALYSIS")
    print("=" * 55)

    print(f"\nTotal sessions analyzed: {len(df)}")

    # Overall cognitive load statistics
    average_load = df["cognitive_load_rating"].mean()

    print(f"Average cognitive load: {average_load:.2f}/5")

    # Group cognitive load by task type
    task_analysis = (
        df.groupby("task_type")
        .agg(
            session_count=("session_id", "count"),
            average_cognitive_load=(
                "cognitive_load_rating", "mean"
            ),
            average_focus_duration=(
                "focus_duration_min", "mean"
            ),
            average_interruptions=(
                "interruptions", "mean"
            ),
            average_task_switches=(
                "task_switches", "mean"
            )
        )
        .round(2)
        .sort_values(
            "average_cognitive_load",
            ascending=False
        )
    )

    # Group cognitive load by rating
    load_distribution = (
        df["cognitive_load_rating"]
        .value_counts()
        .sort_index()
    )

    # Calculate correlations with cognitive load
    correlation_metrics = [
        "cognitive_load_rating",
        "focus_duration_min",
        "interruptions",
        "task_switches",
        "session_duration_min",
        "tasks_completed"
    ]

    correlation_matrix = df[
        correlation_metrics
    ].corr().round(3)

    load_correlations = (
        correlation_matrix["cognitive_load_rating"]
        .drop("cognitive_load_rating")
        .sort_values()
    )

    # Build report
    report = []

    report.append(
        "COGNISTREAM - COGNITIVE LOAD ANALYSIS REPORT"
    )
    report.append("=" * 55)

    report.append(
        f"\nTotal sessions analyzed: {len(df)}"
    )

    report.append(
        f"Average cognitive load: {average_load:.2f}/5"
    )

    report.append(
        "\n\nCOGNITIVE LOAD RATING DISTRIBUTION"
    )
    report.append("-" * 45)
    report.append(load_distribution.to_string())

    report.append(
        "\n\nCOGNITIVE LOAD BY TASK TYPE"
    )
    report.append("-" * 45)
    report.append(task_analysis.to_string())

    report.append(
        "\n\nCORRELATION WITH COGNITIVE LOAD"
    )
    report.append("-" * 45)
    report.append(load_correlations.to_string())

    # Create report directory if needed
    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save report
    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    # Display results
    print("\nCognitive load by task type:")
    print(task_analysis)

    print("\nCorrelations with cognitive load:")
    print(load_correlations)

    print(f"\nReport saved to:\n{REPORT_FILE}")

    print("\nCognitive load analysis completed successfully!")


if __name__ == "__main__":
    main()
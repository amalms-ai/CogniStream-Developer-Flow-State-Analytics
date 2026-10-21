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
    / "focus_efficiency_summary.csv"
)

OUTPUT_REPORT = (
    BASE_DIR
    / "reports"
    / "focus_efficiency_analysis.txt"
)


def main():
    # Check whether the cleaned dataset exists
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {INPUT_FILE}\n"
            "Run src/data_cleaning.py first."
        )

    # Load the cleaned dataset
    df = pd.read_csv(INPUT_FILE)

    # Calculate focus efficiency
    df["focus_efficiency_pct"] = (
        df["focus_duration_min"]
        / df["session_duration_min"]
        * 100
    )

    # Classify sessions by focus efficiency
    df["focus_efficiency_group"] = pd.cut(
        df["focus_efficiency_pct"],
        bins=[-1, 40, 70, 100],
        labels=[
            "Low Efficiency",
            "Moderate Efficiency",
            "High Efficiency",
        ],
        include_lowest=True,
    )

    # Summarize each efficiency group
    summary = (
        df.groupby(
            "focus_efficiency_group",
            observed=False,
        )
        .agg(
            session_count=("session_id", "count"),
            average_focus_efficiency_pct=(
                "focus_efficiency_pct",
                "mean",
            ),
            average_focus_duration_min=(
                "focus_duration_min",
                "mean",
            ),
            average_interruptions=(
                "interruptions",
                "mean",
            ),
            average_task_switches=(
                "task_switches",
                "mean",
            ),
            average_cognitive_load=(
                "cognitive_load_rating",
                "mean",
            ),
        )
        .round(2)
        .reset_index()
    )

    # Save summary as CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_CSV, index=False)

    # Create text report
    total_sessions = len(df)
    average_efficiency = df["focus_efficiency_pct"].mean()
    highest_efficiency = df["focus_efficiency_pct"].max()
    lowest_efficiency = df["focus_efficiency_pct"].min()

    report_lines = [
        "COGNISTREAM: FOCUS EFFICIENCY ANALYSIS",
        "=" * 45,
        "",
        f"Total sessions analyzed: {total_sessions}",
        f"Average focus efficiency: {average_efficiency:.2f}%",
        f"Highest focus efficiency: {highest_efficiency:.2f}%",
        f"Lowest focus efficiency: {lowest_efficiency:.2f}%",
        "",
        "EFFICIENCY GROUP SUMMARY",
        "-" * 45,
        summary.to_string(index=False),
        "",
        "INTERPRETATION",
        "-" * 45,
        (
            "Focus efficiency represents the percentage of a session "
            "spent in focused work, based on the dataset."
        ),
        (
            "Low Efficiency: 40% or less."
        ),
        (
            "Moderate Efficiency: above 40% and up to 70%."
        ),
        (
            "High Efficiency: above 70%."
        ),
        (
            "These groups describe the synthetic session data. "
            "They do not measure a developer's overall ability "
            "or actual mental state."
        ),
    ]

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    # Display results
    print("\nFOCUS EFFICIENCY ANALYSIS")
    print("=" * 40)
    print(f"Total sessions: {total_sessions}")
    print(f"Average focus efficiency: {average_efficiency:.2f}%")
    print(f"Highest focus efficiency: {highest_efficiency:.2f}%")
    print(f"Lowest focus efficiency: {lowest_efficiency:.2f}%")

    print("\nEfficiency group summary:")
    print(summary.to_string(index=False))

    print("\nFiles generated successfully:")
    print(OUTPUT_CSV.relative_to(BASE_DIR))
    print(OUTPUT_REPORT.relative_to(BASE_DIR))


if __name__ == "__main__":
    main()
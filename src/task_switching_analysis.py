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
    / "task_switching_summary.csv"
)

OUTPUT_REPORT = (
    BASE_DIR
    / "reports"
    / "task_switching_analysis.txt"
)


def main():
    # Check whether the cleaned dataset exists
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "Cleaned dataset not found. "
            "Run src/data_cleaning.py first."
        )

    # Load dataset
    df = pd.read_csv(INPUT_FILE)

    # Classify sessions by number of task switches
    df["task_switching_group"] = pd.cut(
        df["task_switches"],
        bins=[-1, 2, 5, float("inf")],
        labels=[
            "Low Switching",
            "Moderate Switching",
            "High Switching",
        ],
    )

    # Summarize each group
    summary = (
        df.groupby(
            "task_switching_group",
            observed=False,
        )
        .agg(
            session_count=("session_id", "count"),
            average_task_switches=("task_switches", "mean"),
            average_focus_duration_min=(
                "focus_duration_min",
                "mean",
            ),
            average_session_duration_min=(
                "session_duration_min",
                "mean",
            ),
            average_interruptions=("interruptions", "mean"),
            average_cognitive_load=(
                "cognitive_load_rating",
                "mean",
            ),
        )
        .round(2)
        .reset_index()
    )

    # Calculate correlations
    switch_focus_corr = df[
        ["task_switches", "focus_duration_min"]
    ].corr().iloc[0, 1]

    switch_load_corr = df[
        ["task_switches", "cognitive_load_rating"]
    ].corr().iloc[0, 1]

    switch_interruptions_corr = df[
        ["task_switches", "interruptions"]
    ].corr().iloc[0, 1]

    # Save CSV summary
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_CSV, index=False)

    # Build report
    report = [
        "COGNISTREAM: TASK-SWITCHING ANALYSIS",
        "=" * 45,
        "",
        f"Total sessions analyzed: {len(df)}",
        (
            "Average task switches per session: "
            f"{df['task_switches'].mean():.2f}"
        ),
        (
            "Correlation between task switches and focus duration: "
            f"{switch_focus_corr:.3f}"
        ),
        (
            "Correlation between task switches and cognitive load: "
            f"{switch_load_corr:.3f}"
        ),
        (
            "Correlation between task switches and interruptions: "
            f"{switch_interruptions_corr:.3f}"
        ),
        "",
        "TASK-SWITCHING GROUP SUMMARY",
        "-" * 45,
        summary.to_string(index=False),
        "",
        "INTERPRETATION",
        "-" * 45,
        (
            "Correlation values near +1 indicate a strong positive "
            "linear relationship; values near -1 indicate a strong "
            "negative linear relationship; values near 0 indicate "
            "little or no linear relationship."
        ),
        (
            "Correlation does not prove that task switching causes "
            "changes in focus or cognitive load."
        ),
        (
            "The results describe synthetic data and should not be "
            "treated as measurements of real developers."
        ),
    ]

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    # Display results
    print("\nTASK-SWITCHING ANALYSIS")
    print("=" * 40)

    print(f"Total sessions: {len(df)}")
    print(
        "Average task switches: "
        f"{df['task_switches'].mean():.2f}"
    )
    print(f"Switches vs focus correlation: {switch_focus_corr:.3f}")
    print(f"Switches vs load correlation: {switch_load_corr:.3f}")
    print(
        "Switches vs interruptions correlation: "
        f"{switch_interruptions_corr:.3f}"
    )

    print("\nGroup summary:")
    print(summary.to_string(index=False))

    print("\nGenerated files:")
    print(OUTPUT_CSV.relative_to(BASE_DIR))
    print(OUTPUT_REPORT.relative_to(BASE_DIR))


if __name__ == "__main__":
    main()
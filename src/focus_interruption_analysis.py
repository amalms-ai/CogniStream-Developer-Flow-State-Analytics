import pandas as pd
from pathlib import Path

# Locate the project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Define input and output files
INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

REPORT_FILE = (
    BASE_DIR
    / "reports"
    / "focus_interruption_analysis.txt"
)


def main():

    # Load the cleaned dataset
    df = pd.read_csv(INPUT_FILE)

    print("=" * 55)
    print("COGNISTREAM - FOCUS AND INTERRUPTION ANALYSIS")
    print("=" * 55)

    print(f"\nTotal sessions: {len(df)}")

    # Calculate average focus duration
    average_focus = df["focus_duration_min"].mean()

    # Calculate average interruptions
    average_interruptions = df["interruptions"].mean()

    # Calculate correlation
    correlation = df[
        ["interruptions", "focus_duration_min"]
    ].corr().iloc[0, 1]

    # Group sessions by interruption count
    df["interruption_group"] = pd.cut(
        df["interruptions"],
        bins=[-1, 2, 5, float("inf")],
        labels=[
            "Low interruptions (0-2)",
            "Medium interruptions (3-5)",
            "High interruptions (6+)"
        ]
    )

    # Compare focus duration across groups
    group_analysis = (
        df.groupby(
            "interruption_group",
            observed=False
        )
        .agg(
            session_count=("session_id", "count"),
            average_focus_duration=(
                "focus_duration_min", "mean"
            ),
            average_session_duration=(
                "session_duration_min", "mean"
            ),
            average_cognitive_load=(
                "cognitive_load_rating", "mean"
            )
        )
        .round(2)
    )

    # Find sessions with the most interruptions
    highest_interruptions = (
        df.sort_values(
            "interruptions",
            ascending=False
        )
        [
            [
                "session_id",
                "developer_id",
                "interruptions",
                "focus_duration_min",
                "session_duration_min"
            ]
        ]
        .head(10)
    )

    # Prepare the report
    report = []

    report.append(
        "COGNISTREAM - FOCUS AND INTERRUPTION ANALYSIS"
    )
    report.append("=" * 55)

    report.append(
        f"\nTotal sessions analyzed: {len(df)}"
    )

    report.append(
        f"Average focus duration: "
        f"{average_focus:.2f} minutes"
    )

    report.append(
        f"Average interruptions per session: "
        f"{average_interruptions:.2f}"
    )

    report.append(
        f"Correlation between interruptions and focus: "
        f"{correlation:.3f}"
    )

    report.append("\n\nFOCUS BY INTERRUPTION GROUP")
    report.append("-" * 55)
    report.append(group_analysis.to_string())

    report.append("\n\nTOP 10 SESSIONS BY INTERRUPTION COUNT")
    report.append("-" * 55)
    report.append(highest_interruptions.to_string(index=False))

    # Ensure the reports directory exists
    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save the report
    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    # Display results
    print(
        f"\nAverage focus duration: "
        f"{average_focus:.2f} minutes"
    )

    print(
        f"Average interruptions: "
        f"{average_interruptions:.2f}"
    )

    print(
        f"Interruption-focus correlation: "
        f"{correlation:.3f}"
    )

    print("\nFocus duration by interruption group:")
    print(group_analysis)

    print(f"\nReport saved to:\n{REPORT_FILE}")

    print("\nAnalysis completed successfully!")


if __name__ == "__main__":
    main()
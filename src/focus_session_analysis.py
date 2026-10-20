import pandas as pd
from pathlib import Path

# Locate the project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input dataset
INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

# Output files
REPORT_FILE = (
    BASE_DIR
    / "reports"
    / "focus_session_analysis.txt"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "focus_session_summary.csv"
)


def main():

    # Load cleaned dataset
    df = pd.read_csv(INPUT_FILE)

    print("=" * 55)
    print("COGNISTREAM - FOCUS SESSION ANALYSIS")
    print("=" * 55)

    print(f"\nTotal sessions analyzed: {len(df)}")

    # Calculate focus percentage
    df["focus_percentage"] = (
        df["focus_duration_min"]
        / df["session_duration_min"]
    ) * 100

    # Categorize sessions by focus duration
    df["focus_group"] = pd.cut(
        df["focus_duration_min"],
        bins=[-1, 29, 59, float("inf")],
        labels=[
            "Short focus (0-29 min)",
            "Medium focus (30-59 min)",
            "Long focus (60+ min)"
        ]
    )

    # Summarize focus groups
    focus_summary = (
        df.groupby("focus_group", observed=False)
        .agg(
            session_count=("session_id", "count"),
            average_focus_duration=(
                "focus_duration_min", "mean"
            ),
            average_session_duration=(
                "session_duration_min", "mean"
            ),
            average_focus_percentage=(
                "focus_percentage", "mean"
            ),
            average_cognitive_load=(
                "cognitive_load_rating", "mean"
            )
        )
        .round(2)
        .reset_index()
    )

    # Calculate overall metrics
    average_focus = df["focus_duration_min"].mean()
    average_focus_percentage = df["focus_percentage"].mean()

    sessions_30_plus = (
        df["focus_duration_min"] >= 30
    ).sum()

    sessions_60_plus = (
        df["focus_duration_min"] >= 60
    ).sum()

    # Save summary dataset
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    focus_summary.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # Prepare report
    report = [
        "COGNISTREAM - FOCUS SESSION ANALYSIS",
        "=" * 50,
        f"Total sessions: {len(df)}",
        f"Average focus duration: {average_focus:.2f} minutes",
        f"Average focus percentage: {average_focus_percentage:.2f}%",
        f"Sessions with at least 30 minutes of focus: {sessions_30_plus}",
        f"Sessions with at least 60 minutes of focus: {sessions_60_plus}",
        "",
        "FOCUS GROUP SUMMARY",
        "-" * 50,
        focus_summary.to_string(index=False),
    ]

    # Save text report
    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    # Display results
    print(f"\nAverage focus duration: {average_focus:.2f} minutes")

    print(
        f"Average focus percentage: "
        f"{average_focus_percentage:.2f}%"
    )

    print(
        f"Sessions with at least 30 minutes of focus: "
        f"{sessions_30_plus}"
    )

    print(
        f"Sessions with at least 60 minutes of focus: "
        f"{sessions_60_plus}"
    )

    print("\nFocus group summary:")
    print(focus_summary.to_string(index=False))

    print(f"\nSummary CSV saved to:\n{OUTPUT_FILE}")
    print(f"\nReport saved to:\n{REPORT_FILE}")

    print("\nFocus session analysis completed successfully!")


if __name__ == "__main__":
    main()
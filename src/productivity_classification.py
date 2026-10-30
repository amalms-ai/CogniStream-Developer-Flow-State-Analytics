from pathlib import Path

import pandas as pd
import plotly.express as px


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

REPORT_DIR = BASE_DIR / "reports"
FIGURES_DIR = BASE_DIR / "figures"

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_productivity_classified.csv"
)

REPORT_FILE = (
    REPORT_DIR
    / "productivity_classification_report.txt"
)

CHART_FILE = (
    FIGURES_DIR
    / "productivity_classification.html"
)


def main():

    # Check dataset
    if not DATA_FILE.exists():
        print("Dataset not found:", DATA_FILE)
        return

    # Load dataset
    df = pd.read_csv(DATA_FILE)

    # Required columns
    required_columns = [
        "focus_duration_min",
        "tasks_completed",
        "interruptions",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Missing columns:", missing_columns)
        return

    # Convert metrics to numeric values
    for column in required_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove invalid records
    df = df.dropna(
        subset=required_columns
    ).copy()

    if df.empty:
        print("No valid records available.")
        return

    # Prevent invalid negative values
    if (
        (df[required_columns] < 0)
        .any()
        .any()
    ):
        print("Negative values found in productivity metrics.")
        print("Please inspect the dataset before classification.")
        return

    # Calculate relative percentile scores
    focus_score = (
        df["focus_duration_min"]
        .rank(pct=True)
    )

    task_score = (
        df["tasks_completed"]
        .rank(pct=True)
    )

    interruption_score = (
        1 - df["interruptions"].rank(pct=True)
    )

    # Calculate overall productivity score
    df["productivity_score"] = (
        focus_score * 0.40
        + task_score * 0.40
        + interruption_score * 0.20
    ) * 100

    # Classify sessions using relative score thresholds
    df["productivity_category"] = pd.cut(
        df["productivity_score"],
        bins=[0, 33.33, 66.67, 100.01],
        labels=[
            "Low Productivity",
            "Moderate Productivity",
            "High Productivity"
        ],
        include_lowest=True
    )

    # Create output folders
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save classified dataset
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # Summarize categories
    category_summary = (
        df.groupby(
            "productivity_category",
            observed=False
        )
        .agg(
            total_sessions=("productivity_score", "size"),
            average_focus_duration=("focus_duration_min", "mean"),
            average_tasks_completed=("tasks_completed", "mean"),
            average_interruptions=("interruptions", "mean"),
        )
        .reset_index()
    )

    # Add cognitive load comparison if available
    if "cognitive_load_rating" in df.columns:

        df["cognitive_load_rating"] = pd.to_numeric(
            df["cognitive_load_rating"],
            errors="coerce"
        )

        cognitive_summary = (
            df.groupby(
                "productivity_category",
                observed=False
            )["cognitive_load_rating"]
            .mean()
            .reset_index()
        )

        category_summary = category_summary.merge(
            cognitive_summary,
            on="productivity_category",
            how="left"
        )

        category_summary = category_summary.rename(
            columns={
                "cognitive_load_rating":
                "average_cognitive_load"
            }
        )

    # Save category comparison chart
    chart = px.bar(
        category_summary,
        x="productivity_category",
        y="total_sessions",
        color="productivity_category",
        title="Developer Sessions by Productivity Category",
        labels={
            "productivity_category": "Productivity Category",
            "total_sessions": "Number of Sessions"
        },
        text="total_sessions"
    )

    chart.write_html(CHART_FILE)

    # Generate report
    lines = [
        "=" * 60,
        "COGNISTREAM PRODUCTIVITY CLASSIFICATION REPORT",
        "=" * 60,
        "",
        f"Total sessions analyzed: {len(df)}",
        "",
        "PRODUCTIVITY SCORING METHOD",
        "-" * 60,
        "Focus duration weight: 40%",
        "Completed tasks weight: 40%",
        "Interruptions weight: 20% (lower is better)",
        "",
        "Classification uses relative percentile scores.",
        "Categories are based on the score distribution.",
        "",
        "PRODUCTIVITY CATEGORY SUMMARY",
        "-" * 60,
        category_summary.round(2).to_string(index=False),
        "",
        "INTERPRETATION",
        "-" * 60,
        "High Productivity: Sessions with relatively higher scores.",
        "Moderate Productivity: Sessions with middle-range scores.",
        "Low Productivity: Sessions with relatively lower scores.",
        "",
        "LIMITATIONS",
        "-" * 60,
        "These categories are analytical benchmarks, not official",
        "performance ratings.",
        "Task complexity and task type may affect comparisons.",
        "Cognitive load is analyzed separately and is not treated",
        "as automatically negative or positive.",
        "",
        "The dataset is synthetic, so findings demonstrate an",
        "analytical workflow rather than verified real-world behavior.",
    ]

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print("\nProductivity classification completed.")
    print("Classified dataset:", OUTPUT_FILE)
    print("Classification report:", REPORT_FILE)
    print("Visualization:", CHART_FILE)

    print("\nCategory summary:")
    print(category_summary.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
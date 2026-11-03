from pathlib import Path

import pandas as pd
import plotly.express as px


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_productivity_classified.csv"
)

REPORT_DIR = BASE_DIR / "reports"
FIGURES_DIR = BASE_DIR / "figures"


def main():

    # Check dataset
    if not DATA_FILE.exists():
        print("Dataset not found:", DATA_FILE)
        return

    # Load dataset
    df = pd.read_csv(DATA_FILE)

    # Required columns
    required_columns = [
        "date",
        "start_hour",
        "productivity_score",
        "productivity_category"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Missing columns:", missing_columns)
        return

    # Convert columns to appropriate data types
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["start_hour"] = pd.to_numeric(
        df["start_hour"],
        errors="coerce"
    )

    df["productivity_score"] = pd.to_numeric(
        df["productivity_score"],
        errors="coerce"
    )

    # Remove invalid records
    df = df.dropna(
        subset=[
            "date",
            "start_hour",
            "productivity_score",
            "productivity_category"
        ]
    ).copy()

    # Validate working hours
    df = df[
        df["start_hour"].between(0, 23)
    ].copy()

    if df.empty:
        print("No valid records available.")
        return

    # Create output folders
    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------
    # 1. PRODUCTIVITY BY WORKING HOUR
    # --------------------------------------------------

    hourly_summary = (
        df.groupby("start_hour")
        .agg(
            total_sessions=("productivity_score", "size"),
            average_productivity_score=(
                "productivity_score", "mean"
            )
        )
        .reset_index()
        .sort_values("start_hour")
    )

    hourly_summary[
        "average_productivity_score"
    ] = hourly_summary[
        "average_productivity_score"
    ].round(2)

    # Save hourly summary
    hourly_summary.to_csv(
        REPORT_DIR / "hourly_productivity_summary.csv",
        index=False
    )

    # Hourly productivity chart
    hourly_chart = px.line(
        hourly_summary,
        x="start_hour",
        y="average_productivity_score",
        markers=True,
        title="Average Productivity Score by Working Hour",
        labels={
            "start_hour": "Starting Hour",
            "average_productivity_score":
                "Average Productivity Score"
        }
    )

    hourly_chart.write_html(
        FIGURES_DIR / "hourly_productivity_trend.html"
    )

    # --------------------------------------------------
    # 2. PRODUCTIVITY BY DATE
    # --------------------------------------------------

    daily_summary = (
        df.groupby(df["date"].dt.date)
        .agg(
            total_sessions=("productivity_score", "size"),
            average_productivity_score=(
                "productivity_score", "mean"
            )
        )
        .reset_index()
    )

    daily_summary.columns = [
        "date",
        "total_sessions",
        "average_productivity_score"
    ]

    daily_summary[
        "average_productivity_score"
    ] = daily_summary[
        "average_productivity_score"
    ].round(2)

    daily_summary.to_csv(
        REPORT_DIR / "daily_productivity_summary.csv",
        index=False
    )

    # Daily productivity chart
    daily_chart = px.line(
        daily_summary,
        x="date",
        y="average_productivity_score",
        markers=True,
        title="Daily Average Productivity Trend",
        labels={
            "date": "Date",
            "average_productivity_score":
                "Average Productivity Score"
        }
    )

    daily_chart.write_html(
        FIGURES_DIR / "daily_productivity_trend.html"
    )

    # --------------------------------------------------
    # 3. PRODUCTIVITY CATEGORY BY WORKING HOUR
    # --------------------------------------------------

    category_summary = (
        df.groupby(
            ["start_hour", "productivity_category"],
            observed=False
        )
        .size()
        .reset_index(name="total_sessions")
    )

    category_summary.to_csv(
        REPORT_DIR / "hourly_productivity_categories.csv",
        index=False
    )

    category_chart = px.bar(
        category_summary,
        x="start_hour",
        y="total_sessions",
        color="productivity_category",
        barmode="stack",
        title="Productivity Categories by Working Hour",
        labels={
            "start_hour": "Starting Hour",
            "total_sessions": "Number of Sessions",
            "productivity_category": "Productivity Category"
        }
    )

    category_chart.write_html(
        FIGURES_DIR / "hourly_productivity_categories.html"
    )

    # --------------------------------------------------
    # 4. GENERATE TEXT REPORT
    # --------------------------------------------------

    highest_hour = hourly_summary.loc[
        hourly_summary["average_productivity_score"].idxmax()
    ]

    lowest_hour = hourly_summary.loc[
        hourly_summary["average_productivity_score"].idxmin()
    ]

    report = [
        "=" * 60,
        "COGNISTREAM TIME-BASED PRODUCTIVITY ANALYSIS",
        "=" * 60,
        "",
        f"Total sessions analyzed: {len(df)}",
        f"Working dates analyzed: {df['date'].nunique()}",
        f"Working hours represented: {df['start_hour'].nunique()}",
        "",
        "HOURLY PRODUCTIVITY SUMMARY",
        "-" * 60,
        hourly_summary.to_string(index=False),
        "",
        "DAILY PRODUCTIVITY SUMMARY",
        "-" * 60,
        daily_summary.to_string(index=False),
        "",
        "KEY OBSERVATIONS",
        "-" * 60,
        (
            f"Highest average productivity score: "
            f"{highest_hour['average_productivity_score']} "
            f"at hour {int(highest_hour['start_hour'])}:00"
        ),
        (
            f"Lowest average productivity score: "
            f"{lowest_hour['average_productivity_score']} "
            f"at hour {int(lowest_hour['start_hour'])}:00"
        ),
        "",
        "NOTE",
        "-" * 60,
        "These findings describe patterns in the available dataset.",
        "They do not prove that working at a particular hour causes",
        "higher or lower productivity.",
        "The dataset is synthetic, so results are illustrative.",
    ]

    report_file = (
        REPORT_DIR / "time_based_productivity_report.txt"
    )

    report_file.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    # Display results
    print("\nTime-based productivity analysis completed.")

    print("\nHourly productivity:")
    print(hourly_summary.to_string(index=False))

    print("\nDaily productivity:")
    print(daily_summary.to_string(index=False))

    print("\nHighest average productivity hour:")
    print(int(highest_hour["start_hour"]), ":00")

    print("\nGenerated reports and visualizations successfully.")


if __name__ == "__main__":
    main()
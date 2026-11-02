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

    # Check whether the dataset exists
    if not DATA_FILE.exists():
        print("Classified dataset not found:", DATA_FILE)
        return

    # Load classified dataset
    df = pd.read_csv(DATA_FILE)

    # Required columns
    required_columns = [
        "developer_id",
        "productivity_category"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Missing columns:", missing_columns)
        return

    # Remove missing values
    df = df.dropna(
        subset=required_columns
    ).copy()

    if df.empty:
        print("No valid records available.")
        return

    # Define category order
    category_order = [
        "High Productivity",
        "Moderate Productivity",
        "Low Productivity"
    ]

    # Count productivity sessions for each developer
    distribution = pd.crosstab(
        df["developer_id"],
        df["productivity_category"]
    )

    # Ensure all categories are included
    distribution = distribution.reindex(
        columns=category_order,
        fill_value=0
    )

    # Add total sessions
    distribution["Total Sessions"] = (
        distribution.sum(axis=1)
    )

    # Calculate percentage distribution
    percentage_distribution = (
        distribution[category_order]
        .div(distribution["Total Sessions"], axis=0)
        * 100
    ).round(2)

    percentage_distribution.columns = [
        f"{category} (%)"
        for category in category_order
    ]

    # Combine counts and percentages
    summary = distribution.join(
        percentage_distribution
    ).reset_index()

    # Sort developers by high productivity session count
    summary = summary.sort_values(
        "High Productivity",
        ascending=False
    )

    # Create output folders
    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save summary CSV
    csv_file = (
        REPORT_DIR
        / "developer_productivity_distribution.csv"
    )

    summary.to_csv(
        csv_file,
        index=False
    )

    # Prepare chart data
    chart_data = (
        distribution[category_order]
        .reset_index()
        .melt(
            id_vars="developer_id",
            var_name="Productivity Category",
            value_name="Number of Sessions"
        )
    )

    # Create stacked bar chart
    chart = px.bar(
        chart_data,
        x="developer_id",
        y="Number of Sessions",
        color="Productivity Category",
        barmode="stack",
        title="Developer-wise Productivity Distribution",
        labels={
            "developer_id": "Developer ID"
        }
    )

    # Save interactive visualization
    html_file = (
        FIGURES_DIR
        / "developer_productivity_distribution.html"
    )

    chart.write_html(html_file)

    # Generate text report
    report_lines = [
        "=" * 65,
        "COGNISTREAM: DEVELOPER PRODUCTIVITY DISTRIBUTION",
        "=" * 65,
        "",
        f"Total sessions analyzed: {len(df)}",
        f"Number of developers: {df['developer_id'].nunique()}",
        "",
        "PRODUCTIVITY DISTRIBUTION BY DEVELOPER",
        "-" * 65,
        summary.round(2).to_string(index=False),
        "",
        "OVERALL CATEGORY DISTRIBUTION",
        "-" * 65,
        df["productivity_category"]
        .value_counts()
        .reindex(category_order, fill_value=0)
        .to_string(),
        "",
        "NOTE",
        "-" * 65,
        (
            "This analysis compares the distribution of classified "
            "work sessions across developers. It does not establish "
            "individual employee performance or skill levels."
        ),
        (
            "The dataset is synthetic, so results demonstrate "
            "an analytical workflow rather than real-world findings."
        )
    ]

    report_file = (
        REPORT_DIR
        / "developer_productivity_distribution.txt"
    )

    report_file.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )

    # Display results
    print("\nDeveloper productivity analysis completed.")

    print("\nDeveloper-wise distribution:")
    print(summary.round(2).to_string(index=False))

    print("\nGenerated files:")
    print("CSV report:", csv_file)
    print("Text report:", report_file)
    print("Interactive chart:", html_file)


if __name__ == "__main__":
    main()
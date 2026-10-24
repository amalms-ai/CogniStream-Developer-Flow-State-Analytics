from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ============================================================
# COGNISTREAM - DAY 13
# TASK COMPLEXITY ANALYSIS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = PROJECT_ROOT / "figures"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def main():

    print("=" * 60)
    print("COGNISTREAM - DAY 13")
    print("TASK COMPLEXITY ANALYSIS")
    print("=" * 60)

    # 1. Load dataset
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    print(f"\nDataset loaded: {DATA_FILE.name}")
    print(f"Total records: {len(df)}")

    # 2. Validate required columns
    required_columns = [
        "task_complexity",
        "focus_duration_min",
        "cognitive_load_rating",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # 3. Clean task complexity categories
    df["task_complexity"] = (
        df["task_complexity"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    complexity_mapping = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
    }

    actual_categories = set(
        df["task_complexity"].dropna().unique()
    )

    unexpected_categories = (
        actual_categories - set(complexity_mapping)
    )

    if unexpected_categories:
        raise ValueError(
            "Unexpected task complexity categories: "
            f"{sorted(unexpected_categories)}"
        )

    # 4. Convert analysis columns to numeric
    df["focus_duration_min"] = pd.to_numeric(
        df["focus_duration_min"],
        errors="coerce",
    )

    df["cognitive_load_rating"] = pd.to_numeric(
        df["cognitive_load_rating"],
        errors="coerce",
    )

    df["complexity_score"] = (
        df["task_complexity"].map(complexity_mapping)
    )

    # 5. Prepare valid records
    analysis_df = df.dropna(
        subset=[
            "task_complexity",
            "focus_duration_min",
            "cognitive_load_rating",
            "complexity_score",
        ]
    ).copy()

    if analysis_df.empty:
        raise ValueError(
            "No valid records are available for analysis."
        )

    print(f"Valid records: {len(analysis_df)}")
    print(
        f"Excluded records: {len(df) - len(analysis_df)}"
    )

    # 6. Task complexity distribution
    complexity_distribution = (
        analysis_df["task_complexity"]
        .value_counts()
        .reindex(
            ["Low", "Medium", "High"],
            fill_value=0,
        )
        .rename_axis("task_complexity")
        .reset_index(name="task_count")
    )

    print("\nTASK COMPLEXITY DISTRIBUTION")
    print(complexity_distribution.to_string(index=False))

    distribution_file = (
        PROCESSED_DIR / "task_complexity_distribution.csv"
    )

    complexity_distribution.to_csv(
        distribution_file,
        index=False,
    )

    # 7. Calculate task complexity statistics
    summary = (
        analysis_df.groupby(
            "task_complexity",
            observed=True,
        )
        .agg(
            task_count=("task_complexity", "size"),
            average_focus_duration=(
                "focus_duration_min", "mean"
            ),
            median_focus_duration=(
                "focus_duration_min", "median"
            ),
            average_cognitive_load=(
                "cognitive_load_rating", "mean"
            ),
            median_cognitive_load=(
                "cognitive_load_rating", "median"
            ),
        )
        .reindex(["Low", "Medium", "High"])
        .dropna(how="all")
        .reset_index()
        .round(2)
    )

    print("\nTASK COMPLEXITY SUMMARY")
    print(summary.to_string(index=False))

    summary_file = (
        PROCESSED_DIR / "task_complexity_summary.csv"
    )

    summary.to_csv(summary_file, index=False)

    # 8. Correlation analysis
    correlation = analysis_df[
        [
            "complexity_score",
            "focus_duration_min",
            "cognitive_load_rating",
        ]
    ].corr(method="spearman").round(3)

    print("\nSPEARMAN CORRELATION")
    print(correlation.to_string())

    correlation_file = (
        REPORTS_DIR / "task_complexity_correlations.csv"
    )

    correlation.to_csv(correlation_file)

    # 9. Generate text report
    report_file = (
        REPORTS_DIR / "task_complexity_analysis_report.txt"
    )

    with report_file.open(
        "w",
        encoding="utf-8",
    ) as report:

        report.write(
            "COGNISTREAM - DAY 13\n"
            "TASK COMPLEXITY ANALYSIS\n"
            + "=" * 60
            + "\n\n"
        )

        report.write(
            f"Total records: {len(df)}\n"
            f"Valid analysis records: {len(analysis_df)}\n"
            f"Excluded records: {len(df) - len(analysis_df)}\n\n"
        )

        report.write("TASK COMPLEXITY DISTRIBUTION\n")
        report.write(
            complexity_distribution.to_string(index=False)
        )

        report.write("\n\nTASK COMPLEXITY SUMMARY\n")
        report.write(summary.to_string(index=False))

        report.write("\n\nSPEARMAN CORRELATION\n")
        report.write(correlation.to_string())

        if not summary.empty:

            highest_load = summary.loc[
                summary["average_cognitive_load"].idxmax()
            ]

            longest_focus = summary.loc[
                summary["average_focus_duration"].idxmax()
            ]

            report.write(
                "\n\nKEY FINDINGS\n"
                f"Highest average cognitive load: "
                f"{highest_load['task_complexity']} "
                f"({highest_load['average_cognitive_load']}).\n"
            )

            report.write(
                f"Longest average focus duration: "
                f"{longest_focus['task_complexity']} "
                f"({longest_focus['average_focus_duration']} minutes).\n"
            )

        report.write(
            "\nCorrelation indicates association, not causation. "
            "Complexity scores represent ordered categories and "
            "do not imply equal distances between categories.\n"
        )

    # 10. Visualize average focus duration
    plt.figure(figsize=(9, 5))

    plt.bar(
        summary["task_complexity"],
        summary["average_focus_duration"],
    )

    plt.title("Average Focus Duration by Task Complexity")
    plt.xlabel("Task Complexity")
    plt.ylabel("Average Focus Duration (minutes)")
    plt.tight_layout()

    focus_chart = (
        FIGURES_DIR / "focus_duration_by_complexity.png"
    )

    plt.savefig(focus_chart, dpi=300)
    plt.close()

    # 11. Visualize average cognitive load
    plt.figure(figsize=(9, 5))

    plt.bar(
        summary["task_complexity"],
        summary["average_cognitive_load"],
    )

    plt.title("Average Cognitive Load by Task Complexity")
    plt.xlabel("Task Complexity")
    plt.ylabel("Average Cognitive Load Rating")
    plt.tight_layout()

    cognitive_chart = (
        FIGURES_DIR / "cognitive_load_by_complexity.png"
    )

    plt.savefig(cognitive_chart, dpi=300)
    plt.close()

    # 12. Visualize task complexity distribution
    plt.figure(figsize=(9, 5))

    plt.bar(
        complexity_distribution["task_complexity"],
        complexity_distribution["task_count"],
    )

    plt.title("Distribution of Task Complexity")
    plt.xlabel("Task Complexity")
    plt.ylabel("Number of Records")
    plt.tight_layout()

    distribution_chart = (
        FIGURES_DIR / "task_complexity_distribution.png"
    )

    plt.savefig(distribution_chart, dpi=300)
    plt.close()

    # 13. Display generated files
    print("\n" + "=" * 60)
    print("DAY 13 ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 60)

    output_files = [
        summary_file,
        distribution_file,
        correlation_file,
        report_file,
        focus_chart,
        cognitive_chart,
        distribution_chart,
    ]

    print("\nGenerated files:")

    for file_path in output_files:
        print(f"- {file_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
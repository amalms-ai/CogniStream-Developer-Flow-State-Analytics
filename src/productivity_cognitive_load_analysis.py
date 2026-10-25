"""
CogniStream - Day 14
Productivity vs Cognitive Load Analysis

Purpose:
Analyze the relationship between cognitive-load ratings
and developer productivity using synthetic activity data.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

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


# --------------------------------------------------
# 2. CREATE OUTPUT FOLDERS
# --------------------------------------------------

for folder in [PROCESSED_DIR, REPORTS_DIR, FIGURES_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 3. LOAD DATASET
# --------------------------------------------------

def main():
    print("=" * 65)
    print("COGNISTREAM - DAY 14")
    print("PRODUCTIVITY VS COGNITIVE LOAD ANALYSIS")
    print("=" * 65)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}\n"
            "Run the data-cleaning script first."
        )

    df = pd.read_csv(DATA_FILE)

    print(f"\nDataset loaded: {DATA_FILE.name}")
    print(f"Total records: {len(df)}")

    # --------------------------------------------------
    # 4. VALIDATE REQUIRED COLUMNS
    # --------------------------------------------------

    required_columns = [
        "cognitive_load_rating",
        "tasks_completed",
        "task_type",
        "focus_duration_min",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # --------------------------------------------------
    # 5. CLEAN REQUIRED VALUES
    # --------------------------------------------------

    analysis_df = df[required_columns].copy()

    numeric_columns = [
        "cognitive_load_rating",
        "tasks_completed",
        "focus_duration_min",
    ]

    for column in numeric_columns:
        analysis_df[column] = pd.to_numeric(
            analysis_df[column],
            errors="coerce",
        )

    analysis_df = analysis_df.dropna(
        subset=[
            "cognitive_load_rating",
            "tasks_completed",
            "focus_duration_min",
            "task_type",
        ]
    )

    analysis_df = analysis_df[
        (analysis_df["cognitive_load_rating"] >= 1)
        & (analysis_df["cognitive_load_rating"] <= 5)
        & (analysis_df["tasks_completed"] >= 0)
        & (analysis_df["focus_duration_min"] >= 0)
    ].copy()

    if analysis_df.empty:
        raise ValueError(
            "No valid records remain after cleaning."
        )

    print(f"Valid records: {len(analysis_df)}")
    print(
        f"Excluded records: {len(df) - len(analysis_df)}"
    )

    # --------------------------------------------------
    # 6. GROUP COGNITIVE LOAD INTO CATEGORIES
    # --------------------------------------------------

    def categorize_load(rating):
        if rating < 2.5:
            return "Low"
        elif rating < 3.5:
            return "Medium"
        return "High"

    analysis_df["cognitive_load_category"] = (
        analysis_df["cognitive_load_rating"]
        .apply(categorize_load)
    )

    category_order = ["Low", "Medium", "High"]

    # --------------------------------------------------
    # 7. SUMMARIZE PRODUCTIVITY BY COGNITIVE LOAD
    # --------------------------------------------------

    summary = (
        analysis_df.groupby(
            "cognitive_load_category",
            observed=True,
        )
        .agg(
            session_count=("tasks_completed", "size"),
            average_tasks_completed=(
                "tasks_completed",
                "mean",
            ),
            median_tasks_completed=(
                "tasks_completed",
                "median",
            ),
            average_focus_duration=(
                "focus_duration_min",
                "mean",
            ),
            average_cognitive_load=(
                "cognitive_load_rating",
                "mean",
            ),
        )
        .reindex(category_order)
        .dropna(how="all")
        .reset_index()
    )

    summary.to_csv(
        PROCESSED_DIR
        / "productivity_by_cognitive_load.csv",
        index=False,
    )

    print("\nPRODUCTIVITY BY COGNITIVE LOAD")
    print(summary.round(2).to_string(index=False))

    # --------------------------------------------------
    # 8. ANALYZE PRODUCTIVITY BY TASK TYPE AND LOAD
    # --------------------------------------------------

    task_summary = (
        analysis_df.groupby(
            ["task_type", "cognitive_load_category"],
            observed=True,
        )
        .agg(
            session_count=("tasks_completed", "size"),
            average_tasks_completed=(
                "tasks_completed",
                "mean",
            ),
            average_focus_duration=(
                "focus_duration_min",
                "mean",
            ),
        )
        .reset_index()
    )

    task_summary.to_csv(
        PROCESSED_DIR
        / "productivity_by_task_type_and_load.csv",
        index=False,
    )

    print("\nPRODUCTIVITY BY TASK TYPE AND COGNITIVE LOAD")
    print(task_summary.round(2).to_string(index=False))

    # --------------------------------------------------
    # 9. CALCULATE CORRELATIONS
    # --------------------------------------------------

    correlation_columns = [
        "cognitive_load_rating",
        "tasks_completed",
        "focus_duration_min",
    ]

    correlations = analysis_df[
        correlation_columns
    ].corr(method="spearman")

    correlations.to_csv(
        REPORTS_DIR
        / "productivity_cognitive_load_correlations.csv"
    )

    print("\nSPEARMAN CORRELATION MATRIX")
    print(correlations.round(3).to_string())

    # --------------------------------------------------
    # 10. CREATE BAR CHART
    # --------------------------------------------------

    plot_summary = summary.dropna(
        subset=["average_tasks_completed"]
    )

    if not plot_summary.empty:
        plt.figure(figsize=(9, 6))

        plt.bar(
            plot_summary["cognitive_load_category"],
            plot_summary["average_tasks_completed"],
        )

        plt.title(
            "Average Tasks Completed by Cognitive Load"
        )
        plt.xlabel("Cognitive Load Category")
        plt.ylabel("Average Tasks Completed")
        plt.tight_layout()

        plt.savefig(
            FIGURES_DIR
            / "productivity_by_cognitive_load.png",
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

    # --------------------------------------------------
    # 11. CREATE FOCUS DURATION CHART
    # --------------------------------------------------

    focus_summary = summary.dropna(
        subset=["average_focus_duration"]
    )

    if not focus_summary.empty:
        plt.figure(figsize=(9, 6))

        plt.bar(
            focus_summary["cognitive_load_category"],
            focus_summary["average_focus_duration"],
        )

        plt.title(
            "Average Focus Duration by Cognitive Load"
        )
        plt.xlabel("Cognitive Load Category")
        plt.ylabel("Average Focus Duration (minutes)")
        plt.tight_layout()

        plt.savefig(
            FIGURES_DIR
            / "focus_duration_by_cognitive_load.png",
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

    # --------------------------------------------------
    # 12. GENERATE TEXT REPORT
    # --------------------------------------------------

    report_lines = [
        "COGNISTREAM - DAY 14",
        "PRODUCTIVITY VS COGNITIVE LOAD ANALYSIS",
        "=" * 55,
        "",
        f"Total original records: {len(df)}",
        f"Valid analysis records: {len(analysis_df)}",
        f"Excluded records: {len(df) - len(analysis_df)}",
        "",
        "PRODUCTIVITY SUMMARY",
        "-" * 55,
        summary.round(2).to_string(index=False),
        "",
        "SPEARMAN CORRELATIONS",
        "-" * 55,
        correlations.round(3).to_string(),
        "",
        "INTERPRETATION GUIDANCE",
        "-" * 55,
        (
            "A negative correlation between cognitive load "
            "and tasks completed indicates that higher "
            "cognitive-load ratings tend to accompany "
            "fewer completed tasks."
        ),
        (
            "A positive correlation indicates that higher "
            "ratings tend to accompany more completed tasks."
        ),
        (
            "A correlation near zero indicates little "
            "monotonic association in this dataset."
        ),
        (
            "Correlation does not prove causation. "
            "Task complexity, task type, and session duration "
            "may also affect the results."
        ),
    ]

    report_path = (
        REPORTS_DIR
        / "productivity_cognitive_load_report.txt"
    )

    report_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    # --------------------------------------------------
    # 13. DISPLAY GENERATED FILES
    # --------------------------------------------------

    print("\n" + "=" * 65)
    print("DAY 14 ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 65)

    print("\nGenerated files:")
    print(
        "- data/processed/"
        "productivity_by_cognitive_load.csv"
    )
    print(
        "- data/processed/"
        "productivity_by_task_type_and_load.csv"
    )
    print(
        "- reports/"
        "productivity_cognitive_load_correlations.csv"
    )
    print(
        "- reports/"
        "productivity_cognitive_load_report.txt"
    )
    print(
        "- figures/productivity_by_cognitive_load.png"
    )
    print(
        "- figures/focus_duration_by_cognitive_load.png"
    )


if __name__ == "__main__":
    main()
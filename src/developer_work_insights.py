import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output paths
INPUT_FILE = BASE_DIR / "data" / "processed" / "developer_activity_cleaned.csv"
REPORT_DIR = BASE_DIR / "reports"
OUTPUT_FILE = REPORT_DIR / "developer_work_insights.txt"

def main():
    print("=" * 55)
    print("COGNISTREAM - DEVELOPER WORK INSIGHTS")
    print("=" * 55)

    # Load cleaned dataset
    if not INPUT_FILE.exists():
        print(f"Dataset not found: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)

    # Check required columns
    required_columns = [
        "task_type",
        "session_duration_min",
        "focus_duration_min",
        "interruptions",
        "task_switches",
        "cognitive_load_rating",
        "tasks_completed"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        print("Missing required columns:", missing)
        return

    # Prepare report directory
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Calculate overall metrics
    average_focus = df["focus_duration_min"].mean()
    average_interruptions = df["interruptions"].mean()
    average_switches = df["task_switches"].mean()
    average_load = df["cognitive_load_rating"].mean()
    average_tasks = df["tasks_completed"].mean()

    # Compare task types
    task_summary = df.groupby("task_type").agg(
        average_focus=("focus_duration_min", "mean"),
        average_cognitive_load=("cognitive_load_rating", "mean"),
        average_interruptions=("interruptions", "mean"),
        average_tasks_completed=("tasks_completed", "mean")
    ).round(2)

    # Identify key findings
    lowest_focus_task = task_summary["average_focus"].idxmin()
    highest_load_task = task_summary["average_cognitive_load"].idxmax()
    highest_interruptions_task = (
        task_summary["average_interruptions"].idxmax()
    )

    # Build insights and recommendations
    insights = [
        "DEVELOPER WORK INSIGHTS REPORT",
        "=" * 55,
        "",
        f"Total work sessions analyzed: {len(df)}",
        "",
        "1. OVERALL WORK PATTERNS",
        "-" * 30,
        f"Average focus duration: {average_focus:.2f} minutes",
        f"Average interruptions: {average_interruptions:.2f}",
        f"Average task switches: {average_switches:.2f}",
        f"Average cognitive load: {average_load:.2f}",
        f"Average tasks completed per session: {average_tasks:.2f}",
        "",
        "2. KEY FINDINGS",
        "-" * 30,
        (
            f"Lowest average focus duration: {lowest_focus_task} "
            f"({task_summary.loc[lowest_focus_task, 'average_focus']:.2f} minutes)"
        ),
        (
            f"Highest average cognitive load: {highest_load_task} "
            f"({task_summary.loc[highest_load_task, 'average_cognitive_load']:.2f})"
        ),
        (
            f"Highest average interruptions: {highest_interruptions_task} "
            f"({task_summary.loc[highest_interruptions_task, 'average_interruptions']:.2f})"
        ),
        "",
        "3. RECOMMENDATIONS",
        "-" * 30,
        (
            f"Review the workflow for {lowest_focus_task}, "
            "as it has the lowest average focus duration."
        ),
        (
            f"Examine the challenges associated with {highest_load_task}, "
            "which has the highest average cognitive load."
        ),
        (
            f"Investigate interruption patterns during {highest_interruptions_task} "
            "to identify possible opportunities to reduce disruptions."
        ),
        (
            "Compare these findings with project reports before making "
            "decisions about workload or work scheduling."
        ),
        "",
        "4. TASK TYPE COMPARISON",
        "-" * 30,
        task_summary.to_string(),
        "",
        "Note: This dataset is synthetic. Findings describe the generated "
        "data and should not be treated as evidence about real developers."
    ]

    # Save report
    report_text = "\n".join(insights)
    OUTPUT_FILE.write_text(report_text, encoding="utf-8")

    print(report_text)
    print("\nInsights report generated successfully!")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
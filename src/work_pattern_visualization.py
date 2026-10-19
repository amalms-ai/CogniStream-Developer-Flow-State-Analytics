import pandas as pd
import matplotlib.pyplot as plt
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

# Output directory
FIGURES_DIR = BASE_DIR / "figures"


def main():

    # Create output directory if it does not exist
    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Load cleaned dataset
    df = pd.read_csv(INPUT_FILE)

    print("=" * 55)
    print("COGNISTREAM - WORK PATTERN VISUALIZATION")
    print("=" * 55)

    print(f"\nTotal sessions analyzed: {len(df)}")

    # -----------------------------------------
    # Chart 1: Focus duration by task type
    # -----------------------------------------

    focus_by_task = (
        df.groupby("task_type")["focus_duration_min"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))

    focus_by_task.plot(
        kind="bar",
        edgecolor="black"
    )

    plt.title("Average Focus Duration by Task Type")
    plt.xlabel("Task Type")
    plt.ylabel("Average Focus Duration (Minutes)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "focus_duration_by_task.png",
        dpi=300
    )

    plt.close()

    print("\n1. Focus duration chart saved.")

    # -----------------------------------------
    # Chart 2: Cognitive load by task type
    # -----------------------------------------

    load_by_task = (
        df.groupby("task_type")["cognitive_load_rating"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))

    load_by_task.plot(
        kind="bar",
        edgecolor="black"
    )

    plt.title("Average Cognitive Load by Task Type")
    plt.xlabel("Task Type")
    plt.ylabel("Average Cognitive Load Rating")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "cognitive_load_by_task.png",
        dpi=300
    )

    plt.close()

    print("2. Cognitive load chart saved.")

    # -----------------------------------------
    # Chart 3: Interruptions versus focus
    # -----------------------------------------

    plt.figure(figsize=(10, 6))

    plt.scatter(
        df["interruptions"],
        df["focus_duration_min"],
        alpha=0.6
    )

    plt.title("Interruptions vs Focus Duration")
    plt.xlabel("Number of Interruptions")
    plt.ylabel("Focus Duration (Minutes)")
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "interruptions_vs_focus.png",
        dpi=300
    )

    plt.close()

    print("3. Interruption analysis chart saved.")

    # -----------------------------------------
    # Display summary
    # -----------------------------------------

    print("\nAverage focus duration by task type:")
    print(focus_by_task.round(2))

    print("\nAverage cognitive load by task type:")
    print(load_by_task.round(2))

    print("\nAll visualizations generated successfully!")

    print(f"\nCharts saved in:\n{FIGURES_DIR}")


if __name__ == "__main__":
    main()

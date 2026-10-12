"""
CogniStream: Developer Flow-State & Cognitive Load Analytics

Purpose:
Generate synthetic developer activity data for analysis.
"""

import random
from pathlib import Path

import pandas as pd


# Ensure the same sample data can be reproduced.
random.seed(42)

# Find the project's root directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the output location.
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "developer_activity.csv"


def generate_developer_data(number_of_sessions=500):
    """Generate sample developer work-session records."""

    developers = [f"DEV{i:03d}" for i in range(1, 11)]
    task_types = ["Coding", "Debugging", "Code Review", "Testing", "Documentation"]
    complexities = ["Low", "Medium", "High"]

    records = []

    for session_number in range(1, number_of_sessions + 1):
        session_duration = random.randint(30, 120)
        focus_duration = random.randint(10, session_duration)
        interruptions = random.randint(0, 10)
        task_switches = random.randint(0, 8)

        records.append(
            {
                "session_id": f"S{session_number:04d}",
                "developer_id": random.choice(developers),
                "date": pd.Timestamp("2026-10-12")
                + pd.Timedelta(days=random.randint(0, 29)),
                "start_hour": random.randint(9, 17),
                "task_type": random.choice(task_types),
                "session_duration_min": session_duration,
                "focus_duration_min": focus_duration,
                "interruptions": interruptions,
                "task_switches": task_switches,
                "task_complexity": random.choice(complexities),
                "cognitive_load_rating": random.randint(1, 5),
                "tasks_completed": random.randint(0, 5),
            }
        )

    return pd.DataFrame(records)


def main():
    """Generate the dataset and save it as a CSV file."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = generate_developer_data()

    data.to_csv(OUTPUT_FILE, index=False)

    print("Developer activity dataset generated successfully!")
    print(f"Total records: {len(data)}")
    print(f"Saved to: {OUTPUT_FILE}")

    print("\nFirst five records:")
    print(data.head())


if __name__ == "__main__":
    main()
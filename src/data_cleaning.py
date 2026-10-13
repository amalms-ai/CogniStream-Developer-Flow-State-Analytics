"""
CogniStream: Developer Flow-State & Cognitive Load Analytics

Purpose:
Validate and clean the synthetic developer activity dataset.
"""

from pathlib import Path

import pandas as pd


# Locate the project directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input and output files.
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "developer_activity.csv"

PROCESSED_FILE = (
    PROJECT_ROOT / "data" / "processed" / "developer_activity_cleaned.csv"
)


# Columns expected in the dataset.
REQUIRED_COLUMNS = [
    "session_id",
    "developer_id",
    "date",
    "start_hour",
    "task_type",
    "session_duration_min",
    "focus_duration_min",
    "interruptions",
    "task_switches",
    "task_complexity",
    "cognitive_load_rating",
    "tasks_completed",
]

VALID_TASK_TYPES = {
    "Coding",
    "Debugging",
    "Code Review",
    "Testing",
    "Documentation",
}

VALID_COMPLEXITIES = {"Low", "Medium", "High"}


def clean_data():
    """Validate the raw dataset and save a cleaned copy."""

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_FILE}"
        )

    # Load the original dataset.
    df = pd.read_csv(RAW_FILE)

    print("Original dataset shape:", df.shape)

    # Check that all expected columns exist.
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {sorted(missing_columns)}"
        )

    # Keep only the expected project columns.
    df = df[REQUIRED_COLUMNS].copy()

    # Convert date values to proper dates.
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert numeric columns to numeric data types.
    numeric_columns = [
        "start_hour",
        "session_duration_min",
        "focus_duration_min",
        "interruptions",
        "task_switches",
        "cognitive_load_rating",
        "tasks_completed",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Remove records with missing required values.
    before_missing_check = len(df)

    df = df.dropna(subset=REQUIRED_COLUMNS).copy()

    removed_missing = before_missing_check - len(df)

    # Remove duplicate session IDs.
    before_duplicate_check = len(df)

    df = df.drop_duplicates(subset=["session_id"], keep="first")

    removed_duplicates = before_duplicate_check - len(df)

    # Validate text fields.
    df["session_id"] = df["session_id"].astype(str).str.strip()
    df["developer_id"] = df["developer_id"].astype(str).str.strip()
    df["task_type"] = df["task_type"].astype(str).str.strip()
    df["task_complexity"] = (
        df["task_complexity"].astype(str).str.strip().str.title()
    )

    # Define the valid-record conditions.
    valid_records = (
        df["session_id"].ne("")
        & df["developer_id"].ne("")
        & df["date"].notna()
        & df["start_hour"].between(0, 23)
        & df["task_type"].isin(VALID_TASK_TYPES)
        & df["session_duration_min"].between(1, 120)
        & df["focus_duration_min"].between(
            0, df["session_duration_min"]
        )
        & df["interruptions"].ge(0)
        & df["task_switches"].ge(0)
        & df["task_complexity"].isin(VALID_COMPLEXITIES)
        & df["cognitive_load_rating"].between(1, 5)
        & df["tasks_completed"].ge(0)
    )

    before_validation = len(df)

    df = df.loc[valid_records].copy()

    removed_invalid = before_validation - len(df)

    # Convert numeric columns to integer types.
    for column in numeric_columns:
        df[column] = df[column].astype(int)

    # Save the cleaned dataset separately.
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED_FILE, index=False)

    # Report the results.
    print("\nData cleaning completed successfully!")
    print("Records removed for missing values:", removed_missing)
    print("Duplicate sessions removed:", removed_duplicates)
    print("Invalid records removed:", removed_invalid)
    print("Cleaned dataset shape:", df.shape)
    print("Remaining missing values:", int(df.isna().sum().sum()))
    print("Remaining duplicate session IDs:",
          int(df["session_id"].duplicated().sum()))
    print("Saved cleaned dataset to:", PROCESSED_FILE)


if __name__ == "__main__":
    clean_data()
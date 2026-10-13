from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)

REPORT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "data_quality_report.txt"
)


def generate_report():
    df = pd.read_csv(DATA_FILE)

    report = [
        "COGNISTREAM - DATA QUALITY REPORT",
        "=" * 40,
        f"Total records: {len(df)}",
        f"Total columns: {len(df.columns)}",
        f"Missing values: {df.isna().sum().sum()}",
        f"Duplicate session IDs: "
        f"{df['session_id'].duplicated().sum()}",
        f"Unique developers: {df['developer_id'].nunique()}",
        "",
        "Column names:",
        *df.columns.tolist(),
    ]

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print("\n".join(report))
    print(f"\nReport saved to: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()
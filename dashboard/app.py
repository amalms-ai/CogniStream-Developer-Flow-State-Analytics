from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "developer_activity_cleaned.csv"
)


# Streamlit page configuration
st.set_page_config(
    page_title="CogniStream Analytics",
    page_icon="📊",
    layout="wide"
)


# Dashboard title
st.title("CogniStream: Developer Analytics Dashboard")

st.markdown(
    "Explore developer focus, cognitive load, interruptions, "
    "and productivity using interactive data visualizations."
)


# Load the existing processed dataset
@st.cache_data
def load_data(path):
    return pd.read_csv(path)


if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()


df = load_data(DATA_FILE)


# Check required columns for the existing dashboard
required_columns = [
    "task_type",
    "focus_duration_min",
    "cognitive_load_rating",
    "interruptions",
    "tasks_completed"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The dataset is missing these columns: "
        + ", ".join(missing_columns)
    )
    st.info(
        "Check the actual column names in "
        "developer_activity_cleaned.csv before proceeding."
    )
    st.stop()


# Sidebar filters
st.sidebar.header("Dashboard Filters")

task_types = sorted(
    df["task_type"].dropna().unique().tolist()
)

selected_tasks = st.sidebar.multiselect(
    "Select task types",
    options=task_types,
    default=task_types
)


# Apply task-type filter
filtered_df = df[
    df["task_type"].isin(selected_tasks)
].copy()


if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()


# KPI cards
st.subheader("Developer Activity Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sessions",
    f"{len(filtered_df):,}"
)

col2.metric(
    "Average Focus Duration",
    f"{filtered_df['focus_duration_min'].mean():.1f} min"
)

col3.metric(
    "Average Cognitive Load",
    f"{filtered_df['cognitive_load_rating'].mean():.2f}"
)

col4.metric(
    "Total Interruptions",
    f"{filtered_df['interruptions'].sum():,.0f}"
)

st.divider()


# Focus duration by task type
st.subheader("Focus Duration by Task Type")

focus_summary = (
    filtered_df.groupby("task_type", as_index=False)
    ["focus_duration_min"]
    .mean()
    .sort_values("focus_duration_min", ascending=False)
)

focus_chart = px.bar(
    focus_summary,
    x="task_type",
    y="focus_duration_min",
    color="focus_duration_min",
    labels={
        "task_type": "Task Type",
        "focus_duration_min": "Average Focus Duration (minutes)"
    },
    title="Average Focus Duration Across Task Types"
)

st.plotly_chart(
    focus_chart,
    use_container_width=True
)


# Cognitive load by task type
st.subheader("Cognitive Load by Task Type")

load_summary = (
    filtered_df.groupby("task_type", as_index=False)
    ["cognitive_load_rating"]
    .mean()
)

load_chart = px.bar(
    load_summary,
    x="task_type",
    y="cognitive_load_rating",
    color="cognitive_load_rating",
    labels={
        "task_type": "Task Type",
        "cognitive_load_rating": "Average Cognitive Load"
    },
    title="Average Cognitive Load Across Task Types"
)

st.plotly_chart(
    load_chart,
    use_container_width=True
)


# Completed tasks by task type
st.subheader("Completed Tasks by Task Type")

productivity_summary = (
    filtered_df.groupby("task_type", as_index=False)
    ["tasks_completed"]
    .sum()
    .sort_values("tasks_completed", ascending=False)
)

productivity_chart = px.bar(
    productivity_summary,
    x="task_type",
    y="tasks_completed",
    labels={
        "task_type": "Task Type",
        "tasks_completed": "Total Tasks Completed"
    },
    title="Total Completed Tasks Across Task Types"
)

st.plotly_chart(
    productivity_chart,
    use_container_width=True
)


# ==========================================================
# DAY 16: DEVELOPER PERFORMANCE COMPARISON
# ==========================================================

st.divider()

st.header("Developer Performance Comparison")

st.markdown(
    "Compare developer activity, completed tasks, focus duration, "
    "interruptions, and cognitive load."
)


# Check columns required for developer-level analysis
developer_required_columns = [
    "developer_id",
    "tasks_completed",
    "focus_duration_min",
    "interruptions",
    "cognitive_load_rating"
]

missing_developer_columns = [
    column for column in developer_required_columns
    if column not in filtered_df.columns
]


if not missing_developer_columns:

    # Aggregate activity metrics for each developer
    aggregation_rules = {
        "total_tasks_completed": ("tasks_completed", "sum"),
        "average_focus_duration": ("focus_duration_min", "mean"),
        "average_interruptions": ("interruptions", "mean"),
        "average_cognitive_load": ("cognitive_load_rating", "mean")
    }

    # Count sessions using session_id when available
    if "session_id" in filtered_df.columns:
        aggregation_rules["total_sessions"] = (
            "session_id",
            "nunique"
        )
    else:
        aggregation_rules["total_sessions"] = (
            "developer_id",
            "size"
        )

    developer_summary = (
        filtered_df.groupby("developer_id")
        .agg(**aggregation_rules)
        .reset_index()
    )

    # Round average metrics for readability
    numeric_columns = developer_summary.select_dtypes(
        include="number"
    ).columns

    developer_summary[numeric_columns] = (
        developer_summary[numeric_columns].round(2)
    )

    # Developer performance table
    st.subheader("Developer Performance Metrics")

    st.dataframe(
        developer_summary,
        use_container_width=True,
        hide_index=True
    )


    # Tasks completed by developer
    st.subheader("Tasks Completed by Developer")

    tasks_chart = px.bar(
        developer_summary.sort_values(
            "total_tasks_completed",
            ascending=False
        ),
        x="developer_id",
        y="total_tasks_completed",
        color="total_tasks_completed",
        labels={
            "developer_id": "Developer",
            "total_tasks_completed": "Total Tasks Completed"
        },
        title="Total Completed Tasks by Developer"
    )

    st.plotly_chart(
        tasks_chart,
        use_container_width=True
    )


    # Average focus duration by developer
    st.subheader("Average Focus Duration by Developer")

    focus_developer_chart = px.bar(
        developer_summary.sort_values(
            "average_focus_duration",
            ascending=False
        ),
        x="developer_id",
        y="average_focus_duration",
        color="average_focus_duration",
        labels={
            "developer_id": "Developer",
            "average_focus_duration": "Average Focus Duration (minutes)"
        },
        title="Average Focus Duration by Developer"
    )

    st.plotly_chart(
        focus_developer_chart,
        use_container_width=True
    )


    # Average interruptions by developer
    st.subheader("Average Interruptions by Developer")

    interruptions_chart = px.bar(
        developer_summary.sort_values(
            "average_interruptions",
            ascending=False
        ),
        x="developer_id",
        y="average_interruptions",
        color="average_interruptions",
        labels={
            "developer_id": "Developer",
            "average_interruptions": "Average Interruptions"
        },
        title="Average Interruptions per Session by Developer"
    )

    st.plotly_chart(
        interruptions_chart,
        use_container_width=True
    )


    # Average cognitive load by developer
    st.subheader("Average Cognitive Load by Developer")

    cognitive_load_chart = px.bar(
        developer_summary.sort_values(
            "average_cognitive_load",
            ascending=False
        ),
        x="developer_id",
        y="average_cognitive_load",
        color="average_cognitive_load",
        labels={
            "developer_id": "Developer",
            "average_cognitive_load": "Average Cognitive Load"
        },
        title="Average Cognitive Load by Developer"
    )

    st.plotly_chart(
        cognitive_load_chart,
        use_container_width=True
    )


else:
    st.warning(
        "Developer performance comparison cannot be generated. "
        "Missing columns: "
        + ", ".join(missing_developer_columns)
    )


# Filtered dataset preview
st.divider()

with st.expander("View Filtered Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# Download filtered dataset
st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="cognistream_filtered_data.csv",
    mime="text/csv"
)


# Dashboard footer
st.caption(
    "CogniStream | Developer Flow-State & Cognitive Load Analytics"
)

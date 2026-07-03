import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Google Play Store Dashboard",
    layout="wide"
)

# ---------------- Sidebar ----------------

st.sidebar.title("📊 Dashboard Menu")

menu = st.sidebar.radio(
    "Select a Task",
    (
        "Home",
        "Task 1",
        "Task 2",
        "Task 3",
        "Task 4",
        "Task 5",
        "Task 6"
    )
)


# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("googleplaystore.csv")
    return df

df = load_data()

if menu == "Home":

    st.title("📱 Google Play Store Dashboard")
    st.write("Internship Project Dashboard")


# -------------------- Data Cleaning --------------------

df = df.dropna(subset=[
    'Category',
    'Rating',
    'Reviews',
    'Installs',
    'Size',
    'Last Updated'
])

df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

df["Installs"] = (
    df["Installs"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace("+", "", regex=False)
)

df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")


def convert_size(size):
    if pd.isna(size):
        return None

    size = str(size)

    if size.endswith("M"):
        return float(size[:-1])

    elif size.endswith("k"):
        return float(size[:-1]) / 1024

    return None


df["Size_MB"] = df["Size"].apply(convert_size)

df["Last Updated"] = pd.to_datetime(
    df["Last Updated"],
    errors="coerce"
)

if menu == "Task 1":

    st.header("📊 Task 1 : App Installs Analysis Dashboard")

    from datetime import datetime
    import pytz

    india = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(india).time()

    start_time = datetime.strptime("15:00", "%H:%M").time()
    end_time = datetime.strptime("17:00", "%H:%M").time()

    if start_time <= current_time <= end_time:

        filtered_df = df[
            (df["Rating"] >= 4.0) &
            (df["Size_MB"] >= 10) &
            (df["Last Updated"].dt.month == 1)
        ]

        top_categories = (
            filtered_df.groupby("Category")["Installs"]
            .sum()
            .nlargest(10)
            .index
        )

        top_df = filtered_df[
            filtered_df["Category"].isin(top_categories)
        ]

        chart_data = (
            top_df.groupby("Category")
            .agg(
                Average_Rating=("Rating", "mean"),
                Total_Reviews=("Reviews", "sum")
            )
            .reset_index()
        )

        fig = px.bar(
            chart_data,
            x="Category",
            y=["Average_Rating", "Total_Reviews"],
            barmode="group",
            title="Average Rating vs Total Reviews"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.warning(
            " This chart is available only between "
            "3:00 PM IST and 5:00 PM IST."
        )

if menu == "Task 2":
    st.header("📊 Task 2")
    st.info("Coming Soon")

if menu == "Task 2":

    st.header("🌍 Task 2 : Interactive Choropleth Map")

    task2_df = df.copy()

    # Clean Installs
    task2_df["Installs"] = (
        task2_df["Installs"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("+", "", regex=False)
    )

    task2_df["Installs"] = pd.to_numeric(
        task2_df["Installs"],
        errors="coerce"
    )

    task2_df = task2_df.dropna(
        subset=["Category", "Installs"]
    )

    # Filter Categories
    task2_df = task2_df[
        ~task2_df["Category"]
        .str.startswith(("A", "C", "G", "S"))
    ]

    # Top 5 Categories
    top5 = (
        task2_df.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    countries = [
        "India",
        "USA",
        "Brazil",
        "Germany",
        "Japan"
    ]

    top5["Country"] = countries[:len(top5)]

    top5["Highlight"] = top5["Installs"].apply(
        lambda x:
        "Above 1 Million"
        if x > 1000000
        else "Below 1 Million"
    )

    st.dataframe(top5)

    fig = px.choropleth(
        top5,
        locations="Country",
        locationmode="country names",
        color="Installs",
        hover_name="Category",
        hover_data=["Highlight"],
        title="Global App Installs by Top 5 Categories"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
if menu == "Task 3":
    st.header("📈 Task 3")
    st.info("Coming Soon")

if menu == "Task 3":

    st.header("📈 Task 3 : Average Installs vs Revenue")

    from datetime import datetime
    from zoneinfo import ZoneInfo
    import plotly.graph_objects as go

    current_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).time()

    start_time = datetime.strptime(
        "13:00",
        "%H:%M"
    ).time()

    end_time = datetime.strptime(
        "14:00",
        "%H:%M"
    ).time()

    if start_time <= current_time <= end_time:

        task3_df = df.copy()

        # -------------------------
        # Clean Installs
        # -------------------------
        task3_df["Installs"] = (
            task3_df["Installs"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("+", "", regex=False)
        )

        task3_df["Installs"] = pd.to_numeric(
            task3_df["Installs"],
            errors="coerce"
        )

        # -------------------------
        # Clean Price
        # -------------------------
        task3_df["Price"] = (
            task3_df["Price"]
            .astype(str)
            .str.replace("$", "", regex=False)
        )

        task3_df["Price"] = pd.to_numeric(
            task3_df["Price"],
            errors="coerce"
        )

        # Revenue
        task3_df["Revenue"] = (
            task3_df["Price"]
            * task3_df["Installs"]
        )

        # -------------------------
        # Android Version
        # -------------------------
        task3_df["Android Ver"] = (
            task3_df["Android Ver"]
            .astype(str)
            .str.extract(r"(\d+\.\d+)")
        )

        task3_df["Android Ver"] = pd.to_numeric(
            task3_df["Android Ver"],
            errors="coerce"
        )

        # -------------------------
        # Size in MB
        # -------------------------
        def convert_size_task3(size):

            if pd.isna(size):
                return None

            size = str(size)

            if size.endswith("M"):
                return float(size[:-1])

            elif size.endswith("k"):
                return float(size[:-1]) / 1024

            return None

        task3_df["Size_MB"] = task3_df["Size"].apply(
            convert_size_task3
        )

        # -------------------------
        # App Name Length
        # -------------------------
        task3_df = task3_df[
            task3_df["App"]
            .astype(str)
            .str.len() <= 30
        ]

        # -------------------------
        # Required Filters
        # -------------------------
        task3_df = task3_df[

            (task3_df["Installs"] >= 10000)

            &

            (task3_df["Revenue"] >= 10000)

            &

            (task3_df["Android Ver"] > 4.0)

            &

            (task3_df["Size_MB"] > 15)

            &

            (task3_df["Content Rating"] == "Everyone")

        ]

        # -------------------------
        # Top 3 Categories
        # -------------------------
        top3 = (

            task3_df
            .groupby("Category")["Installs"]
            .sum()
            .nlargest(3)
            .index

        )

        task3_df = task3_df[
            task3_df["Category"].isin(top3)
        ]

        # -------------------------
        # Average Installs & Revenue
        # -------------------------
        result = (

            task3_df
            .groupby("Type")
            .agg(

                Average_Installs=("Installs", "mean"),

                Average_Revenue=("Revenue", "mean")

            )
            .reset_index()

        )

        # -------------------------
        # Dual Axis Chart
        # -------------------------

        fig = go.Figure()

        fig.add_bar(

            x=result["Type"],

            y=result["Average_Installs"],

            name="Average Installs"

        )

        fig.add_scatter(

            x=result["Type"],

            y=result["Average_Revenue"],

            mode="lines+markers",

            name="Average Revenue",

            yaxis="y2"

        )

        fig.update_layout(

            title="Average Installs vs Revenue (Free vs Paid)",

            xaxis_title="App Type",

            yaxis=dict(

                title="Average Installs"

            ),

            yaxis2=dict(

                title="Average Revenue ($)",

                overlaying="y",

                side="right"

            ),

            legend_title="Metrics"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    else:

        st.info(
            "⏰ This graph is available only between 1:00 PM and 2:00 PM IST."
        )

if menu == "Task 4":
    st.header("📉 Task 4")
    st.info("Coming Soon")

if menu == "Task 5":
    st.header("📋 Task 5")
    st.info("Coming Soon")

if menu == "Task 6":
    st.header("📌 Task 6")
    st.info("Coming Soon")

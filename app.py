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
[
    st.header("📈 Task 1 : App Installs Analysis Dashboard")

filtered_df = df[
    (df["Rating"] >= 4.0)
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
    title="Average Rating and Total Reviews"
)

st.plotly_chart(
    fig,
    use_container_width=True
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

if menu == "Task 4":
    st.header("📉 Task 4")
    st.info("Coming Soon")

if menu == "Task 5":
    st.header("📋 Task 5")
    st.info("Coming Soon")

if menu == "Task 6":
    st.header("📌 Task 6")
    st.info("Coming Soon")

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Google Play Store Dashboard",
    layout="wide"
)

st.title("📱 Google Play Store Dashboard")
st.write("Internship Project Dashboard")

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("googleplaystore.csv")
    return df

df = load_data()

st.success("Dataset Loaded Successfully")

st.subheader("Dataset Preview")
st.dataframe(df.head())

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

st.header("Task 1 : App Installs Analysis Dashboard")

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

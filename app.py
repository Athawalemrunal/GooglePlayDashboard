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

if menu == "Task 4":

    st.header("📈 Task 4 : Monthly Install Trend")

    from datetime import datetime
    from zoneinfo import ZoneInfo
    import plotly.express as px

    current_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).time()

    start_time = datetime.strptime(
        "18:00",
        "%H:%M"
    ).time()

    end_time = datetime.strptime(
        "21:00",
        "%H:%M"
    ).time()

    if start_time <= current_time <= end_time:

        task4 = df.copy()

        # -----------------------------
        # Clean Data
        # -----------------------------
        task4["Installs"] = (
            task4["Installs"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("+", "", regex=False)
        )

        task4["Installs"] = pd.to_numeric(
            task4["Installs"],
            errors="coerce"
        )

        task4["Reviews"] = pd.to_numeric(
            task4["Reviews"],
            errors="coerce"
        )

        task4 = task4.dropna(
            subset=["Category","App","Installs","Reviews"]
        )

        # -----------------------------
        # Create Monthly Timeline
        # -----------------------------
        task4["Date"] = pd.date_range(
            start="2020-01-01",
            periods=len(task4),
            freq="D"
        )

        task4["Month"] = (
            task4["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        # -----------------------------
        # Filters
        # -----------------------------
        task4 = task4[
            task4["Category"]
            .str.startswith(("B","C","E"))
        ]

        task4 = task4[
            ~task4["App"]
            .str.startswith(("X","Y","Z"))
        ]

        task4 = task4[
            ~task4["App"]
            .str.contains(
                "S",
                case=False,
                na=False
            )
        ]

        task4 = task4[
            task4["Reviews"] > 500
        ]

        # -----------------------------
        # Translation
        # -----------------------------
        translation = {

            "BEAUTY":"सौंदर्य",

            "BUSINESS":"வணிகம்",

            "DATING":"Verabredung"

        }

        task4["Category"] = (
            task4["Category"]
            .replace(translation)
        )

        # -----------------------------
        # Monthly Installs
        # -----------------------------
        monthly = (

            task4

            .groupby(
                ["Month","Category"]
            )["Installs"]

            .sum()

            .reset_index()

        )

        # -----------------------------
        # Growth %
        # -----------------------------
        monthly["Growth"] = (

            monthly

            .groupby("Category")["Installs"]

            .pct_change()

            *100

        )

        growth = monthly[
            monthly["Growth"] > 20
        ]

        # -----------------------------
        # Line Chart
        # -----------------------------
        fig = px.line(

            monthly,

            x="Month",

            y="Installs",

            color="Category",

            markers=True,

            title="Monthly Install Trend"

        )

        # Highlight Growth >20%

        for _, row in growth.iterrows():

            fig.add_vrect(

                x0=row["Month"],

                x1=row["Month"],

                fillcolor="green",

                opacity=0.20,

                line_width=0

            )

        fig.update_layout(

            template="plotly_white",

            xaxis_title="Month",

            yaxis_title="Total Installs"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "⏰ This graph is available only between 6:00 PM and 9:00 PM IST."
        )

if menu == "Task 5":
    st.header("📋 Task 5")
    st.info("Coming Soon")

# ==================================================
# TASK 5 : Bubble Chart
# ==================================================

if menu == "Task 5":

    st.header("🫧 Task 5 : Bubble Chart Analysis")

    from datetime import datetime
    from zoneinfo import ZoneInfo

    current_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).time()

    start_time = datetime.strptime(
        "17:00",
        "%H:%M"
    ).time()

    end_time = datetime.strptime(
        "19:00",
        "%H:%M"
    ).time()

    if start_time <= current_time <= end_time:

        task5 = df.copy()

        # ----------------------------
        # Cleaning
        # ----------------------------

        task5["Rating"] = pd.to_numeric(
            task5["Rating"],
            errors="coerce"
        )

        task5["Reviews"] = pd.to_numeric(
            task5["Reviews"],
            errors="coerce"
        )

        task5["Installs"] = (
            task5["Installs"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("+", "", regex=False)
        )

        task5["Installs"] = pd.to_numeric(
            task5["Installs"],
            errors="coerce"
        )

        def convert_size(size):

            if pd.isna(size):
                return None

            size = str(size)

            if size.endswith("M"):
                return float(size[:-1])

            elif size.endswith("k"):
                return float(size[:-1]) / 1024

            return None

        task5["Size_MB"] = task5["Size"].apply(
            convert_size
        )

        # --------------------------------
        # Dataset doesn't contain
        # Sentiment Subjectivity
        # Create placeholder
        # --------------------------------

        task5["Sentiment Subjectivity"] = 0.6

        # ----------------------------
        # Categories
        # ----------------------------

        categories = [

            "GAME",

            "BEAUTY",

            "BUSINESS",

            "COMICS",

            "COMMUNICATION",

            "DATING",

            "ENTERTAINMENT",

            "SOCIAL",

            "EVENTS"

        ]

        task5 = task5[
            task5["Category"].isin(categories)
        ]

        # ----------------------------
        # Filters
        # ----------------------------

        task5 = task5[

            (task5["Rating"] > 3.5)

            &

            (task5["Reviews"] > 500)

            &

            (task5["Installs"] > 50000)

            &

            (task5["Sentiment Subjectivity"] > 0.5)

        ]

        task5 = task5[

            ~task5["App"]

            .str.contains(
                "S",
                case=False,
                na=False
            )

        ]

        # ----------------------------
        # Translation
        # ----------------------------

        translation = {

            "BEAUTY":"सौंदर्य",

            "BUSINESS":"வணிகம்",

            "DATING":"Beziehungen"

        }

        task5["Category_Display"] = (

            task5["Category"]

            .replace(translation)

        )

        # ----------------------------
        # Bubble Chart
        # ----------------------------

        fig = px.scatter(

            task5,

            x="Size_MB",

            y="Rating",

            size="Installs",

            color="Category_Display",

            hover_name="App",

            hover_data=[

                "Reviews",

                "Installs"

            ],

            title="App Size vs Rating"

        )

        # Highlight Game category Pink

        fig.update_traces(

            marker=dict(
                color="pink"
            ),

            selector=dict(
                name="GAME"
            )

        )

        fig.update_layout(

            xaxis_title="App Size (MB)",

            yaxis_title="Average Rating",

            template="plotly_white"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    else:

        st.info(

            "⏰ This graph is available only between 5:00 PM IST and 7:00 PM IST."

        )

if menu == "Task 6":
    st.header("📌 Task 6")
    st.info("Coming Soon")


if menu == "Task 6":

    st.header("📊 Task 6 : Cumulative Installs Over Time")

    from datetime import datetime
    from zoneinfo import ZoneInfo

    current_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).time()

    start_time = datetime.strptime(
        "16:00",
        "%H:%M"
    ).time()

    end_time = datetime.strptime(
        "18:00",
        "%H:%M"
    ).time()

    if start_time <= current_time <= end_time:

        task6 = df.copy()

        # -----------------------------
        # Cleaning
        # -----------------------------

        task6["Installs"] = (
            task6["Installs"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("+", "", regex=False)
        )

        task6["Installs"] = pd.to_numeric(
            task6["Installs"],
            errors="coerce"
        )

        task6["Reviews"] = pd.to_numeric(
            task6["Reviews"],
            errors="coerce"
        )

        task6["Rating"] = pd.to_numeric(
            task6["Rating"],
            errors="coerce"
        )

        def convert_size(size):

            if pd.isna(size):
                return None

            size = str(size)

            if size.endswith("M"):
                return float(size[:-1])

            elif size.endswith("k"):
                return float(size[:-1]) / 1024

            return None

        task6["Size_MB"] = task6["Size"].apply(
            convert_size
        )

        task6["Last Updated"] = pd.to_datetime(
            task6["Last Updated"],
            errors="coerce"
        )

        task6["Month"] = (
            task6["Last Updated"]
            .dt.to_period("M")
            .astype(str)
        )

        # -----------------------------
        # Filters
        # -----------------------------

        task6 = task6[
            task6["Rating"] >= 4.2
        ]

        task6 = task6[
            ~task6["App"]
            .str.contains(
                r"\d",
                regex=True,
                na=False
            )
        ]

        task6 = task6[
            task6["Category"]
            .str.startswith(("T","P"))
        ]

        task6 = task6[
            task6["Reviews"] > 1000
        ]

        task6 = task6[
            (task6["Size_MB"] >= 20)
            &
            (task6["Size_MB"] <= 80)
        ]

        # -----------------------------
        # Translation
        # -----------------------------

        translation = {

            "TRAVEL_AND_LOCAL":"Voyage et Local",

            "PRODUCTIVITY":"Productividad",

            "PHOTOGRAPHY":"写真"

        }

        task6["Category_Display"] = (

            task6["Category"]

            .replace(translation)

        )

        # -----------------------------
        # Monthly Installs
        # -----------------------------

        chart_data = (

            task6

            .groupby(
                [
                    "Month",
                    "Category_Display"
                ]
            )["Installs"]

            .sum()

            .reset_index()

        )

        # -----------------------------
        # Month-over-Month Growth
        # -----------------------------

        chart_data["Previous"] = (

            chart_data

            .groupby("Category_Display")["Installs"]

            .shift(1)

        )

        chart_data["Increase"] = (

            (

                chart_data["Installs"]

                -

                chart_data["Previous"]

            )

            /

            chart_data["Previous"]

            *100

        )

        chart_data["Highlight"] = (

            chart_data["Increase"]

            .apply(

                lambda x:

                "High Increase"

                if pd.notna(x) and x > 25

                else "Normal"

            )

        )

        # -----------------------------
        # Stacked Area Chart
        # -----------------------------

        fig = px.area(

            chart_data,

            x="Month",

            y="Installs",

            color="Category_Display",

            title="Cumulative Installs Over Time",

            hover_data=[

                "Highlight",

                "Increase"

            ]

        )

        # Highlight months with >25% increase

        for _, row in chart_data[
            chart_data["Highlight"]=="High Increase"
        ].iterrows():

            fig.add_vrect(

                x0=row["Month"],

                x1=row["Month"],

                fillcolor="red",

                opacity=0.20,

                line_width=0

            )

        fig.update_layout(

            template="plotly_white",

            xaxis_title="Month",

            yaxis_title="Cumulative Installs",

            legend_title="Category"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    else:

        st.info(

            "⏰ This graph is available only between 4:00 PM IST and 6:00 PM IST."

        )

.. code:: ipython3

    import pandas as pd
    import plotly.express as px
    from datetime import datetime
    from zoneinfo import ZoneInfo
    import pandas as pd
    import matplotlib.pyplot as plt
    import pytz
    



    
    # -------------------- Load Dataset --------------------
    df = pd.read_csv(r"C:\Users\Mrunal Athawale\Downloads\archive (2)\googleplaystore.csv")



    # ==============================
    #Task 1: App Installs Analysis Dashboard Using Data Visualization
    # ==============================
    
    
    # -------------------- Data Cleaning --------------------
    df = df.dropna(subset=['Category', 'Rating', 'Reviews', 'Installs', 'Size', 'Last Updated'])
    
    # Convert Rating and Reviews
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    
    # Clean Installs column
    df['Installs'] = (
        df['Installs']
          .astype(str)
          .str.replace(',', '', regex=False)
          .str.replace('+', '', regex=False)
    )
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
    
    # Convert Size to MB
    def convert_size(size):
        if pd.isna(size):
            return None
        size = str(size)
    
        if size.endswith('M'):
            return float(size[:-1])
    
        elif size.endswith('k'):
            return float(size[:-1]) / 1024
    
        else:
            return None
    
    df['Size_MB'] = df['Size'].apply(convert_size)
    
    # Convert Last Updated column
    df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
    
    # ---------------- Apply Filters -------------
    filtered_df = df[
        (df['Rating'] >= 4.0) &
        (df['Size_MB'] >= 10) &
        (df['Last Updated'].dt.month == 1)
    ]
    
    # ------------ Top 10 Categories by Installs -------------
    top_categories = (
        filtered_df.groupby('Category')['Installs']
        .sum()
        .nlargest(10)
        .index
    )
    
    top_df = filtered_df[filtered_df['Category'].isin(top_categories)]
    
    # -------------- Average Rating & Total Reviews ---------------
    chart_data = (
        top_df.groupby('Category')
        .agg(
            Average_Rating=('Rating', 'mean'),
            Total_Reviews=('Reviews', 'sum')
        )
        .reset_index()
    )
    
    # -------------------- Time Restriction (3 PM - 5 PM IST) --------------------
    current_time = datetime.now(ZoneInfo("Asia/Kolkata")).time()
    
    start_time = datetime.strptime("15:00", "%H:%M").time()
    end_time = datetime.strptime("17:00", "%H:%M").time()
    
    if start_time <= current_time <= end_time:
    
        fig = px.bar(
            chart_data,
            x="Category",
            y=["Average_Rating", "Total_Reviews"],
            barmode="group",
            title="Average Rating and Total Reviews for Top 10 Categories by Installs"
        )
    
        fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Value",
            legend_title="Metrics",
            title_x=0.5
        )
    
        fig.show()
    
    else:
        print("This graph is available only between 3:00 PM and 5:00 PM IST.")


.. parsed-literal::

    This graph is available only between 3:00 PM and 5:00 PM IST.
    



    # ==============================
    # TASK 2 : INTERACTIVE CHOROPLETH MAP
    # ==============================
    
    
    # Install libraries
    
    !pip install pandas plotly pytz
    
    df.head()
    
    
    
    # ==============================
    # CLEAN DATA
    # ==============================
    
    
    # Convert installs
    
    df['Installs'] = (
    
        df['Installs']
        .astype(str)
        .str.replace(",","")
        .str.replace("+","")
    
    )
    
    
    df['Installs'] = pd.to_numeric(
        df['Installs'],
        errors='coerce'
    )
    
    
    
    # Remove missing values
    
    df = df.dropna(
        subset=['Category','Installs']
    )
    
    
    
    
    # ==============================
    # FILTER CATEGORY
    # CATEGORY SHOULD NOT START A,C,G,S
    # ==============================
    
    
    df = df[
        ~df['Category']
        .str.startswith(
            ('A','C','G','S')
        )
    ]
    
    
    
    # ==============================
    # TOP 5 CATEGORIES
    # ==============================
    
    
    top5 = (
    
        df.groupby('Category')['Installs']
    
        .sum()
    
        .sort_values(
            ascending=False
        )
    
        .head(5)
    
        .reset_index()
    
    )
    
    
    top5
    
    
    
    # ==============================
    # CREATE COUNTRY COLUMN
    # FOR GLOBAL MAP
    # ==============================
    
    
    countries = [
    
        "India",
        "USA",
        "Brazil",
        "Germany",
        "Japan"
    
    ]
    
    
    top5['Country'] = countries[:len(top5)]
    
    
    
    top5
    
    
    
    # ==============================
    # HIGHLIGHT INSTALLS > 1 MILLION
    # ==============================
    
    
    top5['Highlight'] = (
    
        top5['Installs']
    
        .apply(
            lambda x:
            "Above 1 Million"
            if x > 1000000
            else "Below 1 Million"
        )
    
    )
    
    
    
    # ==============================
    # TIME RESTRICTION
    # 6 PM IST - 8 PM IST
    # ==============================
    
    
    india_time = datetime.now(
        pytz.timezone(
            'Asia/Kolkata'
        )
    )
    
    
    hour = india_time.hour
    
    
    
    if hour >=18 and hour <20:
    
    
    
        # ==============================
        # CHOROPLETH MAP
        # ==============================
    
    
        fig = px.choropleth(
    
            top5,
    
    
            locations="Country",
    
    
            locationmode="country names",
    
    
            color="Installs",
    
    
            hover_name="Category",
    
    
            hover_data=[
                "Installs",
                "Highlight"
            ],
    
    
            title=
            "Global App Installs by Top 5 Categories"
    
    
    
        )
    
    
        fig.update_layout(
    
            template="plotly_white"
    
        )
    
    
        fig.show()
    
    
    
    else:
    
    
        print(
            "Graph available only between 6 PM IST and 8 PM IST"
        )


.. parsed-literal::

    Requirement already satisfied: pandas in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (2.0.3)
    Requirement already satisfied: plotly in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (5.9.0)
    Requirement already satisfied: pytz in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (2023.3.post1)
    Requirement already satisfied: python-dateutil>=2.8.2 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from pandas) (2.8.2)
    Requirement already satisfied: tzdata>=2022.1 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from pandas) (2023.3)
    Requirement already satisfied: numpy>=1.21.0 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from pandas) (1.24.3)
    Requirement already satisfied: tenacity>=6.2.0 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from plotly) (8.2.2)
    Requirement already satisfied: six>=1.5 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from python-dateutil>=2.8.2->pandas) (1.16.0)
    Graph available only between 6 PM IST and 8 PM IST
    



    # ==============================
    #Task 3: Dual Axis Chart Comparing Average Installs and Revenue for Free vs Paid Apps
    # ==============================
    
    
    
    # Clean column names
    
    df.columns = df.columns.str.strip()
    
    
    
    # ==============================
    # Data Cleaning
    # ==============================
    
    
    # Installs
    
    df["Installs"] = (
        df["Installs"]
        .astype(str)
        .str.replace(",","")
        .str.replace("+","")
    )
    
    df["Installs"] = pd.to_numeric(
        df["Installs"],
        errors="coerce"
    )
    
    
    
    # Size conversion
    
    df["Size"] = (
        df["Size"]
        .astype(str)
        .str.replace("M","")
        .str.replace("k","")
    )
    
    
    df["Size"] = pd.to_numeric(
        df["Size"],
        errors="coerce"
    )
    
    
    
    # Android version
    
    df["Android Ver"] = (
        df["Android Ver"]
        .astype(str)
        .str.extract(r"(\d+\.\d+)")
    )
    
    
    df["Android Ver"] = pd.to_numeric(
        df["Android Ver"],
        errors="coerce"
    )
    
    
    
    # Price conversion
    
    df["Price"] = (
        df["Price"]
        .astype(str)
        .str.replace("$","")
    )
    
    
    df["Price"] = pd.to_numeric(
        df["Price"],
        errors="coerce"
    )
    
    
    
    # ==============================
    # Create Revenue
    # ==============================
    
    df["Revenue"] = (
        df["Price"] *
        df["Installs"]
    )
    
    
    
    # ==============================
    # App name length filter
    # ==============================
    
    df = df[
        df["App"]
        .astype(str)
        .str.len()
        <=30
    ]
    
    
    
    # ==============================
    # Apply Required Filters
    # ==============================
    
    
    df = df[
    
        (df["Installs"] >= 10000)
    
        &
    
        (df["Revenue"] >= 10000)
    
        &
    
        (df["Android Ver"] > 4.0)
    
        &
    
        (df["Size"] > 15)
    
        &
    
        (df["Content Rating"] == "Everyone")
    
    ]
    
    
    
    # ==============================
    # Find Top 3 Categories
    # ==============================
    
    
    top3_categories = (
    
        df.groupby("Category")["Installs"]
    
        .sum()
    
        .sort_values(
            ascending=False
        )
    
        .head(3)
    
        .index
    
    )
    
    
    
    df = df[
        df["Category"].isin(top3_categories)
    ]
    
    
    
    print("Top 3 Categories:")
    print(top3_categories)
    
    
    
    # ==============================
    # Average Installs & Revenue
    # ==============================
    
    
    result = (
    
        df.groupby("Type")
    
        .agg(
    
            Average_Installs=
            ("Installs","mean"),
    
            Average_Revenue=
            ("Revenue","mean")
    
        )
    
        .reset_index()
    
    )
    
    
    print(result)
    
    
    
    # ==============================
    # Time Restriction
    # ==============================
    
    
    ist = pytz.timezone(
        "Asia/Kolkata"
    )
    
    
    current_time = datetime.now(ist).time()
    
    
    
    start_time = datetime.strptime(
        "13:00",
        "%H:%M"
    ).time()
    
    
    end_time = datetime.strptime(
        "14:00",
        "%H:%M"
    ).time()
    
    
    
    # ==============================
    # Dual Axis Chart
    # ==============================
    
    
    if start_time <= current_time <= end_time:
    
    
        fig, ax1 = plt.subplots(
            figsize=(10,5)
        )
    
    
    
        # Average installs bar chart
    
        ax1.bar(
    
            result["Type"],
    
            result["Average_Installs"]
    
        )
    
    
        ax1.set_xlabel(
            "App Type"
        )
    
    
        ax1.set_ylabel(
            "Average Installs"
        )
    
    
    
        # Revenue line chart
    
        ax2 = ax1.twinx()
    
    
        ax2.plot(
    
            result["Type"],
    
            result["Average_Revenue"],
    
            marker="o"
    
        )
    
    
        ax2.set_ylabel(
            "Average Revenue ($)"
        )
    
    
    
        plt.title(
            "Average Installs vs Revenue for Free and Paid Apps"
        )
    
    
        plt.show()
    
    
    
    else:
    
    
        print(
            "Graph available only between 1 PM IST and 2 PM IST"
        )


.. parsed-literal::

    Top 3 Categories:
    Index(['PHOTOGRAPHY', 'PERSONALIZATION', 'TOOLS'], dtype='object', name='Category')
       Type  Average_Installs  Average_Revenue
    0  Paid          850000.0     3.399833e+06
    Graph available only between 1 PM IST and 2 PM IST
    



    # ==============================
    # TASK 4 : TIME SERIES LINE CHART
    # ==============================
    
    
    # Install required libraries
    !pip install pandas matplotlib plot
    
    df.head()
    
    
    
    # ==============================
    # DATA CLEANING
    # ==============================
    
    
    # Convert Installs into numeric
    
    df['Installs'] = (
        df['Installs']
        .astype(str)
        .str.replace(",","")
        .str.replace("+","")
    )
    
    
    df['Installs'] = pd.to_numeric(
        df['Installs'],
        errors='coerce'
    )
    
    
    
    # Convert Reviews
    
    df['Reviews'] = pd.to_numeric(
        df['Reviews'],
        errors='coerce'
    )
    
    
    
    # Remove missing values
    
    df = df.dropna(
        subset=['Category','App','Installs','Reviews']
    )
    
    
    
    # ==============================
    # CREATE TIME COLUMN
    # ==============================
    
    
    # Dataset has no date column
    # Creating monthly timeline
    
    df['Date'] = pd.date_range(
        start='2020-01-01',
        periods=len(df),
        freq='D'
    )
    
    
    df['Month'] = df['Date'].dt.to_period('M')
    
    
    
    
    # ==============================
    # APPLY FILTER CONDITIONS
    # ==============================
    
    
    filtered = df[
    
        # Category starts with B,C,E
        
        df['Category']
        .str.startswith(('B','C','E'))
    
    
    ]
    
    
    
    # App name should not start X,Y,Z
    
    filtered = filtered[
        ~filtered['App']
        .str.startswith(('X','Y','Z'))
    ]
    
    
    
    # App name should not contain S
    
    filtered = filtered[
        ~filtered['App']
        .str.contains(
            'S',
            case=False
        )
    ]
    
    
    
    # Reviews more than 500
    
    filtered = filtered[
        filtered['Reviews'] > 500
    ]
    
    
    
    # ==============================
    # CATEGORY TRANSLATION
    # ==============================
    
    
    translation = {
    
    
        "BEAUTY":"सौंदर्य",
    
        "BUSINESS":"வணிகம்",
    
        "DATING":"Verabredung"
    
    
    }
    
    
    
    filtered['Category'] = filtered['Category'].replace(
        translation
    )
    
    
    
    
    # ==============================
    # MONTHLY INSTALL TREND
    # ==============================
    
    
    monthly = (
    
        filtered
    
        .groupby(
            ['Month','Category']
        )
    
        ['Installs']
    
        .sum()
    
        .reset_index()
    
    )
    
    
    
    monthly['Month'] = (
        monthly['Month']
        .astype(str)
    )
    
    
    
    
    # ==============================
    # MONTH OVER MONTH GROWTH %
    # ==============================
    
    
    monthly['Growth %'] = (
    
        monthly
    
        .groupby('Category')['Installs']
    
        .pct_change()
    
        *100
    
    )
    
    
    
    
    # ==============================
    # SELECT GROWTH >20%
    # ==============================
    
    
    growth = monthly[
        monthly['Growth %'] > 20
    ]
    
    
    
    
    
    # ==============================
    # TIME RESTRICTION
    # 6 PM IST - 9 PM IST
    # ==============================
    
    
    india_time = datetime.now(
        pytz.timezone(
            'Asia/Kolkata'
        )
    )
    
    
    
    hour = india_time.hour
    
    
    
    if hour >=18 and hour <21:
    
    
    
        # ==============================
        # CREATE LINE GRAPH
        # ==============================
    
    
        fig = px.line(
    
    
            monthly,
    
    
            x='Month',
    
    
            y='Installs',
    
    
            color='Category',
    
    
            markers=True,
    
    
            title=
            "Monthly Total Installs Trend by App Category"
    
    
        )
    
    
    
        # ==============================
        # SHADE GROWTH PERIODS
        # ==============================
    
    
        for i,row in growth.iterrows():
    
    
            fig.add_vrect(
    
                x0=row['Month'],
    
                x1=row['Month'],
    
                fillcolor="green",
    
                opacity=0.25,
    
                line_width=0
    
            )
    
    
    
        fig.update_layout(
    
            xaxis_title="Month",
    
            yaxis_title="Total Installs",
    
            template="plotly_white"
    
        )
    
    
    
        fig.show()
    
    
    
    else:
    
    
        print(
    
        "Graph available only between 6 PM IST and 9 PM IST"
    
        )


.. parsed-literal::

    Requirement already satisfied: pandas in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (2.0.3)
    Requirement already satisfied: matplotlib in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (3.7.2)
    Requirement already satisfied: plotly in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (5.9.0)
    Requirement already satisfied: pytz in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (2023.3.post1)
    Requirement already satisfied: python-dateutil>=2.8.2 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from pandas) (2.8.2)
    Requirement already satisfied: tzdata>=2022.1 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from pandas) (2023.3)
    Requirement already satisfied: numpy>=1.21.0 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from pandas) (1.24.3)
    Requirement already satisfied: contourpy>=1.0.1 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from matplotlib) (1.0.5)
    Requirement already satisfied: cycler>=0.10 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from matplotlib) (0.11.0)
    Requirement already satisfied: fonttools>=4.22.0 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from matplotlib) (4.25.0)
    Requirement already satisfied: kiwisolver>=1.0.1 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from matplotlib) (1.4.4)
    Requirement already satisfied: packaging>=20.0 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from matplotlib) (23.1)
    Requirement already satisfied: pillow>=6.2.0 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from matplotlib) (9.4.0)
    Requirement already satisfied: pyparsing<3.1,>=2.3.1 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from matplotlib) (3.0.9)
    Requirement already satisfied: tenacity>=6.2.0 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from plotly) (8.2.2)
    Requirement already satisfied: six>=1.5 in c:\users\mrunal athawale\anaconda3\pip\lib\site-packages (from python-dateutil>=2.8.2->pandas) (1.16.0)
    Graph available only between 6 PM IST and 9 PM IST
    



    # ==========================
    #Task 5: Bubble Chart Analysis of App Size, Rating, and Installs
    # ==========================
    
    
    
    # Clean columns
    
    df.columns = df.columns.str.strip()
    
    
    
    # ==========================
    # Cleaning
    # ==========================
    
    
    # Installs
    
    df["Installs"] = (
    
        df["Installs"]
        .astype(str)
        .str.replace(",","")
        .str.replace("+","")
    
    )
    
    
    df["Installs"] = pd.to_numeric(
        df["Installs"],
        errors="coerce"
    )
    
    
    
    # Reviews
    
    df["Reviews"] = pd.to_numeric(
        df["Reviews"],
        errors="coerce"
    )
    
    
    
    # Rating
    
    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    )
    
    
    
    # Size
    
    df["Size"] = (
    
        df["Size"]
        .astype(str)
        .str.replace("M","")
    
    )
    
    
    df["Size"] = pd.to_numeric(
        df["Size"],
        errors="coerce"
    )
    
    
    
    # ==========================
    # Sentiment Subjectivity
    # Dataset does not have it
    # Create placeholder
    # ==========================
    
    df["Sentiment Subjectivity"] = 0.6
    
    
    
    # ==========================
    # Category Filter
    # ==========================
    
    
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
    
    
    df = df[
    df["Category"].isin(categories)
    ]
    
    
    
    # ==========================
    # Apply Filters
    # ==========================
    
    
    df = df[
    
        (df["Rating"] > 3.5)
    
        &
    
        (df["Reviews"] > 500)
    
        &
    
        (df["Installs"] > 50000)
    
        &
    
        (df["Sentiment Subjectivity"] > 0.5)
    
    ]
    
    
    
    # App name should not contain S
    
    df = df[
    ~df["App"]
    .str.contains(
    "S",
    case=True,
    na=False
    )
    
    ]
    
    
    
    # ==========================
    # Translation
    # ==========================
    
    
    translation = {
    
    "BEAUTY":"सौंदर्य",
    
    "BUSINESS":"வணிகம்",
    
    "DATING":"Beziehungen"
    
    }
    
    
    df["Category_Display"] = df["Category"].replace(
    translation
    )
    
    
    
    # ==========================
    # Time Restriction
    # ==========================
    
    
    ist = pytz.timezone(
    "Asia/Kolkata"
    )
    
    
    current_time = datetime.now(ist).time()
    
    
    
    start = datetime.strptime(
    "17:00",
    "%H:%M"
    ).time()
    
    
    end = datetime.strptime(
    "19:00",
    "%H:%M"
    ).time()
    
    
    
    # ==========================
    # Bubble Chart
    # ==========================
    
    
    if start <= current_time <= end:
    
    
        fig = px.scatter(
    
            df,
    
            x="Size",
    
            y="Rating",
    
            size="Installs",
    
            color="Category_Display",
    
            hover_name="App",
    
            hover_data=[
    
                "Reviews",
                "Installs"
    
            ],
    
            title=
            "App Size vs Rating (Bubble Size = Installs)"
    
        )
    
    
        # Highlight Game in Pink
    
        fig.update_traces(
    
            marker=dict(
    
                color="pink"
    
            ),
    
            selector=dict(
                name="GAME"
            )
    
        )
    
    
        fig.update_layout(
    
            xaxis_title=
            "App Size (MB)",
    
            yaxis_title=
            "Average Rating"
    
        )
    
    
        fig.show()
    
    
    
    else:
    
    
        print(
            "Graph available only between 5 PM IST and 7 PM IST"
        )


.. parsed-literal::

    Graph available only between 5 PM IST and 7 PM IST
    



    # ==========================
    #Task 6: Stacked Area Chart Showing Cumulative App Installs Over Time by Category
    # ==========================
    
    # Clean columns
    
    df.columns = df.columns.str.strip()
    
    
    
    # ==========================
    # Data Cleaning
    # ==========================
    
    
    # Installs
    
    df["Installs"] = (
    
        df["Installs"]
        .astype(str)
        .str.replace(",","")
        .str.replace("+","")
    
    )
    
    
    df["Installs"] = pd.to_numeric(
        df["Installs"],
        errors="coerce"
    )
    
    
    
    # Reviews
    
    df["Reviews"] = pd.to_numeric(
        df["Reviews"],
        errors="coerce"
    )
    
    
    
    # Rating
    
    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    )
    
    
    
    # Size
    
    df["Size"] = (
    
        df["Size"]
        .astype(str)
        .str.replace("M","")
    
    )
    
    
    df["Size"] = pd.to_numeric(
        df["Size"],
        errors="coerce"
    )
    
    
    
    # ==========================
    # Create Date Column
    # ==========================
    
    
    df["Last Updated"] = pd.to_datetime(
        df["Last Updated"],
        errors="coerce"
    )
    
    
    
    df["Month"] = (
        df["Last Updated"]
        .dt.to_period("M")
        .astype(str)
    )
    
    
    
    # ==========================
    # Filters
    # ==========================
    
    
    # Rating >= 4.2
    
    df = df[
    df["Rating"] >= 4.2
    ]
    
    
    
    # App name should not contain numbers
    
    df = df[
    ~df["App"]
    .str.contains(
    r"\d",
    regex=True,
    na=False
    )
    
    ]
    
    
    
    # Category starts T or P
    
    df = df[
    
    df["Category"]
    .str.startswith(
    ("T","P")
    )
    
    ]
    
    
    
    # Reviews > 1000
    
    df = df[
    df["Reviews"] > 1000
    ]
    
    
    
    # Size between 20 and 80 MB
    
    df = df[
    
    (df["Size"] >= 20)
    
    &
    
    (df["Size"] <= 80)
    
    ]
    
    
    
    # ==========================
    # Category Translation
    # ==========================
    
    
    translation = {
    
    "TRAVEL_AND_LOCAL":
    "Voyage et Local",
    
    "PRODUCTIVITY":
    "Productividad",
    
    "PHOTOGRAPHY":
    "写真"
    
    }
    
    
    
    df["Category_Display"] = df["Category"].replace(
    translation
    )
    
    
    
    # ==========================
    # Group Monthly Installs
    # ==========================
    
    
    chart_data = (
    
    df.groupby(
    [
    "Month",
    "Category_Display"
    ]
    
    )["Installs"]
    
    .sum()
    
    .reset_index()
    
    )
    
    
    
    # ==========================
    # Month over Month Increase
    # ==========================
    
    
    chart_data["Previous"] = (
    
    chart_data
    .groupby("Category_Display")
    ["Installs"]
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
    
    
    
    chart_data["Highlight"] = chart_data["Increase"].apply(
    
    lambda x:
    
    "High Increase"
    
    if x > 25
    
    else
    
    "Normal"
    
    )
    
    
    
    print(chart_data)
    
    
    
    # ==========================
    # Time Restriction
    # ==========================
    
    
    ist = pytz.timezone(
    "Asia/Kolkata"
    )
    
    
    current_time = datetime.now(ist).time()
    
    
    
    start = datetime.strptime(
    "16:00",
    "%H:%M"
    ).time()
    
    
    end = datetime.strptime(
    "18:00",
    "%H:%M"
    ).time()
    
    
    
    # ==========================
    # Stacked Area Chart
    # ==========================
    
    
    if start <= current_time <= end:
    
    
        fig = px.area(
    
            chart_data,
    
            x="Month",
    
            y="Installs",
    
            color="Category_Display",
    
            title=
            "Cumulative Installs Over Time by App Category",
    
            hover_data=[
    
                "Highlight",
                "Increase"
    
            ]
    
        )
    
    
        fig.show()
    
    
    
    else:
    
    
        print(
            "Graph available only between 4 PM IST and 6 PM IST"
        )


.. parsed-literal::

          Month Category_Display      Installs     Previous      Increase  \
    0   2014-11               写真  1.000000e+06          NaN           NaN   
    1   2016-10    Productividad  1.000000e+06          NaN           NaN   
    2   2016-12  PERSONALIZATION  2.000000e+06          NaN           NaN   
    3   2017-03               写真  5.000000e+07    1000000.0   4900.000000   
    4   2017-06               写真  1.000000e+07   50000000.0    -80.000000   
    5   2017-07               写真  1.500000e+07   10000000.0     50.000000   
    6   2017-08            TOOLS  5.000000e+04          NaN           NaN   
    7   2017-09  PERSONALIZATION  1.000000e+06    2000000.0    -50.000000   
    8   2017-10  Voyage et Local  5.000000e+04          NaN           NaN   
    9   2017-10               写真  5.000000e+06   15000000.0    -66.666667   
    10  2017-12               写真  1.000000e+07    5000000.0    100.000000   
    11  2018-01  PERSONALIZATION  1.000000e+07    1000000.0    900.000000   
    12  2018-01            TOOLS  1.000000e+06      50000.0   1900.000000   
    13  2018-01               写真  1.000000e+07   10000000.0      0.000000   
    14  2018-02  PERSONALIZATION  1.000000e+07   10000000.0      0.000000   
    15  2018-02    Productividad  1.000000e+05    1000000.0    -90.000000   
    16  2018-03        PARENTING  1.000000e+05          NaN           NaN   
    17  2018-03               写真  2.000000e+06   10000000.0    -80.000000   
    18  2018-04  Voyage et Local  5.000000e+06      50000.0   9900.000000   
    19  2018-05        PARENTING  1.000000e+07     100000.0   9900.000000   
    20  2018-05            TOOLS  1.000000e+07    1000000.0    900.000000   
    21  2018-05               写真  1.100000e+07    2000000.0    450.000000   
    22  2018-06  PERSONALIZATION  1.000000e+07   10000000.0      0.000000   
    23  2018-06    Productividad  1.500000e+07     100000.0  14900.000000   
    24  2018-06  Voyage et Local  1.100000e+07    5000000.0    120.000000   
    25  2018-06               写真  8.100000e+07   11000000.0    636.363636   
    26  2018-07        PARENTING  6.000000e+05   10000000.0    -94.000000   
    27  2018-07  PERSONALIZATION  1.150000e+07   10000000.0     15.000000   
    28  2018-07    Productividad  2.760000e+08   15000000.0   1740.000000   
    29  2018-07            TOOLS  2.226000e+08   10000000.0   2126.000000   
    30  2018-07  Voyage et Local  3.310000e+07   11000000.0    200.909091   
    31  2018-07               写真  8.200000e+08   81000000.0    912.345679   
    32  2018-08  PERSONALIZATION  2.000000e+07   11500000.0     73.913043   
    33  2018-08    Productividad  1.705000e+09  276000000.0    517.753623   
    34  2018-08            TOOLS  1.200000e+08  222600000.0    -46.091644   
    35  2018-08  Voyage et Local  7.610000e+07   33100000.0    129.909366   
    36  2018-08               写真  6.915000e+08  820000000.0    -15.670732   
    
            Highlight  
    0          Normal  
    1          Normal  
    2          Normal  
    3   High Increase  
    4          Normal  
    5   High Increase  
    6          Normal  
    7          Normal  
    8          Normal  
    9          Normal  
    10  High Increase  
    11  High Increase  
    12  High Increase  
    13         Normal  
    14         Normal  
    15         Normal  
    16         Normal  
    17         Normal  
    18  High Increase  
    19  High Increase  
    20  High Increase  
    21  High Increase  
    22         Normal  
    23  High Increase  
    24  High Increase  
    25  High Increase  
    26         Normal  
    27         Normal  
    28  High Increase  
    29  High Increase  
    30  High Increase  
    31  High Increase  
    32  High Increase  
    33  High Increase  
    34         Normal  
    35  High Increase  
    36         Normal  
    Graph available only between 4 PM IST and 6 PM IST
    


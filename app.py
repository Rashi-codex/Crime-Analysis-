import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import folium
from streamlit_folium import st_folium
import json
from PIL import Image
try:
    import plotly.express as px
    import plotly.graph_objects as go
except Exception:
    # plotly may not be installed in the environment; degrade gracefully
    px = None
    go = None


df=pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\dsa\\nlp_interview\\CrimesOnWomenData.csv")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image=Image.open("C:\\Users\\asus\\OneDrive\\Desktop\\dsa\\nlp_interview\\crime.jpg")

col1, col2 = st.columns([1,2])
with col1:
    st.image(image,width=800)

html_title = """
<div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px; text-align: center;">
    <h1 style="color: #333;">Crime Analysis Dashboard</h1>
    <p style="color: #666;">Analyzing crime data to understand trends and patterns.</p>
</div>""" 
st.markdown(html_title, unsafe_allow_html=True)

col3,col4=st.columns([1,2])
with col3:
    box_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    st.markdown("### Crime Type Distribution")
    Rape = df['Rape'].sum()
    K=df['K&A'].sum()
    DD=df['DD'].sum()
    AoW=df['AoW'].sum()
    AoM=df['AoM'].sum()
    DV=df['DV'].sum()
    WT=df['WT'].sum()
    crime_counts = [Rape, K, DD, AoW, AoM, DV, WT]
    labels = ['Rape','K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']      

    plt.pie(crime_counts, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    st.pyplot(plt)

with col4:
    st.markdown("## Dynamic Crime Dashboard")

    crime_cols = [
        'Rape', 'K&A', 'DD',
        'AoW', 'AoM', 'DV', 'WT'
    ]

    # Dropdowns
    selected_year = st.selectbox(
        "Select Year",
        ["All"] + sorted(df['Year'].unique().tolist())
    )

    selected_state = st.selectbox(
        "Select State",
        ["All"] + sorted(df['State'].unique().tolist())
    )

    selected_crime = st.selectbox(
        "Select Crime Category",
        ["All"] + crime_cols
    )

    # ---------------------------
    # CASE 1: ALL ALL ALL
    # ---------------------------
    if (
        selected_year == "All"
        and selected_state == "All"
        and selected_crime == "All"
    ):

        yearly_data = (
            df.groupby('Year')[crime_cols]
            .sum()
        )

        st.subheader(
            "Crime Trend (2001–2021)"
        )

        st.line_chart(yearly_data)

    # ---------------------------
    # CASE 2: Year only
    # ---------------------------
    elif (
        selected_year != "All"
        and selected_state == "All"
        and selected_crime == "All"
    ):

        filtered = df[
            df['Year'] == selected_year
        ]

        state_data = (
            filtered.groupby('State')
            [crime_cols]
            .sum()
        )

        st.subheader(
            f"State-wise Crime in {selected_year}"
        )

        st.bar_chart(state_data)

    # ---------------------------
    # CASE 3: Year + State
    # ---------------------------
    elif (
        selected_year != "All"
        and selected_state != "All"
        and selected_crime == "All"
    ):

        filtered = df[
            (df['Year'] == selected_year)
            &
            (df['State'] == selected_state)
        ]

        crime_data = (
            filtered[crime_cols]
            .sum()
        )

        st.subheader(
            f"Crime Distribution in "
            f"{selected_state}"
        )

        fig, ax = plt.subplots()

        ax.bar(
            crime_data.index,
            crime_data.values
        )

        plt.xticks(rotation=45)

        st.pyplot(fig)

    # ---------------------------
    # CASE 4: State only
    # ---------------------------
    elif (
        selected_year == "All"
        and selected_state != "All"
        and selected_crime == "All"
    ):

        filtered = df[
            df['State']
            == selected_state
        ]

        trend = (
            filtered.groupby('Year')
            [crime_cols]
            .sum()
        )

        st.subheader(
            f"Crime Trend in "
            f"{selected_state}"
        )

        st.line_chart(trend)

    # ---------------------------
    # CASE 5: Crime only
    # ---------------------------
    elif (
        selected_year == "All"
        and selected_state == "All"
        and selected_crime != "All"
    ):

        trend = (
            df.groupby('Year')
            [selected_crime]
            .sum()
        )

        st.subheader(
            f"{selected_crime} Trend"
        )

        st.area_chart(trend)

    # ---------------------------
    # ---------------------------
# CASE 6: Year + Crime
# ---------------------------
    elif (
        selected_year != "All"
        and selected_state == "All"
        and selected_crime != "All"
    ):

        filtered = df[
            df['Year'] == selected_year
        ]

        # Group by state for selected crime
        state_crime = (
            filtered.groupby('State')[selected_crime]
            .sum()
            .reset_index()
        )

        st.subheader(
            f"{selected_crime} Cases Across States ({selected_year})"
        )

        # Check if data exists
        if state_crime.empty:
            st.warning("No data available.")
        else:
            fig, ax = plt.subplots(figsize=(10,5))

            ax.bar(
                state_crime['State'],
                state_crime[selected_crime]
            )

            plt.xticks(rotation=90)

            ax.set_xlabel("States")
            ax.set_ylabel("Crime Count")

            ax.set_title(
                f"{selected_crime} Cases Across States ({selected_year})"
            )

            st.pyplot(fig)
    # ---------------------------
    # CASE 7: State + Crime
    # ---------------------------
    elif (
        selected_year == "All"
        and selected_state != "All"
        and selected_crime != "All"
    ):

        filtered = df[
            df['State']
            == selected_state
        ]

        trend = (
            filtered.groupby('Year')
            [selected_crime]
            .sum()
        )

        st.subheader(
            f"{selected_crime} "
            f"Trend in {selected_state}"
        )

        st.line_chart(trend)

    # ---------------------------
    # CASE 8: Year + State + Crime
    # ---------------------------
    else:

        filtered = df[
            (df['Year'] == selected_year)
            &
            (df['State'] == selected_state)
        ]

        value = filtered[
            selected_crime
        ].sum()

        st.metric(
            f"{selected_crime} Cases",
            int(value)
        )

        fig, ax = plt.subplots()

        ax.bar(
            [selected_crime],
            [value]
        )

        st.pyplot(fig)


# -------------------------------
# Crime Statistics Cards
# -------------------------------

crime_totals = df[
    ['Rape', 'K&A', 'DD',
     'AoW', 'AoM', 'DV', 'WT']
].sum()

# Max and Min category
max_crime = crime_totals.idxmax()
max_cases = crime_totals.max()

min_crime = crime_totals.idxmin()
min_cases = crime_totals.min()

# Total crime count
total_cases = crime_totals.sum()

# Average crime
avg_cases = int(crime_totals.mean())

st.markdown("## 📊 Crime Dashboard Insights")

col1, col2, col3, col4 = st.columns(4)

# -------------------------------
# Card Buttons
# -------------------------------

with col1:
    total_btn = st.button(
        f"📊 Total Cases\n{total_cases:,}",
        use_container_width=True
    )

    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#667eea,#764ba2);
        padding:15px;
        border-radius:20px;
        color:white;
        text-align:center;
        margin-top:-60px;
        pointer-events:none;
    ">
        <h4>Total Cases</h4>
        <p>Reported Crimes</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    max_btn = st.button(
        f"🔥 {max_crime}",
        use_container_width=True
    )

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg,#ff4e50,#f9d423);
        padding:15px;
        border-radius:20px;
        color:white;
        text-align:center;
        margin-top:-60px;
        pointer-events:none;
    ">
        <h4>Highest Crime</h4>
        <h2>{max_crime}</h2>
        <h3>{max_cases:,}</h3>
        <p>Most Dangerous Category</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    min_btn = st.button(
        f"🟢 {min_crime}",
        use_container_width=True
    )

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg,#11998e,#38ef7d);
        padding:15px;
        border-radius:20px;
        color:white;
        text-align:center;
        margin-top:-60px;
        pointer-events:none;
    ">
        <h4>Lowest Crime</h4>
        <h2>{min_crime}</h2>
        <h3>{min_cases:,}</h3>
        <p>Least Reported Crime</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_btn = st.button(
        f"📈 Avg {avg_cases:,}",
        use_container_width=True
    )

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg,#fc5c7d,#6a82fb);
        padding:15px;
        border-radius:20px;
        color:white;
        text-align:center;
        margin-top:-60px;
        pointer-events:none;
    ">
        <h4>Average Cases</h4>
        <h2>{avg_cases:,}</h2>
        <p>Across Categories</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# Dynamic Insights
# -------------------------------

st.markdown("### 📝 Crime Insights")

if max_btn:
    st.markdown(f"""
    <div style="
        background-color:wheat;
        padding:20px;
        border-left:8px solid red;
        border-radius:10px;
        color:black;
    ">
        ⚠️ <b>Crime Alert:</b>
        <span style="color:red;">
        <b>{max_crime}</b>
        </span>
        has the highest reported cases
        with over <b>{max_cases:,}</b>
        incidents reported.

        This suggests stronger awareness,
        law enforcement, and prevention
        measures are needed.
    </div>
    """, unsafe_allow_html=True)

elif min_btn:
    st.markdown(f"""
    <div style="
        background-color:wheat;
        padding:20px;
        border-left:8px solid green;
        border-radius:10px;
        color:black;
    ">
        ✅ <b>Low Crime Insight:</b>
         {min_crime} 
        has the lowest reported crime
        count with <b>{min_cases:,}</b>
        cases.

        However, lower numbers do not
        always mean lower risk because
        underreporting can exist.
    </div>
    """, unsafe_allow_html=True)

elif total_btn:
    st.markdown(f"""
    <div style="
        background-color:wheat;
        padding:20px;
        border-left:8px solid blue;
        border-radius:10px;
        color:black;
    ">
        📊 <b>Overall Crime Summary:</b>

        A total of {total_cases:,} 
        crime cases have been reported
        across all categories.

        Historical analysis suggests
        certain categories require
        urgent intervention.
    </div>
    """, unsafe_allow_html=True)

elif avg_btn:
    st.markdown(f"""
    <div style="
        background-color:wheat;
        padding:20px;
        border-left:8px solid purple;
        border-radius:10px;
        color:black;
    ">
        📈 <b>Average Crime Insight:</b>

        The average number of reported
        cases across crime categories is
        {avg_cases:,}.

        This helps compare category
        severity relative to overall data.
    </div>
    """, unsafe_allow_html=True)
        
st.markdown("## 🗺️ Interactive Crime Map")

crime_cols = [
    'Rape', 'K&A', 'DD',
    'AoW', 'AoM', 'DV', 'WT'
]

# Total crime count per state
state_crime = (
    df.groupby('State')[crime_cols]
    .sum()
)

state_crime['Total Cases'] = (
    state_crime.sum(axis=1)
)

state_crime = state_crime.reset_index()

# Fix state names
state_mapping = {
    "A & N Islands":
    "Andaman and Nicobar Islands",

    "D & N Haveli":
    "Dadra and Nagar Haveli and Daman and Diu",

    "Delhi UT":
    "Delhi"
}

state_crime['State'] = (
    state_crime['State']
    .replace(state_mapping)
)

# Load geojson
with open(
    "C:\\Users\\asus\\OneDrive\\Desktop\\dsa\\nlp_interview\\india_states.geojson",
    "r",
    encoding="utf-8"
) as f:
    india_states = json.load(f)

# Create map
m = folium.Map(
    location=[22.5, 80],
    zoom_start=4,
    tiles="CartoDB positron"
)

# Choropleth
folium.Choropleth(
    geo_data=india_states,
    data=state_crime,
    columns=[
        "State",
        "Total Cases"
    ],
    key_on="feature.properties.NAME_1",
    fill_color="YlOrRd",
    fill_opacity=0.8,
    line_opacity=0.4,
    legend_name="Total Crime Cases (2001–2021)"
).add_to(m)

# Hover tooltip
folium.GeoJson(
    india_states,
    style_function=lambda x: {
        'fillColor': 'transparent',
        'color': 'black',
        'weight': 0.5
    },

    tooltip=folium.GeoJsonTooltip(
        fields=['NAME_1'],
        aliases=['State:'],
        localize=True
    )
).add_to(m)

# Display map
st_folium(
    m,
    width=1000,
    height=600
)

# State dropdown
selected_state = st.selectbox(
    "Select State",
    state_crime['State']
)

# Selected state data
selected_data = state_crime[
    state_crime['State']
    == selected_state
]

total_cases = int(
    selected_data[
        'Total Cases'
    ].values[0]
)

# Card UI
st.markdown(f"""
<div style="
background: linear-gradient(135deg, #ff6a00, #ee0979);
padding:25px;
border-radius:20px;
color:white;
text-align:center;
margin-top:20px;
box-shadow:0 4px 12px rgba(0,0,0,0.2);
">

<h2>🚨 {selected_state}</h2>

<h1> {total_cases:,} </h1>

<h4>Total Crime Cases (2001–2021)</h4>

</div>
""", unsafe_allow_html=True)


# Insight message
st.markdown(f"""
<div style="
background-color:wheat;
padding:15px;
border-left:6px solid red;
border-radius:10px;
margin-top:10px;
color:black;
font-size:18px;
">

⚠️ <b>Insight:</b>

<b>{selected_state}</b> reported around
<b>{total_cases:,}</b> crime cases
against women between
<b>2001–2021</b>.

This region may require stronger
safety awareness and preventive
measures based on historical trends.

</div>
""", unsafe_allow_html=True)
import datetime
import json
from pathlib import Path
from PIL import Image
import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from streamlit_folium import st_folium

try:
    import plotly.express as px
    import plotly.graph_objects as go
except Exception:
    px = None
    go = None

# ---------------------------------------------------------
# Page Configuration (Must be the first Streamlit command)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Crime Against Women Analysis Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# ---------------------------------------------------------
# File Paths (Relative, OS-independent)
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "CrimesOnWomenData.csv"
IMAGE_PATH = BASE_DIR / "crime.jpg"
GEOJSON_PATH = BASE_DIR / "india_states.geojson"

# ---------------------------------------------------------
# Data Loading & Normalization (Cached for high performance)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
        
    # Standardize state names: Title Case & strip whitespace
    df['State'] = df['State'].astype(str).str.strip().str.title()
    
    # Clean nomenclature to match standard Census / GeoJSON boundaries
    cleaning_map = {
        'A & N Islands': 'Andaman and Nicobar',
        'D & N Haveli': 'Dadra and Nagar Haveli',
        'D&N Haveli': 'Dadra and Nagar Haveli',
        'Daman & Diu': 'Daman and Diu',
        'Delhi Ut': 'Delhi',
        'Jammu & Kashmir': 'Jammu and Kashmir',
        'Odisha': 'Orissa',
        'Uttarakhand': 'Uttaranchal'
    }
    df['State'] = df['State'].replace(cleaning_map)
    return df

@st.cache_data
def load_geojson():
    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

df = load_data()
india_states = load_geojson()

# ---------------------------------------------------------
# Header Banner
# ---------------------------------------------------------
col1, col2 = st.columns([1, 2])
with col1:
    if IMAGE_PATH.exists():
        image = Image.open(IMAGE_PATH)
        st.image(image, use_container_width=True)

with col2:
    html_title = """
    <div style="background: linear-gradient(135deg, #1f2937, #111827); padding: 25px; border-radius: 12px; text-align: center; color: white; margin-bottom: 10px;">
        <h1 style="color: #f3f4f6; margin-bottom: 5px;">🛡️ Crime Analysis Dashboard</h1>
        <p style="color: #9ca3af; font-size: 16px; margin-top: 0;">Comprehensive Analysis of Crimes Against Women in India (2001–2021)</p>
    </div>
    """
    st.markdown(html_title, unsafe_allow_html=True)

# ---------------------------------------------------------
# High-Level Distribution & Dynamic Exploration
# ---------------------------------------------------------
crime_cols = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
crime_labels = {
    'Rape': 'Rape (Sec. 376)',
    'K&A': 'Kidnapping & Abduction',
    'DD': 'Dowry Deaths (Sec. 304B)',
    'AoW': 'Assault on Women (Sec. 354)',
    'AoM': 'Insult to Modesty (Sec. 509)',
    'DV': 'Domestic Violence (Sec. 498A)',
    'WT': 'Women Trafficking (ITPA)'
}

col3, col4 = st.columns([1, 2])

with col3:
    st.markdown("### 📊 National Crime Distribution")
    crime_totals_pie = [df[col].sum() for col in crime_cols]
    
    fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
    ax_pie.pie(
        crime_totals_pie,
        labels=crime_cols,
        autopct='%1.1f%%',
        startangle=140,
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e6ff']
    )
    ax_pie.axis('equal')
    st.pyplot(fig_pie)
    plt.close(fig_pie)

with col4:
    st.markdown("## 🔍 Dynamic Crime Explorer")

    c_filter1, c_filter2, c_filter3 = st.columns(3)
    with c_filter1:
        selected_year = st.selectbox(
            "Select Year",
            ["All"] + sorted(df['Year'].unique().tolist()),
            key="explorer_year"
        )
    with c_filter2:
        selected_state = st.selectbox(
            "Select State",
            ["All"] + sorted(df['State'].unique().tolist()),
            key="explorer_state"
        )
    with c_filter3:
        selected_crime = st.selectbox(
            "Select Crime Category",
            ["All"] + crime_cols,
            key="explorer_crime"
        )

    # ---------------------------
    # CASE 1: ALL ALL ALL
    # ---------------------------
    if (
        selected_year == "All"
        and selected_state == "All"
        and selected_crime == "All"
    ):
        yearly_data = df.groupby('Year')[crime_cols].sum()
        st.subheader("National Crime Trend (2001–2021)")
        st.line_chart(yearly_data)

    # ---------------------------
    # CASE 2: Year only
    # ---------------------------
    elif (
        selected_year != "All"
        and selected_state == "All"
        and selected_crime == "All"
    ):
        filtered = df[df['Year'] == selected_year]
        state_data = filtered.groupby('State')[crime_cols].sum()
        st.subheader(f"State-wise Crime Distribution ({selected_year})")
        st.bar_chart(state_data)

    # ---------------------------
    # CASE 3: Year + State
    # ---------------------------
    elif (
        selected_year != "All"
        and selected_state != "All"
        and selected_crime == "All"
    ):
        filtered = df[(df['Year'] == selected_year) & (df['State'] == selected_state)]
        crime_data = filtered[crime_cols].sum()
        st.subheader(f"Crime Breakdown in {selected_state} ({selected_year})")

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(crime_data.index, crime_data.values, color='#4A90E2')
        plt.xticks(rotation=45)
        ax.set_ylabel("Reported Incidents")
        st.pyplot(fig)
        plt.close(fig)

    # ---------------------------
    # CASE 4: State only
    # ---------------------------
    elif (
        selected_year == "All"
        and selected_state != "All"
        and selected_crime == "All"
    ):
        filtered = df[df['State'] == selected_state]
        trend = filtered.groupby('Year')[crime_cols].sum()
        st.subheader(f"Crime Trend in {selected_state} (2001–2021)")
        st.line_chart(trend)

    # ---------------------------
    # CASE 5: Crime only
    # ---------------------------
    elif (
        selected_year == "All"
        and selected_state == "All"
        and selected_crime != "All"
    ):
        trend = df.groupby('Year')[selected_crime].sum()
        st.subheader(f"{selected_crime} Trend Across India (2001–2021)")
        st.area_chart(trend)

    # ---------------------------
    # CASE 6: Year + Crime
    # ---------------------------
    elif (
        selected_year != "All"
        and selected_state == "All"
        and selected_crime != "All"
    ):
        filtered = df[df['Year'] == selected_year]
        state_crime_subset = filtered.groupby('State')[selected_crime].sum().reset_index()

        st.subheader(f"{selected_crime} Incidents by State ({selected_year})")
        if state_crime_subset.empty:
            st.warning("No data available.")
        else:
            fig, ax = plt.subplots(figsize=(10, 4.5))
            ax.bar(state_crime_subset['State'], state_crime_subset[selected_crime], color='#E74C3C')
            plt.xticks(rotation=90)
            ax.set_xlabel("States / UTs")
            ax.set_ylabel("Crime Count")
            st.pyplot(fig)
            plt.close(fig)

    # ---------------------------
    # CASE 7: State + Crime
    # ---------------------------
    elif (
        selected_year == "All"
        and selected_state != "All"
        and selected_crime != "All"
    ):
        filtered = df[df['State'] == selected_state]
        trend = filtered.groupby('Year')[selected_crime].sum()
        st.subheader(f"{selected_crime} Trend in {selected_state}")
        st.line_chart(trend)

    # ---------------------------
    # CASE 8: Year + State + Crime
    # ---------------------------
    else:
        filtered = df[(df['Year'] == selected_year) & (df['State'] == selected_state)]
        value = int(filtered[selected_crime].sum())
        st.metric(f"{selected_crime} Cases in {selected_state} ({selected_year})", f"{value:,}")

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar([selected_crime], [value], color='#9B59B6')
        ax.set_ylabel("Reported Cases")
        st.pyplot(fig)
        plt.close(fig)

st.divider()

# ---------------------------------------------------------
# Executive KPI Statistics & Interactive Insights
# ---------------------------------------------------------
crime_totals = df[crime_cols].sum()
max_crime = crime_totals.idxmax()
max_cases = crime_totals.max()
min_crime = crime_totals.idxmin()
min_cases = crime_totals.min()
total_cases = crime_totals.sum()
avg_cases = int(crime_totals.mean())

st.markdown("## 📈 National Crime Insights & Metrics")

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#4F46E5,#7C3AED); padding:18px; border-radius:14px; color:white; text-align:center;">
        <span style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">Total Incidents</span>
        <h2 style="margin: 8px 0; font-size: 28px;">{total_cases:,}</h2>
        <p style="margin: 0; font-size: 12px; opacity: 0.85;">21-Year Aggregated Total</p>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#DC2626,#EA580C); padding:18px; border-radius:14px; color:white; text-align:center;">
        <span style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">Predominant Crime</span>
        <h2 style="margin: 8px 0; font-size: 28px;">{max_crime}</h2>
        <p style="margin: 0; font-size: 12px; opacity: 0.85;">{max_cases:,} Reported Cases</p>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#059669,#10B981); padding:18px; border-radius:14px; color:white; text-align:center;">
        <span style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">Lowest Reported</span>
        <h2 style="margin: 8px 0; font-size: 28px;">{min_crime}</h2>
        <p style="margin: 0; font-size: 12px; opacity: 0.85;">{min_cases:,} Reported Cases</p>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#2563EB,#06B6D4); padding:18px; border-radius:14px; color:white; text-align:center;">
        <span style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">Category Average</span>
        <h2 style="margin: 8px 0; font-size: 28px;">{avg_cases:,}</h2>
        <p style="margin: 0; font-size: 12px; opacity: 0.85;">Mean Per Offense Head</p>
    </div>
    """, unsafe_allow_html=True)

# Interactive Insight Tabs
st.markdown("### 💡 Analytical Takeaways")
tab_overview, tab_dv, tab_trend = st.tabs(["Overview Summary", "Domestic Violence Impact", "Reporting Shifts"])

with tab_overview:
    st.info(
        f"**National Overview:** Across all tracked categories between 2001 and 2021, a cumulative total of **{total_cases:,}** crimes against women were documented. "
        f"The most prevalent offense was **{max_crime}** with **{max_cases:,}** cases, representing over **{((max_cases/total_cases)*100):.1f}%** of all reported incidents."
    )

with tab_dv:
    st.warning(
        "**Domestic Violence (IPC 498A):** Cruelty by Husband and In-laws consistently forms the largest share of crimes against women in India. "
        "Studies indicate that while legal recourse expanded with the Protection of Women from Domestic Violence Act (2005), institutional support and fast-track courts remain key policy priorities."
    )

with tab_trend:
    st.success(
        "**Post-2012 Reporting Trajectory:** Following the 2012 criminal law reforms, reporting of assault (IPC 354) and kidnapping (IPC 363-373) surged. "
        "Domain analysts emphasize that elevated numbers in modern years frequently reflect enhanced reporting infrastructure and reduced social stigma rather than merely rising crime rates."
    )

st.divider()

# ---------------------------------------------------------
# Interactive Choropleth Map (Folium)
# ---------------------------------------------------------
st.markdown("## 🗺️ Geospatial Crime Density Map")
st.markdown("Interactive state-wise crime density across India. Hover over any state to inspect boundary information.")

state_crime_agg = df.groupby('State')[crime_cols].sum()
state_crime_agg['Total Cases'] = state_crime_agg.sum(axis=1)
state_crime_agg = state_crime_agg.reset_index()

m = folium.Map(
    location=[22.5, 80],
    zoom_start=4.5,
    tiles="CartoDB positron"
)

folium.Choropleth(
    geo_data=india_states,
    data=state_crime_agg,
    columns=["State", "Total Cases"],
    key_on="feature.properties.NAME_1",
    fill_color="YlOrRd",
    fill_opacity=0.8,
    line_opacity=0.4,
    legend_name="Total Reported Crimes Against Women (2001–2021)"
).add_to(m)

folium.GeoJson(
    india_states,
    style_function=lambda x: {
        'fillColor': 'transparent',
        'color': '#333333',
        'weight': 0.6
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['NAME_1'],
        aliases=['State / UT:'],
        localize=True
    )
).add_to(m)

st_folium(m, width=1100, height=580)

# ---------------------------------------------------------
# State Drill-down Card
# ---------------------------------------------------------
col_drill1, col_drill2 = st.columns([1, 2])

with col_drill1:
    selected_map_state = st.selectbox(
        "Select State for Detailed Assessment",
        sorted(state_crime_agg['State'].unique()),
        key="map_state_drilldown"
    )
    
    state_row = state_crime_agg[state_crime_agg['State'] == selected_map_state]
    if not state_row.empty:
        state_total = int(state_row['Total Cases'].values[0])
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF512F, #DD2476); padding:22px; border-radius:16px; color:white; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.15);">
            <h3 style="margin: 0; font-size: 22px;">📍 {selected_map_state}</h3>
            <h1 style="margin: 10px 0; font-size: 34px;">{state_total:,}</h1>
            <p style="margin: 0; font-size: 14px; opacity: 0.9;">Total Reported Cases (2001–2021)</p>
        </div>
        """, unsafe_allow_html=True)

with col_drill2:
    if not state_row.empty:
        state_yearly = df[df['State'] == selected_map_state].groupby('Year')[crime_cols].sum()
        st.markdown(f"### 📈 20-Year Trend in {selected_map_state}")
        st.line_chart(state_yearly)
        
        st.info(
            f"**Analytical Insight for {selected_map_state}:** "
            f"Over the 2001–2021 period, {selected_map_state} recorded **{state_total:,}** total reported incidents against women. "
            f"Analyzing category trajectories helps identify whether localized interventions should focus on domestic cruelty, public space safety, or prevention of trafficking."
        )
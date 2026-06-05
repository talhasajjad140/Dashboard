import streamlit as st
import pandas as pd
from filters import load_data, apply_filters, get_unique_values
from charts import (pie_chart, histogram, line_chart, bar_chart, scatter_plot,
                    box_plot, heatmap, area_chart, count_plot, violin_plot)

st.set_page_config(
    page_title="Storm Events Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

        html, body, .stApp {
            background: #F5F4F0;
            color: #1A1A1A;
            font-family: 'DM Sans', sans-serif;
        }

        /* DARK SIDEBAR */
        [data-testid="stSidebar"] {
            background: #141414 !important;
            border-right: none !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            background: #141414 !important;
            padding: 0;
        }
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            background: #141414 !important;
            padding: 0 1.1rem 2rem 1.1rem;
        }
        [data-testid="stSidebar"] * { color: #E8E8E0 !important; }
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] { display: none; }

        .sb-header {
            background: #1F1F1F;
            margin: 0 -1.1rem 1.2rem -1.1rem;
            padding: 1.2rem 1.1rem 1rem 1.1rem;
            border-bottom: 1px solid #2E2E2E;
        }
        .sb-title {
            font-family: 'DM Mono', monospace !important;
            font-size: 0.72rem !important;
            font-weight: 500 !important;
            letter-spacing: 2.5px !important;
            text-transform: uppercase !important;
            color: #FFFFFF !important;
        }
        .sb-subtitle {
            font-family: 'DM Mono', monospace !important;
            font-size: 0.6rem !important;
            color: #555555 !important;
            letter-spacing: 1px !important;
            margin-top: 0.2rem !important;
        }

        .f-label {
            font-family: 'DM Mono', monospace;
            font-size: 0.58rem;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #555555 !important;
            margin: 1.3rem 0 0.35rem 0;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .f-label::before {
            content: '';
            display: inline-block;
            width: 14px;
            height: 1px;
            background: #333333;
        }

        .sb-divider {
            border: none;
            border-top: 1px dotted #2A2A2A;
            margin: 1rem 0 0.2rem 0;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: #1E1E1E !important;
            border: 1px solid #2E2E2E !important;
            border-radius: 4px !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] * {
            color: #D0D0C8 !important;
            background: transparent !important;
        }
        [data-testid="stSidebar"] [data-baseweb="menu"] {
            background: #1E1E1E !important;
            border: 1px solid #2E2E2E !important;
        }
        [data-testid="stSidebar"] [role="option"] {
            background: #1E1E1E !important;
        }
        [data-testid="stSidebar"] [role="option"]:hover {
            background: #2A2A2A !important;
        }
        [data-testid="stSidebar"] [data-baseweb="tag"] {
            background: #2E2E2E !important;
            border: 1px solid #3E3E3E !important;
            border-radius: 3px !important;
        }
        [data-testid="stSidebar"] [data-baseweb="tag"] span {
            color: #C8C8C0 !important;
            font-size: 0.72rem !important;
        }

        [data-testid="stSidebar"] div[data-testid="stSliderTrack"] {
            background: #2A2A2A !important;
        }
        [data-testid="stSidebar"] div[data-testid="stSliderRange"] {
            background: #AAAAAA !important;
        }
        [data-testid="stSidebar"] [role="slider"] {
            background: #FFFFFF !important;
            border: 2px solid #AAAAAA !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebar"] [data-baseweb="slider"] div[style*="rgb(255"] {
            background: #AAAAAA !important;
        }
        [data-testid="stSidebar"] [data-testid="stThumbValue"],
        [data-testid="stSidebar"] [data-testid="stTickBarMin"],
        [data-testid="stSidebar"] [data-testid="stTickBarMax"] {
            color: #555555 !important;
            font-family: 'DM Mono', monospace !important;
            font-size: 0.65rem !important;
        }

        [data-testid="stSidebar"] [data-baseweb="input"] > div {
            background: #1E1E1E !important;
            border: 1px solid #2E2E2E !important;
            border-radius: 4px !important;
        }
        [data-testid="stSidebar"] input {
            color: #D0D0C8 !important;
            font-family: 'DM Mono', monospace !important;
            font-size: 0.75rem !important;
            background: transparent !important;
        }
        [data-testid="stSidebar"] input::placeholder {
            color: #444444 !important;
            opacity: 1 !important;
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown p {
            color: #666666 !important;
            font-size: 0.75rem !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            background: transparent !important;
            color: #666666 !important;
            border: 1px dotted #333333 !important;
            border-radius: 3px !important;
            box-shadow: none !important;
            padding: 0.5rem 0.8rem !important;
            font-family: 'DM Mono', monospace !important;
            font-size: 0.65rem !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            margin-top: 0.4rem !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: #1E1E1E !important;
            color: #CCCCCC !important;
            border-color: #555555 !important;
        }

        /* MAIN AREA */
        #MainMenu, footer, header { visibility: hidden; }
        .stApp [data-testid="stHeader"] { background: #F5F4F0; }
        .block-container { padding-top: 1.8rem; padding-bottom: 2rem; }
        section.main > div { max-width: 100%; }

        .page-header {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            margin-bottom: 0.3rem;
        }
        .page-title {
            font-family: 'DM Mono', monospace;
            font-size: 1.5rem;
            font-weight: 400;
            color: #1A1A1A;
            letter-spacing: -0.5px;
            line-height: 1;
        }
        .page-title em { font-style: normal; color: #999999; }
        .page-badge {
            font-family: 'DM Mono', monospace;
            font-size: 0.6rem;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: #999999;
            border: 1px solid #D8D7D2;
            padding: 0.25rem 0.55rem;
            border-radius: 2px;
        }
        .page-rule {
            height: 1px;
            background: linear-gradient(to right, #1A1A1A 30%, #D8D7D2 100%);
            margin: 0.6rem 0 0.4rem 0;
        }
        .page-desc {
            font-size: 0.8rem;
            color: #888888;
            margin-bottom: 1.4rem;
        }

        .section-head {
            font-family: 'DM Mono', monospace;
            font-size: 0.6rem;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            color: #999999;
            margin: 1.6rem 0 0.8rem 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .section-head::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #E0DFDA;
        }

        .kpi-wrap {
            background: #FFFFFF;
            border: 1px solid #E0DFDA;
            border-radius: 6px;
            padding: 1.1rem 1rem;
            position: relative;
            overflow: hidden;
        }
        .kpi-wrap::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 2px;
            background: #E0DFDA;
        }
        .kpi-wrap.hi::after { background: #1A1A1A; }
        .kpi-num {
            font-family: 'DM Mono', monospace;
            font-size: 1.9rem;
            font-weight: 400;
            color: #1A1A1A;
            line-height: 1;
            letter-spacing: -2px;
        }
        .kpi-label {
            font-family: 'DM Mono', monospace;
            font-size: 0.58rem;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: #AAAAAA;
            margin-bottom: 0.55rem;
        }
        .kpi-sub {
            font-size: 0.68rem;
            color: #BBBBBB;
            margin-top: 0.4rem;
        }

        .stApp [data-testid="stImage"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }

        .thin-rule {
            height: 1px;
            background: #E0DFDA;
            margin: 0.6rem 0 1.2rem 0;
        }

        .footer {
            font-family: 'DM Mono', monospace;
            font-size: 0.6rem;
            letter-spacing: 1.2px;
            color: #BBBBAA;
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px dotted #D8D7D2;
        }

        hr { border-color: #E0DFDA; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="page-header">
        <div class="page-title">Storm Events <em>/</em> US Weather Data</div>
        <div class="page-badge">NOAA · 1996–2026</div>
    </div>
    <div class="page-rule"></div>
    <div class="page-desc">Severe weather patterns across the United States — filtered, segmented, analysed.</div>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def init_data():
    return load_data("data")

df = pd.DataFrame()
with st.spinner("Loading NOAA storm data..."):
    try:
        df = init_data()
      st.write(df.columns.tolist())
    except FileNotFoundError:
        st.error("Dataset not found. Add .csv or .csv.gz files inside the data/ folder.")
        st.stop()

def sidebar_label(text):
    st.sidebar.markdown(f'<div class="f-label">{text}</div>', unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <div class="sb-header">
        <div class="sb-title">⚡ Controls</div>
        <div class="sb-subtitle">Filter storm event records</div>
    </div>
    """,
    unsafe_allow_html=True,
)

sidebar_label("Year Range")
valid_years = df['year'].dropna()
if len(valid_years) == 0:
    st.sidebar.warning("Year data not available.")
    st.stop()

years = sorted(valid_years.astype(int).unique())
if len(years) == 1:
    sel = st.sidebar.selectbox("Year", options=years, index=0, label_visibility="collapsed")
    year_val = int(sel) if sel is not None else int(years[0])
    year_range = (year_val, year_val)
else:
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=int(years[0]),
        max_value=int(years[-1]),
        value=(int(years[0]), int(years[-1])),
        label_visibility="collapsed"
    )

st.sidebar.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

sidebar_label("States")
states = st.sidebar.multiselect(
    "Select States",
    options=get_unique_values(df, 'state'),
    default=get_unique_values(df, 'state'),
    label_visibility="collapsed"
)

st.sidebar.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

sidebar_label("Event Types")
event_types = st.sidebar.multiselect(
    "Select Event Types",
    options=get_unique_values(df, 'event_type'),
    default=get_unique_values(df, 'event_type'),
    label_visibility="collapsed"
)

st.sidebar.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

sidebar_label("Property Damage")
damage_max = df['damage_property'].max()
if pd.isna(damage_max) or damage_max <= 0:
    st.sidebar.write("All values are 0 or unavailable")
    damage_range = (0.0, 0.0)
else:
    damage_range = st.sidebar.slider(
        "Property Damage Range ($)",
        min_value=0.0,
        max_value=float(damage_max),
        value=(0.0, float(damage_max)),
        label_visibility="collapsed"
    )

st.sidebar.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

sidebar_label("Search")
search_term = st.sidebar.text_input(
    "Search",
    placeholder="Tornado, Texas...",
    label_visibility="collapsed"
)

st.sidebar.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
if st.sidebar.button("reset filters", use_container_width=True):
    st.rerun()

filtered_df = apply_filters(df, year_range, states, event_types, search_term, damage_range)

if len(filtered_df) == 0:
    st.warning("No data matches your filters. Try adjusting them.")
    st.stop()

st.markdown('<div class="section-head">Summary</div>', unsafe_allow_html=True)

def kpi(label, num, sub, hi=False):
    cls = "kpi-wrap hi" if hi else "kpi-wrap"
    return f"""
    <div class="{cls}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-num">{num}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(kpi("Total Events", f"{len(filtered_df):,}", "Storm records 1996–2026"), unsafe_allow_html=True)
with col2:
    deaths = int(filtered_df['deaths_direct'].sum()) if 'deaths_direct' in filtered_df.columns else 0
    st.markdown(kpi("Direct Deaths", f"{deaths:,}", "Fatalities reported", hi=True), unsafe_allow_html=True)
with col3:
    injuries = int(filtered_df['injuries_direct'].sum()) if 'injuries_direct' in filtered_df.columns else 0
    st.markdown(kpi("Injuries", f"{injuries:,}", "Direct injuries"), unsafe_allow_html=True)
with col4:
    dmg = filtered_df['damage_property'].sum()
    st.markdown(kpi("Property Damage", f"${dmg:,.0f}", "Estimated direct loss"), unsafe_allow_html=True)

st.markdown('<div class="thin-rule"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-head">Analysis</div>', unsafe_allow_html=True)

def render_chart(fig):
    st.pyplot(fig, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    render_chart(pie_chart(filtered_df))
with col_b:
    render_chart(histogram(filtered_df))

col_c, col_d = st.columns(2)
with col_c:
    render_chart(line_chart(filtered_df))
with col_d:
    render_chart(bar_chart(filtered_df))

col_e, col_f = st.columns(2)
with col_e:
    render_chart(scatter_plot(filtered_df))
with col_f:
    render_chart(box_plot(filtered_df))

col_g, col_h = st.columns(2)
with col_g:
    render_chart(area_chart(filtered_df))
with col_h:
    render_chart(count_plot(filtered_df))

render_chart(heatmap(filtered_df))
render_chart(violin_plot(filtered_df))

st.markdown(
    '<div class="footer">Storm Events Dashboard · NOAA National Weather Service · EDA Course Project</div>',
    unsafe_allow_html=True,
)

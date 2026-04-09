# ============================================================
# HALAMAN 2 — PROJECT DETAIL & COMPARISON
# PT NexWave · Kerja Praktik Jan–Feb 2026
# ============================================================

# ============================================================
# BAGIAN 1 — IMPORT LIBRARY
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np


# ============================================================
# BAGIAN 2 — KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="Project Detail — RF Network Testing",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# BAGIAN 3 — CUSTOM STYLING
# Font: DM Sans, Force Light Mode, OpenStreetMap
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&display=swap');

    /* ─── FORCE LIGHT MODE ─── */
    html, body, [class*="css"], [data-testid] {
        color-scheme: light !important;
    }
    body, .stApp {
        background-color: #F0F2F8 !important;
        color: #1E1B4B !important;
    }


    /* DM Sans untuk semua teks, kecuali Material Icons font */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif !important;
    }
    .material-icons, .material-icons-sharp, .material-icons-outlined,
    [class*="material-icon"] {
        font-family: 'Material Icons' !important;
    }

    /* Sembunyikan header sidebar (keyboard_double) TANPA hapus nav links */
    [data-testid="stSidebarHeader"] { display: none !important; }

    /* ── EXPANDER: Fix icon numpuk di judul ── */
    details > summary {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        padding: 12px 16px !important;
        cursor: pointer !important;
        list-style: none !important;
        overflow: visible !important;
    }
    details > summary > svg {
        flex-shrink: 0 !important;
        min-width: 20px !important;
    }
    details > summary > div,
    details > summary > p,
    details > summary > span {
        flex: 1 1 auto !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #1E1B4B !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        line-height: 1.4 !important;
        word-break: break-word !important;
        margin: 0 !important;
    }
    details > summary::-webkit-details-marker { display: none !important; }

    [data-testid="stAppViewContainer"] { background-color: #F0F2F8 !important; }
    [data-testid="stSidebar"]          { background-color: #a4e5fc !important; border-right: 1px solid #E2E8F0 !important; }
    [data-testid="stHeader"]           { background-color: #F0F2F8 !important; }

    /* Override teks agar tidak ikut dark mode */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] div,
    [data-testid="stAppViewContainer"] label {
        color: #1E1B4B;
    }

    .dash-header {
        background: linear-gradient(135deg, #0891B2 0%, #4F46E5 100%);
        border-radius: 16px; padding: 20px 28px; margin-bottom: 20px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .dash-title { font-size: 22px; font-weight: 800; color: #FFFFFF !important; }
    .dash-sub   { font-size: 12px; color: rgba(255,255,255,0.80) !important; margin-top: 2px; }

    .section-title {
        font-size: 13px; font-weight: 700; color: #4F46E5 !important;
        text-transform: uppercase; letter-spacing: 1px;
        border-left: 3px solid #4F46E5; padding-left: 10px;
        margin-bottom: 16px; margin-top: 8px;
    }

    .metric-card {
        background: ##EEF2FF !important; border: 1px solid #E2E8F0;
        border-radius: 14px; padding: 16px 20px; text-align: center;
        box-shadow: 0 2px 8px rgba(79,70,229,0.06);
    }
    .metric-label { font-size: 11px; color: #64748B !important; margin-bottom: 6px; letter-spacing: 0.5px; text-transform: uppercase; font-weight: 600; }
    .metric-value { font-size: 26px; font-weight: 800; line-height: 1; }
    .metric-unit  { font-size: 11px; color: #64748B !important; margin-top: 5px; }

    .spot-card {
        border-radius: 10px; padding: 10px 14px;
        margin-bottom: 6px; font-size: 12px; line-height: 1.6;
        word-break: break-word;
    }
    .spot-bad  { background: #FEF2F2 !important; border-left: 4px solid #DC2626; color: #7F1D1D !important; }
    .spot-good { background: #F0FDF4 !important; border-left: 4px solid #16A34A; color: #14532D !important; }

    /* Fix tulisan numpuk di spot card */
    .spot-card b { display: inline-block; margin-bottom: 2px; }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: #F1F5F9 !important; border-radius: 8px;
        padding: 6px 18px; font-size: 13px; font-weight: 600;
        color: #64748B !important; border: none;
    }
    .stTabs [aria-selected="true"] { background: #4F46E5 !important; color: #FFFFFF !important; }

    .stExpander { border: 1px solid #E0E7FF !important; border-radius: 12px !important; background: #FFFFFF !important; }
    .stExpander p, .stExpander span { color: #374151 !important; }
    .stExpander strong { color: #1E1B4B !important; }

    /* Fix label selectbox dan multiselect agar terbaca */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #1E1B4B !important;
    }

    /* Stat row — tidak numpuk */
    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 7px 12px;
        background: #F8F9FF;
        border-radius: 8px;
        margin-bottom: 5px;
        font-size: 13px;
        flex-wrap: wrap;
        gap: 4px;
    }
    .stat-label { color: #64748B; white-space: nowrap; }
    .stat-value { font-weight: 700; color: #1E1B4B !important; white-space: nowrap; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# BAGIAN 4 — KONSTANTA & THRESHOLD 3GPP
# ============================================================

KPI_FILES = {
    "RSRP"      : "data/RSRP_ALL.csv",
    "RSRQ"      : "data/RSRQ_ALL.csv",
    "SINR"      : "data/SINR_ALL.csv",
    "Throughput": "data/THROUGHPUT_ALL.csv",
    "ECI"       : "data/ECI_ALL.csv",
    "PCI"       : "data/PCI_ALL.csv",
    "RFMODE"    : "data/RFMODE_ALL.csv",
}

KPI_COLORS = {
    "RSRP"      : "#5032DC",
    "RSRQ"      : "#0000FF",
    "SINR"      : "#5032DC",
    "Throughput": "#2E00FE",
    "PCI"       : "#DC2626",
    "ECI"       : "#059669",
    "RFMODE"    : "#0284C7",
}

# Threshold 3GPP — (good, fair, bad)
THRESHOLDS_3GPP = {
    "RSRP": [
        (-85,  "Excellent", "#5032DC"),
        (-95,  "Good",      "#548235"),
        (-105, "Fair",      "#00FF00"),
        (-110, "Poor",      "#FFFF00"),
        (None, "No Signal", "#FF0000"),
    ],
    "RSRQ": [
        (-10,  "Excellent", "#0000FF"),
        (-14,  "Good",      "#00FFFF"),
        (-16,  "Fair",      "#62FF07"),
        (-18,  "Poor",      "#FAFA00"),
        (None, "No Signal", "#FF0303"),
    ],
    "SINR": [
        (20,   "Excellent", "#5032DC"),
        (15,   "Very Good", "#0000FF"),
        (10,   "Good",      "#00FFFF"),
        (3,    "Fair",      "#B2DF8A"),
        (0,    "Marginal",  "#D7FF0E"),
        (None, "Poor",      "#FF0000"),
    ],
    "Throughput": [
        (10,   "Excellent", "#2E00FE"),
        (5,    "Good",      "#3D7539"),
        (3,    "Fair",      "#37FE00"),
        (1,    "Poor",      "#FEED00"),
        (None, "Bad",       "#FE0000"),
    ],
}

NUMERIC_KPIS = ["RSRP", "RSRQ", "SINR", "Throughput"]

COLOR_MAP_KPI = {
    "Excellent": "#5032DC",
    "Very Good": "#0000FF",
    "Good":      "#00FFFF",
    "Fair":      "#B2DF8A",
    "Marginal":  "#D7FF0E",
    "Poor":      "#FFFF00",
    "Bad":       "#FE0000",
    "No Signal": "#FF0000",
}


# ============================================================
# BAGIAN 5 — LOAD DATA
# ============================================================

@st.cache_data
def load_all_data():
    dfs = []
    for kpi, path in KPI_FILES.items():
        if os.path.exists(path):
            try:
                df_temp = pd.read_csv(path)
                df_temp["KPI_NAME"] = kpi
                dfs.append(df_temp)
            except:
                pass
    if not dfs:
        return pd.DataFrame()
    combined = pd.concat(dfs, ignore_index=True)
    def parse_numeric(val):
        try:
            return float(str(val).split("/")[0].strip())
        except:
            return None
    combined["VALUE_NUM"]     = combined["VALUE"].apply(parse_numeric)
    combined["Project_Clean"] = combined["Project"].str.replace("_", " ").str.strip()
    return combined

df_all = load_all_data()


# ============================================================
# BAGIAN 6 — FUNGSI KLASIFIKASI SPOT (3GPP)
# ============================================================

def classify_spot(kpi, value):
    if kpi not in THRESHOLDS_3GPP or value is None or np.isnan(value):
        return "Unknown", "#94A3B8"

    thresholds = THRESHOLDS_3GPP[kpi]

    for thresh, label, color in thresholds:
        if thresh is None:
            return label, color

        # KPI negatif → semakin besar (mendekati 0) semakin baik
        if kpi in ["RSRP", "RSRQ"]:
            if value >= thresh:
                return label, color
        else:
            # KPI positif
            if value >= thresh:
                return label, color

    return "Unknown", "#94A3B8"

def get_kpi_color_dynamic(kpi, value):
    """Return warna palette kantor berdasarkan nilai KPI aktual."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "#94A3B8"
    _, color = classify_spot(kpi, value)
    return color

def get_spot_category(kpi, value):
    label, _ = classify_spot(kpi, value)
    if label in ["Excellent", "Good"]:
        return "good"
    elif label in ["Poor", "No Signal"]:
        return "bad"
    else:
        return "fair"

def get_color_map_for_kpi(kpi):
    if kpi not in THRESHOLDS_3GPP:
        return {}

    return {
        label: color
        for _, label, color in THRESHOLDS_3GPP[kpi]
    }


# ============================================================
# BAGIAN 7 — SIDEBAR
# ============================================================

current_page = os.path.basename(__file__)  # ← Pakai os.path.basename seperti di app.py

with st.sidebar:
    st.markdown("<div class='sidebar-title'>Menu Utama</div>", unsafe_allow_html=True)
    
    if current_page == "app.py":
        st.markdown("**Main Dashboard**")
    else:
        st.page_link("app.py", label="Main Dashboard")

    if current_page == "01_Project_Detail.py":  # ← Ini nama file sebenarnya
        st.markdown("**Project Detail**")
    else:
        st.page_link("pages/01_Project_Detail.py", label="Project Detail")
    
    st.divider()

    if df_all.empty:
        st.warning("⚠️ Data tidak ditemukan.")
        selected_project  = None
        selected_kpi      = "RSRP"
        compare_projects  = []
        compare_kpi       = "RSRP"
        selected_mode     = "Semua"
    else:
        all_projects = sorted(df_all["Project_Clean"].unique().tolist())

        st.markdown("**Project Spesifik**")
        selected_project = st.selectbox("Pilih Project", all_projects, label_visibility="collapsed")

        st.markdown("**KPI yang ditampilkan**")
        selected_kpi = st.selectbox("Pilih KPI", NUMERIC_KPIS, label_visibility="collapsed")

        all_modes    = ["Semua"] + sorted(df_all["Mode"].dropna().unique().tolist())
        selected_mode = st.selectbox("Filter Mode", all_modes, label_visibility="collapsed")

        st.divider()
        st.markdown("**Comparison**")
        compare_projects = st.multiselect(
            "Pilih Project untuk dibandingkan",
            all_projects,
            default=all_projects[:3] if len(all_projects) >= 3 else all_projects,
            label_visibility="collapsed"
        )
        compare_kpi = st.selectbox("KPI Comparison", NUMERIC_KPIS, key="cmp_kpi", label_visibility="collapsed")

    st.divider()
    st.markdown(
        "<div style='font-size:11px;color:#000000'>"
        "Disusun oleh:<br>"
        "<b style='color:#000000'>Ilham Candra Harmawan</b> · 5003231172<br>"
        "<b style='color:#000000'>Muhammad Al Fatih Nafiudin Sya'bani</b> · 5003231189"
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# BAGIAN 8 — FILTER DATA
# ============================================================

if not df_all.empty and selected_project:
    df_proj = df_all[df_all["Project_Clean"] == selected_project].copy()
    if selected_mode != "Semua":
        df_proj = df_proj[df_proj["Mode"] == selected_mode]

    df_kpi = df_proj[
        (df_proj["KPI_NAME"] == selected_kpi) &
        (df_proj["VALUE_NUM"].notna())
    ].copy()

    df_kpi["Spot"] = df_kpi["VALUE_NUM"].apply(
        lambda v: get_spot_category(selected_kpi, v)
    )
    df_kpi["Label"] = df_kpi["VALUE_NUM"].apply(
        lambda v: classify_spot(selected_kpi, v)[0]
    )
else:
    df_proj = pd.DataFrame()
    df_kpi  = pd.DataFrame()


# ============================================================
# BAGIAN 9 — HEADER
# ============================================================

st.markdown(f"""
<div class='dash-header'>
    <div>
        <div class='dash-title'>Project Detail &amp; Comparison</div>
        <div class='dash-sub'>Analisis Spesifik Per Project · RF Network Testing · PT NexWave</div>
    </div>
    <div style='background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.25);
                border-radius:10px;padding:8px 14px;font-size:11px;color:#FFFFFF;text-align:right;line-height:1.7'>
        Ilham Candra Harmawan · 5003231172<br>Muhammad Al Fatih Nafiudin Sya'bani · 5003231189
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# BAGIAN 10 — EXECUTIVE SUMMARY PER PROJECT
# ============================================================

if not df_proj.empty:
    st.markdown(
        f"<div class='section-title'>Executive Summary — {selected_project}</div>",
        unsafe_allow_html=True
    )

    tab_avg, tab_med = st.tabs(["Average", "Median"])

    def render_proj_cards(agg_func):
        cols = st.columns(len(NUMERIC_KPIS))
        for i, kpi in enumerate(NUMERIC_KPIS):
            subset = df_proj[df_proj["KPI_NAME"] == kpi]["VALUE_NUM"].dropna()
            val    = agg_func(subset) if len(subset) > 0 else None
            val_str = f"{val:.1f}" if val is not None else "—"
            cols[i].markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>{kpi}</div>
                <div class='metric-value' style='color:{get_kpi_color_dynamic(kpi, val)}'>{val_str}</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_avg:
        render_proj_cards(lambda s: s.mean())
    with tab_med:
        render_proj_cards(lambda s: s.median())

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# BAGIAN 11 — SAMPLE DISTRIBUTION
# ============================================================

if not df_kpi.empty:
    st.markdown(
        f"<div class='section-title'>Sample Distribution — {selected_kpi}</div>",
        unsafe_allow_html=True
    )

    tab_count, tab_pct = st.tabs(["Count", "Percentage"])

    dist = df_kpi["Label"].value_counts().reset_index()
    dist.columns = ["Kategori", "Count"]
    dist["Percentage"] = (dist["Count"] / dist["Count"].sum() * 100).round(1)

    order_map = {
        "RSRP":       ["Excellent", "Good", "Fair", "Poor", "No Signal"],
        "RSRQ":       ["Excellent", "Good", "Fair", "Poor", "No Signal"],
        "SINR":       ["Excellent", "Very Good", "Good", "Fair", "Marginal", "Poor"],
        "Throughput": ["Excellent", "Good", "Fair", "Poor", "Bad"],
    }
    order = order_map.get(selected_kpi, list(dist["Kategori"].unique()))
    dist["order"] = dist["Kategori"].map({v: i for i, v in enumerate(order)})
    dist = dist.sort_values("order").drop("order", axis=1)

    color_map_dist = get_color_map_for_kpi(selected_kpi)

    _plotly_layout = dict(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8F9FF",
        font=dict(color="#374151", family="DM Sans, sans-serif"),
        margin=dict(l=10, r=10, t=10, b=20),
    )

    with tab_count:
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(f"<div style='font-size:13px;font-weight:600;color:#374151;margin-bottom:4px'>Distribusi Count — {selected_kpi}</div>", unsafe_allow_html=True)
            fig_bar = px.bar(
                dist, x="Kategori", y="Count",
                color="Kategori",
                color_discrete_map=color_map_dist,
                text="Count",
            )
            fig_bar.update_layout(**_plotly_layout, showlegend=False)
            fig_bar.update_traces(textposition="outside")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_d2:
            st.markdown(f"<div style='font-size:13px;font-weight:600;color:#374151;margin-bottom:4px'>Proporsi — {selected_kpi}</div>", unsafe_allow_html=True)
            fig_pie = px.pie(
                dist, names="Kategori", values="Count",
                color="Kategori",
                color_discrete_map=color_map_dist,
                hole=0.4,
            )
            fig_pie.update_layout(paper_bgcolor="#FFFFFF", font=dict(color="#374151", family="DM Sans, sans-serif"), margin=dict(l=10, r=10, t=10, b=20))
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab_pct:
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown(f"<div style='font-size:13px;font-weight:600;color:#374151;margin-bottom:4px'>Distribusi Persentase — {selected_kpi}</div>", unsafe_allow_html=True)
            fig_bar2 = px.bar(
                dist, x="Kategori", y="Percentage",
                color="Kategori",
                color_discrete_map=color_map_dist,
                text=dist["Percentage"].apply(lambda x: f"{x}%"),
            )
            fig_bar2.update_layout(**_plotly_layout, showlegend=False, yaxis_title="Percentage (%)")
            fig_bar2.update_traces(textposition="outside")
            st.plotly_chart(fig_bar2, use_container_width=True)

        with col_d2:
            st.markdown(
                "<div style='font-size:14px;font-weight:700;color:#1E1B4B;margin-bottom:10px'>Detail Distribusi</div>",
                unsafe_allow_html=True
            )
            for _, row in dist.iterrows():
                cat   = row["Kategori"]
                cnt   = row["Count"]
                pct   = row["Percentage"]
                color = color_map_dist.get(cat, "#94A3B8")
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;align-items:center;
                            padding:8px 12px;background:#F8F9FF;border-radius:8px;
                            margin-bottom:6px;border-left:4px solid {color};flex-wrap:wrap;gap:4px'>
                    <span style='font-weight:600;color:{color}'>{cat}</span>
                    <span style='color:#374151'>{cnt:,} titik &nbsp;·&nbsp; <b style="color:#1E1B4B">{pct}%</b></span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# BAGIAN 12 — GEOGRAPHIC MAP
# Menggunakan open-street-map (warna lebih tegas & jelas)
# ============================================================

if not df_kpi.empty:
    st.markdown(
        f"<div class='section-title'>Geographic Map — {selected_kpi} · {selected_project}</div>",
        unsafe_allow_html=True
    )

    df_map = df_kpi[
        df_kpi["Latitude"].notna() &
        df_kpi["Longitude"].notna()
    ].copy()

    df_map = df_map[
        df_map["Latitude"].between(-12, 6) &
        df_map["Longitude"].between(95, 142)
    ]

    if not df_map.empty:
        if selected_kpi in THRESHOLDS_3GPP:
            fig_map = px.scatter_mapbox(
                df_map,
                lat="Latitude", lon="Longitude",
                color="VALUE_NUM",
                color_continuous_scale=["#FF0000", "#FFFF00", "#00FF00", "#548235", "#5032DC"],
                range_color=[df_map["VALUE_NUM"].quantile(0.05), df_map["VALUE_NUM"].quantile(0.95)],
                hover_name="Project_Clean",
                hover_data={"VALUE_NUM": True, "Label": True, "Mode": True, "Latitude": False, "Longitude": False},
                mapbox_style="open-street-map",   # ← OpenStreetMap: lebih tegas & berwarna
                zoom=12,
                title=f"Peta {selected_kpi} — {selected_project}",
                labels={"VALUE_NUM": selected_kpi, "Label": "Kualitas"},
            )
        else:
            fig_map = px.scatter_mapbox(
                df_map,
                lat="Latitude", lon="Longitude",
                color="Label",
                hover_name="Project_Clean",
                mapbox_style="open-street-map",
                zoom=12,
                title=f"Peta {selected_kpi} — {selected_project}",
            )

        fig_map.update_layout(
            paper_bgcolor="#FFFFFF",
            font=dict(color="#374151", family="DM Sans"),
            margin=dict(l=0, r=0, t=40, b=0),
            height=480,
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Tidak ada data koordinat valid untuk project dan KPI yang dipilih.")

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# BAGIAN 13 — BAD SPOT & GOOD SPOT
# ============================================================

if not df_kpi.empty and selected_kpi in THRESHOLDS_3GPP:
    st.markdown(
        f"<div class='section-title'>Bad Spot & Good Spot — {selected_kpi}</div>",
        unsafe_allow_html=True
    )

    col_bad, col_good = st.columns(2)

    is_higher_better = selected_kpi in ["SINR", "Throughput"]

    if is_higher_better:
        df_bad  = df_kpi.nsmallest(10, "VALUE_NUM")
        df_good = df_kpi.nlargest(10, "VALUE_NUM")
    else:
        df_bad  = df_kpi.nsmallest(10, "VALUE_NUM")
        df_good = df_kpi.nlargest(10, "VALUE_NUM")

    kpi_unit_map = {"RSRP": "dBm", "RSRQ": "dB", "SINR": "dB", "Throughput": "Mbps"}
    unit_str = kpi_unit_map.get(selected_kpi, "")

    with col_bad:
        st.markdown(
            "<div style='font-size:14px;font-weight:700;color:#DC2626;margin-bottom:8px'>Bad Spot — 10 Titik Terburuk</div>",
            unsafe_allow_html=True
        )
        for _, row in df_bad.iterrows():
            lat   = row.get("Latitude", "—")
            lon   = row.get("Longitude", "—")
            val   = row["VALUE_NUM"]
            label = row.get("Label", "—")
            lat_str = f"{lat:.5f}" if isinstance(lat, float) else str(lat)
            lon_str = f"{lon:.5f}" if isinstance(lon, float) else str(lon)
            st.markdown(f"""
            <div class='spot-card spot-bad'>
                <b style='font-size:13px'>{val:.1f} {unit_str}</b>
                &nbsp;·&nbsp; <span style='font-size:12px'>{label}</span><br>
                <span style='font-size:11px'>📍 {lat_str}, {lon_str}</span>
            </div>
            """, unsafe_allow_html=True)

    with col_good:
        st.markdown(
            "<div style='font-size:14px;font-weight:700;color:#16A34A;margin-bottom:8px'>Good Spot — 10 Titik Terbaik</div>",
            unsafe_allow_html=True
        )
        for _, row in df_good.iterrows():
            lat   = row.get("Latitude", "—")
            lon   = row.get("Longitude", "—")
            val   = row["VALUE_NUM"]
            label = row.get("Label", "—")
            lat_str = f"{lat:.5f}" if isinstance(lat, float) else str(lat)
            lon_str = f"{lon:.5f}" if isinstance(lon, float) else str(lon)
            st.markdown(f"""
            <div class='spot-card spot-good'>
                <b style='font-size:13px'>{val:.1f} {unit_str}</b>
                &nbsp;·&nbsp; <span style='font-size:12px'>{label}</span><br>
                <span style='font-size:11px'>📍 {lat_str}, {lon_str}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# BAGIAN 14 — COMPARISON ANTAR PROJECT
# ============================================================

if not df_all.empty and compare_projects:
    st.markdown(
        f"<div class='section-title'>Comparison Antar Project — {compare_kpi}</div>",
        unsafe_allow_html=True
    )

    df_cmp = df_all[
        (df_all["Project_Clean"].isin(compare_projects)) &
        (df_all["KPI_NAME"] == compare_kpi) &
        (df_all["VALUE_NUM"].notna())
    ].copy()

    _cmp_layout = dict(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8F9FF",
        font=dict(color="#374151", family="DM Sans, sans-serif"),
        xaxis=dict(tickangle=30, tickfont=dict(size=9)),
        margin=dict(l=10, r=10, t=10, b=80),
    )

    if not df_cmp.empty:
        tab_box, tab_bar, tab_violin = st.tabs(["Box Plot", "Bar Chart", "Violin Plot"])

        with tab_box:
            st.markdown(f"<div style='font-size:13px;font-weight:600;color:#374151;margin-bottom:4px'>Sebaran {compare_kpi} per Project</div>", unsafe_allow_html=True)
            fig_box = px.box(
                df_cmp, x="Project_Clean", y="VALUE_NUM",
                color="Project_Clean",
                labels={"VALUE_NUM": compare_kpi, "Project_Clean": "Project"},
                color_discrete_sequence=px.colors.qualitative.Bold,
            )
            fig_box.update_layout(**_cmp_layout, showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)

        with tab_bar:
            df_avg_cmp = df_cmp.groupby("Project_Clean")["VALUE_NUM"].agg(
                Average="mean", Median="median", Std="std"
            ).reset_index()

            st.markdown(f"<div style='font-size:13px;font-weight:600;color:#374151;margin-bottom:4px'>Rata-rata {compare_kpi} per Project (±Std Dev)</div>", unsafe_allow_html=True)
            fig_bar = px.bar(
                df_avg_cmp, x="Project_Clean", y="Average",
                error_y="Std",
                color="Average",
                color_continuous_scale=["#FF0000", "#FEED00", "#5032DC"],
                labels={"Average": f"Avg {compare_kpi}", "Project_Clean": "Project"},
                text=df_avg_cmp["Average"].apply(lambda x: f"{x:.1f}"),
            )
            fig_bar.update_layout(**_cmp_layout, coloraxis_showscale=False)
            fig_bar.update_traces(textposition="outside")
            st.plotly_chart(fig_bar, use_container_width=True)

        with tab_violin:
            st.markdown(f"<div style='font-size:13px;font-weight:600;color:#374151;margin-bottom:4px'>Distribusi {compare_kpi} per Project</div>", unsafe_allow_html=True)
            fig_vln = px.violin(
                df_cmp, x="Project_Clean", y="VALUE_NUM",
                color="Project_Clean", box=True, points="outliers",
                labels={"VALUE_NUM": compare_kpi, "Project_Clean": "Project"},
                color_discrete_sequence=px.colors.qualitative.Bold,
            )
            fig_vln.update_layout(**_cmp_layout, showlegend=False)
            st.plotly_chart(fig_vln, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# BAGIAN 15 — COMPARISON ANTAR KPI (dalam satu project)
# ============================================================

if not df_proj.empty:
    st.markdown(
        f"<div class='section-title'>Comparison Antar KPI — {selected_project}</div>",
        unsafe_allow_html=True
    )

    radar_data = []
    for kpi in NUMERIC_KPIS:
        subset = df_proj[df_proj["KPI_NAME"] == kpi]["VALUE_NUM"].dropna()
        if len(subset) == 0:
            continue
        avg = subset.mean()
        if kpi == "RSRP":
            score = max(0, min(100, (avg + 140) / (140 - 44) * 100))
        elif kpi == "RSRQ":
            score = max(0, min(100, (avg + 20) / 17 * 100))
        elif kpi == "SINR":
            score = max(0, min(100, (avg + 10) / 40 * 100))
        elif kpi == "Throughput":
            score = max(0, min(100, avg / 150 * 100))
        else:
            continue
        radar_data.append({"KPI": kpi, "Score": round(score, 1), "Avg": round(avg, 1)})

    if radar_data:
        col_radar, col_table = st.columns([1, 1])

        with col_radar:
            categories = [d["KPI"] for d in radar_data]
            values     = [d["Score"] for d in radar_data]
            values_closed     = values + [values[0]]
            categories_closed = categories + [categories[0]]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill="toself",
                fillcolor="rgba(79,70,229,0.15)",
                line=dict(color="#4F46E5", width=2),
                name=selected_project,
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100],
                                    tickfont=dict(size=10), gridcolor="#E2E8F0"),
                    angularaxis=dict(tickfont=dict(size=12, color="#1E1B4B")),
                    bgcolor="#F8F9FF",
                ),
                paper_bgcolor="#FFFFFF",
                showlegend=False,
                font=dict(color="#374151", family="DM Sans, sans-serif"),
                margin=dict(l=40, r=40, t=20, b=40),
                height=350,
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_table:
            st.markdown(
                "<div style='font-size:14px;font-weight:700;color:#1E1B4B;margin-bottom:10px'>Nilai Rata-rata & Score per KPI</div>",
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            for d in radar_data:
                score = d["Score"]
                color = get_kpi_color_dynamic(d["KPI"], d["Avg"])
                bar_w = int(score)
                st.markdown(f"""
                <div style='margin-bottom:16px'>
                    <div style='display:flex;justify-content:space-between;margin-bottom:5px;flex-wrap:wrap;gap:4px'>
                        <span style='font-weight:700;color:#1E1B4B'>{d["KPI"]}</span>
                        <span style='color:{color};font-weight:600'>{d["Avg"]}</span>
                    </div>
                    <div style='background:#E2E8F0;border-radius:4px;height:8px;overflow:hidden'>
                        <div style='width:{bar_w}%;background:{color};height:100%;border-radius:4px'></div>
                    </div>
                    <div style='font-size:11px;color:#64748B;margin-top:3px'>Score: {score}/100</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# BAGIAN 16 — STATISTICAL DISTRIBUTION
# ============================================================

if not df_kpi.empty:
    st.markdown(
        f"<div class='section-title'>Statistical Distribution — {selected_kpi}</div>",
        unsafe_allow_html=True
    )

    col_hist, col_stats = st.columns([2, 1])

    with col_hist:
        st.markdown(
            f"<div style='font-size:13px;font-weight:600;color:#374151;margin-bottom:4px'>Distribusi Nilai {selected_kpi}</div>",
            unsafe_allow_html=True
        )
        fig_hist = px.histogram(
            df_kpi, x="VALUE_NUM",
            color="Label",
            color_discrete_map=get_color_map_for_kpi(selected_kpi),
            nbins=50,
            labels={"VALUE_NUM": selected_kpi, "Label": "Kualitas"},
        )
        fig_hist.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#F8F9FF",
            font=dict(color="#374151", family="DM Sans, sans-serif"),
            margin=dict(l=10, r=10, t=10, b=20),
            legend=dict(orientation="h", yanchor="top", y=-0.15),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_stats:
        vals = df_kpi["VALUE_NUM"].dropna()
        st.markdown(
            "<div style='font-size:14px;font-weight:700;color:#1E1B4B;margin-bottom:10px'>Statistik Deskriptif</div>",
            unsafe_allow_html=True
        )
        stats = {
            "Count"   : f"{len(vals):,} titik",
            "Mean"    : f"{vals.mean():.2f}",
            "Median"  : f"{vals.median():.2f}",
            "Std Dev" : f"{vals.std():.2f}",
            "Min"     : f"{vals.min():.2f}",
            "Max"     : f"{vals.max():.2f}",
            "Q1 (25%)": f"{vals.quantile(0.25):.2f}",
            "Q3 (75%)": f"{vals.quantile(0.75):.2f}",
        }
        for label, val in stats.items():
            st.markdown(f"""
            <div class='stat-row'>
                <span class='stat-label'>{label}</span>
                <span class='stat-value'>{val}</span>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# BAGIAN 17 — FOOTER
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center;font-size:11px;color:#64748B;padding:10px'>"
    "RF Dashboard · PT NexWave Kerja Praktik · Jan–Feb 2026"
    "</div>",
    unsafe_allow_html=True
)

st.markdown("""
<style>

/* FONT UTAMA (AMAN) */
body, .stApp {
    font-family: 'DM Sans', sans-serif !important;
}

/* Fix Material Icons supaya tidak jadi teks */
.material-icons,
.material-icons-outlined,
.material-icons-round,
.material-icons-sharp,
[class*="material-icons"] {
    font-family: 'Material Icons' !important;
    font-style: normal !important;
}

/* Fix tombol sidebar mobile */
[data-testid="stSidebarCollapseButton"] span {
    font-family: 'Material Icons' !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

    /* HIDE DEFAULT SIDEBAR NAVIGATION */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

</style>
""", unsafe_allow_html=True)

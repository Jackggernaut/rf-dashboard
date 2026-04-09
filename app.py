# ============================================================
# RF NETWORK TESTING DASHBOARD
# PT NexWave · Kerja Praktik Jan–Feb 2026
# ============================================================
# STRUKTUR FILE:
#   app.py                        ← Halaman 1: Main Dashboard
#   pages/01_Project_Detail.py    ← Halaman 2: Per Project & Comparison
# ============================================================
# CARA JALANKAN:
#   streamlit run app.py
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
    page_title="Main Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# BAGIAN 3 — CUSTOM STYLING (CSS)
# Font: DM Sans (lebih estetik & modern)
# Force light mode agar konsisten di dark/light
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&display=swap');

    /* ─── FORCE LIGHT MODE — override dark theme ─── */
    .stApp {
    background-color: #1f49c4;
    }

    /* DM Sans untuk semua teks */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif !important;
    }

    /* Sembunyikan header sidebar TANPA hapus nav links */
    [data-testid="stSidebarHeader"] { display: none !important; }

    /* ── EXPANDER FIX ──
       Icon "keyboard_arrow_right" dari Material Icons render jadi teks karena
       wildcard font override. Fix: font-size:0 di summary biar icon invisible,
       lalu restore ukuran font di child element teks-nya.
       Expand tetap jalan karena elemen tidak di-display:none.
    */
    details > summary {
        font-size: 0 !important;          /* hide icon teks tanpa display:none */
        display: flex !important;
        align-items: center !important;
        padding: 12px 16px !important;
        cursor: pointer !important;
        list-style: none !important;
        gap: 0 !important;
    }
    details > summary::-webkit-details-marker { display: none !important; }
    details > summary::marker              { content: '' !important; }
    details > summary::before              { content: none !important; }

    /* Restore font-size pada teks label KPI */
    details > summary > div,
    details > summary > p,
    details > summary > span {
        font-size: 14px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        color: #1E1B4B !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        line-height: 1.4 !important;
        word-break: break-word !important;
        margin: 0 !important;
        flex: 1 1 auto !important;
    }

    /* SVG chevron — restore ukuran, taruh di kanan */
    details > summary > svg {
        width: 18px !important;
        height: 18px !important;
        flex-shrink: 0 !important;
        margin-left: auto !important;
    }

    /* Background utama */
    [data-testid="stAppViewContainer"] { background-color: #EEF2FF !important; }
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"] {
        background-color: #1f49c4 !important;
        border-right: 1px solid #C7D2FE !important;
    }
    [data-testid="stHeader"]           { background-color: #F0F2F8 !important; }
    /* Fix: konten tidak kepotong header Streamlit */
    [data-testid="stMainBlockContainer"] { padding-top: 3.5rem !important; }

    /* Override warna teks default Streamlit supaya tidak ikut dark mode */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] div,
    [data-testid="stAppViewContainer"] label {
        color: #1E1B4B;
    }

    /* Header dashboard */
    .dash-header {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #2563EB 100%);
        border-radius: 16px;
        padding: 20px 28px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .dash-title { font-size: 22px; font-weight: 800; color: #FFFFFF !important; }
    .dash-sub   { font-size: 12px; color: rgba(255,255,255,0.80) !important; margin-top: 2px; }
    .dash-badge {
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 11px;
        color: #FFFFFF !important;
        text-align: right;
        line-height: 1.6;
    }

    /* Kartu metrik */
    .metric-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(79,70,229,0.06);
    }
    .metric-label { font-size: 11px; color: #64748B !important; margin-bottom: 6px; letter-spacing: 0.5px; text-transform: uppercase; font-weight: 600; }
    .metric-value { font-size: 28px; font-weight: 800; line-height: 1; }
    .metric-unit  { font-size: 11px; color: #64748B !important; margin-top: 5px; font-weight: 500; }

    /* Kartu section */
    .section-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(79,70,229,0.04);
    }

    /* Judul section */
    .section-title {
        font-size: 13px;
        font-weight: 700;
        color: #4F46E5 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-left: 3px solid #4F46E5;
        padding-left: 10px;
        margin-bottom: 16px;
    }

    /* KPI Definition card */
    .kpi-def-card {
        background: #F8F9FF !important;
        border: 1px solid #E0E7FF;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 10px;
    }
    .kpi-def-name  { font-size: 15px; font-weight: 700; color: #1E1B4B !important; }
    .kpi-def-full  { font-size: 12px; color: #6366F1 !important; font-weight: 500; margin-bottom: 8px; }
    .kpi-def-body  { font-size: 13px; color: #475569 !important; line-height: 1.8; }

    /* Insight card */
    .insight-card {
        background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%) !important;
        border: 1px solid #C7D2FE;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    .insight-num {
        width: 26px; height: 26px;
        border-radius: 50%;
        background: #4F46E5;
        color: #FFFFFF !important;
        font-size: 12px;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .insight-text { font-size: 13px; color: #1E1B4B !important; line-height: 1.7; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: #F1F5F9 !important;
        border-radius: 8px;
        padding: 6px 18px;
        font-size: 13px;
        font-weight: 600;
        color: #64748B !important;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: #4F46E5 !important;
        color: #FFFFFF !important;
    }

    /* Expander container */
    .stExpander {
        border: 1px solid #E0E7FF !important;
        border-radius: 12px !important;
        background: #FFFFFF !important;
        overflow: visible !important;
    }
    /* Sembunyikan elemen toggle icon Streamlit yang render sebagai teks */
    [data-testid="stExpanderToggleIcon"] {
        display: none !important;
    }
    .stExpander summary p {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        line-height: 1.4 !important;
    }

    /* Sidebar text */
    .sidebar-title { font-size: 16px; font-weight: 800; color: #1E1B4B !important; margin-bottom: 4px; }
    .sidebar-sub   { font-size: 11px; color: #64748B !important; margin-bottom: 16px; }

    /* Semua markdown text di dalam expander agar tidak dark */
    .stExpander p, .stExpander li, .stExpander span {
        color: #374151 !important;
    }
    .stExpander strong { color: #1E1B4B !important; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# BAGIAN 4 — DEFINISI KPI
# ============================================================

KPI_INFO = {
    "RSRP": {
        "full"    : "Reference Signal Received Power",
        "color"   : "#5032DC",
        "unit"    : "dBm",
        "desc"    : """
        
**Apa itu RSRP?**
RSRP adalah indikator utama yang mengukur kekuatan sinyal LTE yang diterima perangkat dari satu cell tertentu (Reference Signal). Nilai ini diukur dalam satuan dBm dan mewakili daya sinyal pilot yang dikirimkan oleh eNodeB (base station).

**Mengapa penting?**
RSRP digunakan sebagai dasar pengambilan keputusan handover — perangkat akan berpindah ke cell lain ketika RSRP cell saat ini lebih rendah dibanding cell tetangga. Selain itu, RSRP juga menjadi acuan utama dalam drive test untuk mengevaluasi coverage area suatu jaringan.

**Cara membaca nilainya:**
Nilai RSRP selalu negatif. Semakin mendekati 0, semakin kuat sinyalnya. Misalnya, RSRP −80 dBm jauh lebih baik daripada −110 dBm.
        """,
        "threshold": {"Excellent": "≥ -85 dBm", "Good": "-85 s/d -95 dBm", "Fair": "-95 s/d -105 dBm", "Poor": "-105 s/d -110 dBm", "No Signal": "< -110 dBm"},
        "numeric" : True,
        "good_val": -80,
        "bad_val" : -110,
    },
    "RSRQ": {
        "full"    : "Reference Signal Received Quality",
        "color"   : "#0000FF",
        "unit"    : "dB",
        "desc"    : """
        
**Apa itu RSRQ?**
RSRQ mengukur kualitas sinyal referensi yang diterima dengan mempertimbangkan interferensi dan noise yang ada di jaringan. Berbeda dengan RSRP yang hanya mengukur kekuatan sinyal, RSRQ menggambarkan "kebersihan" sinyal dari gangguan sekitar.

**Mengapa penting?**
Nilai RSRP yang bagus tidak menjamin koneksi yang stabil apabila RSRQ buruk. RSRQ yang rendah menandakan bahwa area tersebut mengalami interferensi tinggi dari cell-cell lain atau dari noise lingkungan. Ini sering terjadi di area padat seperti pusat kota.

**Cara membaca nilainya:**
Nilai RSRQ juga selalu negatif. Semakin mendekati 0, semakin baik kualitasnya. RSRQ −9 dB ke atas dianggap baik untuk komunikasi data.
        """,
        "threshold": { "Excellent": "≥ -10 dB", "Good": "-10 s/d -14 dB", "Fair": "-14 s/d -16 dB", "Poor": "-16 s/d -18 dB", "No Signal": "< -18 dB"},
        "numeric" : True,
        "good_val": -10,
        "bad_val" : -20,
    },
    "SINR": {
        "full"    : "Signal to Interference plus Noise Ratio",
        "color"   : "#5032DC",
        "unit"    : "dB",
        "desc"    : """
        
**Apa itu SINR?**
SINR adalah rasio antara kekuatan sinyal yang diinginkan terhadap total interferensi ditambah noise yang ada di sekitarnya. Ini merupakan salah satu KPI paling kritis dalam menentukan kualitas koneksi data secara aktual.

**Mengapa penting?**
SINR secara langsung menentukan Modulation and Coding Scheme (MCS) yang digunakan — semakin tinggi SINR, semakin tinggi order modulasi yang bisa dipakai (hingga 256-QAM), yang berarti throughput lebih tinggi. SINR rendah memaksa sistem menggunakan modulasi rendah (QPSK) yang menghasilkan throughput minimal.

**Cara membaca nilainya:**
Berbeda dengan RSRP dan RSRQ, SINR bisa bernilai positif. Nilai di atas 20 dB sangat baik. Nilai di bawah 0 dB menunjukkan interferensi sangat dominan.
        """,
        "threshold": {"Excellent": "≥ 20 dB", "Very Good": "15 s/d 20 dB", "Good": "10 s/d 15 dB", "Fair": "3 s/d 10 dB", "Marginal": "0 s/d 3 dB", "Poor": "< 0 dB"},
        "numeric" : True,
        "good_val": 20,
        "bad_val" : 0,
    },
    "Throughput": {
        "full"    : "Data Transfer Rate (Actual)",
        "color"   : "#2E00FE",
        "unit"    : "Mbps",
        "desc"    : """
        
**Apa itu Throughput?**
Throughput adalah kecepatan transfer data aktual yang berhasil diterima atau dikirim oleh pengguna dalam jaringan, diukur dalam Mbps. Ini berbeda dengan kapasitas teoritis jaringan — throughput mencerminkan performa nyata yang dirasakan pengguna.

**Mengapa penting?**
Throughput adalah KPI yang paling langsung dirasakan oleh end-user. Nilai throughput rendah adalah sinyal utama bahwa pengguna mengalami masalah pada layanan internet. Throughput dipengaruhi oleh banyak faktor sekaligus: kondisi radio (RSRP, RSRQ, SINR), alokasi resource block, jumlah pengguna aktif di cell yang sama, dan kondisi backhaul.

**Cara membaca nilainya:**
Tidak ada nilai negatif. Semakin tinggi semakin baik. Untuk LTE standar, throughput DL di atas 50 Mbps dianggap baik. 5G NR dapat mencapai ratusan Mbps.
        """,
        "threshold": {"Excellent": "≥ 10 Mbps", "Good": "5 s/d 10 Mbps", "Fair": "3 s/d 5 Mbps", "Poor": "1 s/d 3 Mbps", "Bad": "< 1 Mbps"},
        "numeric" : True,
        "good_val": 50,
        "bad_val" : 5,
    },
    "ECI": {
        "full"    : "E-UTRAN Cell Identifier",
        "color"   : "#059669",
        "unit"    : "",
        "desc"    : """
        
**Apa itu ECI?**
ECI (E-UTRAN Cell Identifier) adalah identitas unik yang diberikan kepada setiap cell dalam jaringan LTE. ECI terdiri dari eNodeB ID dan Cell ID, sehingga setiap sektor antena di setiap base station memiliki identitas yang berbeda di seluruh jaringan.

**Mengapa penting?**
ECI memungkinkan sistem dan engineer untuk mengidentifikasi secara tepat cell mana yang sedang melayani perangkat. Dalam analisis drive test, ECI digunakan untuk memetakan coverage masing-masing cell, mendeteksi anomali seperti pilot pollution (satu perangkat dilayani oleh terlalu banyak cell dengan sinyal hampir sama kuat), serta mendukung proses optimasi neighbor list dan handover.

**Format nilai:**
ECI biasanya ditampilkan dalam format "eNodeB ID / Cell ID", misalnya "392068 / 61" yang berarti eNodeB 392068, sektor/cell 61.
        """,
        "threshold": {"Normal": "Format eNodeB/Cell valid", "Anomali": "Pilot pollution / missing neighbor"},
        "numeric" : False,
        "good_val": None,
        "bad_val" : None,
    },
    "PCI": {
        "full"    : "Physical Cell Identity",
        "color"   : "#DC2626",
        "unit"    : "",
        "desc"    : """
        
**Apa itu PCI?**
PCI (Physical Cell Identity) adalah identitas fisik layer yang digunakan perangkat untuk membedakan sinyal dari cell-cell yang berbeda di udara. Nilai PCI berkisar antara 0 hingga 503, dan dialokasikan oleh operator saat perencanaan jaringan.

**Mengapa penting?**
Alokasi PCI yang buruk dapat menyebabkan dua masalah serius: PCI Collision (dua cell bertetangga memiliki PCI yang sama, menyebabkan perangkat bingung) dan PCI Confusion (cell-cell dalam neighbor list memiliki PCI yang sama, mengganggu handover). Kedua masalah ini berdampak langsung pada kualitas layanan.

**Cara membaca nilainya:**
Dalam drive test, PCI digunakan untuk mengidentifikasi cell serving dan memvalidasi apakah alokasi PCI sudah sesuai rencana. PCI juga digunakan untuk menghitung PSS dan SSS dalam proses sinkronisasi.
        """,
        "threshold": {"Valid": "0 – 503, unik di area", "Collision": "PCI sama di cell bertetangga", "Confusion": "PCI sama di neighbor list"},
        "numeric" : False,
        "good_val": None,
        "bad_val" : None,
    },
    "RFMODE": {
        "full"    : "Radio Frequency Mode",
        "color"   : "#0284C7",
        "unit"    : "",
        "desc"    : """
        
**Apa itu RF Mode?**
RF Mode menunjukkan teknologi atau mode radio yang sedang aktif digunakan oleh perangkat dalam jaringan. Mode ini bisa berupa LTE (4G), NR (5G New Radio), atau mode IDLE ketika perangkat tidak aktif melakukan komunikasi data.

**Mengapa penting?**
RF Mode sangat mempengaruhi karakteristik performa yang diukur. Pengukuran pada mode IDLE berbeda dengan CONNECTED karena resource radio belum sepenuhnya dialokasikan. Selain itu, mode NR (5G) akan menghasilkan nilai throughput jauh lebih tinggi dibanding LTE pada kondisi radio yang sama, sehingga analisis performa harus mempertimbangkan mode yang aktif.

**Mode yang umum ditemui dalam drive test:**
- **IDLE**: Perangkat terhubung ke jaringan tapi tidak aktif transfer data
- **LTE Connected**: Aktif menggunakan jaringan 4G LTE
- **NR Connected**: Aktif menggunakan jaringan 5G NR (standalone atau NSA)
        """,
        "threshold": {"LTE Connected": "Mode 4G aktif", "NR Connected": "Mode 5G aktif", "IDLE": "Tidak aktif transfer data"},
        "numeric" : False,
        "good_val": None,
        "bad_val" : None,
    },
}

# KPI numerik saja (untuk kartu metrik)
NUMERIC_KPIS    = [k for k, v in KPI_INFO.items() if v["numeric"]]
SUMMARY_KPIS    = ["RSRP", "RSRQ", "SINR", "Throughput"]  # untuk Executive Summary

# Mapping file CSV
KPI_FILES = {
    "RSRP"      : "data/RSRP_ALL.csv",
    "RSRQ"      : "data/RSRQ_ALL.csv",
    "SINR"      : "data/SINR_ALL.csv",
    "Throughput": "data/THROUGHPUT_ALL.csv",
    "ECI"       : "data/ECI_ALL.csv",
    "PCI"       : "data/PCI_ALL.csv",
    "RFMODE"    : "data/RFMODE_ALL.csv",
}

# Threshold 3GPP untuk insight otomatis
THRESHOLDS = {
    "RSRP"      : {"good": -80,  "bad": -110},
    "RSRQ"      : {"good": -10,  "bad": -20},
    "SINR"      : {"good": 20,   "bad": 0},
    "Throughput": {"good": 50,   "bad": 5},
}


# ============================================================
# BAGIAN 5 — LOAD & PROSES DATA
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
            except Exception as e:
                st.warning(f"Gagal membaca {path}: {e}")

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
# BAGIAN 6 — FUNGSI GENERATE KEY INSIGHTS OTOMATIS
# ============================================================

def generate_insights(df):
    insights = []

    if df.empty:
        return ["Data belum tersedia untuk dianalisis."]

    for kpi, thresh in THRESHOLDS.items():
        subset = df[df["KPI_NAME"] == kpi]["VALUE_NUM"].dropna()
        if len(subset) == 0:
            continue

        avg_val  = subset.mean()
        good_val = thresh["good"]
        bad_val  = thresh["bad"]

        if kpi in ["RSRP", "RSRQ", "SINR"] and bad_val is not None:
            pct_bad  = (subset < bad_val).mean()  * 100
            pct_good = (subset >= good_val).mean() * 100
        elif kpi == "Throughput":
            pct_bad  = (subset < bad_val).mean()  * 100
            pct_good = (subset >= good_val).mean() * 100
        else:
            continue

        unit = KPI_INFO[kpi]["unit"]

        if pct_bad > 20:
            insights.append({
                "type"  : "warning",
                "title" : f"{kpi} — Perlu Perhatian",
                "body"  : f"Rata-rata {kpi} sebesar {avg_val:.1f} {unit} dengan {pct_bad:.0f}% titik pengukuran berada di zona buruk (< {bad_val} {unit} berdasarkan standar 3GPP). "
                          f"Kondisi ini mengindikasikan adanya area dengan coverage atau kualitas sinyal yang tidak memadai dan perlu tindakan optimasi.",
                "saran" : f"Lakukan audit cell coverage di area dengan {kpi} rendah, evaluasi tilt dan azimuth antena, serta pertimbangkan penambahan site baru atau small cell untuk meningkatkan {kpi}."
            })
        elif pct_good > 70:
            insights.append({
                "type"  : "good",
                "title" : f"{kpi} — Performa Baik",
                "body"  : f"Rata-rata {kpi} sebesar {avg_val:.1f} {unit} dengan {pct_good:.0f}% titik pengukuran berada di zona baik (≥ {good_val} {unit}). "
                          f"Ini menunjukkan kualitas {kpi} secara keseluruhan sudah memenuhi standar layanan.",
                "saran" : f"Pertahankan konfigurasi jaringan saat ini dan lakukan monitoring berkala untuk memastikan konsistensi performa {kpi}."
            })
        else:
            insights.append({
                "type"  : "neutral",
                "title" : f"{kpi} — Performa Moderat",
                "body"  : f"Rata-rata {kpi} sebesar {avg_val:.1f} {unit}. Sekitar {pct_good:.0f}% titik sudah baik, namun masih ada {pct_bad:.0f}% titik di zona buruk. "
                          f"Distribusi nilai yang variatif mengindikasikan inkonsistensi kualitas antar area.",
                "saran" : f"Identifikasi cluster area dengan {kpi} rendah menggunakan geographic map, lalu prioritaskan optimasi pada lokasi tersebut."
            })

    rsrp_data = df[df["KPI_NAME"] == "RSRP"]["VALUE_NUM"].dropna()
    tp_data   = df[df["KPI_NAME"] == "Throughput"]["VALUE_NUM"].dropna()

    if len(rsrp_data) > 10 and len(tp_data) > 10:
        avg_rsrp = rsrp_data.mean()
        avg_tp   = tp_data.mean()
        if avg_rsrp >= -90 and avg_tp < 20:
            insights.append({
                "type"  : "warning",
                "title" : "Anomali: RSRP Baik tapi Throughput Rendah",
                "body"  : f"Rata-rata RSRP ({avg_rsrp:.1f} dBm) tergolong cukup baik, namun rata-rata Throughput ({avg_tp:.1f} Mbps) masih rendah. "
                          f"Ini mengindikasikan bahwa masalah bukan pada coverage, melainkan pada interferensi (RSRQ/SINR) atau kapasitas jaringan.",
                "saran" : "Fokuskan analisis pada RSRQ dan SINR untuk mendeteksi sumber interferensi. Evaluasi juga kapasitas backhaul dan load sharing antar cell."
            })

    return insights if insights else [{"type": "neutral", "title": "Data terbatas", "body": "Belum cukup data untuk menghasilkan insight otomatis.", "saran": ""}]


# ============================================================
# BAGIAN 7 — SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("<div class='sidebar-title'>📡 Main Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-sub'>PT NexWave · Jan–Feb 2026</div>", unsafe_allow_html=True)
    st.divider()

    if df_all.empty:
        st.warning("⚠️ File CSV tidak ditemukan.\nPastikan folder `data/` berisi file CSV.")
        selected_projects = []
        selected_mode     = "Semua"
    else:
        all_projects      = sorted(df_all["Project_Clean"].unique().tolist())
        default_projects  = all_projects
        selected_projects = st.multiselect("Filter Project", all_projects, default=default_projects)

        all_modes     = ["Semua"] + sorted(df_all["Mode"].dropna().unique().tolist())
        selected_mode = st.selectbox("Filter Mode", all_modes)

    st.divider()
    st.markdown(
        "<div style='font-size:11px;color:#64748B'>"
        "Disusun oleh:<br>"
        "<b style='color:#4F46E5'>Ilham Candra Harmawan.</b> · 5003231172<br>"
        "<b style='color:#4F46E5'>Muhammad Al Fatih Nafiudin Sya'bani</b> · 5003231189</div>",
        unsafe_allow_html=True
    )


# ============================================================
# BAGIAN 8 — TERAPKAN FILTER
# ============================================================

if not df_all.empty and selected_projects:
    df = df_all[df_all["Project_Clean"].isin(selected_projects)].copy()
    if selected_mode != "Semua":
        df = df[df["Mode"] == selected_mode]
else:
    df = df_all.copy() if not df_all.empty else pd.DataFrame()


# ============================================================
# BAGIAN 9 — HEADER HALAMAN
# ============================================================

st.markdown("""
<div class='dash-header'>
    <div>
        <div class='dash-title'>📡 Main Dashboard</div>
        <div class='dash-sub'>Multi-Project Network Performance Monitoring System · PT NexWave</div>
    </div>
    <div class='dash-badge'>
        Ilham Candra Harmawan. · 5003231172<br>
        Muhammad Al Fatih Nafiudin Sya'bani · 5003231189
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# BAGIAN 10 — EXECUTIVE SUMMARY
# ============================================================

st.markdown("<div class='section-title'>Executive Summary</div>", unsafe_allow_html=True)

tab_avg, tab_med = st.tabs(["📊 Average", "📈 Median"])

def get_kpi_color(kpi, value):
    """Return hex warna sesuai colour palette kantor untuk tiap nilai KPI."""
    if value is None:
        return "#94A3B8"
    palette = {
        "RSRP": [
            (-85,  "#5032DC"),
            (-95,  "#548235"),
            (-105, "#00FF00"),
            (-110, "#FFFF00"),
            (None, "#FF0000"),
        ],
        "RSRQ": [
            (-10,  "#0000FF"),
            (-14,  "#00FFFF"),
            (-16,  "#62FF07"),
            (-18,  "#FAFA00"),
            (None, "#FF0303"),
        ],
        "SINR": [
            (20,   "#5032DC"),
            (15,   "#0000FF"),
            (10,   "#00FFFF"),
            (3,    "#B2DF8A"),
            (0,    "#D7FF0E"),
            (None, "#FF0000"),
        ],
        "Throughput": [
            (10,   "#2E00FE"),
            (5,    "#3D7539"),
            (3,    "#37FE00"),
            (1,    "#FEED00"),
            (None, "#FE0000"),
        ],
    }
    if kpi not in palette:
        return "#94A3B8"
    for thresh, color in palette[kpi]:
        if thresh is None:
            return color
        if value >= thresh:
            return color
    return "#94A3B8"

def render_summary_cards(agg_func):
    cols = st.columns(len(SUMMARY_KPIS))
    for i, kpi in enumerate(SUMMARY_KPIS):
        info = KPI_INFO[kpi]
        if not df.empty and kpi in df["KPI_NAME"].values:
            subset = df[df["KPI_NAME"] == kpi]["VALUE_NUM"].dropna()
            val    = agg_func(subset) if len(subset) > 0 else None
        else:
            val = None
        val_str = f"{val:.1f}" if val is not None else "—"
        cols[i].markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{kpi}</div>
            <div class='metric-value' style='color:{get_kpi_color(kpi, val)}'>{val_str}</div>
            <div class='metric-unit'>{info["unit"]}</div>
        </div>
        """, unsafe_allow_html=True)

with tab_avg:
    render_summary_cards(lambda s: s.mean())
with tab_med:
    render_summary_cards(lambda s: s.median())

st.markdown("<br>", unsafe_allow_html=True)

# Statistik total
col_t1, col_t2, col_t3 = st.columns(3)
total_proj   = df_all["Project"].nunique()  if not df_all.empty else 0
total_record = len(df_all)                  if not df_all.empty else 0
kpi_count    = df_all["KPI_NAME"].nunique() if not df_all.empty else 0

col_t1.markdown(f"<div class='metric-card'><div class='metric-label'>Total Project</div><div class='metric-value' style='color:#4F46E5'>{total_proj}</div><div class='metric-unit'>All Time</div></div>", unsafe_allow_html=True)
col_t2.markdown(f"<div class='metric-card'><div class='metric-label'>Completed</div><div class='metric-value' style='color:#059669'>{total_proj}</div><div class='metric-unit'>100%</div></div>", unsafe_allow_html=True)
col_t3.markdown(f"<div class='metric-card'><div class='metric-label'>Total Records</div><div class='metric-value' style='color:#7C3AED'>{total_record:,}</div><div class='metric-unit'>{kpi_count} KPI types</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# BAGIAN 11 — KPI DEFINITIONS (ACCORDION)
# Judul KPI dipisah agar tidak numpuk + bar chart per project
# ============================================================

st.markdown("<div class='section-title'>KPI Definitions</div>", unsafe_allow_html=True)

KPI_COLORS_MAP = {
    "RSRP"      : "#5032DC",
    "RSRQ"      : "#0000FF",
    "SINR"      : "#5032DC",
    "Throughput": "#2E00FE",
    "ECI"       : "#059669",
    "PCI"       : "#DC2626",
    "RFMODE"    : "#0284C7",
}

for kpi, info in KPI_INFO.items():
    with st.expander(f"**{kpi} — {info['full']}**", expanded=False):

        st.markdown(f"""
        <div class="kpi-def-card">
            <div class="kpi-def-name">{kpi}</div>
            <div class="kpi-def-full">{info['full']}</div>
            <div class="kpi-def-body">{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

        # OPTIONAL: grafik
        if info["numeric"] and not df_all.empty and kpi in df_all["KPI_NAME"].values:
            st.markdown("---")
            st.markdown(f"**📊 Rata-rata {kpi} per Project**")

            df_kpi_all = df_all[df_all["KPI_NAME"] == kpi].copy()
            df_avg_proj = (
                df_kpi_all.groupby("Project_Clean")["VALUE_NUM"]
                .mean()
                .reset_index()
                .rename(columns={"VALUE_NUM": f"Avg {kpi}"})
            )

            fig_bar = px.bar(
                df_avg_proj,
                x="Project_Clean",
                y=f"Avg {kpi}",
                text=df_avg_proj[f"Avg {kpi}"].apply(lambda x: f"{x:.1f}")
            )

            st.plotly_chart(fig_bar, use_container_width=True)


# ============================================================
# BAGIAN 12 — KEY INSIGHTS & RECOMMENDATIONS (OTOMATIS)
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Key Insights & Recommendations</div>", unsafe_allow_html=True)

insights = generate_insights(df)

color_map = {
    "warning": ("#FEF3C7", "#D97706", "#92400E"),
    "good"   : ("#D1FAE5", "#059669", "#065F46"),
    "neutral": ("#EEF2FF", "#4F46E5", "#1E1B4B"),
}

for i, insight in enumerate(insights):
    if isinstance(insight, dict):
        bg, border, text = color_map.get(insight["type"], color_map["neutral"])
        st.markdown(f"""
        <div style='background:{bg};border:1px solid {border};border-radius:12px;
                    padding:16px 18px;margin-bottom:10px;'>
            <div style='font-size:14px;font-weight:700;color:{text};margin-bottom:6px'>
                {i+1}. {insight["title"]}
            </div>
            <div style='font-size:13px;color:#374151;line-height:1.7;margin-bottom:8px'>
                {insight["body"]}
            </div>
            <div style='font-size:12px;color:{border};font-weight:600'>
                💡 Rekomendasi: {insight["saran"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='insight-card'>
            <div class='insight-num'>{i+1}</div>
            <div class='insight-text'>{insight}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# BAGIAN 13 — FOOTER
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

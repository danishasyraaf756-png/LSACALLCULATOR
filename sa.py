import streamlit as st
import numpy as np

# 1. Konfigurasi Halaman (Page Config)
st.set_page_config(
    page_title="Kalkulator LSA Survey",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Styling CSS Khas untuk Kecantikan UI
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #2b580c;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1e3d08;
        color: #ffffff;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #2b580c;
    }
    </style>
""", unsafe_allow_html=True)

# Tajuk Utama dengan Hiasan Emoji
st.title("📐 Kalkulator Larasan Sudut (LSA)")
st.markdown("*Kaedah Persamaan Cerapan (Observation Equation Method) — Rujukan Nota Page 74-76*")
st.markdown("---")

# Fungsi Penukaran DMS & Decimal Degrees
def dms_to_deg(d, m, s):
    return d + m/60.0 + s/3600.0

def deg_to_dms(decimal_deg):
    d = int(decimal_deg)
    m_float = (decimal_deg - d) * 60
    m = int(m_float)
    s = (m_float - m) * 60
    return f"{d}° {m}' {s:.2f}\""

# Sidebar untuk Panduan Ringkas
with st.sidebar:
    st.header("📌 Panduan Penggunaan")
    st.info(
        "1. Masukkan nilai **Darjah**, **Minit**, dan **Saat** bagi sudut A, B, dan C.\n"
        "2. Pastikan syarat jumlah pulangan (biasanya **360° 0' 0''**) diisi dengan betul.\n"
        "3. Tekan butang **'Kira Mengikut Formula Matriks'** di bawah."
    )
    st.markdown("---")
    st.caption("Dibangunkan untuk Kursus Ukur Kejuruteraan / Geomatik.")

# Layout Input Menggunakan Container/Tabs supaya lebih teratur
tab1, tab2 = st.tabs(["📝 Masukkan Data Cerapan", "ℹ️ Info Formula Matriks"])

with tab1:
    st.subheader("1. Masukkan Nilai Cerapan Asal (DMS)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔵 Sudut A")
        da = st.number_input("Darjah A", value=150, step=1, key="da")
        ma = st.number_input("Minit A", value=20, step=1, key="ma")
        sa = st.number_input("Saat A", value=30.0, step=0.1, key="sa")

    with col2:
        st.markdown("#### 🟢 Sudut B")
        db = st.number_input("Darjah B", value=80, step=1, key="db")
        mb = st.number_input("Minit B", value=17, step=1, key="mb")
        sb = st.number_input("Saat B", value=35.0, step=0.1, key="sb")

    with col3:
        st.markdown("#### 🟠 Sudut C")
        dc = st.number_input("Darjah C", value=129, step=1, key="dc")
        mc = st.number_input("Minit C", value=21, step=1, key="mc")
        sc = st.number_input("Saat C", value=30.0, step=0.1, key="sc")

    st.markdown("---")
    st.subheader("2. Syarat Jumlah Bulatan")
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        dtot = st.number_input("Darjah Total", value=360, step=1, key="dtot")
    with col_t2:
        mtot = st.number_input("Minit Total", value=0, step=1, key="mtot")
    with col_t3:
        st_sum_sec = st.number_input("Saat Total", value=0.0, step=0.1, key="stot")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Butang Pengiraan Utama
    calculate_clicked = st.button("🚀 Kira Mengikut Formula Matriks (LSA)")

with tab2:
    st.subheader("Nota Rujukan Formula Matriks")
    st.latex(r"X = (A^T A)^{-1} A^T L")
    st.write("Kaedah ini melaraskan nilai cerapan mentah meminimumkan jumlah ralat تربيع (residuals) berdasarkan syarat geometri yang ditetapkan.")

# Proses Pengiraan & Paparan Keputusan
if calculate_clicked:
    # 1. Tukar kepada decimal degrees
    L1 = dms_to_deg(da, ma, sa)
    L2 = dms_to_deg(db, mb, sb)
    L3 = dms_to_deg(dc, mc, sc)
    total_val = dms_to_deg(dtot, mtot, st_sum_sec)
    
    # Mengikut nota langkah 1: A + B = Total - C
    s_val_AB = total_val - L3
    
    # 2. Bina Vektor L
    L = np.array([L1, L2, s_val_AB])
    
    # 3. Bina Matriks A
    A_mat = np.array([
        [1, 0],
        [0, 1],
        [1, 1]
    ])
    
    # 4. Pengiraan Matriks LSA: X = (A^T * A)^(-1) * A^T * L
    At = A_mat.T
    AtA = np.dot(At, A_mat)
    AtA_inv = np.linalg.inv(AtA)
    AtL = np.dot(At, L)
    X = np.dot(AtA_inv, AtL)
    
    # Nilai laras A dan B
    adj_A = X[0]
    adj_B = X[1]
    
    # Nilai laras C dikira semula menggunakan syarat 360° - (A + B)
    adj_C = total_val - (adj_A + adj_B)
    
    # Bahagian Keputusan dengan Reka Bentuk Kotak Elegan
    st.markdown("---")
    st.subheader("✨ Keputusan Selepas Larasan (Adjusted Values)")
    
    res1, res2, res3 = st.columns(3)
    
    with res1:
        st.success("Nilai Laras A")
        st.markdown(f"### `{deg_to_dms(adj_A)}`")
    with res2:
        st.success("Nilai Laras B")
        st.markdown(f"### `{deg_to_dms(adj_B)}`")
    with res3:
        st.success("Nilai Laras C")
        st.markdown(f"### `{deg_to_dms(adj_C)}`")
        
    st.balloons() # Memberi kesan animasi ringkas apabila berjaya dikira
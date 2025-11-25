import streamlit as st
from PIL import Image
from style import inject_global_style, render_sidebar

st.set_page_config(
    page_title="PREDICTEL - Sistem Prediksi Churn",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_global_style()


st.markdown("""
<style>
    /* =========================================
       SIDEBAR STYLING
       ========================================= */
    
    /* Memaksa semua teks di sidebar menjadi PUTIH agar terbaca di background biru */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }
    
    /* Header 'PREDICTEL' di Sidebar */
    .sidebar-logo {
        font-family: 'Arial Black', sans-serif;
        font-size: 2.2rem;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 0px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Garis pemisah di bawah logo PREDICTEL */
    .sidebar-divider {
        height: 2px;
        background-color: #FFFFFF;
        margin-bottom: 20px;
        opacity: 0.3;
    }

    /* Style Navigasi Halaman (Radio Button / Links) */
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 1.1rem !important;
        font-weight: 500;
        padding: 10px;
    }
    
    /* =========================================
       MAIN PAGE STYLING
       ========================================= */
    
    .main {
        background-color: #FFFFFF;
    }
    
    /* Kartu Hero Biru Besar */
    .hero-container {
        background: linear-gradient(90deg, #0083B8 0%, #00A3E0 50%, #00E0FF 100%); /* Biru gradasi PREDICTEL */
        padding: 3rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 131, 184, 0.3);
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: #FFFFFF !important;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        line-height: 1.6;
        color: #F0F9FF !important;
    }
    
    /* Kartu Info (Cara Kerja & Tentang) */
    .info-card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #00A3E0; /* Border Cyan */
        height: 100%;
        color: #333333;
    }
    .card-header {
        color: #0F172A;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Tombol Mulai (Custom) */
    div.stButton > button {
        background-color: #FFFFFF;
        color: #0083B8;
        border: 2px solid white;
        font-weight: 800;
        padding: 0.6rem 1.5rem;
        border-radius: 10px;
    }
    div.stButton > button:hover {
        background-color: #E0F2FE;
        color: #006080;
        border-color: #E0F2FE;
    }

</style>
""", unsafe_allow_html=True)

render_sidebar("Home")

st.markdown("""
<div class="hero-container">
    <div class="hero-title">SISTEM PREDIKSI CUSTOMER CHURN</div>
    <div class="hero-subtitle">
        Aplikasi analisis berbasis Machine Learning untuk memprediksi dan mencegah 
        kehilangan pelanggan dengan akurasi tinggi menggunakan algoritma Logistic Regression.
    </div>
    <br>
</div>
""", unsafe_allow_html=True)

col_spacer, col_button = st.columns([4, 1])
with col_button:
    if st.button("🚀 Mulai Input Data", type="primary", use_container_width=True):
        st.switch_page("pages/Input_Data.py")


col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <div class="card-header">
            ⚙️ Cara Kerja
        </div>
        <ol style="margin-left: 1rem; line-height: 1.8;">
            <li><strong>Input Data Pelanggan</strong><br>Unggah file CSV dataset Telco Customer Churn.</li>
            <li><strong>Processing Data</strong><br>Sistem membersihkan data dan melakukan encoding otomatis.</li>
            <li><strong>Latih Data</strong><br>Model Logistic Regression mempelajari pola churn dari data.</li>
            <li><strong>Visualisasi Data</strong><br>Lihat grafik dan hasil analisis mendalam.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div class="info-card">
        <div class="card-header">
            🧠 Tentang Sistem
        </div>
        <p style="line-height: 1.6; text-align: justify;">
            <strong>Predictel</strong> adalah sistem prediksi berbasis Machine Learning yang dibangun 
            untuk membantu perusahaan telekomunikasi mengidentifikasi pelanggan yang berisiko 
            berhenti berlangganan (churn).
            <br><br>
            Sistem ini menggunakan algoritma <strong>Logistic Regression</strong> yang telah dilatih 
            dengan 19 fitur penting meliputi data demografis, riwayat layanan, dan pola 
            pembayaran pelanggan.
        </p>
    </div>
    """, unsafe_allow_html=True)
import streamlit as st

from style import inject_global_style, render_sidebar

st.set_page_config(
    page_title="PREDICTEL - Sistem Prediksi Churn",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_style()
render_sidebar("Home")

st.markdown(
    """
    <div class="app-hero">
        <div class="hero-content">
            <div class="hero-badge">
                <span>📡</span>
                <span>PREDICTEL Analytics Platform</span>
            </div>
            <h1 class="hero-title">
                Prediksi Customer Churn dengan Machine Learning
            </h1>
            <p class="hero-subtitle">
                Platform analitik berbasis AI untuk memprediksi risiko churn pelanggan
                telekomunikasi menggunakan algoritma Logistic Regression yang akurat dan dapat diinterpretasi.
            </p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="hero-stat-value">Logistic Regression</div>
                    <div class="hero-stat-label">Algoritma ML</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-value">19+ Features</div>
                    <div class="hero-stat-label">Fitur Analisis</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-value">Real-time</div>
                    <div class="hero-stat-label">Prediksi</div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Mulai Analisis", type="primary", use_container_width=True):
        st.switch_page("pages/Input_Data.py")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("⚡ Workflow Otomatis")
    st.write(
        "Pipeline end-to-end yang terintegrasi: upload data → preprocessing otomatis → training model → visualisasi hasil → prediksi individual."
    )
    st.markdown("""
    - Data cleaning dan encoding otomatis
    - Feature scaling yang optimal
    - Handling missing values (median/mean/modus)
    - Train/test split yang seimbang
    """)

    st.markdown("---")

    st.subheader("📊 Visualisasi Canggih")
    st.write(
        "Dashboard interaktif dengan berbagai jenis grafik untuk mengeksplorasi pola churn dan memahami perilaku pelanggan secara mendalam."
    )
    st.markdown("""
    - Scatter plots dan bar charts
    - Distribusi churn per kategori
    - Correlation heatmaps
    - Interactive filtering
    """)

    st.markdown("---")

    st.subheader("🔧 Preprocessing Fleksibel")
    st.write(
        "Berbagai opsi preprocessing data yang dapat disesuaikan dengan karakteristik dataset dan kebutuhan analisis spesifik."
    )
    st.markdown("""
    - Pilihan handling missing values
    - Multiple encoding strategies
    - Feature scaling methods
    - Data validation checks
    """)

with col2:
    st.subheader("🧠 Machine Learning")
    st.write(
        "Menggunakan algoritma Logistic Regression yang telah dioptimasi untuk dataset churn telekomunikasi dengan interpretabilitas yang tinggi."
    )
    st.markdown("""
    - Akurasi model yang konsisten
    - ROC AUC score untuk evaluasi
    - Confusion matrix yang informatif
    - Feature importance analysis
    """)

    st.markdown("---")

    st.subheader("🎯 Prediksi Akurat")
    st.write(
        "Simulasi prediksi real-time untuk pelanggan individual dengan probabilitas churn dan rekomendasi tindakan bisnis."
    )
    st.markdown("""
    - Input data pelanggan yang mudah
    - Hasil prediksi instan
    - Confidence score yang detail
    - Business insights yang actionable
    """)

    st.markdown("---")

    st.subheader("💼 Business Impact")
    st.write(
        "Mendukung pengambilan keputusan bisnis dengan insights yang dapat diimplementasikan untuk program retensi pelanggan."
    )
    st.markdown("""
    - Identifikasi pelanggan high-risk
    - Analisis faktor churn utama
    - ROI calculation untuk retensi
    - Strategic recommendations
    """)

st.markdown("---")
st.markdown("## 🚀 Quick Start Guide")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        **Step 1: Input Data**

        📂 Upload dataset CSV dengan format Telco Customer Churn

        ✅ Validasi otomatis struktur data
        """
    )

with col2:
    st.markdown(
        """
        **Step 2: Preprocessing**

        ⚙️ Pilih metode handling missing values

        🔄 Automatic feature engineering
        """
    )

with col3:
    st.markdown(
        """
        **Step 3: Model Training**

        🧪 Train Logistic Regression model

        📊 Evaluasi performa model
        """
    )

with col4:
    st.markdown(
        """
        **Step 4: Analysis**

        📈 Visualisasi insights

        🎯 Prediksi individual
        """
    )

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        """
        <div style="text-align: center; color: var(--text-muted); padding: 2rem;">
            <p>
                <strong>PREDICTEL</strong> - Customer Churn Analytics Platform<br>
                Powered by Streamlit & Scikit-learn | Built for Telecom Industry
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

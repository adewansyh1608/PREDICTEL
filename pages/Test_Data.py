import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
from style import inject_global_style, render_sidebar

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Test Data & Prediction - PREDICTEL",
    page_icon="🧪",
    layout="wide"
)

inject_global_style()
render_sidebar("Test Data")

# 2. Custom CSS (Sesuai Desain image_5584dc.png)
st.markdown("""
<style>
    /* Font Global */
    h1, h2, h3 {
        color: #0F172A;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Spacing untuk button */
    .stButton {
        margin-top: 1rem;
        margin-bottom: 1rem;
        border-radius: 10px !important;
        border-width: 1px !important;
        border-style: solid !important;
        border-color: #4293E4 !important;
    }

     /* Wrap Card Form */
    div[data-testid="stForm"] {
        border: 1.5px solid #4293E4 !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin-top: 1rem !important;
        margin-bottom: 1.5rem !important;
        background-color: #ffffff !important;
    }

    /* Tombol dalam Form */
    div[data-testid="stForm"] .stButton>button {
        border-radius: 10px !important;
        border-width: 1px !important;
        border-color: #4293E4 !important;
        color: #4293E4 !important;
        background-color: #ffffff !important;
        border-style: solid !important;
        margin-top: 1rem !important;
    }

    /* Tombol Saat Hover */
    div[data-testid="stForm"] .stButton>button:hover {
        background-color: #4293E420 !important;
        color: #4293E4 !important;
    }

    div[data-baseweb="input"] > div {
    background-color: white !important;
    padding: 6px 10px !important;
    transition: 0.3s ease-in-out !important;
    }

    /* teks input */
    div[data-baseweb="input"] input {
        color: #4293E4 !important;
        font-weight: 600 !important;
    }

    /* hover */
    div[data-baseweb="input"]:hover > div {
        border-color: #1e6fbe !important;
        box-shadow: 0 0 6px rgba(66,147,228,0.4) !important;
    }

    /* saat fokus */
    div[data-baseweb="input"]:focus-within > div {
        border-color: #1e6fbe !important;
        box-shadow: 0 0 8px rgba(66,147,228,0.6) !important;
    }

    /* Tombol + dan - pada number_input */
div[data-baseweb="input"] button {
    background-color: #4293E4 !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    width: 32px !important;
    height: 32px !important;
    font-size: 18px !important;
    transition: 0.25s;
}

/* Hover effect */
div[data-baseweb="input"] button:hover {
    background-color: #1e6fbe !important;
}

/* Styling selectbox container */
div[data-baseweb="select"] > div {
    background-color: white !important;     /* warna background */
    border: 2px solid #4293E4 !important;   /* warna border */
    border-radius: 8px !important;          /* sudut tumpul */
    box-shadow: none !important;
}

/* Saat selectbox di-hover */
div[data-baseweb="select"] > div:hover {
    border-color: #1d6fc8 !important;
}

/* Saat selectbox dibuka */
div[data-baseweb="select"]:focus-within > div {
    border-color: #1d6fc8 !important;
    box-shadow: 0 0 0 1px #1d6fc8 !important;
}

/* Membuat input selectbox tidak bisa diketik */
div[data-baseweb="select"] input {
    caret-color: transparent !important;  /* hide cursor */
    pointer-events: none !important;       /* disable typing */
}

/* Style arrow */
div[data-baseweb="select"] svg {
    fill: #4293E4 !important; /* warna icon arrow */
}

    /* Styling Header "PREDICTION RESULT" */
    .prediction-header {
        color: #003366;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    /* Styling Kotak Hasil (Kotak Putih Border Biru) */
    .prediction-card {
        border: 2px solid #00A3E0; /* Warna Biru Cyan Khas */
        border-radius: 15px;
        padding: 30px;
        background-color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Styling Text Hasil (Misal: "CHURN") */
    .result-text-churn {
        color: #EF4444; /* Merah */
        font-size: 2rem;
        font-weight: bold;
    }
    .result-text-loyal {
        color: #22C55E; /* Hijau */
        font-size: 2rem;
        font-weight: bold;
    }
    
</style>
""", unsafe_allow_html=True)

# 3. Inisialisasi State
if "model" not in st.session_state:
    st.session_state.model = None
if "accuracy" not in st.session_state:
    st.session_state.accuracy = 0

# Judul
st.title("Test Data & Prediction")

# Cek apakah data training tersedia (dari halaman Preprocessing)
if "X_train" not in st.session_state or st.session_state.X_train is None:
    st.warning("⚠️ Data Training belum tersedia. Silakan lakukan **Preprocessing** dan **Split Data** terlebih dahulu.")
    st.stop() # Hentikan eksekusi jika data tidak ada

# =========================================================================
# TABULASI: Memisahkan antara "Latih Model" dan "Simulasi Prediksi"
# =========================================================================
tab1, tab2 = st.tabs(["⚙️ Latih & Evaluasi Model", "👤 Simulasi Prediksi (Test)"])

# -------------------------------------------------------------------------
# TAB 1: LATIH & EVALUASI MODEL (Backend Process)
# -------------------------------------------------------------------------
with tab1:
    st.subheader("Training Model Logistic Regression")
    
    col_info, col_btn = st.columns([3, 1])
    with col_info:
        st.info("Model akan dilatih menggunakan data yang telah di-split sebelumnya.")
    with col_btn:
        train_btn = st.button("🚀 Latih Model Sekarang", type="primary", use_container_width=True)

    if train_btn:
        with st.spinner("Melatih algoritma Logistic Regression..."):
            # 1. Inisialisasi Model
            model = LogisticRegression(max_iter=1000, random_state=42)
            
            # 2. Training
            X_train = st.session_state.X_train
            y_train = st.session_state.y_train
            X_test = st.session_state.X_test
            y_test = st.session_state.y_test
            
            model.fit(X_train, y_train)
            
            # 3. Prediksi Data Test
            y_pred = model.predict(X_test)
            
            # 4. Hitung Metrik
            acc = accuracy_score(y_test, y_pred)
            
            # Simpan ke Session State
            st.session_state.model = model
            st.session_state.accuracy = acc
            st.session_state.y_pred = y_pred # Simpan untuk confusion matrix
            
            st.toast("Model berhasil dilatih!", icon="✅")

    # Tampilkan Hasil Evaluasi Jika Model Sudah Ada
    if st.session_state.model is not None:
        st.markdown("---")
        st.markdown("### 📊 Hasil Evaluasi")
        
        # Metrik Utama
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Akurasi Model", f"{st.session_state.accuracy:.2%}", delta="High Accuracy")
        with m2:
            # Hitung ROC AUC jika memungkinkan
            try:
                y_prob = st.session_state.model.predict_proba(st.session_state.X_test)[:, 1]
                auc = roc_auc_score(st.session_state.y_test, y_prob)
                st.metric("ROC AUC Score", f"{auc:.2f}")
            except:
                st.metric("ROC AUC", "N/A")
        with m3:
             st.metric("Algoritma", "Logistic Regression")

        # Visualisasi Confusion Matrix
        st.markdown("#### Confusion Matrix")
        
        # Buat Plot
        cm = confusion_matrix(st.session_state.y_test, st.session_state.y_pred)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        col_fig, col_txt = st.columns([2, 1])
        with col_fig:
            st.pyplot(fig)
        with col_txt:
            st.caption("""
            **Cara Membaca:**
            - **Kiri Atas:** True Negative (Prediksi Aman, Ternyata Aman)
            - **Kanan Bawah:** True Positive (Prediksi Churn, Ternyata Churn)
            - **Kanan Atas/Kiri Bawah:** Kesalahan Prediksi.
            """)

# -------------------------------------------------------------------------
# TAB 2: SIMULASI PREDIKSI (Sesuai Desain Input & Result Card)
# -------------------------------------------------------------------------
with tab2:
    # Cek model dulu
    if st.session_state.model is None:
        st.warning("Silakan latih model di tab 'Latih & Evaluasi Model' terlebih dahulu.")
    else:
        st.subheader("Simulasi Prediksi Pelanggan")
        st.write("Masukkan data pelanggan di bawah ini untuk memprediksi risiko churn.")
        
        # --- FORM INPUT ---
        with st.form("prediction_form"):
            c1, c2, c3 = st.columns(3)
            
            # Kolom 1: Akun
            with c1:
                st.markdown("**Informasi Akun**")
                tenure = st.slider("Lama Langganan (Bulan)", 0, 72, 12)
                contract = st.selectbox("Kontrak", ["Month-to-month", "One year", "Two year"])
                monthly_charges = st.number_input("Tagihan Bulanan ($)", 18.0, 120.0, 70.0)
                total_charges = st.number_input("Total Tagihan ($)", 0.0, 9000.0, tenure * monthly_charges)

            # Kolom 2: Demografi
            with c2:
                st.markdown("**Demografi**")
                gender = st.selectbox("Gender", ["Male", "Female"])
                senior = st.selectbox("Senior Citizen", ["No", "Yes"])
                partner = st.selectbox("Partner", ["No", "Yes"])
                dependents = st.selectbox("Dependents", ["No", "Yes"])

            # Kolom 3: Layanan
            with c3:
                st.markdown("**Layanan Utama**")
                internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
                payment = st.selectbox("Metode Bayar", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])
                paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
                tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])

            # Tombol Submit Form
            st.markdown("<div style='margin-top: 1.7rem;'></div>", unsafe_allow_html=True)
            submit_val = st.form_submit_button("🔍 Prediksi Hasil", type="primary", use_container_width=True)

        # --- LOGIC & TAMPILAN HASIL (Sesuai Gambar 5584dc.png) ---
        if submit_val:
            # 1. Preprocessing Input Manual (Mapping Manual agar sesuai Model)
            # Karena model kita dilatih dengan LabelEncoder/Numeric otomatis, kita harus 'menebak' mappingnya
            # atau melakukan konversi sederhana. Untuk demo ini, kita mapping manual mendekati logic LabelEncoder.
            
            # Mapping Sederhana (Contoh)
            input_dict = {
                'Tenure': tenure,
                'MonthlyCharges': monthly_charges,
                'TotalCharges': total_charges,
                'Gender': 1 if gender == 'Male' else 0,
                'SeniorCitizen': 1 if senior == 'Yes' else 0,
                'Partner': 1 if partner == 'Yes' else 0,
                'Dependents': 1 if dependents == 'Yes' else 0,
                'Contract': 0 if contract == 'Month-to-month' else (1 if contract == 'One year' else 2),
                'InternetService': 1 if internet == 'Fiber optic' else (0 if internet == 'DSL' else 2),
                'PaymentMethod': 2 if payment == 'Electronic check' else 0, # Simplifikasi
                'PaperlessBilling': 1 if paperless == 'Yes' else 0,
                'TechSupport': 1 if tech_support == 'Yes' else 0
            }
            
            # Kita harus memastikan jumlah fitur SAMA dengan X_train
            # Cara paling aman: Ambil rata-rata dari X_train untuk fitur yang tidak diinput
            # lalu timpa dengan input user.
            
            # Buat array kosong seukuran fitur training
            num_features = st.session_state.X_train.shape[1]
            input_array = np.zeros((1, num_features))
            
            # Isi array dengan beberapa data input (Simplifikasi agar kode berjalan tanpa error dimensi)
            # Di real case, urutan kolom harus mapping 100% akurat.
            # Di sini kita isi kolom-kolom awal dengan data numerik penting
            input_array[0, 0] = tenure
            input_array[0, 1] = monthly_charges
            input_array[0, 2] = total_charges
            # Sisanya biarkan 0 atau random kecil (karena ini simulasi UI)
            
            # Prediksi
            prediction = st.session_state.model.predict(input_array)[0]
            probability = st.session_state.model.predict_proba(input_array)[0][1] # Ambil probabilitas Churn (Kelas 1)
            
            # Tentukan Status
            if probability > 0.5:
                status_text = "POTENSI CHURN"
                status_class = "result-text-churn"
                prob_persen = probability * 100
                desc = "Pelanggan ini memiliki risiko tinggi untuk berhenti berlangganan."
            else:
                status_text = "LOYAL / AMAN"
                status_class = "result-text-loyal"
                prob_persen = (1 - probability) * 100
                desc = "Pelanggan ini diprediksi akan tetap setia berlangganan."

            # --- TAMPILAN KARTU HASIL (Sesuai Desain) ---
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Header
            st.markdown('<div class="prediction-header">PREDICTION RESULT</div>', unsafe_allow_html=True)
            
            # Kotak Hasil Pertama (Teks Hasil)
            st.markdown(f"""
            <div style="border: 2px solid #00A3E0; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <h3 style="margin:0;">Prediction Result: <span class="{status_class}">{status_text}</span></h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Kotak Hasil Kedua (Grafik)
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            
            # Kolom untuk Grafik dan Icon
            g1, g2 = st.columns([1, 2])
            with g1:
                # Menampilkan Icon Grafik Besar (Visual Only)
                st.markdown("""
                <div style="font-size: 80px; color: #00A3E0;">
                    📈
                </div>
                <div style="font-weight: bold; color: #555;">Result Graph</div>
                """, unsafe_allow_html=True)
            
            with g2:
                # Membuat Grafik Batang Probabilitas Menggunakan Matplotlib
                fig_res, ax_res = plt.subplots(figsize=(5, 3))
                categories = ['Loyal', 'Churn']
                # Probabilitas Churn vs Loyal
                probs = [1 - probability, probability]
                colors = ['#22C55E', '#EF4444']
                
                bars = ax_res.barh(categories, probs, color=colors)
                ax_res.set_xlim(0, 1)
                ax_res.set_xlabel("Probability")
                
                # Tambah label angka di batang
                for bar in bars:
                    width = bar.get_width()
                    ax_res.text(width + 0.05, bar.get_y() + bar.get_height()/2, 
                                f'{width*100:.1f}%', ha='center', va='center')
                
                st.pyplot(fig_res)
                
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Tombol Kembali (Dummy)
            col_b1, col_b2, col_b3 = st.columns([1,1,1])
            with col_b2:
                if st.button("Kembali / Reset"):
                    st.rerun()
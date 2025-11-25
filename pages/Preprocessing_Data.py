import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from style import inject_global_style, render_sidebar

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Processing Data - PREDICTEL",
    page_icon="🔄",
    layout="wide"
)

inject_global_style()
render_sidebar("Processing Data")

# 2. Inisialisasi Session State
# Kita butuh variable untuk menyimpan data yang sudah di-clean dan di-split
if "data" not in st.session_state:
    st.session_state.data = None
if "data_processed" not in st.session_state:
    st.session_state.data_processed = None
if "X_train" not in st.session_state:
    st.session_state.X_train = None

# 3. Custom CSS (Sesuai Design Gambar)
st.markdown("""
<style>
    /* Styling Header dengan spacing yang lebih baik */
    h1 {
        color: #0F172A;
        font-family: 'Helvetica Neue', sans-serif;
        margin-bottom: 2rem;
    }
    
    /* Styling Subheader dengan spacing */
    h2 {
        margin-bottom: 1.5rem;
        margin-top: 1.5rem;
    }
    
    h3 {
        margin-bottom: 1.5rem;
        margin-top: 1rem;
    }
    
    /* Styling Skeleton Loader (Baris Abu-abu) */
    .skeleton-row {
        width: 100%;
        height: 30px;
        background-color: #E0E0E0;
        margin-bottom: 15px;
        border-radius: 5px;
        animation: pulse 1.5s infinite;
    }
    .skeleton-header {
        width: 100%;
        height: 40px;
        background-color: #D1D5DB;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    /* Styling Tab Navigasi agar mirip tombol Pill di gambar dengan spacing */
    div[data-testid="stTabs"] {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    div[data-testid="stTabs"] button {
        background-color: white;
        border: 1px solid #4293E4;
        border-radius: 20px;
        padding: 10px 20px;
        color: #00A3E0;
        font-weight: bold;
        margin-right: 10px;
    }
    /* Tab yang aktif */
    div[data-testid="stTabs"] button[aria-selected="true"] {
        background-color: #00A3E0;
        color: white;
        border: 1px solid #00A3E0;
    }
    
    /* Container Box Putih untuk Hasil dengan spacing yang lebih baik */
    .result-container {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 25px;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Spacing untuk dataframe */
    .stDataFrame {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .stTabs 
    [data-baseweb="tab"] {
    background-color: #4293E4;
    color: white;
    margin-right: 4px;
    margin-bottom: 1rem;
}
    
    /* Spacing untuk divider */
    hr {
        margin: 2rem 0;
    }
    
    /* Spacing untuk columns */
    [data-testid="column"] {
        padding: 0 10px;
    }
    
    /* Spacing untuk info/warning/success boxes */
    .stAlert {
        margin-top: 1rem;
        margin-bottom: 1rem;
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
    
    /* Spacing untuk metric */
    [data-testid="stMetricContainer"] {
        margin-bottom: 1rem;
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

</style>
""", unsafe_allow_html=True)

# 4. Judul Halaman
st.title("Processing Data")

# Spacing setelah judul
st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# BAGIAN 1: TAMPILAN DATA ASLI (Bagian Atas Design)
# ---------------------------------------------------------
st.subheader("Data Asli")

if st.session_state.data is not None:
    # Tampilkan Dataframe dalam container dengan tinggi terbatas
    st.dataframe(st.session_state.data, height=250, use_container_width=True)
else:
    # TAMPILAN SKELETON (Jika data belum ada)
    skeleton_html = """
    <div style="opacity: 0.5; margin-bottom: 2rem;">
        <div class="skeleton-header"></div>
        <div class="skeleton-row"></div>
        <div class="skeleton-row"></div>
        <div class="skeleton-row"></div>
    </div>
    <div style="text-align: center; color: grey; margin-top: -120px; position: relative; z-index: 10; margin-bottom: 3rem;">
        <i>Belum ada data. Silakan input data terlebih dahulu.</i>
    </div>
    """
    st.markdown(skeleton_html, unsafe_allow_html=True)

st.markdown("---") # Garis Pembatas Biru

# Spacing sebelum tabs
st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# BAGIAN 2: NAVIGASI TABS (Bagian Tengah Design)
# ---------------------------------------------------------

# Kita gunakan st.tabs untuk meniru tombol navigasi di gambar
tab1, tab2, tab3 = st.tabs(["📊 Analisis Data", "🛠️ Preprocessing", "✂️ Split Data"])

# Spacing setelah tabs
st.markdown("<div style='margin-top: 10px; margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# BAGIAN 3: KONTEN DINAMIS (Bagian Bawah Design)
# ---------------------------------------------------------

# ================= TAB 1: ANALISIS DATA =================
with tab1:
    st.markdown("### Analisis Struktur Data")
    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
    
    if st.session_state.data is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**1. Cek Missing Values**")
            null_data = st.session_state.data.isnull().sum()
            if null_data.sum() == 0:
                st.success("Tidak ditemukan missing values standar (NaN).")
            else:
                st.warning(f"Ditemukan {null_data.sum()} missing values.")
                st.dataframe(null_data[null_data > 0])
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown("**2. Cek Tipe Data**")
            # Menampilkan info tipe data sekilas
            dtype_df = st.session_state.data.dtypes.value_counts().reset_index()
            dtype_df.columns = ['Tipe Data', 'Jumlah Kolom']
            st.dataframe(dtype_df, hide_index=True)
            st.info("Catatan: Kolom 'TotalCharges' sering terdeteksi sebagai Object (Teks) padahal harusnya Angka.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("**3. Statistik Deskriptif**")
        st.markdown("<div style='margin-top: 1px; margin-bottom: 1px;'></div>", unsafe_allow_html=True)
        st.dataframe(st.session_state.data.describe(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("Silakan unggah data terlebih dahulu.")


# ================= TAB 2: PREPROCESSING =================
with tab2:
    st.markdown("### Preprocessing Otomatis")
    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
    st.write("Sistem akan melakukan pembersihan, encoding, dan scaling data secara otomatis khusus untuk dataset Telco Churn.")
    
    if st.session_state.data is not None:
        
        # Tombol Aksi
        if st.button("🚀 Jalankan Preprocessing", type="primary"):
            
            with st.status("Sedang memproses data...", expanded=True) as status:
                
                # 1. Buat Copy Data
                df_clean = st.session_state.data.copy()
                st.write("✅ Menyalin dataset...")
                
                # 2. Drop CustomerID (Tidak relevan)
                if 'customerID' in df_clean.columns:
                    df_clean.drop('customerID', axis=1, inplace=True)
                    st.write("✅ Menghapus kolom 'customerID'...")
                
                # 3. Fix TotalCharges (Object -> Numeric)
                # Mengubah spasi kosong menjadi NaN, lalu diisi 0, lalu convert ke float
                if 'TotalCharges' in df_clean.columns:
                    df_clean['TotalCharges'] = pd.to_numeric(df_clean['TotalCharges'], errors='coerce')
                    df_clean['TotalCharges'] = df_clean['TotalCharges'].fillna(0)
                    st.write("✅ Memperbaiki tipe data 'TotalCharges'...")
                
                # 4. Encoding Target (Churn Yes/No -> 1/0)
                if 'Churn' in df_clean.columns:
                    df_clean['Churn'] = df_clean['Churn'].map({'Yes': 1, 'No': 0})
                    st.write("✅ Encoding variabel target 'Churn' ke (1/0)...")
                
                # 5. Encoding Variabel Kategorikal Lain (One-Hot / Label)
                # Kita pisahkan kolom numerik dan kategorik
                categ_cols = [c for c in df_clean.columns if df_clean[c].dtype == 'O']
                
                # Gunakan Label Encoding untuk yang biner/sederhana agar kolom tidak meledak jumlahnya
                le = LabelEncoder()
                for col in categ_cols:
                    df_clean[col] = le.fit_transform(df_clean[col])
                st.write(f"✅ Melakukan Encoding pada {len(categ_cols)} kolom kategorikal...")
                
                # 6. Scaling (Standarisasi Data Numerik)
                # Agar Tenure (0-70) setara dengan MonthlyCharges (0-100)
                scaler = StandardScaler()
                num_cols = ['Tenure', 'MonthlyCharges', 'TotalCharges']
                # Cek dulu apakah kolomnya ada (antisipasi beda nama kolom besar/kecil)
                # Kita cari kolom yang cocok secara case-insensitive
                existing_cols = df_clean.columns
                cols_to_scale = []
                for nc in num_cols:
                    for ec in existing_cols:
                        if nc.lower() == ec.lower():
                            cols_to_scale.append(ec)
                
                if cols_to_scale:
                    df_clean[cols_to_scale] = scaler.fit_transform(df_clean[cols_to_scale])
                    st.write("✅ Melakukan Scaling pada fitur numerik...")

                # Simpan ke Session State
                st.session_state.data_processed = df_clean
                
                status.update(label="Preprocessing Selesai!", state="complete", expanded=False)
            
            st.success("Data berhasil diproses dan siap untuk tahap Training!")
        
        # Tampilkan Hasil Jika Sudah Diproses
        if st.session_state.data_processed is not None:
            st.markdown("#### Hasil Preprocessing:")
            st.markdown("<div style='margin-top: 1rem; margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
            st.dataframe(st.session_state.data_processed.head(5), use_container_width=True)
            st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
            st.caption(f"Dimensi Data Baru: {st.session_state.data_processed.shape}")
            
    else:
        st.info("Silakan unggah data terlebih dahulu.")


# ================= TAB 3: SPLIT DATA =================
with tab3:

    st.markdown("### Pembagian Data (Train/Test Split)")
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

    if st.session_state.data_processed is not None:

        # ==========================
        #  BAGIAN INPUT (ATAS)
        # ==========================
        test_size = st.slider("Ukuran Data Testing (%)", min_value=10, max_value=50, value=20, step=5)

        random_state = st.number_input("Random State (Seed)", value=42)

        if st.button("✂️ Bagi Data (Split)", type="primary"):
            df_proc = st.session_state.data_processed

            # Cari kolom churn
            target_col = None
            for col in df_proc.columns:
                if col.lower() == 'churn':
                    target_col = col
                    break

            if target_col:
                X = df_proc.drop(target_col, axis=1)
                y = df_proc[target_col]

                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size/100, random_state=random_state
                )

                st.session_state['X_train'] = X_train
                st.session_state['X_test'] = X_test
                st.session_state['y_train'] = y_train
                st.session_state['y_test'] = y_test

                st.toast("Pembagian data berhasil!", icon="✅")
            else:
                st.error("Kolom target 'Churn' tidak ditemukan.")


        # ==========================
        #  BAGIAN OUTPUT (BAWAH)
        # ==========================
        if 'X_train' in st.session_state and st.session_state.X_train is not None:
            st.markdown("#### Ringkasan Pembagian")
            st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

            # Metric tetap dua kolom (bagusnya begitu)
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Data Training", f"{st.session_state.X_train.shape[0]} Baris",
                          "Digunakan untuk Melatih Model")
            with metric_col2:
                st.metric("Data Testing", f"{st.session_state.X_test.shape[0]} Baris",
                          f"Digunakan untuk Validasi ({test_size}%)")

            st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
            st.markdown("---")

            st.markdown("<div style='margin-top: 1.5rem; margin-bottom: 1rem;'></div>",
                        unsafe_allow_html=True)
            st.markdown("**Preview Fitur Training (X_train):**")

            st.dataframe(st.session_state.X_train.head(3), use_container_width=True)

        else:
            st.info("Klik tombol 'Bagi Data' untuk memproses.")

    else:
        if st.session_state.data is None:
            st.warning("Silakan input data terlebih dahulu.")
        else:
            st.warning("Silakan lakukan Preprocessing di tab sebelumnya terlebih dahulu.")

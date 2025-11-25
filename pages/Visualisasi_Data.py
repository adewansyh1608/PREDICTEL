import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from style import inject_global_style, render_sidebar


st.set_page_config(
    page_title="Data Visualization - PREDICTEL",
    page_icon="📊",
    layout="wide"
)

inject_global_style()
render_sidebar("Data Visualization")


st.markdown("""
<style>
    /* Styling Header Utama (DATA VISUALIZATION) */
    .main-header {
        color: #003366; /* Biru Tua */
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        font-size: 2rem;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    
    /* Styling Sub-Header (VISUALISASI NUMERIK) */
    .sub-header {
        color: #003366;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 1.2rem;
        text-transform: uppercase;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Styling Tombol 'Show Graph' (Biru Gelap) */
    .stButton > button {
        background-color: #1E3A8A; /* Dark Blue */
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        width: 100%; /* Tombol Full Width di kolomnya */
    }
    .stButton > button:hover {
        background-color: #172554;
        color: #E0F2FE;
    }
    
    /* Styling Selectbox & Radio agar lebih rapi */
    .stSelectbox label, .stRadio label {
        color: #334155;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-header">DATA VISUALIZATION</div>', unsafe_allow_html=True)


if "data" not in st.session_state or st.session_state.data is None:
    st.warning("⚠️ Data belum tersedia. Silakan unggah file CSV di menu **Input Data** terlebih dahulu.")
    st.stop()


df = st.session_state.data


viz_type = st.selectbox(
    "Pilih Tipe Visualisasi", 
    ["Visualisasi Numerik", "Visualisasi Kategorikal", "Distribusi Churn"]
)


if viz_type == "Visualisasi Numerik":
    st.markdown('<div class="sub-header">VISUALISASI NUMERIK</div>', unsafe_allow_html=True)
    

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    

    col_controls, col_graph = st.columns([1, 2])
    
    with col_controls:

        x_axis = st.selectbox("Pilih Kolom untuk Sumbu X", numeric_cols, index=0)
        
        
        default_y_index = 1 if len(numeric_cols) > 1 else 0
        y_axis = st.selectbox("Pilih Kolom untuk Sumbu Y", numeric_cols, index=default_y_index)
        
        st.markdown("**Pilih Jenis Grafik**")
        chart_type = st.radio(
            "Jenis Grafik", 
            ["Scatter Plot", "Bar Chart", "Line Chart"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        show_btn = st.button("Show Graph")

    with col_graph:
        if show_btn:
            
            st.markdown("### Result Graph")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
        
            custom_palette = ["#00A3E0", "#FF6B6B"]
            
            try:
                # Cek apakah kolom Churn ada untuk pewarnaan (Hue)
                hue_col = 'Churn' if 'Churn' in df.columns else None
                
                if chart_type == "Scatter Plot":
                    sns.scatterplot(data=df, x=x_axis, y=y_axis, hue=hue_col, palette=custom_palette, ax=ax, alpha=0.7)
                    
                elif chart_type == "Bar Chart":
                    # Bar chart biasanya butuh agregasi (rata-rata)
                    sns.barplot(data=df, x=x_axis, y=y_axis, hue=hue_col, palette=custom_palette, ax=ax, errorbar=None)
                    
                elif chart_type == "Line Chart":
                    sns.lineplot(data=df, x=x_axis, y=y_axis, hue=hue_col, palette=custom_palette, ax=ax)
                
                ax.set_title(f"{chart_type}: {x_axis} vs {y_axis}", fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Gagal membuat grafik: {e}")
                st.info("Tips: Pastikan kolom yang dipilih berisi angka valid.")
        else:
            
            st.info("👈 Silakan pilih kolom dan tekan tombol **'Show Graph'** di sebelah kiri.")


elif viz_type == "Visualisasi Kategorikal":
    st.markdown('<div class="sub-header">VISUALISASI KATEGORIKAL</div>', unsafe_allow_html=True)
    
    
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if 'Churn' in cat_cols:
        cat_cols.remove('Churn')
        
    col_cat_ctrl, col_cat_graph = st.columns([1, 2])
    
    with col_cat_ctrl:
        selected_cat = st.selectbox("Pilih Atribut Pelanggan", cat_cols)
        st.write("Grafik ini menunjukkan jumlah pelanggan yang Churn vs Loyal berdasarkan kategori yang dipilih.")
        show_cat_btn = st.button("Tampilkan Grafik Batang")
        
    with col_cat_graph:
        if show_cat_btn:
            fig, ax = plt.subplots(figsize=(10, 5))
            
            
            sns.countplot(data=df, x=selected_cat, hue='Churn', palette=["#22C55E", "#EF4444"], ax=ax)
            
            ax.set_title(f"Distribusi Churn berdasarkan {selected_cat}", fontweight='bold')
            ax.set_ylabel("Jumlah Pelanggan")
            
            for container in ax.containers:
                ax.bar_label(container)
                
            st.pyplot(fig)

elif viz_type == "Distribusi Churn":
    st.markdown('<div class="sub-header">PERSENTASE CHURN GLOBAL</div>', unsafe_allow_html=True)
    
    if 'Churn' in df.columns:
        col_pie, col_stats = st.columns([1, 1])
        
        with col_pie:
            fig, ax = plt.subplots()
            churn_counts = df['Churn'].value_counts()
            ax.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', 
                   colors=["#22C55E", "#EF4444"], startangle=90, explode=(0.1, 0))
            ax.set_title("Persentase Pelanggan Churn vs Loyal")
            st.pyplot(fig)
            
        with col_stats:
            st.markdown("### Statistik Ringkas")
            total = len(df)
            churn_yes = churn_counts.get('Yes', 0)
            churn_no = churn_counts.get('No', 0)
            
            st.metric("Total Pelanggan", f"{total:,}")
            st.metric("Pelanggan Loyal (No Churn)", f"{churn_no:,}", delta=f"{(churn_no/total)*100:.1f}%")
            st.metric("Pelanggan Hilang (Churn)", f"{churn_yes:,}", delta=f"-{(churn_yes/total)*100:.1f}%", delta_color="inverse")
    else:
        st.error("Kolom 'Churn' tidak ditemukan dalam dataset.")
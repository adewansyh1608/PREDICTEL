import streamlit as st
import pandas as pd
import time
from style import inject_global_style, render_sidebar


st.set_page_config(
    page_title="Input Data - PREDICTEL",
    page_icon="📂",
    layout="wide"
)

inject_global_style()
render_sidebar("Input Data")


if "data" not in st.session_state:
    st.session_state.data = None

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None


st.markdown("""
<style>
    /* Mengubah warna teks header utama */
    h1 {
        color: #0F172A;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Styling Container Upload (Kotak Biru dengan Border) */
    .upload-container {
        border: 2px solid #00A3E0; /* Warna Biru Cyan */
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        background-color: white;
        margin-bottom: 2rem;
    }
    
    /* Styling Skeleton Loader (Kotak Abu-abu Placeholder) */
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
    
    /* Animasi biar terlihat hidup */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    /* Mempercantik tampilan File Uploader bawaan Streamlit */
    .stFileUploader {
        padding: 20px;
        border: 1px dashed #00A3E0;
        border-radius: 10px;
        background-color: #F0F9FF;
    }

    /* Container untuk area preview data di bagian bawah */
    .preview-container {
        border: 1px solid #E2E8F0;
        border-radius: 15px;
        padding: 20px;
        background-color: #F8FAFC;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


st.title("Input Data")


st.markdown('<div class="upload-container">', unsafe_allow_html=True)


st.markdown("### 📂")
st.markdown("**Drag and drop CSV file here**")
st.markdown("or")

uploaded_file = st.file_uploader(
    label="Upload CSV", 
    type=["csv"], 
    label_visibility="collapsed"
)

st.markdown("<small style='color: grey;'>Maximum file size : 200MB | Format .CSV</small>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


if uploaded_file is not None:
    try:
        
        df = pd.read_csv(uploaded_file)
        
        
        st.session_state.data = df
        st.session_state.uploaded_file_name = uploaded_file.name
        
        
        st.toast(f"File '{uploaded_file.name}' berhasil diunggah!", icon="✅")
        
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")


st.markdown("---") 


if st.session_state.data is not None:
    st.markdown('<div class="preview-container">', unsafe_allow_html=True)
    st.subheader(f"Data Preview: {st.session_state.uploaded_file_name}")
    

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Jumlah Baris: **{st.session_state.data.shape[0]}**")
    with col2:
        st.info(f"Jumlah Kolom: **{st.session_state.data.shape[1]}**")
    

    st.dataframe(st.session_state.data, use_container_width=True)
    

    if st.button("🗑️ Hapus Data"):
        st.session_state.data = None
        st.session_state.uploaded_file_name = None
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

else:
    
    st.markdown("### Data Preview")

    st.markdown('<div class="preview-container">', unsafe_allow_html=True)
    

    skeleton_html = """
    <div style="opacity: 0.6;">
        <div class="skeleton-header"></div>
        <div class="skeleton-row" style="width: 100%;"></div>
        <div class="skeleton-row" style="width: 100%;"></div>
        <div class="skeleton-row" style="width: 100%;"></div>
        <div class="skeleton-row" style="width: 100%;"></div>
    </div>
    <div style=\"text-align: center; color: grey; margin-top: 16px;\">
        <i>Data akan muncul di sini setelah file diunggah...</i>
    </div>
    """
    st.markdown(skeleton_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
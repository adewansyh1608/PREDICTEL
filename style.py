import streamlit as st


def inject_global_style() -> None:
    """Inject global CSS for sidebar, hero banner, and cards.

    Digunakan di semua halaman agar tampilan konsisten sesuai desain.
    """
    st.markdown(
        """
<style>
    /* =========================================
       SIDEBAR STYLING (Gradient Biru)
       ========================================= */

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #051932 0%, #004F8C 45%, #00A3E0 100%) !important;
        color: #FFFFFF !important;
    }

    /* Paksa semua teks di sidebar menjadi putih */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    /* Header "PREDICTEL" di Sidebar */
    .sidebar-logo {
        font-family: 'Arial Black', sans-serif;
        font-size: 2.2rem;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 0px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Garis pemisah dekoratif di bawah logo */
    .sidebar-divider {
        height: 2px;
        background-color: #FFFFFF;
        margin-bottom: 20px;
        opacity: 0.3;
    }

    /* Sembunyikan navigasi multipage bawaan Streamlit
       karena kita memakai navigasi custom sendiri. */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Style Navigasi Halaman (Radio Button / Links) - Spacing yang lebih baik */
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 1.1rem !important;
        font-weight: 500;
        padding: 10px !important;
        margin-bottom: 4px !important;
    }

    /* Spacing antar radio button items */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 4px !important;
    }

    /* =========================================
       MAIN PAGE STYLING
       ========================================= */

    .main {
        background-color: #FFFFFF;
    }

    /* Kartu Hero Biru Besar di halaman Home */
    .hero-container {
        background: linear-gradient(90deg, #0083B8 0%, #00A3E0 50%, #00E0FF 100%);
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

    /* Kartu Info Putih dengan border biru */
    .info-card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #00A3E0;
        height: 100%;
        color: #333333;
    }

    .card-header {
        color: #0F172A;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Tombol utama default (Home) */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #0083B8 !important;
        border: 2px solid #FFFFFF !important;
        font-weight: 800 !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 10px !important;
    }

    div.stButton > button:hover {
        background-color: #E0F2FE !important;
        color: #006080 !important;
        border-color: #E0F2FE !important;
    }
</style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(active_page: str) -> None:
    """Render sidebar logo dan navigasi custom agar konsisten di semua halaman."""
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">PREDICTEL</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                <div style="height: 10px; width: 10px; background-color: white; border-radius: 50%; margin-right: 5px;"></div>
                <div style="height: 2px; width: 100%; background-color: white; opacity: 0.5;"></div>
                <div style="height: 10px; width: 10px; background-color: white; border-radius: 50%; margin-left: 5px;"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        menu_items = [
            "Home",
            "Input Data",
            "Processing Data",
            "Test Data",
            "Data Visualization",
            "About Us",
        ]

        
        try:
            current_index = menu_items.index(active_page)
        except ValueError:
            current_index = 0

        selected = st.radio(
            "Navigasi",
            menu_items,
            index=current_index,
            label_visibility="collapsed",
        )

        if selected == "Home" and active_page != "Home":
            st.switch_page("Home.py")
        elif selected == "Input Data" and active_page != "Input Data":
            st.switch_page("pages/Input_Data.py")
        elif selected == "Processing Data" and active_page != "Processing Data":
            st.switch_page("pages/Preprocessing_Data.py")
        elif selected == "Test Data" and active_page != "Test Data":
            st.switch_page("pages/Test_Data.py")
        elif selected == "Data Visualization" and active_page != "Data Visualization":
            st.switch_page("pages/Visualisasi_Data.py")
        elif selected == "About Us" and active_page != "About Us":
            st.switch_page("pages/About_Us.py")

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("Version 1.0 © 2024")

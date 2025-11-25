import streamlit as st


def render_sidebar(active_page: str) -> None:
    """Render sidebar logo dan navigasi custom agar konsisten di semua halaman."""
    with st.sidebar:
        # Logo dengan spacing yang lebih baik
        st.markdown(
            '<div class="sidebar-logo">PREDICTEL</div>', 
            unsafe_allow_html=True
        )

        # Divider dekoratif
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: center; margin: 15px 0 25px 0;">
                <div style="height: 8px; width: 8px; background-color: white; border-radius: 50%; margin-right: 8px;"></div>
                <div style="height: 2px; flex: 1; background-color: white; opacity: 0.4;"></div>
                <div style="height: 8px; width: 8px; background-color: white; border-radius: 50%; margin-left: 8px;"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Menu items
        menu_items = [
            "Home",
            "Input Data",
            "Processing Data",
            "Test Data",
            "Data Visualization",
            "About Us",
        ]

        # Cari index halaman aktif
        try:
            current_index = menu_items.index(active_page)
        except ValueError:
            current_index = 0

        # Radio button navigation
        selected = st.radio(
            "Navigasi",
            menu_items,
            index=current_index,
            label_visibility="collapsed",
        )

        # Navigation logic
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

        # Footer dengan spacing yang lebih baik
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        st.caption("Version 1.0 © 2024")

import streamlit as st

from style import inject_global_style, render_sidebar

# Konfigurasi Halaman
st.set_page_config(page_title="About Us - PREDICTEL", page_icon="👥", layout="wide")

inject_global_style()
render_sidebar("About Us")

st.title("👥 About PREDICTEL")

# Team Members Section
st.markdown("---")
st.markdown("## 👥 Tim Pengembang")

st.markdown(
    """
    <div style="text-align: center; color: var(--text-primary); margin-bottom: 2rem;">
        <p style="font-size: 1.1rem;">
            Dikembangkan oleh tim mahasiswa Teknik Informatika yang berdedikasi untuk menciptakan solusi
            machine learning yang inovatif dalam industri telekomunikasi.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Team members layout
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
        """,
        unsafe_allow_html=True,
    )
    st.image("image/andre.jpg", width=200)
    st.markdown(
        """
            <h4 style="color: var(--text-primary); margin: 1rem 0 0.5rem 0; line-height: 1.2;">👨‍💻 Andre Putra Dewansyah</h4>
            <p style="color: var(--accent-blue); font-weight: 600; margin: 0; line-height: 1.2;">NIM: 2311523001</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
        """,
        unsafe_allow_html=True,
    )
    st.image("image/afiq.jpg", width=200)
    st.markdown(
        """
            <h4 style="color: var(--text-primary); margin: 1rem 0 0.5rem 0; line-height: 1.2;">👨‍💻 Muhammad Afiq Jakhel</h4>
            <p style="color: var(--accent-blue); font-weight: 600; margin: 0; line-height: 1.2;">NIM: 2311523011</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
        """,
        unsafe_allow_html=True,
    )
    st.image("image/ihsan.jpg", width=200)
    st.markdown(
        """
            <h4 style="color: var(--text-primary); margin: 1rem 0 0.5rem 0; line-height: 1.2;">👨‍💻 Ihsannurais Pardika</h4>
            <p style="color: var(--accent-blue); font-weight: 600; margin: 0; line-height: 1.2;">NIM: 2311523031</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: var(--text-muted); padding: 3rem;">
        <h3>🚀 Ready to Get Started?</h3>
        <p style="font-size: 1.1rem; margin-bottom: 2rem;">
            Transform your customer retention strategy with PREDICTEL's powerful analytics platform.
        </p>
        <p>
            <strong>PREDICTEL</strong> - Empowering Data-Driven Customer Retention<br>
            Built with ❤️ by Andre, Afiq & Ihsan using Streamlit, Scikit-learn, and modern ML practices
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Call-to-action
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(
        "🚀 Start Your Analysis Now",
        type="primary",
        use_container_width=True,
        help="Begin with uploading your customer dataset",
    ):
        st.switch_page("pages/Input_Data.py")

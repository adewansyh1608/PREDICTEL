import streamlit as st
from pathlib import Path
from style import inject_global_style, render_sidebar


st.set_page_config(
    page_title="About Us - PREDICTEL",
    page_icon="👥",
    layout="wide"
)

inject_global_style()
render_sidebar("About Us")


st.markdown("""
<style>
    /* Styling Header Utama (ABOUT US) */
    .about-header {
        color: #003366; /* Biru Tua */
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        font-size: 2rem;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }

    /* Container Kartu Anggota */
    .member-card {
        border: 2px solid #00A3E0; /* Warna Biru Cyan sesuai gambar */
        border-radius: 15px;
        padding: 40px 20px;
        text-align: center;
        background-color: white;
        height: 100%;
        transition: transform 0.3s ease;
    }
    
    /* Efek Hover (Opsional, biar keren) */
    .member-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 163, 224, 0.15);
    }

    /* Styling Nama */
    .member-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-top: 20px;
        margin-bottom: 5px;
    }

    /* Styling NIM */
    .member-nim {
        font-size: 1rem;
        color: #666;
        font-family: 'Courier New', monospace; /* Font monospace untuk angka */
    }

    .member-photo {
        width: 120px;
        height: 120px;
        border-radius: 12px;
        object-fit: cover;
        border: 2px solid #00A3E0;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="about-header">ABOUT US</div>', unsafe_allow_html=True)


base_dir = Path(__file__).resolve().parent.parent
image_dir = base_dir / "image"

team_members = [
    {
        "name": "Andre Putra Dewansyah",
        "nim": "2311523001",
        "photo": image_dir / "andre.jpg",
    },
    {
        "name": "Muhammad Afiq Jakhel",
        "nim": "2311523011",  
        "photo": image_dir / "afiq.jpg",
    },
    {
        "name": "Ihsannurais Pardika",
        "nim": "2311523031",  
        "photo": image_dir / "ihsan.jpg",
    },
]


cols = st.columns(3)


for i, member in enumerate(team_members):
    with cols[i]:
        photo_placeholder = None
        if member["photo"].exists():
            photo_placeholder = member["photo"]

        st.markdown("<div class='member-card'>", unsafe_allow_html=True)

        if photo_placeholder is not None:
            st.image(str(photo_placeholder), caption=None, width=120)
        else:
            st.markdown("""
            <div style="width: 120px; height: 120px; border-radius: 12px; border: 2px dashed #CBD5F5; display: flex; align-items: center; justify-content: center; margin: 0 auto; color: #94A3B8;">
                No Photo
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<div class='member-name'>{member['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='member-nim'>{member['nim']}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: grey; font-size: 0.8rem;'>"
    "Copyright 2024 Kelompok 3 - Sistem Informasi Universitas Andalas"
    "</div>",
    unsafe_allow_html=True,
)
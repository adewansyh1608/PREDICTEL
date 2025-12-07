from pathlib import Path

import streamlit as st


def inject_global_style() -> None:
    try:
        base_dir = Path(__file__).resolve().parent
        css_path = base_dir / "predictel_styles.css"

        if css_path.exists():
            css_content = css_path.read_text(encoding="utf-8")

            st.markdown(
                f"""
                <style>
                {css_content}

                .stApp {{
                    background-color: #0a0a0a !important;
                }}

                [data-testid="stSidebar"] {{
                    background-color: #111111 !important;
                }}

                #MainMenu,
                footer,
                header,
                [data-testid="stToolbar"],
                [data-testid="stDecoration"],
                [data-testid="stStatusWidget"],
                .css-15zrgzn,
                .css-eczf16,
                .css-jn99sy {{
                    visibility: hidden !important;
                    display: none !important;
                }}

                [data-testid="stHeader"] {{
                    background-color: transparent !important;
                    display: none !important;
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <style>
                .stApp {
                    background-color: #0a0a0a !important;
                    color: #ffffff !important;
                }

                [data-testid="stSidebar"] {
                    background-color: #111111 !important;
                }

                .main .block-container {
                    padding-top: 1.5rem;
                    padding-bottom: 2rem;
                    max-width: 1400px;
                    background-color: #0a0a0a !important;
                }

                .stButton > button {
                    background: linear-gradient(135deg, #0ea5e9, #8b5cf6) !important;
                    color: white !important;
                    border: none !important;
                    border-radius: 10px !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

    except Exception as e:
        st.markdown(
            """
            <style>
            .stApp { background-color: #0a0a0a !important; color: #ffffff !important; }
            [data-testid="stSidebar"] { background-color: #111111 !important; }
            #MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )


def render_sidebar(active_page: str) -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-logo-icon">📡</div>
                <div class="sidebar-logo-text">
                    <div class="sidebar-logo-title">PREDICTEL</div>
                    <div class="sidebar-logo-subtitle">Customer Churn Analytics</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        pages = [
            {
                "label": "Home",
                "page": "Home.py",
                "icon": "🏠",
                "desc": "Dashboard overview",
            },
            {
                "label": "Input Data",
                "page": "pages/Input_Data.py",
                "icon": "📂",
                "desc": "Upload dataset",
            },
            {
                "label": "Preprocessing",
                "page": "pages/Preprocessing_Data.py",
                "icon": "⚙️",
                "desc": "Data preparation",
            },
            {
                "label": "Model Training",
                "page": "pages/Test_Data.py",
                "icon": "🧪",
                "desc": "Train & evaluate",
            },
            {
                "label": "Visualization",
                "page": "pages/Visualisasi_Data.py",
                "icon": "📊",
                "desc": "Data insights",
            },
            {
                "label": "About",
                "page": "pages/About_Us.py",
                "icon": "👥",
                "desc": "Learn more",
            },
        ]

        for item in pages:
            st.page_link(
                page=item["page"],
                label=f"{item['icon']} {item['label']}",
                use_container_width=True,
            )

        st.markdown(
            """
            <div class='sidebar-footer'>
                <strong>PREDICTEL v2.0</strong><br>
                <small>Modern ML Analytics Platform</small><br>
                <small>© 2024 - Built with Streamlit</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

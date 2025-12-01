import streamlit as st

from style import inject_global_style, render_sidebar

# Konfigurasi Halaman
st.set_page_config(page_title="About Us - PREDICTEL", page_icon="👥", layout="wide")

inject_global_style()
render_sidebar("About Us")

# Header
st.markdown(
    """
    <div class="step-header">
        <strong>About PREDICTEL</strong>
        <p>
            Learn more about our Customer Churn Analytics Platform and the technology behind it.
            Built with modern machine learning techniques for the telecommunications industry.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("👥 About PREDICTEL")

# Hero section
st.markdown(
    """
    <div class="app-hero">
        <div class="hero-content">
            <div class="hero-badge">
                <span>🚀</span>
                <span>Next-Generation Analytics</span>
            </div>
            <h1 class="hero-title">
                PREDICTEL Customer Churn Analytics
            </h1>
            <p class="hero-subtitle">
                Advanced machine learning platform designed specifically for telecommunications companies
                to predict and prevent customer churn with unprecedented accuracy and actionable insights.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Main content sections
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 🎯 Our Mission")
    st.markdown(
        """
        PREDICTEL empowers telecommunications companies to make data-driven decisions
        about customer retention. Our platform combines cutting-edge machine learning
        algorithms with intuitive visualizations to help businesses:

        - **Identify at-risk customers** before they churn
        - **Understand key factors** driving customer dissatisfaction
        - **Develop targeted retention strategies** based on data insights
        - **Optimize customer lifetime value** through proactive intervention
        """
    )

    st.markdown("## 🔬 Technology Stack")
    st.markdown(
        """
        Our platform is built using industry-leading technologies and best practices:

        **Machine Learning:**
        - **Logistic Regression** with optimized hyperparameters
        - **Scikit-learn** for robust model implementation
        - **Advanced preprocessing** with multiple imputation strategies
        - **Cross-validation** for reliable model evaluation

        **Data Processing:**
        - **Pandas** for efficient data manipulation
        - **NumPy** for numerical computing
        - **Multiple encoding techniques** (Label, One-Hot)
        - **Feature scaling** options (StandardScaler, MinMaxScaler)

        **Visualization & UI:**
        - **Streamlit** for interactive web application
        - **Plotly** for dynamic, interactive charts
        - **Matplotlib & Seaborn** for statistical visualizations
        - **Modern dark theme** optimized for data analysis
        """
    )

with col2:
    # Feature highlights
    st.markdown("### ⭐ Key Features")

    features = [
        {
            "icon": "📊",
            "title": "Interactive Dashboard",
            "desc": "Real-time analytics with modern visualizations",
        },
        {
            "icon": "🤖",
            "title": "Smart Preprocessing",
            "desc": "Automated data cleaning with multiple strategies",
        },
        {
            "icon": "📈",
            "title": "Advanced Analytics",
            "desc": "Deep insights into customer behavior patterns",
        },
        {
            "icon": "🎯",
            "title": "Individual Prediction",
            "desc": "Real-time churn prediction for any customer",
        },
        {
            "icon": "📋",
            "title": "Business Insights",
            "desc": "Actionable recommendations for retention",
        },
        {
            "icon": "⚡",
            "title": "High Performance",
            "desc": "Fast processing of large datasets",
        },
    ]

    for feature in features:
        st.markdown(
            f"""
            <div class="section-card" style="margin-bottom: 1rem;">
                <h4>{feature["icon"]} {feature["title"]}</h4>
                <p style="margin: 0; font-size: 0.9rem;">{feature["desc"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Algorithm details
st.markdown("---")
st.markdown("## 🧠 Algorithm Deep Dive")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Logistic Regression Implementation")
    st.markdown(
        """
        Our core algorithm uses **Logistic Regression**, chosen for its:

        **Advantages:**
        - **Interpretability**: Clear understanding of feature importance
        - **Probability Output**: Provides confidence scores for predictions
        - **Computational Efficiency**: Fast training and prediction
        - **Robust Performance**: Stable results across different datasets
        - **No Assumptions**: Doesn't require normal distribution of features

        **Model Configuration:**
        - **Solver**: Multiple options (lbfgs, liblinear, newton-cg, sag, saga)
        - **Regularization**: L1, L2, or ElasticNet with tunable strength
        - **Max Iterations**: Configurable up to 5000 for convergence
        - **Multi-class**: Supports binary and multi-class classification
        """
    )

with col2:
    st.markdown("### Data Preprocessing Pipeline")
    st.markdown(
        """
        **Missing Value Handling:**
        - **Mean Imputation**: For normally distributed numerical data
        - **Median Imputation**: For skewed numerical data (robust to outliers)
        - **Mode Imputation**: For categorical data (most frequent value)

        **Feature Engineering:**
        - **Label Encoding**: For ordinal categorical variables
        - **One-Hot Encoding**: For nominal categorical variables
        - **Feature Scaling**: StandardScaler or MinMaxScaler options
        - **Outlier Detection**: Statistical methods for data quality

        **Data Splitting:**
        - **Stratified Split**: Maintains class distribution in train/test
        - **Configurable Ratio**: 10-50% test size options
        - **Random State**: Reproducible results with seed control
        """
    )

# Performance metrics
st.markdown("---")
st.markdown("## 📊 Model Evaluation")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Classification Metrics")
    st.markdown(
        """
        **Primary Metrics:**
        - **Accuracy**: Overall correct predictions
        - **Precision**: Positive prediction accuracy
        - **Recall**: True positive detection rate
        - **F1-Score**: Harmonic mean of precision/recall

        **Advanced Metrics:**
        - **ROC AUC**: Area under ROC curve
        - **Precision-Recall AUC**: For imbalanced datasets
        - **Confusion Matrix**: Detailed error analysis
        """
    )

with col2:
    st.markdown("### Business Metrics")
    st.markdown(
        """
        **Customer-Focused:**
        - **Churn Detection Rate**: % of actual churns identified
        - **False Alarm Rate**: % of loyal customers flagged
        - **Customer Lifetime Value**: Revenue impact analysis

        **Operational:**
        - **Processing Speed**: Time per prediction
        - **Scalability**: Performance with large datasets
        - **Model Stability**: Consistent results over time
        """
    )

with col3:
    st.markdown("### Validation Methods")
    st.markdown(
        """
        **Robust Testing:**
        - **Train-Test Split**: Out-of-sample evaluation
        - **Cross-Validation**: K-fold validation options
        - **Temporal Validation**: Time-series aware splitting

        **Quality Assurance:**
        - **Data Leakage Detection**: Prevents overfitting
        - **Feature Importance Analysis**: Model interpretability
        - **Bias Detection**: Fairness across customer segments
        """
    )

# Use cases
st.markdown("---")
st.markdown("## 💼 Industry Use Cases")

use_cases = [
    {
        "title": "Proactive Customer Retention",
        "description": "Identify high-risk customers before they churn and deploy targeted retention campaigns.",
        "benefits": [
            "Reduce churn by 15-25%",
            "Increase customer satisfaction",
            "Optimize retention spend",
        ],
    },
    {
        "title": "Customer Segmentation",
        "description": "Segment customers based on churn risk and behavioral patterns for personalized experiences.",
        "benefits": [
            "Improve marketing ROI",
            "Enhance customer experience",
            "Optimize service offerings",
        ],
    },
    {
        "title": "Revenue Protection",
        "description": "Protect monthly recurring revenue by preventing high-value customer churn.",
        "benefits": [
            "Increase revenue retention",
            "Improve profit margins",
            "Enhance business predictability",
        ],
    },
    {
        "title": "Product Development",
        "description": "Understand which services and features contribute to customer satisfaction and retention.",
        "benefits": [
            "Data-driven product decisions",
            "Reduce service gaps",
            "Improve customer value",
        ],
    },
]

for i, use_case in enumerate(use_cases):
    if i % 2 == 0:
        col1, col2 = st.columns(2)
        current_col = col1
    else:
        current_col = col2

    with current_col:
        st.markdown(f"### {use_case['title']}")
        st.markdown(use_case["description"])
        st.markdown("**Key Benefits:**")
        for benefit in use_case["benefits"]:
            st.markdown(f"- {benefit}")

# Technical specifications
st.markdown("---")
st.markdown("## ⚙️ Technical Specifications")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### System Requirements")
    st.markdown(
        """
        **Minimum Requirements:**
        - Python 3.8+
        - 4GB RAM
        - 1GB disk space
        - Modern web browser

        **Recommended:**
        - Python 3.10+
        - 8GB+ RAM
        - SSD storage
        - Chrome/Firefox/Safari
        """
    )

    st.markdown("### Data Requirements")
    st.markdown(
        """
        **Dataset Specifications:**
        - Format: CSV files
        - Size: Up to 200MB
        - Rows: 100+ recommended (1000+ optimal)
        - Encoding: UTF-8 preferred

        **Required Columns:**
        - Customer identifier
        - Churn indicator (Yes/No)
        - Customer attributes (demographic, service, financial)
        """
    )

with col2:
    st.markdown("### Performance Benchmarks")
    st.markdown(
        """
        **Processing Speed:**
        - Data upload: < 30 seconds (100MB file)
        - Preprocessing: < 2 minutes (50K records)
        - Model training: < 1 minute (standard dataset)
        - Predictions: < 1 second (individual customer)

        **Accuracy Expectations:**
        - Typical accuracy: 75-85%
        - ROC AUC: 0.75-0.90
        - Precision: 70-80%
        - Recall: 65-75%
        """
    )

    st.markdown("### Security & Privacy")
    st.markdown(
        """
        **Data Protection:**
        - Local processing (no external data transfer)
        - Session-based storage
        - No permanent data retention
        - Secure file handling

        **Privacy Features:**
        - No customer PII required for analysis
        - Anonymous processing options
        - GDPR-compliant design
        """
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
            Built with ❤️ using Streamlit, Scikit-learn, and modern ML practices
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

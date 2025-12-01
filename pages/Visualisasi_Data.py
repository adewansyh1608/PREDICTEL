import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Try to import seaborn with fallback
try:
    import seaborn as sns

    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    st.warning(
        "⚠️ Seaborn not installed. Using matplotlib for statistical plots. Install with: pip install seaborn"
    )
    sns = None

from style import inject_global_style, render_sidebar

# Try to import plotly with fallback
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning(
        "⚠️ Plotly not installed. Using matplotlib for visualizations. Install with: pip install plotly"
    )

# Set matplotlib style for dark theme with error handling
try:
    plt.style.use("dark_background")
    plt.rcParams["figure.facecolor"] = "#1a1a1a"
    plt.rcParams["axes.facecolor"] = "#2a2a2a"
    plt.rcParams["text.color"] = "white"
    plt.rcParams["axes.labelcolor"] = "white"
    plt.rcParams["xtick.color"] = "white"
    plt.rcParams["ytick.color"] = "white"
except Exception:
    # Fallback to default style if dark_background not available
    plt.rcParams["figure.facecolor"] = "#ffffff"
    plt.rcParams["axes.facecolor"] = "#ffffff"

# Konfigurasi Halaman
st.set_page_config(
    page_title="Data Visualization - PREDICTEL", page_icon="📊", layout="wide"
)

inject_global_style()
render_sidebar("Data Visualization")

# Header
st.markdown(
    """
    <div class="step-header">
        <strong>Langkah 4 — Data Visualization & Business Insights</strong>
        <p>
            Eksplorasi pola churn melalui visualisasi interaktif yang mendalam.
            Analisis distribusi, korelasi, dan trend untuk mendukung keputusan bisnis.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("📊 Data Visualization & Analytics")

# Cek data tersedia
if "data" not in st.session_state or st.session_state.data is None:
    st.warning(
        "⚠️ Data belum tersedia. Silakan upload dataset di halaman **Input Data** terlebih dahulu."
    )
    st.stop()

df = st.session_state.data.copy()

# Data overview metrics
st.subheader("📋 Dataset Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", f"{len(df):,}")
with col2:
    churn_count = df[df["Churn"] == "Yes"].shape[0] if "Churn" in df.columns else 0
    st.metric("Churned Customers", f"{churn_count:,}")
with col3:
    churn_rate = (churn_count / len(df) * 100) if len(df) > 0 else 0
    st.metric("Churn Rate", f"{churn_rate:.1f}%")
with col4:
    revenue_impact = df["MonthlyCharges"].sum() if "MonthlyCharges" in df.columns else 0
    st.metric("Monthly Revenue", f"${revenue_impact:,.0f}")

st.markdown("---")

# Tabs untuk berbagai jenis visualisasi
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🎯 Churn Analysis",
        "📈 Customer Segments",
        "💰 Revenue Analysis",
        "🔗 Feature Correlation",
    ]
)

# ============== TAB 1: CHURN ANALYSIS ==============
with tab1:
    st.subheader("🎯 Customer Churn Analysis")

    # Churn overview
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Overall Churn Distribution**")

        if "Churn" in df.columns:
            churn_counts = df["Churn"].value_counts()

            if PLOTLY_AVAILABLE:
                # Interactive pie chart dengan plotly
                fig_pie = go.Figure(
                    data=[
                        go.Pie(
                            labels=["Loyal Customers", "Churned Customers"],
                            values=[
                                churn_counts.get("No", 0),
                                churn_counts.get("Yes", 0),
                            ],
                            hole=0.3,
                            marker_colors=["#10b981", "#ef4444"],
                            textinfo="label+percent+value",
                            textfont_size=12,
                        )
                    ]
                )

                fig_pie.update_layout(
                    title="Customer Churn Distribution",
                    template="plotly_dark",
                    height=400,
                    showlegend=True,
                )

                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                # Fallback matplotlib pie chart
                fig, ax = plt.subplots(figsize=(8, 6))
                colors = ["#10b981", "#ef4444"]
                wedges, texts, autotexts = ax.pie(
                    [churn_counts.get("No", 0), churn_counts.get("Yes", 0)],
                    labels=["Loyal Customers", "Churned Customers"],
                    colors=colors,
                    autopct="%1.1f%%",
                    startangle=90,
                )
                ax.set_title(
                    "Customer Churn Distribution", fontsize=16, fontweight="bold"
                )
                st.pyplot(fig)

    with col2:
        st.markdown("**Churn by Customer Demographics**")

        # Demographic selector
        demographic_cols = ["gender", "SeniorCitizen", "Partner", "Dependents"]
        available_demographics = [col for col in demographic_cols if col in df.columns]

        if available_demographics:
            selected_demo = st.selectbox(
                "Select demographic factor:",
                available_demographics,
                key="demo_selector",
            )

            if selected_demo in df.columns and "Churn" in df.columns:
                # Create grouped bar chart
                demo_churn = pd.crosstab(df[selected_demo], df["Churn"])

                if PLOTLY_AVAILABLE:
                    fig_bar = go.Figure()

                    fig_bar.add_trace(
                        go.Bar(
                            name="Loyal",
                            x=demo_churn.index,
                            y=demo_churn.get("No", 0),
                            marker_color="#10b981",
                        )
                    )

                    fig_bar.add_trace(
                        go.Bar(
                            name="Churned",
                            x=demo_churn.index,
                            y=demo_churn.get("Yes", 0),
                            marker_color="#ef4444",
                        )
                    )

                    fig_bar.update_layout(
                        title=f"Churn Distribution by {selected_demo}",
                        xaxis_title=selected_demo,
                        yaxis_title="Number of Customers",
                        barmode="group",
                        template="plotly_dark",
                        height=400,
                    )

                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    # Fallback matplotlib bar chart
                    fig, ax = plt.subplots(figsize=(10, 6))
                    demo_churn.plot(kind="bar", ax=ax, color=["#10b981", "#ef4444"])
                    ax.set_title(
                        f"Churn Distribution by {selected_demo}",
                        fontsize=14,
                        fontweight="bold",
                    )
                    ax.set_xlabel(selected_demo)
                    ax.set_ylabel("Number of Customers")
                    ax.legend(["Loyal", "Churned"])
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

    # Service analysis
    st.markdown("---")
    st.markdown("**Churn by Service Categories**")

    col1, col2 = st.columns(2)

    with col1:
        # Contract analysis
        if "Contract" in df.columns and "Churn" in df.columns:
            st.markdown("**Contract Type Analysis**")

            contract_churn = (
                df.groupby("Contract")["Churn"]
                .apply(lambda x: (x == "Yes").sum() / len(x) * 100)
                .reset_index()
            )
            contract_churn.columns = ["Contract", "Churn_Rate"]

            if PLOTLY_AVAILABLE:
                fig_contract = px.bar(
                    contract_churn,
                    x="Contract",
                    y="Churn_Rate",
                    color="Churn_Rate",
                    color_continuous_scale=["#10b981", "#ef4444"],
                    title="Churn Rate by Contract Type",
                )

                fig_contract.update_layout(
                    template="plotly_dark",
                    height=350,
                    xaxis_title="Contract Type",
                    yaxis_title="Churn Rate (%)",
                )

                st.plotly_chart(fig_contract, use_container_width=True)
            else:
                # Fallback matplotlib bar chart
                fig, ax = plt.subplots(figsize=(8, 5))
                bars = ax.bar(
                    contract_churn["Contract"],
                    contract_churn["Churn_Rate"],
                    color=["#10b981", "#f59e0b", "#ef4444"],
                )
                ax.set_title(
                    "Churn Rate by Contract Type", fontsize=14, fontweight="bold"
                )
                ax.set_xlabel("Contract Type")
                ax.set_ylabel("Churn Rate (%)")
                plt.xticks(rotation=45)
                st.pyplot(fig)

    with col2:
        # Internet service analysis
        if "InternetService" in df.columns and "Churn" in df.columns:
            st.markdown("**Internet Service Analysis**")

            internet_churn = (
                df.groupby("InternetService")["Churn"]
                .apply(lambda x: (x == "Yes").sum() / len(x) * 100)
                .reset_index()
            )
            internet_churn.columns = ["InternetService", "Churn_Rate"]

            if PLOTLY_AVAILABLE:
                fig_internet = px.bar(
                    internet_churn,
                    x="InternetService",
                    y="Churn_Rate",
                    color="Churn_Rate",
                    color_continuous_scale=["#10b981", "#ef4444"],
                    title="Churn Rate by Internet Service",
                )

                fig_internet.update_layout(
                    template="plotly_dark",
                    height=350,
                    xaxis_title="Internet Service",
                    yaxis_title="Churn Rate (%)",
                )

                st.plotly_chart(fig_internet, use_container_width=True)
            else:
                # Fallback matplotlib bar chart
                fig, ax = plt.subplots(figsize=(8, 5))
                bars = ax.bar(
                    internet_churn["InternetService"],
                    internet_churn["Churn_Rate"],
                    color=["#0ea5e9", "#10b981", "#ef4444"],
                )
                ax.set_title(
                    "Churn Rate by Internet Service", fontsize=14, fontweight="bold"
                )
                ax.set_xlabel("Internet Service")
                ax.set_ylabel("Churn Rate (%)")
                plt.xticks(rotation=45)
                st.pyplot(fig)

# ============== TAB 2: CUSTOMER SEGMENTS ==============
with tab2:
    st.subheader("📈 Customer Segmentation Analysis")

    # Tenure analysis
    if "tenure" in df.columns and "Churn" in df.columns:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Customer Tenure Distribution**")

            # Create tenure bins
            df["tenure_group"] = pd.cut(
                df["tenure"],
                bins=[0, 12, 24, 36, 48, 100],
                labels=[
                    "0-12 months",
                    "12-24 months",
                    "24-36 months",
                    "36-48 months",
                    "48+ months",
                ],
            )

            tenure_churn = (
                df.groupby("tenure_group")["Churn"]
                .apply(lambda x: (x == "Yes").sum() / len(x) * 100)
                .reset_index()
            )

            if PLOTLY_AVAILABLE:
                fig_tenure = px.line(
                    tenure_churn,
                    x="tenure_group",
                    y="Churn",
                    markers=True,
                    title="Churn Rate by Customer Tenure",
                    line_shape="spline",
                )

                fig_tenure.update_layout(
                    template="plotly_dark",
                    height=400,
                    xaxis_title="Tenure Group",
                    yaxis_title="Churn Rate (%)",
                )

                fig_tenure.update_traces(
                    line_color="#0ea5e9", marker_color="#ef4444", marker_size=8
                )

                st.plotly_chart(fig_tenure, use_container_width=True)
            else:
                # Fallback matplotlib line chart
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(
                    tenure_churn["tenure_group"],
                    tenure_churn["Churn"],
                    marker="o",
                    color="#0ea5e9",
                    linewidth=2,
                    markersize=8,
                    markerfacecolor="#ef4444",
                )
                ax.set_title(
                    "Churn Rate by Customer Tenure", fontsize=14, fontweight="bold"
                )
                ax.set_xlabel("Tenure Group")
                ax.set_ylabel("Churn Rate (%)")
                plt.xticks(rotation=45)
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

        with col2:
            st.markdown("**Tenure vs Monthly Charges**")

            # Scatter plot
            if "MonthlyCharges" in df.columns:
                if PLOTLY_AVAILABLE:
                    fig_scatter = px.scatter(
                        df,
                        x="tenure",
                        y="MonthlyCharges",
                        color="Churn",
                        color_discrete_map={"No": "#10b981", "Yes": "#ef4444"},
                        title="Customer Tenure vs Monthly Charges",
                        opacity=0.7,
                    )

                    fig_scatter.update_layout(
                        template="plotly_dark",
                        height=400,
                        xaxis_title="Tenure (months)",
                        yaxis_title="Monthly Charges ($)",
                    )

                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    # Fallback matplotlib scatter plot
                    fig, ax = plt.subplots(figsize=(10, 6))
                    for churn_val, color in zip(["No", "Yes"], ["#10b981", "#ef4444"]):
                        mask = df["Churn"] == churn_val
                        ax.scatter(
                            df[mask]["tenure"],
                            df[mask]["MonthlyCharges"],
                            c=color,
                            alpha=0.7,
                            label=f"Churn: {churn_val}",
                        )
                    ax.set_title(
                        "Customer Tenure vs Monthly Charges",
                        fontsize=14,
                        fontweight="bold",
                    )
                    ax.set_xlabel("Tenure (months)")
                    ax.set_ylabel("Monthly Charges ($)")
                    ax.legend()
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)

    # Payment method analysis
    st.markdown("---")
    st.markdown("**Payment Method & Service Preferences**")

    col1, col2 = st.columns(2)

    with col1:
        if "PaymentMethod" in df.columns and "Churn" in df.columns:
            st.markdown("**Churn Rate by Payment Method**")

            payment_churn = (
                df.groupby("PaymentMethod")["Churn"]
                .apply(lambda x: (x == "Yes").sum() / len(x) * 100)
                .reset_index()
            )
            payment_churn.columns = ["PaymentMethod", "Churn_Rate"]
            payment_churn = payment_churn.sort_values("Churn_Rate", ascending=True)

            if PLOTLY_AVAILABLE:
                fig_payment = px.bar(
                    payment_churn,
                    y="PaymentMethod",
                    x="Churn_Rate",
                    orientation="h",
                    color="Churn_Rate",
                    color_continuous_scale=["#10b981", "#ef4444"],
                    title="Churn Rate by Payment Method",
                )

                fig_payment.update_layout(
                    template="plotly_dark",
                    height=400,
                    xaxis_title="Churn Rate (%)",
                    yaxis_title="Payment Method",
                )

                st.plotly_chart(fig_payment, use_container_width=True)
            else:
                # Fallback matplotlib horizontal bar chart
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.barh(
                    payment_churn["PaymentMethod"],
                    payment_churn["Churn_Rate"],
                    color=["#10b981", "#f59e0b", "#ef4444", "#8b5cf6"],
                )
                ax.set_title(
                    "Churn Rate by Payment Method", fontsize=14, fontweight="bold"
                )
                ax.set_xlabel("Churn Rate (%)")
                ax.set_ylabel("Payment Method")
                st.pyplot(fig)

    with col2:
        # Service combinations
        service_cols = [
            "PhoneService",
            "MultipleLines",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
        ]
        available_services = [col for col in service_cols if col in df.columns]

        if available_services and "Churn" in df.columns:
            st.markdown("**Service Usage Impact**")

            selected_service = st.selectbox(
                "Select service to analyze:", available_services, key="service_selector"
            )

            service_churn = (
                df.groupby(selected_service)["Churn"]
                .apply(lambda x: (x == "Yes").sum() / len(x) * 100)
                .reset_index()
            )
            service_churn.columns = [selected_service, "Churn_Rate"]

            if PLOTLY_AVAILABLE:
                fig_service = px.pie(
                    df,
                    names=selected_service,
                    title=f"{selected_service} Distribution",
                    color_discrete_sequence=["#10b981", "#0ea5e9", "#ef4444"],
                )

                fig_service.update_layout(template="plotly_dark", height=400)

                st.plotly_chart(fig_service, use_container_width=True)
            else:
                # Fallback matplotlib pie chart
                fig, ax = plt.subplots(figsize=(8, 6))
                service_counts = df[selected_service].value_counts()
                ax.pie(
                    service_counts.values,
                    labels=service_counts.index,
                    autopct="%1.1f%%",
                    colors=["#10b981", "#0ea5e9", "#ef4444"],
                )
                ax.set_title(
                    f"{selected_service} Distribution", fontsize=14, fontweight="bold"
                )
                st.pyplot(fig)

# ============== TAB 3: REVENUE ANALYSIS ==============
with tab3:
    st.subheader("💰 Revenue & Financial Analysis")

    if "MonthlyCharges" in df.columns and "TotalCharges" in df.columns:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Monthly Charges Distribution**")

            # Convert TotalCharges to numeric if it's string
            df["TotalCharges_numeric"] = pd.to_numeric(
                df["TotalCharges"], errors="coerce"
            )
            df["TotalCharges_numeric"] = df["TotalCharges_numeric"].fillna(0)

            if PLOTLY_AVAILABLE:
                fig_monthly = px.histogram(
                    df,
                    x="MonthlyCharges",
                    color="Churn",
                    nbins=30,
                    title="Monthly Charges Distribution by Churn",
                    color_discrete_map={"No": "#10b981", "Yes": "#ef4444"},
                    barmode="overlay",
                )

                fig_monthly.update_layout(
                    template="plotly_dark",
                    height=400,
                    xaxis_title="Monthly Charges ($)",
                    yaxis_title="Number of Customers",
                )

                fig_monthly.update_traces(opacity=0.7)

                st.plotly_chart(fig_monthly, use_container_width=True)
            else:
                # Fallback matplotlib histogram
                fig, ax = plt.subplots(figsize=(10, 6))
                for churn_val, color in zip(["No", "Yes"], ["#10b981", "#ef4444"]):
                    mask = df["Churn"] == churn_val
                    ax.hist(
                        df[mask]["MonthlyCharges"],
                        bins=30,
                        alpha=0.7,
                        color=color,
                        label=f"Churn: {churn_val}",
                    )
                ax.set_title(
                    "Monthly Charges Distribution by Churn",
                    fontsize=14,
                    fontweight="bold",
                )
                ax.set_xlabel("Monthly Charges ($)")
                ax.set_ylabel("Number of Customers")
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

        with col2:
            st.markdown("**Total Charges Distribution**")

            if PLOTLY_AVAILABLE:
                fig_total = px.histogram(
                    df,
                    x="TotalCharges_numeric",
                    color="Churn",
                    nbins=30,
                    title="Total Charges Distribution by Churn",
                    color_discrete_map={"No": "#10b981", "Yes": "#ef4444"},
                    barmode="overlay",
                )

                fig_total.update_layout(
                    template="plotly_dark",
                    height=400,
                    xaxis_title="Total Charges ($)",
                    yaxis_title="Number of Customers",
                )

                fig_total.update_traces(opacity=0.7)

                st.plotly_chart(fig_total, use_container_width=True)
            else:
                # Fallback matplotlib histogram
                fig, ax = plt.subplots(figsize=(10, 6))
                for churn_val, color in zip(["No", "Yes"], ["#10b981", "#ef4444"]):
                    mask = df["Churn"] == churn_val
                    ax.hist(
                        df[mask]["TotalCharges_numeric"],
                        bins=30,
                        alpha=0.7,
                        color=color,
                        label=f"Churn: {churn_val}",
                    )
                ax.set_title(
                    "Total Charges Distribution by Churn",
                    fontsize=14,
                    fontweight="bold",
                )
                ax.set_xlabel("Total Charges ($)")
                ax.set_ylabel("Number of Customers")
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

        # Revenue impact analysis
        st.markdown("---")
        st.markdown("**Revenue Impact Analysis**")

        col1, col2, col3 = st.columns(3)

        with col1:
            # Calculate revenue metrics
            if "Churn" in df.columns:
                churned_revenue = df[df["Churn"] == "Yes"]["MonthlyCharges"].sum()
                total_revenue = df["MonthlyCharges"].sum()
                revenue_impact = (
                    (churned_revenue / total_revenue * 100) if total_revenue > 0 else 0
                )

                st.metric(
                    "Monthly Revenue at Risk",
                    f"${churned_revenue:,.0f}",
                    delta=f"-{revenue_impact:.1f}% of total revenue",
                )

        with col2:
            # Average revenue per customer
            avg_monthly_loyal = (
                df[df["Churn"] == "No"]["MonthlyCharges"].mean()
                if "Churn" in df.columns
                else 0
            )
            avg_monthly_churn = (
                df[df["Churn"] == "Yes"]["MonthlyCharges"].mean()
                if "Churn" in df.columns
                else 0
            )

            st.metric("Avg Monthly Charges (Loyal)", f"${avg_monthly_loyal:.2f}")

            st.metric(
                "Avg Monthly Charges (Churned)",
                f"${avg_monthly_churn:.2f}",
                delta=f"{avg_monthly_churn - avg_monthly_loyal:+.2f}",
            )

        with col3:
            # Customer lifetime value impact
            if "tenure" in df.columns:
                avg_tenure_loyal = (
                    df[df["Churn"] == "No"]["tenure"].mean()
                    if "Churn" in df.columns
                    else 0
                )
                avg_tenure_churn = (
                    df[df["Churn"] == "Yes"]["tenure"].mean()
                    if "Churn" in df.columns
                    else 0
                )

                clv_loyal = avg_monthly_loyal * avg_tenure_loyal
                clv_churn = avg_monthly_churn * avg_tenure_churn

                st.metric("Customer Lifetime Value (Loyal)", f"${clv_loyal:,.0f}")

                st.metric(
                    "Customer Lifetime Value (Churned)",
                    f"${clv_churn:,.0f}",
                    delta=f"{clv_churn - clv_loyal:+,.0f}",
                )

# ============== TAB 4: FEATURE CORRELATION ==============
with tab4:
    st.subheader("🔗 Feature Correlation & Relationships")

    # Prepare numeric data for correlation
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) > 1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Feature Correlation Matrix**")

            # Calculate correlation matrix
            corr_matrix = df[numeric_cols].corr()

            if PLOTLY_AVAILABLE:
                # Create correlation heatmap
                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=".2f",
                    aspect="auto",
                    color_continuous_scale="RdBu",
                    title="Feature Correlation Heatmap",
                )

                fig_corr.update_layout(template="plotly_dark", height=500)

                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                # Fallback matplotlib heatmap
                fig, ax = plt.subplots(figsize=(12, 8))
                try:
                    im = ax.imshow(corr_matrix, cmap="RdBu", aspect="auto")
                    ax.set_xticks(range(len(corr_matrix.columns)))
                    ax.set_yticks(range(len(corr_matrix.columns)))
                    ax.set_xticklabels(corr_matrix.columns, rotation=45, ha="right")
                    ax.set_yticklabels(corr_matrix.columns)

                    # Add correlation values as text
                    for i in range(len(corr_matrix.columns)):
                        for j in range(len(corr_matrix.columns)):
                            corr_val = corr_matrix.iloc[i, j]
                            text_color = "white" if abs(corr_val) > 0.5 else "black"
                            ax.text(
                                j,
                                i,
                                f"{corr_val:.2f}",
                                ha="center",
                                va="center",
                                color=text_color,
                            )

                    ax.set_title(
                        "Feature Correlation Heatmap", fontsize=14, fontweight="bold"
                    )
                    plt.colorbar(im)
                except Exception as e:
                    # Simple fallback if heatmap fails
                    ax.text(
                        0.5,
                        0.5,
                        "Correlation Matrix\n(Install seaborn for better visualization)",
                        ha="center",
                        va="center",
                        transform=ax.transAxes,
                    )
                st.pyplot(fig)

        with col2:
            st.markdown("**Feature Relationships**")

            # Interactive feature selector
            feature_x = st.selectbox(
                "Select X-axis feature:", numeric_cols, key="corr_x"
            )
            feature_y = st.selectbox(
                "Select Y-axis feature:", numeric_cols, index=1, key="corr_y"
            )

            if feature_x != feature_y:
                if PLOTLY_AVAILABLE:
                    fig_relationship = px.scatter(
                        df,
                        x=feature_x,
                        y=feature_y,
                        color="Churn" if "Churn" in df.columns else None,
                        color_discrete_map={"No": "#10b981", "Yes": "#ef4444"}
                        if "Churn" in df.columns
                        else None,
                        title=f"{feature_x} vs {feature_y}",
                        opacity=0.7,
                        trendline="ols" if "Churn" not in df.columns else None,
                    )

                    fig_relationship.update_layout(template="plotly_dark", height=450)

                    st.plotly_chart(fig_relationship, use_container_width=True)
                else:
                    # Fallback matplotlib scatter plot
                    fig, ax = plt.subplots(figsize=(10, 6))
                    if "Churn" in df.columns:
                        for churn_val, color in zip(
                            ["No", "Yes"], ["#10b981", "#ef4444"]
                        ):
                            mask = df["Churn"] == churn_val
                            ax.scatter(
                                df[mask][feature_x],
                                df[mask][feature_y],
                                c=color,
                                alpha=0.7,
                                label=f"Churn: {churn_val}",
                            )
                        ax.legend()
                    else:
                        ax.scatter(
                            df[feature_x], df[feature_y], alpha=0.7, color="#0ea5e9"
                        )

                    ax.set_title(
                        f"{feature_x} vs {feature_y}", fontsize=14, fontweight="bold"
                    )
                    ax.set_xlabel(feature_x)
                    ax.set_ylabel(feature_y)
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)

                # Show correlation coefficient
                correlation = df[feature_x].corr(df[feature_y])
                st.metric(
                    f"Correlation ({feature_x} vs {feature_y})", f"{correlation:.3f}"
                )

    # Feature importance (if model is available)
    if "model" in st.session_state and st.session_state.model is not None:
        st.markdown("---")
        st.markdown("**Model Feature Importance**")

        if hasattr(st.session_state.model, "coef_"):
            feature_names = st.session_state.X_train.columns
            coefficients = st.session_state.model.coef_[0]

            importance_df = pd.DataFrame(
                {
                    "Feature": feature_names,
                    "Importance": np.abs(coefficients),
                    "Coefficient": coefficients,
                }
            ).sort_values("Importance", ascending=True)

            if PLOTLY_AVAILABLE:
                fig_importance = px.bar(
                    importance_df.tail(10),  # Top 10 features
                    y="Feature",
                    x="Importance",
                    orientation="h",
                    color="Coefficient",
                    color_continuous_scale="RdBu",
                    title="Top 10 Most Important Features (Logistic Regression)",
                )

                fig_importance.update_layout(
                    template="plotly_dark",
                    height=500,
                    xaxis_title="Feature Importance (|Coefficient|)",
                    yaxis_title="Features",
                )

                st.plotly_chart(fig_importance, use_container_width=True)
            else:
                # Fallback matplotlib horizontal bar chart
                fig, ax = plt.subplots(figsize=(10, 8))
                top_features = importance_df.tail(10)
                colors = [
                    "#ef4444" if coef < 0 else "#10b981"
                    for coef in top_features["Coefficient"]
                ]
                bars = ax.barh(
                    top_features["Feature"], top_features["Importance"], color=colors
                )

                ax.set_title(
                    "Top 10 Most Important Features (Logistic Regression)",
                    fontsize=14,
                    fontweight="bold",
                )
                ax.set_xlabel("Feature Importance (|Coefficient|)")
                ax.set_ylabel("Features")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

    # Data quality overview
    st.markdown("---")
    st.markdown("**Data Quality Overview**")

    col1, col2 = st.columns(2)

    with col1:
        # Missing values heatmap
        missing_data = df.isnull().sum()
        missing_df = pd.DataFrame(
            {
                "Column": missing_data.index,
                "Missing_Count": missing_data.values,
                "Missing_Percentage": (missing_data.values / len(df) * 100).round(2),
            }
        )
        missing_df = missing_df[missing_df["Missing_Count"] > 0]

        if len(missing_df) > 0:
            if PLOTLY_AVAILABLE:
                fig_missing = px.bar(
                    missing_df,
                    x="Column",
                    y="Missing_Percentage",
                    color="Missing_Percentage",
                    color_continuous_scale="Reds",
                    title="Missing Values by Column",
                )

                fig_missing.update_layout(
                    template="plotly_dark",
                    height=400,
                    xaxis_title="Columns",
                    yaxis_title="Missing Percentage (%)",
                )

                st.plotly_chart(fig_missing, use_container_width=True)
            else:
                # Fallback matplotlib bar chart
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.bar(
                    missing_df["Column"],
                    missing_df["Missing_Percentage"],
                    color="#ef4444",
                )
                ax.set_title("Missing Values by Column", fontsize=14, fontweight="bold")
                ax.set_xlabel("Columns")
                ax.set_ylabel("Missing Percentage (%)")
                plt.xticks(rotation=45)
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
        else:
            st.success("✅ No missing values detected!")

    with col2:
        # Data types distribution
        dtype_counts = df.dtypes.value_counts()
        dtype_df = pd.DataFrame(
            {"Data_Type": dtype_counts.index.astype(str), "Count": dtype_counts.values}
        )

        if PLOTLY_AVAILABLE:
            fig_types = px.pie(
                dtype_df,
                names="Data_Type",
                values="Count",
                title="Data Types Distribution",
                color_discrete_sequence=["#0ea5e9", "#10b981", "#f59e0b", "#ef4444"],
            )

            fig_types.update_layout(template="plotly_dark", height=400)

            st.plotly_chart(fig_types, use_container_width=True)
        else:
            # Fallback matplotlib pie chart
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(
                dtype_df["Count"],
                labels=dtype_df["Data_Type"],
                autopct="%1.1f%%",
                colors=["#0ea5e9", "#10b981", "#f59e0b", "#ef4444"],
            )
            ax.set_title("Data Types Distribution", fontsize=14, fontweight="bold")
            st.pyplot(fig)

# Summary insights
st.markdown("---")
st.subheader("💡 Key Insights Summary")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🎯 Churn Patterns Identified:**")
    insights = []

    if "Churn" in df.columns and "Contract" in df.columns:
        contract_churn_rates = df.groupby("Contract")["Churn"].apply(
            lambda x: (x == "Yes").sum() / len(x) * 100
        )
        highest_churn_contract = contract_churn_rates.idxmax()
        insights.append(f"• {highest_churn_contract} contracts show highest churn risk")

    if "InternetService" in df.columns and "Churn" in df.columns:
        internet_churn_rates = df.groupby("InternetService")["Churn"].apply(
            lambda x: (x == "Yes").sum() / len(x) * 100
        )
        highest_churn_internet = internet_churn_rates.idxmax()
        insights.append(
            f"• {highest_churn_internet} internet service has highest churn"
        )

    if "MonthlyCharges" in df.columns and "Churn" in df.columns:
        avg_charges_churn = df[df["Churn"] == "Yes"]["MonthlyCharges"].mean()
        avg_charges_loyal = df[df["Churn"] == "No"]["MonthlyCharges"].mean()
        if avg_charges_churn > avg_charges_loyal:
            insights.append(f"• Higher monthly charges correlate with churn risk")

    for insight in insights:
        st.write(insight)

with col2:
    st.markdown("**💼 Business Recommendations:**")
    recommendations = [
        "• Focus retention efforts on high-risk segments",
        "• Review pricing strategy for high-churn services",
        "• Improve customer onboarding for new subscribers",
        "• Implement proactive customer success programs",
        "• Consider loyalty programs for long-term customers",
    ]

    for rec in recommendations:
        st.write(rec)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: var(--text-muted); padding: 1rem;">
        📊 <strong>Data Visualization Complete</strong><br>
        Use these insights to develop targeted customer retention strategies
    </div>
    """,
    unsafe_allow_html=True,
)

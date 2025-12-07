import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    sns = None

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    px = None
    go = None

try:
    plt.style.use("dark_background")
    plt.rcParams["figure.facecolor"] = "#1a1a1a"
    plt.rcParams["axes.facecolor"] = "#2a2a2a"
    plt.rcParams["text.color"] = "white"
    plt.rcParams["axes.labelcolor"] = "white"
    plt.rcParams["xtick.color"] = "white"
    plt.rcParams["ytick.color"] = "white"
except Exception:
    plt.rcParams["figure.facecolor"] = "#ffffff"
    plt.rcParams["axes.facecolor"] = "#ffffff"

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from style import inject_global_style, render_sidebar

st.set_page_config(
    page_title="Model Training & Testing - PREDICTEL", page_icon="🧪", layout="wide"
)

inject_global_style()
render_sidebar("Test Data")

st.markdown(
    """
    <div class="step-header">
        <strong>Langkah 3 — Model Training & Performance Evaluation</strong>
        <p>
            Train Logistic Regression model dengan data yang telah dipreproses,
            evaluasi performa model, dan lakukan prediksi individual untuk customer churn.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("🧪 Model Training & Testing")

if (
    "X_train" not in st.session_state
    or st.session_state.X_train is None
    or st.session_state.X_test is None
):
    st.warning(
        "⚠️ Data training belum tersedia. Silakan lakukan **Preprocessing** terlebih dahulu."
    )
    st.stop()

if "model" not in st.session_state:
    st.session_state.model = None
if "model_metrics" not in st.session_state:
    st.session_state.model_metrics = {}

tab1, tab2, tab3 = st.tabs(
    ["⚙️ Model Training", "📊 Performance Evaluation", "🎯 Individual Prediction"]
)

with tab1:
    st.subheader("🚀 Logistic Regression Training")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("**🔧 Model Configuration**")

        with st.expander("⚙️ Hyperparameter Settings", expanded=True):
            col_hyper1, col_hyper2 = st.columns(2)

            with col_hyper1:
                max_iter = st.number_input(
                    "Maximum Iterations:",
                    min_value=100,
                    max_value=5000,
                    value=1000,
                    step=100,
                    help="Maximum number of iterations for solver convergence",
                )

                random_state = st.number_input(
                    "Random State:",
                    min_value=0,
                    max_value=999,
                    value=42,
                    help="Seed for reproducibility",
                )

            with col_hyper2:
                solver = st.selectbox(
                    "Solver:",
                    ["lbfgs", "liblinear", "newton-cg", "sag", "saga"],
                    index=0,
                    help="Algorithm to use for optimization",
                )

                C = st.selectbox(
                    "Regularization Strength (C):",
                    [0.01, 0.1, 1.0, 10.0, 100.0],
                    index=2,
                    help="Inverse regularization strength (smaller = stronger regularization)",
                )

    with col2:
        st.markdown("**📊 Dataset Info**")

        train_samples = st.session_state.X_train.shape[0]
        test_samples = st.session_state.X_test.shape[0]
        n_features = st.session_state.X_train.shape[1]

        st.metric("Training Samples", f"{train_samples:,}")
        st.metric("Test Samples", f"{test_samples:,}")
        st.metric("Features", n_features)

        class_dist = st.session_state.y_train.value_counts()
        churn_pct = class_dist.get(1, 0) / len(st.session_state.y_train) * 100
        st.metric("Churn Rate", f"{churn_pct:.1f}%")

    st.markdown("---")

    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button(
            "🚀 Train Logistic Regression Model",
            type="primary",
            use_container_width=True,
        ):
            with st.status("🔄 Training model...", expanded=True) as status:
                try:
                    model = LogisticRegression(
                        max_iter=max_iter, random_state=random_state, solver=solver, C=C
                    )

                    st.write("✅ Initializing Logistic Regression...")
                    model.fit(st.session_state.X_train, st.session_state.y_train)
                    st.write("✅ Model training completed...")

                    y_pred = model.predict(st.session_state.X_test)
                    y_pred_proba = model.predict_proba(st.session_state.X_test)[:, 1]
                    st.write("✅ Predictions generated...")

                    accuracy = accuracy_score(st.session_state.y_test, y_pred)
                    precision = precision_score(st.session_state.y_test, y_pred)
                    recall = recall_score(st.session_state.y_test, y_pred)
                    f1 = f1_score(st.session_state.y_test, y_pred)
                    auc_roc = roc_auc_score(st.session_state.y_test, y_pred_proba)
                    st.write("✅ Performance metrics calculated...")

                    st.session_state.model = model
                    st.session_state.model_metrics = {
                        "accuracy": accuracy,
                        "precision": precision,
                        "recall": recall,
                        "f1_score": f1,
                        "roc_auc": auc_roc,
                        "y_pred": y_pred,
                        "y_pred_proba": y_pred_proba,
                    }

                    status.update(
                        label="✅ Model training successful!",
                        state="complete",
                        expanded=False,
                    )

                except Exception as e:
                    st.error(f"❌ Training failed: {str(e)}")
                    status.update(
                        label="❌ Training failed!", state="error", expanded=False
                    )

    if st.session_state.model is not None:
        st.markdown("---")
        st.subheader("✅ Training Results")

        metrics = st.session_state.model_metrics

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Accuracy", f"{metrics['accuracy']:.3f}")
        with col2:
            st.metric("Precision", f"{metrics['precision']:.3f}")
        with col3:
            st.metric("Recall", f"{metrics['recall']:.3f}")
        with col4:
            st.metric("F1-Score", f"{metrics['f1_score']:.3f}")
        with col5:
            st.metric("ROC AUC", f"{metrics['roc_auc']:.3f}")

        with st.expander("📋 Model Coefficients (Feature Importance)", expanded=False):
            feature_names = st.session_state.X_train.columns
            coefficients = st.session_state.model.coef_[0]

            coef_df = pd.DataFrame(
                {
                    "Feature": feature_names,
                    "Coefficient": coefficients,
                    "Abs_Coefficient": np.abs(coefficients),
                }
            ).sort_values("Abs_Coefficient", ascending=False)

            st.dataframe(coef_df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("📊 Model Performance Analysis")

    if st.session_state.model is None:
        st.warning("⚠️ Please train the model first in the **Model Training** tab.")
    else:
        metrics = st.session_state.model_metrics
        y_test = st.session_state.y_test
        y_pred = metrics["y_pred"]
        y_pred_proba = metrics["y_pred_proba"]

        st.markdown("### 🎯 Performance Overview")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Confusion Matrix**")
            cm = confusion_matrix(y_test, y_pred)

            if PLOTLY_AVAILABLE:
                fig_cm = go.Figure(
                    data=go.Heatmap(
                        z=cm,
                        x=["Predicted No Churn", "Predicted Churn"],
                        y=["Actual No Churn", "Actual Churn"],
                        colorscale="Blues",
                        showscale=True,
                        text=cm,
                        texttemplate="%{text}",
                        textfont={"size": 20},
                    )
                )

                fig_cm.update_layout(
                    title="Confusion Matrix",
                    xaxis_title="Predicted",
                    yaxis_title="Actual",
                    height=400,
                    template="plotly_dark",
                )

                st.plotly_chart(fig_cm, use_container_width=True)
            else:
                fig, ax = plt.subplots(figsize=(8, 6))
                if SEABORN_AVAILABLE:
                    sns.heatmap(
                        cm,
                        annot=True,
                        fmt="d",
                        cmap="Blues",
                        ax=ax,
                        xticklabels=["Predicted No Churn", "Predicted Churn"],
                        yticklabels=["Actual No Churn", "Actual Churn"],
                    )
                else:
                    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
                    ax.set_xticks(range(2))
                    ax.set_yticks(range(2))
                    ax.set_xticklabels(["Predicted No Churn", "Predicted Churn"])
                    ax.set_yticklabels(["Actual No Churn", "Actual Churn"])

                    thresh = cm.max() / 2.0
                    for i in range(2):
                        for j in range(2):
                            ax.text(
                                j,
                                i,
                                str(cm[i, j]),
                                ha="center",
                                va="center",
                                color="white" if cm[i, j] > thresh else "black",
                            )

                ax.set_title("Confusion Matrix", fontsize=14, fontweight="bold")
                ax.set_ylabel("Actual")
                ax.set_xlabel("Predicted")
                st.pyplot(fig)

        with col2:
            st.markdown("**Classification Metrics**")

            tn, fp, fn, tp = cm.ravel()

            metrics_data = {
                "Metric": [
                    "True Positives",
                    "False Positives",
                    "True Negatives",
                    "False Negatives",
                ],
                "Count": [tp, fp, tn, fn],
                "Description": [
                    "Correctly predicted Churn",
                    "Incorrectly predicted Churn",
                    "Correctly predicted No Churn",
                    "Incorrectly predicted No Churn",
                ],
            }

            st.dataframe(
                pd.DataFrame(metrics_data), use_container_width=True, hide_index=True
            )

        st.markdown("### 📈 Model Performance Curves")

        col1, col2 = st.columns(2)

        with col1:
            fpr, tpr, _ = roc_curve(y_test, y_pred_proba)

            if PLOTLY_AVAILABLE:
                fig_roc = go.Figure()
                fig_roc.add_trace(
                    go.Scatter(
                        x=fpr,
                        y=tpr,
                        mode="lines",
                        name=f"ROC Curve (AUC = {metrics['roc_auc']:.3f})",
                        line=dict(color="#0ea5e9", width=3),
                    )
                )
                fig_roc.add_trace(
                    go.Scatter(
                        x=[0, 1],
                        y=[0, 1],
                        mode="lines",
                        name="Random Classifier",
                        line=dict(dash="dash", color="gray"),
                    )
                )

                fig_roc.update_layout(
                    title="ROC Curve",
                    xaxis_title="False Positive Rate",
                    yaxis_title="True Positive Rate",
                    template="plotly_dark",
                    height=400,
                )

                st.plotly_chart(fig_roc, use_container_width=True)
            else:
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.plot(
                    fpr,
                    tpr,
                    color="#0ea5e9",
                    linewidth=3,
                    label=f"ROC Curve (AUC = {metrics['roc_auc']:.3f})",
                )
                ax.plot(
                    [0, 1],
                    [0, 1],
                    color="gray",
                    linestyle="--",
                    label="Random Classifier",
                )
                ax.set_title("ROC Curve", fontsize=14, fontweight="bold")
                ax.set_xlabel("False Positive Rate")
                ax.set_ylabel("True Positive Rate")
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

        with col2:
            precision_curve, recall_curve, _ = precision_recall_curve(
                y_test, y_pred_proba
            )

            if PLOTLY_AVAILABLE:
                fig_pr = go.Figure()
                fig_pr.add_trace(
                    go.Scatter(
                        x=recall_curve,
                        y=precision_curve,
                        mode="lines",
                        name=f"PR Curve (F1 = {metrics['f1_score']:.3f})",
                        line=dict(color="#10b981", width=3),
                    )
                )

                baseline = y_test.mean()
                fig_pr.add_hline(
                    y=baseline,
                    line_dash="dash",
                    line_color="gray",
                    annotation_text=f"Baseline ({baseline:.3f})",
                )

                fig_pr.update_layout(
                    title="Precision-Recall Curve",
                    xaxis_title="Recall",
                    yaxis_title="Precision",
                    template="plotly_dark",
                    height=400,
                )

                st.plotly_chart(fig_pr, use_container_width=True)
            else:
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.plot(
                    recall_curve,
                    precision_curve,
                    color="#10b981",
                    linewidth=3,
                    label=f"PR Curve (F1 = {metrics['f1_score']:.3f})",
                )

                baseline = y_test.mean()
                ax.axhline(
                    y=baseline,
                    color="gray",
                    linestyle="--",
                    label=f"Baseline ({baseline:.3f})",
                )

                ax.set_title("Precision-Recall Curve", fontsize=14, fontweight="bold")
                ax.set_xlabel("Recall")
                ax.set_ylabel("Precision")
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

with tab3:
    st.subheader("🎯 Individual Customer Prediction")

    if st.session_state.model is None:
        st.warning("⚠️ Please train the model first in the **Model Training** tab.")
    else:
        st.markdown("Enter customer details below to predict churn probability:")

        with st.form("individual_prediction_form_clean"):
            col1, col2, col3 = st.columns(3)

            feature_names = st.session_state.X_train.columns.tolist()
            input_values = {}

            with col1:
                st.markdown("**Account Information**")

                col_slider, col_value = st.columns([3, 1])
                with col_slider:
                    input_values["tenure"] = st.slider(
                        "Tenure",
                        min_value=0,
                        max_value=72,
                        value=12,
                        step=1,
                        key="tenure_slider",
                    )
                with col_value:
                    st.markdown(f"**{input_values['tenure']}** months")

                input_values["monthly_charges"] = st.number_input(
                    "Monthly Charges ($)", 0.0, 200.0, 65.0, step=1.0
                )
                input_values["total_charges"] = st.number_input(
                    "Total Charges ($)", 0.0, 10000.0, 1500.0, step=10.0
                )

                st.markdown("---")
                st.markdown("**Summary:**")
                st.write(f"📅 Tenure: **{input_values['tenure']} months**")
                st.write(f"💰 Monthly: **${input_values['monthly_charges']:.2f}**")
                st.write(f"💳 Total: **${input_values['total_charges']:.2f}**")

            with col2:
                st.markdown("**Demographics**")
                input_values["senior_citizen"] = st.selectbox(
                    "Senior Citizen",
                    [0, 1],
                    index=0,
                    format_func=lambda x: "No (0)" if x == 0 else "Yes (1)",
                )
                input_values["gender"] = st.selectbox(
                    "Gender",
                    [0, 1],
                    format_func=lambda x: "Female" if x == 0 else "Male",
                )
                input_values["partner"] = st.selectbox(
                    "Has Partner",
                    [0, 1],
                    format_func=lambda x: "No" if x == 0 else "Yes",
                )
                input_values["dependents"] = st.selectbox(
                    "Has Dependents",
                    [0, 1],
                    format_func=lambda x: "No" if x == 0 else "Yes",
                )

            with col3:
                st.markdown("**Services**")
                input_values["internet_service"] = st.selectbox(
                    "Internet Service",
                    [0, 1, 2],
                    format_func=lambda x: ["DSL", "Fiber Optic", "No"][x],
                )
                input_values["contract"] = st.selectbox(
                    "Contract",
                    [0, 1, 2],
                    format_func=lambda x: ["Month-to-Month", "One Year", "Two Year"][x],
                )
                input_values["payment_method"] = st.selectbox(
                    "Payment Method",
                    [0, 1, 2, 3],
                    format_func=lambda x: [
                        "Electronic Check (0)",
                        "Mailed Check (1)",
                        "Bank Transfer (2)",
                        "Credit Card (3)",
                    ][x],
                )
                input_values["paperless_billing"] = st.selectbox(
                    "Paperless Billing",
                    [0, 1],
                    format_func=lambda x: "No" if x == 0 else "Yes",
                )

            submitted = st.form_submit_button(
                "🔍 Predict Churn",
                type="primary",
                use_container_width=True,
                key="predict_churn_btn_clean",
            )

            if submitted:
                try:
                    n_features = st.session_state.X_train.shape[1]

                    input_array = np.zeros((1, n_features))

                    for i in range(n_features):
                        input_array[0, i] = st.session_state.X_train.iloc[:, i].mean()

                    feature_mapping = {
                        "tenure": input_values.get("tenure", 12),
                        "monthly_charges": input_values.get("monthly_charges", 65.0),
                        "total_charges": input_values.get("total_charges", 1500.0),
                        "senior_citizen": input_values.get("senior_citizen", 0),
                        "gender": input_values.get("gender", 0),
                        "partner": input_values.get("partner", 0),
                        "dependents": input_values.get("dependents", 0),
                        "contract": input_values.get("contract", 0),
                        "internet_service": input_values.get("internet_service", 0),
                        "payment_method": input_values.get("payment_method", 0),
                        "paperless_billing": input_values.get("paperless_billing", 0),
                    }

                    if n_features >= 3:
                        input_array[0, 0] = feature_mapping["tenure"]
                        input_array[0, 1] = feature_mapping["monthly_charges"]
                        input_array[0, 2] = feature_mapping["total_charges"]

                    if n_features >= 6:
                        input_array[0, 3] = feature_mapping["senior_citizen"]
                        input_array[0, 4] = feature_mapping["gender"]
                        input_array[0, 5] = feature_mapping["partner"]

                    if n_features >= 10:
                        input_array[0, 6] = feature_mapping["dependents"]
                        input_array[0, 7] = feature_mapping["contract"]
                        input_array[0, 8] = feature_mapping["internet_service"]
                        input_array[0, 9] = feature_mapping["payment_method"]

                    if n_features >= 11:
                        input_array[0, 10] = feature_mapping["paperless_billing"]

                    prediction = st.session_state.model.predict(input_array)[0]
                    probability = st.session_state.model.predict_proba(input_array)[0]
                    churn_prob = probability[1]

                    st.markdown("---")
                    st.markdown("### 🎯 Prediction Result")

                    if churn_prob > 0.5:
                        result_class = "prediction-result-churn"
                        result_text = "HIGH RISK CHURN"
                        result_desc = "⚠️ This customer has a high probability of churning. Consider retention strategies."
                        prob_color = "#ef4444"
                    else:
                        result_class = "prediction-result-loyal"
                        result_text = "LOYAL CUSTOMER"
                        result_desc = "✅ This customer is likely to remain loyal. Continue providing excellent service."
                        prob_color = "#10b981"

                    st.markdown(
                        f"""
                        <div class="prediction-card">
                            <h2 style="color: {prob_color}; text-align: center; margin-bottom: 1rem;">{result_text}</h2>
                            <p style="font-size: 1.1rem; margin: 1rem 0; text-align: center;">{result_desc}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown("#### Churn Probability")
                    progress_bar = st.progress(churn_prob)

                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.markdown(
                            f"<h3 style='text-align: center; color: {prob_color}; margin: 1rem 0;'>{churn_prob * 100:.1f}%</h3>",
                            unsafe_allow_html=True,
                        )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**🎯 Confidence Breakdown**")
                        confidence_data = {
                            "Outcome": ["Will Churn", "Will Stay"],
                            "Probability": [
                                f"{probability[1]:.1%}",
                                f"{probability[0]:.1%}",
                            ],
                            "Confidence": [
                                "High" if probability[1] > 0.7 else "Medium",
                                "High" if probability[0] > 0.7 else "Medium",
                            ],
                        }
                        st.dataframe(
                            pd.DataFrame(confidence_data),
                            use_container_width=True,
                            hide_index=True,
                        )

                    with col2:
                        st.markdown("**💡 Business Recommendations**")
                        if churn_prob > 0.7:
                            st.error("🚨 Immediate intervention required")
                            st.write("• Offer personalized retention deals")
                            st.write("• Schedule customer service call")
                            st.write("• Analyze service satisfaction")
                        elif churn_prob > 0.5:
                            st.warning("⚠️ Monitor closely")
                            st.write("• Send customer satisfaction survey")
                            st.write("• Offer service upgrades")
                            st.write("• Check for service issues")
                        else:
                            st.success("✅ Customer appears stable")
                            st.write("• Continue current service level")
                            st.write("• Consider upselling opportunities")
                            st.write("• Maintain regular communication")

                except Exception as e:
                    st.error(f"❌ Prediction failed: {str(e)}")
                    st.markdown("""
                    **Troubleshooting:**
                    - Ensure the model is trained first in the 'Model Training' tab
                    - Check that preprocessing was completed successfully
                    - Verify that your dataset has the required features
                    - Try refreshing the page and retraining the model
                    """)

                    with st.expander("🔧 Debug Information"):
                        if st.session_state.model is not None:
                            st.write(f"Model type: {type(st.session_state.model)}")
                            if hasattr(st.session_state, "X_train"):
                                st.write(
                                    f"Training data shape: {st.session_state.X_train.shape}"
                                )
                            st.write(f"Input values: {input_values}")
                        else:
                            st.write("❌ No model found - please train the model first")

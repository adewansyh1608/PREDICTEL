import numpy as np
import pandas as pd
import streamlit as st
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from style import inject_global_style, render_sidebar

# Konfigurasi Halaman
st.set_page_config(
    page_title="Preprocessing Data - PREDICTEL", page_icon="⚙️", layout="wide"
)

inject_global_style()
render_sidebar("Processing Data")

# Inisialisasi Session State
if "data" not in st.session_state:
    st.session_state.data = None
if "data_processed" not in st.session_state:
    st.session_state.data_processed = None
if "X_train" not in st.session_state:
    st.session_state.X_train = None
if "X_test" not in st.session_state:
    st.session_state.X_test = None
if "y_train" not in st.session_state:
    st.session_state.y_train = None
if "y_test" not in st.session_state:
    st.session_state.y_test = None
if "scaler" not in st.session_state:
    st.session_state.scaler = None
if "preprocessing_config" not in st.session_state:
    st.session_state.preprocessing_config = {}

# Header
st.markdown(
    """
    <div class="step-header">
        <strong>Langkah 2 — Data Preprocessing & Model Preparation</strong>
        <p>
            Lakukan preprocessing data dengan berbagai opsi handling missing values,
            feature encoding, dan data scaling untuk persiapan machine learning model.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("⚙️ Data Preprocessing")

# Cek data tersedia
if st.session_state.data is None:
    st.warning(
        "⚠️ Data belum tersedia. Silakan upload dataset di halaman **Input Data** terlebih dahulu."
    )
    st.stop()

# Tampilan Data Asli
st.subheader("📋 Dataset Overview")
with st.expander("🔍 Lihat Data Asli", expanded=False):
    st.dataframe(st.session_state.data, height=300, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", f"{st.session_state.data.shape[0]:,}")
    with col2:
        st.metric("Total Columns", st.session_state.data.shape[1])
    with col3:
        missing_count = st.session_state.data.isnull().sum().sum()
        st.metric("Missing Values", missing_count)

st.markdown("---")

# Tabs untuk Preprocessing
tab1, tab2, tab3 = st.tabs(
    ["🔧 Data Analysis", "⚙️ Preprocessing Options", "✂️ Train/Test Split"]
)

# ============== TAB 1: DATA ANALYSIS ==============
with tab1:
    st.subheader("📊 Data Quality Analysis")

    df = st.session_state.data

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🔍 Missing Values Analysis**")
        # Missing values analysis
        missing_data = df.isnull().sum()
        missing_df = pd.DataFrame(
            {
                "Column": missing_data.index,
                "Missing Count": missing_data.values,
                "Missing %": (missing_data.values / len(df) * 100).round(2),
            }
        )
        missing_df = missing_df[missing_df["Missing Count"] > 0]

        if len(missing_df) > 0:
            st.dataframe(missing_df, hide_index=True, use_container_width=True)
        else:
            st.success("✅ No missing values detected!")

        # Handle TotalCharges special case (blank spaces)
        if "TotalCharges" in df.columns:
            blank_count = (df["TotalCharges"] == " ").sum()
            if blank_count > 0:
                st.warning(
                    f"⚠️ Found {blank_count} blank values (spaces) in TotalCharges column"
                )

    with col2:
        st.markdown("**📋 Data Types Overview**")
        dtype_info = pd.DataFrame(
            {
                "Column": df.columns,
                "Data Type": df.dtypes.astype(str),
                "Unique Values": [df[col].nunique() for col in df.columns],
            }
        )
        st.dataframe(dtype_info, hide_index=True, use_container_width=True)

    # Statistical Summary
    st.markdown("**📈 Numerical Features Summary**")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.dataframe(df[numeric_cols].describe(), use_container_width=True)
    else:
        st.info("Tidak ada kolom numerik yang terdeteksi.")

# ============== TAB 2: PREPROCESSING OPTIONS ==============
with tab2:
    st.subheader("⚙️ Preprocessing Configuration")

    # Configuration Form
    with st.form("preprocessing_config_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🔧 Missing Values Strategy**")
            missing_strategy = st.selectbox(
                "Pilih metode untuk handling missing values:",
                ["mean", "median", "most_frequent"],
                help="• Mean: Rata-rata (untuk data numerik)\n• Median: Nilai tengah (robust terhadap outlier)\n• Most Frequent: Modus (untuk data kategorikal)",
            )

            st.markdown("**📊 Scaling Method**")
            scaling_method = st.selectbox(
                "Pilih metode scaling:",
                ["StandardScaler", "MinMaxScaler", "None"],
                help="• StandardScaler: Z-score normalization\n• MinMaxScaler: Scale ke range 0-1\n• None: Tidak ada scaling",
            )

        with col2:
            st.markdown("**🎯 Target Column**")
            target_column = st.selectbox(
                "Pilih kolom target (Churn):",
                [
                    col
                    for col in st.session_state.data.columns
                    if "churn" in col.lower()
                ],
                help="Kolom yang berisi informasi churn (Yes/No)",
            )

            st.markdown("**✂️ Test Split Size**")
            test_size = (
                st.slider(
                    "Persentase data untuk testing:",
                    min_value=10,
                    max_value=50,
                    value=20,
                    step=5,
                    help="Persentase data yang akan digunakan untuk testing model",
                )
                / 100
            )

            random_state = st.number_input(
                "Random State (untuk reproducibility):",
                min_value=0,
                max_value=999,
                value=42,
            )

        # Submit Button
        submitted = st.form_submit_button(
            "🚀 Run Preprocessing",
            type="primary",
            use_container_width=True,
            key="preprocessing_submit_btn",
        )

        if submitted:
            with st.status("🔄 Processing data...", expanded=True) as status:
                try:
                    # 1. Copy data
                    df_clean = st.session_state.data.copy()
                    st.write("✅ Copying dataset...")

                    # 2. Remove irrelevant columns
                    columns_to_drop = (
                        ["customerID"] if "customerID" in df_clean.columns else []
                    )
                    if columns_to_drop:
                        df_clean = df_clean.drop(columns=columns_to_drop)
                        st.write(f"✅ Removing columns: {columns_to_drop}")

                    # 3. Handle TotalCharges special case (blank spaces)
                    if "TotalCharges" in df_clean.columns:
                        # Replace blank spaces with NaN
                        df_clean["TotalCharges"] = df_clean["TotalCharges"].replace(
                            " ", np.nan
                        )
                        # Convert to numeric
                        df_clean["TotalCharges"] = pd.to_numeric(
                            df_clean["TotalCharges"], errors="coerce"
                        )
                        st.write("✅ Fixed TotalCharges column...")

                    # 4. Separate features and target
                    if target_column in df_clean.columns:
                        # Encode target variable
                        if df_clean[target_column].dtype == "object":
                            df_clean[target_column] = df_clean[target_column].map(
                                {"Yes": 1, "No": 0}
                            )
                            st.write("✅ Encoding target variable (Yes=1, No=0)...")

                        X = df_clean.drop(target_column, axis=1)
                        y = df_clean[target_column]
                    else:
                        st.error(f"Target column '{target_column}' not found!")
                        st.stop()

                    # 5. Handle missing values
                    numeric_features = X.select_dtypes(include=[np.number]).columns
                    categorical_features = X.select_dtypes(include=["object"]).columns

                    # For numeric features
                    if len(numeric_features) > 0:
                        if missing_strategy == "most_frequent":
                            # Use median for numeric when most_frequent is selected
                            imputer_num = SimpleImputer(strategy="median")
                        else:
                            imputer_num = SimpleImputer(strategy=missing_strategy)

                        X[numeric_features] = imputer_num.fit_transform(
                            X[numeric_features]
                        )
                        st.write(
                            f"✅ Handling missing values (numeric): {missing_strategy}"
                        )

                    # For categorical features
                    if len(categorical_features) > 0:
                        imputer_cat = SimpleImputer(strategy="most_frequent")
                        X[categorical_features] = imputer_cat.fit_transform(
                            X[categorical_features]
                        )
                        st.write(
                            "✅ Handling missing values (categorical): most_frequent"
                        )

                    # 6. Encode categorical variables
                    if len(categorical_features) > 0:
                        label_encoders = {}
                        for col in categorical_features:
                            le = LabelEncoder()
                            X[col] = le.fit_transform(X[col].astype(str))
                            label_encoders[col] = le
                        st.write(
                            f"✅ Label encoding for {len(categorical_features)} categorical columns"
                        )

                    # 7. Feature Scaling
                    scaler = None
                    if scaling_method == "StandardScaler":
                        from sklearn.preprocessing import StandardScaler

                        scaler = StandardScaler()
                        X_scaled = pd.DataFrame(
                            scaler.fit_transform(X), columns=X.columns, index=X.index
                        )
                        X = X_scaled
                        st.write("✅ Standardization scaling applied")
                    elif scaling_method == "MinMaxScaler":
                        from sklearn.preprocessing import MinMaxScaler

                        scaler = MinMaxScaler()
                        X_scaled = pd.DataFrame(
                            scaler.fit_transform(X), columns=X.columns, index=X.index
                        )
                        X = X_scaled
                        st.write("✅ MinMax scaling applied")
                    else:
                        st.write("✅ No scaling applied")

                    # 8. Train/Test Split
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=test_size, random_state=random_state, stratify=y
                    )
                    st.write(f"✅ Data split: {len(X_train)} train, {len(X_test)} test")

                    # Save to session state
                    st.session_state.data_processed = pd.concat([X, y], axis=1)
                    st.session_state.X_train = X_train
                    st.session_state.X_test = X_test
                    st.session_state.y_train = y_train
                    st.session_state.y_test = y_test
                    st.session_state.scaler = scaler
                    st.session_state.preprocessing_config = {
                        "missing_strategy": missing_strategy,
                        "scaling_method": scaling_method,
                        "target_column": target_column,
                        "test_size": test_size,
                        "random_state": random_state,
                    }

                    status.update(
                        label="✅ Preprocessing completed!",
                        state="complete",
                        expanded=False,
                    )

                except Exception as e:
                    st.error(f"❌ Error during preprocessing: {str(e)}")
                    status.update(
                        label="❌ Preprocessing failed!", state="error", expanded=False
                    )

    # Show preprocessing results
    if st.session_state.data_processed is not None:
        st.markdown("---")
        st.subheader("✅ Preprocessing Results")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Features", st.session_state.X_train.shape[1])
        with col2:
            st.metric("Training Samples", st.session_state.X_train.shape[0])
        with col3:
            st.metric("Test Samples", st.session_state.X_test.shape[0])

        # Show sample of processed data
        with st.expander("🔍 Preview Processed Data", expanded=False):
            st.markdown("**Training Features (X_train) - First 5 rows:**")
            st.dataframe(st.session_state.X_train.head(), use_container_width=True)

            st.markdown("**Training Target (y_train) - First 10 values:**")
            st.write(st.session_state.y_train.head(10).tolist())

# ============== TAB 3: TRAIN/TEST SPLIT INFO ==============
with tab3:
    st.subheader("✂️ Data Split Information")

    if st.session_state.X_train is not None:
        # Split statistics
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📊 Split Statistics**")
            total_samples = len(st.session_state.X_train) + len(st.session_state.X_test)
            train_pct = len(st.session_state.X_train) / total_samples * 100
            test_pct = len(st.session_state.X_test) / total_samples * 100

            metrics_data = {
                "Dataset": ["Training", "Testing", "Total"],
                "Samples": [
                    len(st.session_state.X_train),
                    len(st.session_state.X_test),
                    total_samples,
                ],
                "Percentage": [f"{train_pct:.1f}%", f"{test_pct:.1f}%", "100.0%"],
            }
            st.dataframe(
                pd.DataFrame(metrics_data), hide_index=True, use_container_width=True
            )

        with col2:
            st.markdown("**🎯 Target Distribution**")
            train_target_dist = st.session_state.y_train.value_counts()
            test_target_dist = st.session_state.y_test.value_counts()

            dist_data = {
                "Class": ["No Churn (0)", "Churn (1)"],
                "Train Count": [
                    train_target_dist.get(0, 0),
                    train_target_dist.get(1, 0),
                ],
                "Test Count": [test_target_dist.get(0, 0), test_target_dist.get(1, 0)],
            }
            st.dataframe(
                pd.DataFrame(dist_data), hide_index=True, use_container_width=True
            )

        # Configuration summary
        if st.session_state.preprocessing_config:
            st.markdown("**⚙️ Preprocessing Configuration**")
            config = st.session_state.preprocessing_config

            config_display = {
                "Parameter": [
                    "Missing Values Strategy",
                    "Scaling Method",
                    "Target Column",
                    "Test Size",
                    "Random State",
                ],
                "Value": [
                    config.get("missing_strategy", "N/A"),
                    config.get("scaling_method", "N/A"),
                    config.get("target_column", "N/A"),
                    f"{config.get('test_size', 0) * 100:.0f}%",
                    config.get("random_state", "N/A"),
                ],
            }
            st.dataframe(
                pd.DataFrame(config_display), hide_index=True, use_container_width=True
            )

        # Next step button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "➡️ Lanjut ke Model Training", type="primary", use_container_width=True
            ):
                st.switch_page("pages/Test_Data.py")

    else:
        st.info(
            "🔧 Silakan lakukan preprocessing terlebih dahulu di tab **Preprocessing Options**."
        )

# Warning jika data belum diproses
if st.session_state.data_processed is None:
    st.markdown("---")
    st.info(
        "💡 **Tips**: Lakukan preprocessing data terlebih dahulu sebelum melanjutkan ke tahap training model."
    )

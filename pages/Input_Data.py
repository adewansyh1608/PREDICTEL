import pandas as pd
import streamlit as st

from style import inject_global_style, render_sidebar

st.set_page_config(page_title="Input Data - PREDICTEL", page_icon="📂", layout="wide")

inject_global_style()
render_sidebar("Input Data")

if "data" not in st.session_state:
    st.session_state.data = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

st.markdown(
    """
    <div class="step-header">
        <strong>Langkah 1 — Dataset Upload & Validation</strong>
        <p>
            Upload dataset pelanggan telekomunikasi dalam format CSV.
            System akan melakukan validasi otomatis dan menampilkan preview data.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("📂 Input Data")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📂 Upload Customer Dataset")
    st.markdown("*Drag and drop your CSV file below, or click Browse files*")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        accept_multiple_files=False,
        help="Upload a CSV file containing customer data with churn information",
    )


    with st.expander("📋 Dataset Requirements", expanded=False):
        st.markdown("""
        **Required Format:**
        - File format: CSV (.csv)
        - Encoding: UTF-8 recommended
        - Size limit: 200MB
        - Headers: First row should contain column names

        **Expected Columns (Telco Customer Churn):**
        - `customerID`: Unique customer identifier
        - `gender`: Customer gender (Male/Female)
        - `SeniorCitizen`: Senior citizen status (0/1)
        - `Partner`: Has partner (Yes/No)
        - `Dependents`: Has dependents (Yes/No)
        - `tenure`: Months as customer
        - `PhoneService`: Has phone service (Yes/No)
        - `MultipleLines`: Multiple lines (Yes/No/No phone service)
        - `InternetService`: Internet service type (DSL/Fiber optic/No)
        - `OnlineSecurity`: Online security (Yes/No/No internet service)
        - `OnlineBackup`: Online backup (Yes/No/No internet service)
        - `DeviceProtection`: Device protection (Yes/No/No internet service)
        - `TechSupport`: Tech support (Yes/No/No internet service)
        - `StreamingTV`: Streaming TV (Yes/No/No internet service)
        - `StreamingMovies`: Streaming movies (Yes/No/No internet service)
        - `Contract`: Contract term (Month-to-month/One year/Two year)
        - `PaperlessBilling`: Paperless billing (Yes/No)
        - `PaymentMethod`: Payment method
        - `MonthlyCharges`: Monthly charges amount
        - `TotalCharges`: Total charges amount
        - `Churn`: Customer churned (Yes/No) - TARGET VARIABLE

        **Note:** Not all columns are required, but `Churn` column is essential for model training.
        """)

with col2:
    st.markdown("### 📊 Dataset Information")

    if st.session_state.data is not None:
        df = st.session_state.data

        col_metric1, col_metric2 = st.columns(2)
        with col_metric1:
            st.metric("Rows", f"{df.shape[0]:,}")
            st.metric("Columns", df.shape[1])
        with col_metric2:
            memory_usage = df.memory_usage(deep=True).sum() / 1024
            if memory_usage < 1024:
                memory_str = f"{memory_usage:.1f} KB"
            else:
                memory_str = f"{memory_usage / 1024:.1f} MB"
            st.metric("Memory Usage", memory_str)
            st.metric("File Name", st.session_state.uploaded_file_name or "N/A")

        st.markdown("**Data Quality:**")

        missing_count = df.isnull().sum().sum()
        if missing_count == 0:
            st.success("✅ No missing values")
        else:
            st.warning(f"⚠️ {missing_count} missing values detected")

        if "Churn" in df.columns:
            st.success("✅ Target column 'Churn' found")
            churn_dist = df["Churn"].value_counts()
            if len(churn_dist) >= 2:
                churn_dict = {k: int(v) for k, v in churn_dist.items()}
                st.info(f"📊 Churn distribution: {churn_dict}")
        else:
            st.error("❌ 'Churn' column not found")

        duplicates = df.duplicated().sum()
        if duplicates == 0:
            st.success("✅ No duplicate rows")
        else:
            st.warning(f"⚠️ {duplicates} duplicate rows found")

    else:
        st.info("Upload a dataset to see information here")

        st.markdown("### 📥 Need Sample Data?")
        st.markdown(
            """
            Don't have a dataset? You can:
            - [Download Telco Customer Churn dataset from Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
            - Use any CSV file with similar customer churn structure
            """
        )

if uploaded_file is not None:
    try:
        with st.spinner("Processing uploaded file..."):
            df = pd.read_csv(uploaded_file)

            if df.empty:
                st.error(
                    "❌ The uploaded file is empty. Please upload a valid CSV file."
                )
            elif len(df.columns) < 2:
                st.error("❌ The dataset must have at least 2 columns.")
            else:
                st.session_state.data = df
                st.session_state.uploaded_file_name = uploaded_file.name

                st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

                st.rerun()

    except UnicodeDecodeError:
        st.error("❌ Error reading file. Please ensure the file is UTF-8 encoded CSV.")
    except pd.errors.EmptyDataError:
        st.error("❌ The uploaded file appears to be empty.")
    except pd.errors.ParserError as e:
        st.error(f"❌ Error parsing CSV file: {str(e)}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")

if st.session_state.data is not None:
    st.markdown("---")
    st.subheader("📋 Dataset Preview & Analysis")

    tab1, tab2, tab3 = st.tabs(
        ["🔍 Data Preview", "📊 Statistical Summary", "🔧 Data Types"]
    )

    with tab1:
        st.markdown("**First 10 rows of your dataset:**")
        st.dataframe(
            st.session_state.data.head(10), use_container_width=True, height=400
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔄 Refresh Preview", help="Reload the dataset preview"):
                st.rerun()

        with col2:
            if st.button("📊 Show Full Dataset", help="Display the complete dataset"):
                st.dataframe(st.session_state.data, use_container_width=True)

        with col3:
            if st.button(
                "🗑️ Remove Dataset", help="Clear the uploaded dataset", type="secondary"
            ):
                st.session_state.data = None
                st.session_state.uploaded_file_name = None
                st.rerun()

    with tab2:
        st.markdown("**Statistical Summary:**")

        numeric_cols = st.session_state.data.select_dtypes(include=["number"]).columns
        categorical_cols = st.session_state.data.select_dtypes(
            include=["object"]
        ).columns

        if len(numeric_cols) > 0:
            st.markdown("*Numerical Features:*")
            st.dataframe(
                st.session_state.data[numeric_cols].describe(), use_container_width=True
            )

        if len(categorical_cols) > 0:
            st.markdown("*Categorical Features:*")
            cat_summary = pd.DataFrame(
                {
                    "Column": categorical_cols,
                    "Unique Values": [
                        st.session_state.data[col].nunique() for col in categorical_cols
                    ],
                    "Most Frequent": [
                        st.session_state.data[col].mode()[0]
                        if len(st.session_state.data[col].mode()) > 0
                        else "N/A"
                        for col in categorical_cols
                    ],
                    "Missing Values": [
                        st.session_state.data[col].isnull().sum()
                        for col in categorical_cols
                    ],
                }
            )
            st.dataframe(cat_summary, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("**Column Information:**")

        column_info = pd.DataFrame(
            {
                "Column Name": st.session_state.data.columns,
                "Data Type": st.session_state.data.dtypes.astype(str),
                "Non-Null Count": st.session_state.data.count(),
                "Null Count": st.session_state.data.isnull().sum(),
                "Unique Values": [
                    st.session_state.data[col].nunique()
                    for col in st.session_state.data.columns
                ],
                "Sample Value": [
                    str(st.session_state.data[col].iloc[0])
                    if len(st.session_state.data) > 0
                    else "N/A"
                    for col in st.session_state.data.columns
                ],
            }
        )

        st.dataframe(column_info, use_container_width=True, hide_index=True)

        st.markdown("**Data Type Distribution:**")
        dtype_counts = st.session_state.data.dtypes.value_counts()
        col1, col2 = st.columns([1, 2])

        with col1:
            for dtype, count in dtype_counts.items():
                st.metric(f"{dtype}", f"{count} columns")

        with col2:
            for dtype in dtype_counts.index:
                cols_of_type = st.session_state.data.select_dtypes(
                    include=[dtype]
                ).columns.tolist()
                st.write(f"**{dtype}:** {', '.join(cols_of_type)}")

    st.markdown("---")

    can_proceed = True
    issues = []

    if "Churn" not in st.session_state.data.columns:
        can_proceed = False
        issues.append("❌ 'Churn' column is missing (required for model training)")

    if len(st.session_state.data) < 100:
        issues.append("⚠️ Dataset has less than 100 rows (recommended: 1000+)")

    if len(issues) > 0:
        st.markdown("**⚠️ Issues Detected:**")
        for issue in issues:
            st.write(issue)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if can_proceed:
            if st.button(
                "➡️ Proceed to Data Preprocessing",
                type="primary",
                use_container_width=True,
                help="Continue to the next step: data preprocessing",
            ):
                st.switch_page("pages/Preprocessing_Data.py")
        else:
            st.button(
                "❌ Cannot Proceed - Fix Issues Above",
                disabled=True,
                use_container_width=True,
                help="Please resolve the issues above before proceeding",
            )

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: var(--text-muted); padding: 2rem;">
        <h4>💡 Pro Tips</h4>
        <p>
            • Ensure your CSV file has proper headers in the first row<br>
            • Check that the 'Churn' column contains 'Yes'/'No' values<br>
            • Remove any unnecessary columns before upload to improve processing speed<br>
            • Verify data quality - missing values will be handled in preprocessing
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

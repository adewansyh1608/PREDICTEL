import streamlit as st

st.set_page_config(page_title="Slider Test - PREDICTEL", page_icon="🎛️", layout="wide")

st.title("🎛️ Slider Functionality Test")

st.markdown("### Testing Slider Value Display")

# Test different slider configurations
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Basic Slider Test**")

    # Test 1: Basic slider
    tenure_value = st.slider("Tenure (months)", 0, 72, 12)
    st.write(f"Current Value: **{tenure_value}** months")

    # Test 2: Slider with format
    charges_value = st.slider("Monthly Charges", 0, 200, 65, format="$%d")
    st.write(f"Current Value: **${charges_value}**")

    # Test 3: Float slider
    rating_value = st.slider("Rating", 0.0, 5.0, 3.5, step=0.1)
    st.write(f"Current Value: **{rating_value:.1f}**")

with col2:
    st.markdown("**Enhanced Slider Test**")

    # Test 4: Slider with columns for value display
    col_slider, col_display = st.columns([3, 1])
    with col_slider:
        age_value = st.slider("Customer Age", 18, 80, 35, key="age_test")
    with col_display:
        st.markdown(f"**{age_value}** years")

    # Test 5: Multiple sliders
    st.markdown("**Service Quality Metrics**")
    internet_speed = st.slider("Internet Speed (Mbps)", 1, 100, 25)
    st.info(f"Speed: {internet_speed} Mbps")

    satisfaction = st.slider("Satisfaction Score", 1, 10, 7)
    st.success(f"Score: {satisfaction}/10")

# Summary section
st.markdown("---")
st.markdown("### 📊 Current Values Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.metric("Tenure", f"{tenure_value} months")
    st.metric("Monthly Charges", f"${charges_value}")

with summary_col2:
    st.metric("Rating", f"{rating_value:.1f}/5.0")
    st.metric("Customer Age", f"{age_value} years")

with summary_col3:
    st.metric("Internet Speed", f"{internet_speed} Mbps")
    st.metric("Satisfaction", f"{satisfaction}/10")

# Test interactive updates
st.markdown("---")
st.markdown("### 🔄 Interactive Update Test")

if st.button("Refresh Values"):
    st.balloons()
    st.success("All values refreshed successfully!")

# Visual feedback
if tenure_value > 36:
    st.success("🎉 Long-term customer!")
elif tenure_value > 12:
    st.info("📈 Established customer")
else:
    st.warning("🆕 New customer - retention focus needed")

# CSS Test
st.markdown(
    """
<style>
/* Test if CSS affects slider visibility */
.stSlider label {
    color: #ffffff !important;
    font-weight: 600 !important;
}

.test-value-display {
    background: #1a1a1a;
    padding: 0.5rem;
    border-radius: 0.5rem;
    border: 1px solid #0ea5e9;
    color: #ffffff;
    text-align: center;
    font-weight: bold;
}
</style>
""",
    unsafe_allow_html=True,
)

# Custom value display
st.markdown(
    f"""
<div class="test-value-display">
    Selected Tenure: {tenure_value} months | Monthly Charges: ${charges_value}
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown(
    "**✅ If you can see all the values clearly, the slider is working correctly!**"
)

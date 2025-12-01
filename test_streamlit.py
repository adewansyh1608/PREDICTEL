import streamlit as st

# Simple Streamlit configuration test
st.set_page_config(page_title="Config Test - PREDICTEL", page_icon="🧪", layout="wide")

st.title("🧪 Streamlit Configuration Test")

st.success("✅ Streamlit is working correctly!")

st.markdown("### Configuration Status")
st.info("If you see this page without warnings, the configuration is clean.")

st.markdown("### Expected Results")
st.markdown("""
- ✅ No config warnings in terminal
- ✅ Dark theme applied correctly
- ✅ Professional appearance
- ✅ All components rendering properly
""")

# Test basic components
col1, col2 = st.columns(2)

with col1:
    st.metric("Test Metric", "100%", "Perfect")
    st.button("Test Button", type="primary")

with col2:
    st.selectbox("Test Selector", ["Option 1", "Option 2"])
    progress_bar = st.progress(0.75)

st.markdown("---")
st.success("🎉 PREDICTEL Configuration Test Completed Successfully!")

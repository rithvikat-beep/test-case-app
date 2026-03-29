import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="Test Case Prioritization", layout="wide")

# Custom CSS (🔥 UI upgrade)
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #667eea, #764ba2);
}
.title {
    text-align: center;
    color: white;
    font-size: 40px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #f0f0f0;
    margin-bottom: 30px;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="title">🧪 Test Case Prioritization</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload CSV & analyze test cases intelligently</p>', unsafe_allow_html=True)

# Upload section
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    file = st.file_uploader("📂 Upload CSV File", type=["csv"])
    st.markdown('</div>', unsafe_allow_html=True)

# Processing
if file is not None:
    try:
        df = pd.read_csv(file)

        required_cols = ["test_case", "execution_time", "failure_history", "coverage"]
        missing = [col for col in required_cols if col not in df.columns]

        if missing:
            st.error(f"❌ Missing columns: {', '.join(missing)}")
        else:
            df["priority_score"] = (
                df["failure_history"] * 0.5 +
                df["coverage"] * 0.3 -
                df["execution_time"] * 0.2
            )

            df = df.sort_values(by="priority_score", ascending=False)

            # Metrics (🔥 looks professional)
            st.markdown("### 📊 Summary")
            col1, col2, col3 = st.columns(3)

            col1.metric("Total Test Cases", len(df))
            col2.metric("Top Priority Score", round(df["priority_score"].max(), 2))
            col3.metric("Lowest Priority Score", round(df["priority_score"].min(), 2))

            # Table
            st.markdown("### 📋 Prioritized Results")
            st.dataframe(df, use_container_width=True)

            # Download button (🔥 extra marks)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Results",
                csv,
                "prioritized_test_cases.csv",
                "text/csv"
            )

            st.success("✅ Analysis Completed Successfully")

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

import streamlit as st
import pandas as pd

# ✅ Page config
st.set_page_config(page_title="Test Case Prioritization", layout="wide")

# ✅ Dark UI + styling
st.markdown("""
<style>
/* Hide default header/footer */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Background */
.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

/* Text */
h1, h2, h3, h4, h5, h6, p, div {
    color: white !important;
}

/* Card style */
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.3);
}

/* Buttons */
.stButton>button {
    background-color: #3b82f6;
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    font-size: 16px;
    border: none;
}
.stButton>button:hover {
    background-color: #2563eb;
}

/* File uploader */
.stFileUploader {
    background-color: #111827;
    padding: 15px;
    border-radius: 10px;
}

/* Table */
.stDataFrame {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# 🎯 Title
st.markdown("<h1 style='text-align:center;'>🧪 Test Case Prioritization System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload your dataset or follow the sample format below</p>", unsafe_allow_html=True)

# 📌 Sample Data
sample_data = pd.DataFrame({
    "Test Case": ["Login", "Signup", "Payment"],
    "Execution Time": [5, 4, 6],
    "Failure History": [3, 1, 5],
    "Coverage": [80, 70, 90]
})

st.markdown("### 📌 Sample CSV Format")
st.dataframe(sample_data, use_container_width=True)

# 📥 Download sample
csv_sample = sample_data.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Sample CSV", csv_sample, "sample.csv")

# 📂 Upload
st.markdown("### 📂 Upload Your CSV")
uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

# 🚀 Process
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.markdown("### 📊 Uploaded Data")
    st.dataframe(df, use_container_width=True)

    required_cols = ["Execution Time", "Failure History", "Coverage"]

    if all(col in df.columns for col in required_cols):

        # 🎯 Priority calculation
        df["Priority Score"] = (
            0.5 * df["Failure History"] +
            0.3 * df["Coverage"] -
            0.2 * df["Execution Time"]
        )

        df = df.sort_values(by="Priority Score", ascending=False)

        # 📊 Metrics
        st.markdown("### 📈 Summary")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Test Cases", len(df))
        col2.metric("Max Score", round(df["Priority Score"].max(), 2))
        col3.metric("Min Score", round(df["Priority Score"].min(), 2))

        # 🏆 Highlight top test case
        top_case = df.iloc[0]["Test Case"]
        st.success(f"🏆 Top Priority Test Case: {top_case}")

        # 📋 Results
        st.markdown("### 🚀 Prioritized Results")
        st.dataframe(df, use_container_width=True)

        # 📥 Download results
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results", csv, "prioritized_results.csv")

    else:
        st.error("❌ CSV must contain: Execution Time, Failure History, Coverage")

else:
    st.info("👆 Upload your CSV file to begin")

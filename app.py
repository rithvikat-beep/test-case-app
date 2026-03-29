import streamlit as st
import pandas as pd

# ✅ Page config
st.set_page_config(page_title="Test Case Prioritization", layout="wide")

# ✅ DARK UI FIX (no white text issue)
st.markdown("""
<style>

/* Hide header/footer */
header {visibility: hidden;}
footer {visibility: hidden;}

/* App background */
.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
}

/* Headings */
h1, h2, h3 {
    color: white;
}

/* Normal text */
p, label {
    color: #e5e7eb !important;
}

/* Table fix */
[data-testid="stDataFrame"] {
    background-color: #111827 !important;
}

[data-testid="stDataFrame"] div {
    color: #e5e7eb !important;
}

/* File uploader fix */
section[data-testid="stFileUploader"] {
    background-color: #111827;
    border-radius: 10px;
    padding: 10px;
}

section[data-testid="stFileUploader"] * {
    color: #e5e7eb !important;
}

/* Buttons */
.stButton>button {
    background-color: #3b82f6;
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    font-size: 15px;
    border: none;
}
.stButton>button:hover {
    background-color: #2563eb;
}

/* Download button */
.stDownloadButton>button {
    background-color: #10b981;
    color: white;
}

/* Info / alert */
.stAlert {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# 🎯 Title
st.markdown("<h1 style='text-align:center;'>🧪 Test Case Prioritization System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload your CSV or follow the sample format</p>", unsafe_allow_html=True)

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

# 🚀 Processing
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.markdown("### 📊 Uploaded Data")
    st.dataframe(df, use_container_width=True)

    required_cols = ["Execution Time", "Failure History", "Coverage"]

    if all(col in df.columns for col in required_cols):

        # Priority calculation
        df["Priority Score"] = (
            0.5 * df["Failure History"] +
            0.3 * df["Coverage"] -
            0.2 * df["Execution Time"]
        )

        df = df.sort_values(by="Priority Score", ascending=False)

        # Metrics
        st.markdown("### 📈 Summary")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Cases", len(df))
        col2.metric("Max Score", round(df["Priority Score"].max(), 2))
        col3.metric("Min Score", round(df["Priority Score"].min(), 2))

        # Top case
        st.success(f"🏆 Top Priority: {df.iloc[0]['Test Case']}")

        # Results
        st.markdown("### 🚀 Prioritized Results")
        st.dataframe(df, use_container_width=True)

        # Download results
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results", csv, "results.csv")

    else:
        st.error("❌ CSV must contain: Execution Time, Failure History, Coverage")

else:
    st.info("👆 Upload your CSV file to begin")

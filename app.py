import streamlit as st
import pandas as pd

# ✅ Page config
st.set_page_config(page_title="Test Case Prioritization", layout="wide")

# ✅ FINAL UI FIX (dark outside + white inside)
st.markdown("""
<style>

/* Hide default header/footer */
header {visibility: hidden;}
footer {visibility: hidden;}

/* 🌑 Dark background */
.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
}

/* 🔥 Headings */
h1 {
    color: #ffffff !important;
    font-weight: 800 !important;
    text-align: center;
}

h2, h3 {
    color: #e5e7eb !important;
    font-weight: 700 !important;
}

/* Text outside */
p, label {
    color: #d1d5db !important;
}

/* 📊 TABLE - white box + dark text */
[data-testid="stDataFrame"] {
    background-color: white !important;
    border-radius: 10px;
}

[data-testid="stDataFrame"] div {
    color: #111827 !important;
    font-weight: 600;
}

/* 📂 FILE UPLOADER - white box */
section[data-testid="stFileUploader"] {
    background-color: white !important;
    border-radius: 10px;
    padding: 12px;
}

/* 🔥 Fix uploader text + filename */
section[data-testid="stFileUploader"] * {
    color: #111827 !important;
    font-weight: 600;
}

/* Specifically fix uploaded file name */
section[data-testid="stFileUploader"] span {
    color: #111827 !important;
    font-weight: 700 !important;
}

/* Inputs */
input, textarea {
    background-color: white !important;
    color: black !important;
}

/* Buttons */
.stButton>button {
    background-color: #3b82f6;
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
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

/* Alerts */
.stAlert {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# 🎯 Title
st.markdown("<h1>🧪 Test Case Prioritization System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload your CSV or follow the sample format below</p>", unsafe_allow_html=True)

# 📌 Sample Data
sample_data = pd.DataFrame({
    "Test Case": ["Login", "Signup", "Payment"],
    "Execution Time": [5, 4, 6],
    "Failure History": [3, 1, 5],
    "Coverage": [80, 70, 90]
})

st.markdown("## 📌 Sample CSV Format")
st.dataframe(sample_data, use_container_width=True)

# 📥 Download sample
csv_sample = sample_data.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Sample CSV", csv_sample, "sample.csv")

# 📂 Upload
st.markdown("## 📂 Upload Your CSV")
uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

# 🚀 Processing
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.markdown("## 📊 Uploaded Data")
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
        st.markdown("## 📈 Summary")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Cases", len(df))
        col2.metric("Max Score", round(df["Priority Score"].max(), 2))
        col3.metric("Min Score", round(df["Priority Score"].min(), 2))

        # 🏆 Highlight
        st.success(f"🏆 Top Priority: {df.iloc[0]['Test Case']}")

        # 📋 Results
        st.markdown("## 🚀 Prioritized Results")
        st.dataframe(df, use_container_width=True)

        # 📥 Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results", csv, "results.csv")

    else:
        st.error("❌ CSV must contain: Execution Time, Failure History, Coverage")

else:
    st.info("👆 Upload your CSV file to begin")

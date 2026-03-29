import streamlit as st
import pandas as pd

# ✅ Page config
st.set_page_config(page_title="Test Case Prioritization", layout="wide")

# ✅ FINAL DARK UI — centered title, visible inputs & buttons
st.markdown("""
<style>
/* Hide header/footer */
header {visibility: hidden;}
footer {visibility: hidden;}

/* 🌑 App background */
.stApp {
    background: linear-gradient(to right, #0f172a, #020617);
}

/* 📝 Headings — CENTERED */
h1 {
    color: #ffffff !important;
    font-weight: 800 !important;
    text-align: center !important;
}
h2, h3 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* Text */
p, label, span, div {
    color: #e2e8f0 !important;
}

/* ───────────────────────────────────────────
   🔍 Search / Text Input  — dark bg, white text
─────────────────────────────────────────── */
input[type="text"],
input[type="search"],
.stTextInput input,
[data-testid="stTextInput"] input {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
    caret-color: #38bdf8 !important;
}

input[type="text"]::placeholder,
input[type="search"]::placeholder,
.stTextInput input::placeholder {
    color: #94a3b8 !important;
}

/* ───────────────────────────────────────────
   🔥 File Uploader — dark, no white boxes
─────────────────────────────────────────── */
.stFileUploader,
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] > div,
[data-testid="stFileUploader"] section {
    background-color: #0f172a !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #0f172a !important;
    color: #e2e8f0 !important;
    border: 2px dashed #475569 !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color: #38bdf8 !important;
    font-weight: 600 !important;
}

/* Browse files button inside uploader */
[data-testid="stFileUploaderDropzone"] button {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
}

/* ───────────────────────────────────────────
   📊 DataFrame / Table
─────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    background-color: #020617 !important;
    color: white !important;
}

/* ───────────────────────────────────────────
   🔘 Generic Buttons (Prioritize, etc.)
─────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(90deg, #3b82f6, #6366f1) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
.stButton > button:hover {
    opacity: 0.9;
}

/* Secondary / outline buttons */
button[kind="secondary"] {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
}

/* ───────────────────────────────────────────
   📥 Download Buttons
─────────────────────────────────────────── */
.stDownloadButton > button {
    background: linear-gradient(90deg, #10b981, #22c55e) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ───────────────────────────────────────────
   📊 Metric cards
─────────────────────────────────────────── */
[data-testid="stMetric"] {
    background-color: #1e293b !important;
    border-radius: 12px !important;
    padding: 16px !important;
    border: 1px solid #334155 !important;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}
[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
}

/* ───────────────────────────────────────────
   ✅ Info / Success / Error boxes
─────────────────────────────────────────── */
[data-testid="stAlert"] {
    background-color: #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# 🎯 Title — centered via CSS above
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

        # 🏆 Top case
        st.success(f"🏆 Top Priority: {df.iloc[0]['Test Case']}")

        # 📋 Results
        st.markdown("## 🚀 Prioritized Results")
        st.dataframe(df, use_container_width=True)

        # 📥 Download results
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results", csv, "results.csv")
    else:
        st.error("❌ CSV must contain: Execution Time, Failure History, Coverage")
else:
    st.info("👆 Upload your CSV file to begin")

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Test Case Prioritization", layout="wide")

st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: linear-gradient(to right, #0f172a, #020617);
}

h1 {
    color: #ffffff !important;
    font-weight: 800 !important;
    text-align: center !important;
}
h2, h3 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

p, label, span, div {
    color: #e2e8f0 !important;
}

/* ═══════════════════════════════════════════
   🔍 DATAFRAME HOVER TOOLBAR
   (Search + Fullscreen + Download icons)
   Appears top-right when hovering a table
═══════════════════════════════════════════ */

/* Toolbar container */
[data-testid="stElementToolbar"] {
    background-color: #1e293b !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
    padding: 2px 4px !important;
}

/* Each icon button in the toolbar */
[data-testid="stElementToolbarButton"] > button,
[data-testid="stElementToolbar"] button {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    border: none !important;
    border-radius: 6px !important;
}

[data-testid="stElementToolbarButton"] > button:hover,
[data-testid="stElementToolbar"] button:hover {
    background-color: #334155 !important;
}

/* SVG icons inside toolbar buttons — make them white */
[data-testid="stElementToolbarButton"] svg,
[data-testid="stElementToolbar"] svg {
    fill: #f1f5f9 !important;
    color: #f1f5f9 !important;
}
[data-testid="stElementToolbarButton"] svg path,
[data-testid="stElementToolbar"] svg path,
[data-testid="stElementToolbarButton"] svg rect,
[data-testid="stElementToolbar"] svg rect {
    fill: #f1f5f9 !important;
    stroke: #f1f5f9 !important;
}

/* 🔍 Search INPUT that opens when clicking search icon */
[data-testid="stElementToolbar"] input,
[data-testid="stElementToolbarButton"] input,
[data-testid="stDataFrame"] input[type="text"],
[data-testid="stDataFrameResizable"] input[type="text"],
input[aria-label="Search"],
input[placeholder="Search…"],
input[placeholder="Search"] {
    background-color: #0f172a !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
    border-radius: 6px !important;
    caret-color: #38bdf8 !important;
    outline: none !important;
}
input[aria-label="Search"]::placeholder,
input[placeholder="Search…"]::placeholder {
    color: #64748b !important;
}

/* ═══════════════════════════════════════════
   📊 FULLSCREEN MODAL — dark background
═══════════════════════════════════════════ */
[data-testid="stFullScreenFrame"],
[data-testid="stFullScreenFrame"] > div,
.fullscreen-container {
    background-color: #0f172a !important;
    color: #f1f5f9 !important;
}

/* ═══════════════════════════════════════════
   🔥 File Uploader
═══════════════════════════════════════════ */
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

[data-testid="stFileUploaderDropzone"] button {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
}

/* ═══════════════════════════════════════════
   📊 DataFrame table
═══════════════════════════════════════════ */
[data-testid="stDataFrame"],
[data-testid="stDataFrameResizable"] {
    background-color: #0f172a !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ═══════════════════════════════════════════
   🔘 Buttons
═══════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(90deg, #3b82f6, #6366f1) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
.stButton > button:hover { opacity: 0.9; }

button[kind="secondary"] {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
}

.stDownloadButton > button {
    background: linear-gradient(90deg, #10b981, #22c55e) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ═══════════════════════════════════════════
   📊 Metric cards
═══════════════════════════════════════════ */
[data-testid="stMetric"] {
    background-color: #1e293b !important;
    border-radius: 12px !important;
    padding: 16px !important;
    border: 1px solid #334155 !important;
}
[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; }

/* ═══════════════════════════════════════════
   ✅ Alerts
═══════════════════════════════════════════ */
[data-testid="stAlert"] {
    background-color: #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
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

csv_sample = sample_data.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Sample CSV", csv_sample, "sample.csv")

st.markdown("## 📂 Upload Your CSV")
uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.markdown("## 📊 Uploaded Data")
    st.dataframe(df, use_container_width=True)

    required_cols = ["Execution Time", "Failure History", "Coverage"]
    if all(col in df.columns for col in required_cols):
        df["Priority Score"] = (
            0.5 * df["Failure History"] +
            0.3 * df["Coverage"] -
            0.2 * df["Execution Time"]
        )
        df = df.sort_values(by="Priority Score", ascending=False)

        st.markdown("## 📈 Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cases", len(df))
        col2.metric("Max Score", round(df["Priority Score"].max(), 2))
        col3.metric("Min Score", round(df["Priority Score"].min(), 2))

        st.success(f"🏆 Top Priority: {df.iloc[0]['Test Case']}")

        st.markdown("## 🚀 Prioritized Results")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results", csv, "results.csv")
    else:
        st.error("❌ CSV must contain: Execution Time, Failure History, Coverage")
else:
    st.info("👆 Upload your CSV file to begin")

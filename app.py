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

/* Hide Streamlit's built-in dataframe toolbar completely */
[data-testid="stElementToolbar"] {
    display: none !important;
}

/* File Uploader */
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

/* Search input */
.stTextInput input {
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
    caret-color: #38bdf8 !important;
}
.stTextInput input::placeholder {
    color: #64748b !important;
}

/* DataFrame */
[data-testid="stDataFrame"],
[data-testid="stDataFrameResizable"] {
    background-color: #0f172a !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #3b82f6, #6366f1) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
.stButton > button:hover { opacity: 0.9; }

.stDownloadButton > button {
    background: linear-gradient(90deg, #10b981, #22c55e) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #1e293b !important;
    border-radius: 12px !important;
    padding: 16px !important;
    border: 1px solid #334155 !important;
}
[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; }

/* Alerts */
[data-testid="stAlert"] {
    background-color: #1e293b !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)


def show_table(df, label=""):
    """Show dataframe with custom Search + Expand controls."""
    st.markdown(f"#### {label}" if label else "", unsafe_allow_html=True)

    # Controls row: Search + Expand
    col_search, col_expand = st.columns([5, 1])
    with col_search:
        search = st.text_input("", placeholder="🔍 Search...", key=f"search_{label}", label_visibility="collapsed")
    with col_expand:
        expand = st.toggle("⛶ Expand", key=f"expand_{label}")

    # Filter rows
    filtered = df.copy()
    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
        filtered = df[mask]

    # Show table — tall if expanded
    height = 600 if expand else 250
    st.dataframe(filtered, use_container_width=True, height=height)


# ─── Title ───────────────────────────────────────
st.markdown("<h1>🧪 Test Case Prioritization System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload your CSV or follow the sample format below</p>", unsafe_allow_html=True)

# ─── Sample Data ─────────────────────────────────
sample_data = pd.DataFrame({
    "test_case": ["Login_Test", "Signup_Test", "Payment_Test", "Search_Test", "Profile_Update"],
    "execution_time": [5, 4, 6, 3, 4],
    "failure_history": [3, 1, 5, 0, 2],
    "coverage": [85, 70, 90, 60, 75]
})

st.markdown("## 📌 Sample CSV Format")
show_table(sample_data, "Sample Data")

csv_sample = sample_data.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Sample CSV", csv_sample, "sample.csv")

# ─── Upload ──────────────────────────────────────
st.markdown("## 📂 Upload Your CSV")
uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.markdown("## 📊 Uploaded Data")
    show_table(df, "Uploaded Data")

    required_cols = ["execution_time", "failure_history", "coverage"]
    if all(col in df.columns for col in required_cols):
        df["Priority Score"] = (
            0.5 * df["failure_history"] +
            0.3 * df["coverage"] -
            0.2 * df["execution_time"]
        )
        df = df.sort_values(by="Priority Score", ascending=False)

        st.markdown("## 📈 Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cases", len(df))
        col2.metric("Max Score", round(df["Priority Score"].max(), 2))
        col3.metric("Min Score", round(df["Priority Score"].min(), 2))

        st.success(f"🏆 Top Priority: {df.iloc[0]['test_case']}")

        st.markdown("## 🚀 Prioritized Results")
        show_table(df, "Prioritized Results")

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results", csv, "results.csv")
    else:
        st.error("❌ CSV must contain: execution_time, failure_history, coverage")
else:
    st.info("👆 Upload your CSV file to begin")

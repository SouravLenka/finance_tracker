import streamlit as st
from pathlib import Path

from pdf_processing.extractor import extract_transactions
from llm.categorizer import categorize_transaction
from analysis.analytics_engine import compute_metrics
from visualization.dashboard import show_dashboard


# ------------------ PAGE STYLING ------------------
st.set_page_config(layout="wide")
st.title("AI Personal Finance Tracker")

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #ffffff;
}
section[data-testid="stSidebar"] {
    background-color: #161a23;
}
.stAlert {
    border-radius: 12px;
}
[data-testid="stDataFrame"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ------------------ SIDEBAR ------------------
st.sidebar.header("⚙️ Settings")

monthly_budget = st.sidebar.number_input(
    "Set Monthly Budget (₹)",
    min_value=1000,
    max_value=100000,
    value=5000,
    step=500
)


# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader(
    "Upload PhonePe Statement (PDF or DOCX)",
    type=["pdf", "docx"]
)

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1].lower()
    temp_path = Path(f"temp_statement.{ext}")

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully ✅")

    if st.button("Process Bank Statement"):
        with st.spinner("Extracting transactions..."):
            raw_transactions = extract_transactions(str(temp_path))

        if not raw_transactions:
            st.error("❌ No transactions could be extracted from this statement.")
            st.stop()

        # ------------------ APPLY CATEGORIZATION ------------------
        transactions = []
        for t in raw_transactions:
            transactions.append({
                "date": t["date"],
                "description": t["description"],
                "amount": t["amount"],
                "category": categorize_transaction(t["description"])
            })

        st.success(f"Extracted {len(transactions)} transactions 📄")

        # ------------------ ANALYTICS ------------------
        metrics = compute_metrics(transactions, monthly_budget)

        # ------------------ AI INSIGHTS (TEMP DISABLED) ------------------
        insights = {
            "summary": "AI adviser is disabled (local-only mode).",
            "warnings": [],
            "recommendations": []
        }

        # ------------------ DASHBOARD ------------------
        show_dashboard(transactions, metrics, insights)

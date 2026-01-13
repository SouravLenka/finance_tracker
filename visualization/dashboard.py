import streamlit as st
import pandas as pd
import plotly.express as px


def show_dashboard(transactions, metrics, insights):
    df = pd.DataFrame(transactions)

    st.header("📊 Personal Finance Dashboard")

    # ------------------ SUMMARY CARDS ------------------
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Total Income", f"₹ {metrics['total_income']}")
    c2.metric("💸 Total Expense", f"₹ {metrics['total_expense']}")
    c3.metric("💾 Savings", f"₹ {metrics['savings']}")

    st.info(metrics["budget_alert"])
    st.divider()

    # ------------------ CATEGORY PIE ------------------
    st.subheader("📌 Spending by Category")

    cat_df = (
        df[df["amount"] < 0]
        .groupby("category")["amount"]
        .sum()
        .abs()
        .reset_index()
    )

    if cat_df.empty:
        st.info("📌 No expense data available to display category breakdown.")
    else:
        fig_pie = px.pie(
            cat_df,
            names="category",
            values="amount",
            hole=0.45
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.caption("This chart shows how your expenses are distributed across categories.")

    # ------------------ CATEGORY BAR ------------------
    st.subheader("📦 Category-wise Expense Comparison")

    if cat_df.empty:
        st.info("📦 Not enough expense data to compare categories.")
    else:
        fig_bar = px.bar(
            cat_df,
            x="category",
            y="amount",
            color="category"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.caption("Compare spending amounts between different categories.")

    st.divider()

    # ------------------ TRANSACTION TABLE ------------------
    st.subheader("📄 All Transactions")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # ------------------ AI / LOCAL ADVISOR ------------------
    st.subheader("🤖 Financial Advisor")

    st.caption(
        "Advice below is generated locally based on your spending patterns "
        "and does not require any external AI service."
    )

    with st.container(border=True):
        st.markdown("### 🧠 Summary")
        st.write(insights.get("summary", "No summary available."))

        if insights.get("warnings"):
            st.markdown("### ⚠️ Warnings")
            for w in insights["warnings"]:
                st.warning(w)

        if insights.get("recommendations"):
            st.markdown("### 💡 Recommendations")
            for r in insights["recommendations"]:
                st.success(r)

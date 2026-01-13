import pandas as pd


def compute_metrics(transactions: list, monthly_budget: int) -> dict:
    """
    Computes financial metrics from structured transactions.
    """

    df = pd.DataFrame(transactions)

    if df.empty:
        return {}

    # ------------------ CLEAN DATA ------------------
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount", "date"])

    # ------------------ DATE PARSING ------------------
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # ------------------ PERIOD ------------------
    start_date = df["date"].min().date()
    end_date = df["date"].max().date()

    # ------------------ MONTH COLUMN ------------------
    df["month"] = df["date"].dt.to_period("M").astype(str)

    # ------------------ SPLIT ------------------
    income_df = df[df["amount"] > 0]
    expense_df = df[df["amount"] < 0]

    # ------------------ TOTALS ------------------
    total_income = income_df["amount"].sum()
    total_expense = expense_df["amount"].abs().sum()

    savings = total_income - total_expense

    # ✅ NEW METRIC
    total_money_handled = total_income + total_expense

    # ------------------ CATEGORY BREAKDOWN ------------------
    category_breakdown = (
        expense_df
        .groupby("category")["amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
        .to_dict()
    )

    # ------------------ MONTHLY EXPENSE ------------------
    monthly_expense = (
        expense_df
        .groupby("month")["amount"]
        .sum()
        .abs()
        .to_dict()
    )

    # ------------------ BUDGET ALERT ------------------
    latest_month = max(monthly_expense.keys(), default=None)
    latest_spending = monthly_expense.get(latest_month, 0)

    if latest_month is None:
        budget_alert = "ℹ️ Not enough data to evaluate budget."
    elif latest_spending > monthly_budget:
        budget_alert = (
            f"⚠️ Budget Alert: You spent ₹{latest_spending:.2f} in {latest_month}, "
            f"exceeding your budget of ₹{monthly_budget}."
        )
    else:
        budget_alert = (
            f"✅ Budget OK: ₹{latest_spending:.2f} spent in {latest_month} "
            f"out of ₹{monthly_budget} budget."
        )

    # ------------------ FINAL OUTPUT ------------------
    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "total_money_handled": round(total_money_handled, 2),  # 👈 NEW
        "savings": round(savings, 2),
        "category_breakdown": category_breakdown,
        "monthly_expense": monthly_expense,
        "budget_alert": budget_alert,
        "period": f"{start_date} → {end_date}"
    }

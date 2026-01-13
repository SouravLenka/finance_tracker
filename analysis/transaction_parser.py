import re
from pathlib import Path
from datetime import datetime
from llm.categorizer import categorize_transaction
from rag.rag_categorizer import rag_categorize

RAW_TEXT_PATH = Path("data/extracted/raw_text.txt")

DATE_PATTERN = re.compile(
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}"
)

AMOUNT_PATTERN = re.compile(r"₹\s*([\d,]+(?:\.\d+)?)")


def parse_phonepe_statement():
    if not RAW_TEXT_PATH.exists():
        raise FileNotFoundError("raw_text.txt not found. Run extractor first.")

    text = RAW_TEXT_PATH.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    transactions = []
    i = 0

    while i < len(lines):
        date_match = DATE_PATTERN.search(lines[i])

        if date_match:
            raw_date = date_match.group(0)

            # ✅ Convert to clean ISO date
            clean_date = datetime.strptime(raw_date, "%b %d, %Y").strftime("%Y-%m-%d")

            description = ""
            txn_type = None
            amount = None

            for j in range(i + 1, min(i + 10, len(lines))):
                line = lines[j].lower()

                if "paid to" in line or "received from" in line:
                    description = lines[j]

                if "debit" in line:
                    txn_type = "DEBIT"
                elif "credit" in line:
                    txn_type = "CREDIT"

                amt_match = AMOUNT_PATTERN.search(lines[j])
                if amt_match:
                    amount = float(amt_match.group(1).replace(",", ""))

            if description and txn_type and amount is not None:
                signed_amount = -amount if txn_type == "DEBIT" else amount

                transactions.append({
                    "date": clean_date,  # 🔥 CLEAN DATE ONLY
                    "description": description,
                    "amount": signed_amount,
                    "type": txn_type,
                    "category": categorize_transaction(description)
                })

            i += 8
        else:
            i += 1

    return transactions

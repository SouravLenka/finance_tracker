import pdfplumber
from docx import Document
import re
from pathlib import Path


# ---------------- REGEX ----------------
DATE_RE = re.compile(
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}",
    re.IGNORECASE
)

AMOUNT_RE = re.compile(
    r"(Debit|Credit)\s+INR\s+([\d,]+\.\d{2})",
    re.IGNORECASE
)

TIME_RE = re.compile(r"\d{1,2}:\d{2}\s?(AM|PM)", re.IGNORECASE)


# ---------------- CORE PARSER ----------------
def parse_phonepe_lines(lines):
    transactions = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Detect date (transaction start)
        date_match = DATE_RE.match(line)
        if not date_match:
            i += 1
            continue

        date = date_match.group(0)

        # Skip optional time line
        j = i + 1
        if j < len(lines) and TIME_RE.match(lines[j]):
            j += 1

        # Description line
        if j >= len(lines):
            i += 1
            continue

        description = lines[j].strip()

        # Look ahead for amount
        amount = None
        txn_type = None

        k = j
        while k < min(j + 8, len(lines)):
            amt_match = AMOUNT_RE.search(lines[k])
            if amt_match:
                txn_type = amt_match.group(1).lower()
                amount = float(amt_match.group(2).replace(",", ""))
                break
            k += 1

        if amount is not None:
            transactions.append({
                "date": date,
                "description": description,
                "amount": amount if txn_type == "credit" else -amount
            })

        i = k + 1

    return transactions


# ---------------- DOCX ----------------
def extract_from_docx(path: Path):
    doc = Document(path)
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    lines = text.split("\n")
    return parse_phonepe_lines(lines)


# ---------------- PDF ----------------
def extract_from_pdf(path: Path):
    all_lines = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_lines.extend(text.split("\n"))

    return parse_phonepe_lines(all_lines)


# ---------------- PUBLIC API ----------------
def extract_transactions(file_path: str):
    """
    Main extractor used by app.py
    Returns: list[dict]
    """

    path = Path(file_path)

    if not path.exists():
        return []

    if path.suffix.lower() == ".pdf":
        return extract_from_pdf(path)

    if path.suffix.lower() == ".docx":
        return extract_from_docx(path)

    return []

markdown

# 💰 AI Personal Finance Tracker

A **local-first, privacy-preserving personal finance analysis tool** that processes **PhonePe bank statements (PDF / DOCX)** and converts them into **structured transactions, financial insights, and interactive dashboards**.

> ⚠️ Your financial data never leaves your system.

## 🚀 Features

- 📄 Upload PhonePe PDF or DOCX statements
- 🔍 Accurate transaction extraction
- 🧾 Smart merchant-based categorization
- 📊 Interactive financial dashboards
- 💰 Income, expense, savings & money-handled metrics
- ⚠️ Monthly budget alerts
- 🌓 Clean, dark-themed UI
- 🔐 Fully local & private

## 🧠 How It Works

Upload Statement
↓
Text Extraction Engine
↓
Transaction Structuring
↓
Rule-based Categorization
↓
Analytics Engine
↓
Interactive Dashboard

## 📂 Project Structure

finance_tracker/
│
├── app.py # Streamlit app entry point
│
├── pdf_processing/
│ └── extractor.py # PDF/DOCX transaction extraction
│
├── analysis/
│ ├── categorizer.py # Merchant → category mapping
│ ├── analytics_engine.py # Financial calculations
│ └── insights.py # AI advice layer (optional / local)
│
├── visualization/
│ └── dashboard.py # Charts & UI
│
├── data/
│ └── uploaded_pdfs/ # Temporary uploads
│
├── requirements.txt
└── README.md

## 📊 Financial Metrics Calculated

- **Total Income**
- **Total Expense**
- **Savings**
- **Total Money Handled**
- **Category-wise spending**
- **Monthly expense trends**
- **Budget status alerts**

---

## 🧾 Supported Categories

- Food & Grocery
- Online Shopping
- Offline Shopping
- Transport & Travel
- Bills & Subscriptions
- Education
- Accommodation
- Entertainment
- Healthcare
- Income
- Personal Transfers
- Other (fallback)

Categories are derived using **real merchant patterns** from the statement.

---

## 🔐 Privacy First

- ✅ No cloud upload
- ✅ No OCR
- ✅ No external APIs required
- ✅ Works fully offline
- ❌ No sensitive data leaves your machine

---

## 🖥️ Tech Stack

- **Python 3.10+**
- **Streamlit** – UI
- **pdfplumber** – PDF text extraction
- **python-docx** – DOCX support
- **Pandas** – Data processing
- **Plotly** – Visualizations

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/souravlenka/finance-tracker.git
cd finance-tracker
```

### 2️⃣ Create Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App

```bash
python -m streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 🧪 Supported Statement Types

| Format                   | Status     |
| ------------------------ | ---------- |
| PhonePe PDF (text-based) | ✅         |
| PhonePe DOCX             | ✅         |
| Scanned PDFs (images)    | ❌         |
| Other banks              | 🚧 Planned |

---

## 🤖 AI Adviser (Optional)

- Currently **disabled by default**
- Can be upgraded to:
  - Local LLM (Ollama / LM Studio)
  - OpenAI (with API key)

- Designed for financial advice only, not extraction

---

## 📌 Roadmap

- 🔄 RAG-based smart categorization
- 🤖 Local LLM financial adviser
- 📤 Export reports (CSV / PDF)
- 🏦 Multi-bank support
- ☁️ Optional Streamlit Cloud deployment

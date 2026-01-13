from langchain_openai import ChatOpenAI
from openai import OpenAIError
from rag.merchant_store import get_cached_category, cache_category

ALLOWED_CATEGORIES = [
    "Food & Grocery",
    "Online Shopping",
    "Shopping",
    "Transport",
    "Bills & Subscriptions",
    "Education",
    "Accommodation",
    "Entertainment",
    "Healthcare",
    "Income",
    "Personal Transfers",
    "Other"
]


def rag_categorize(description: str) -> str:
    merchant = description.strip().lower()

    # 1️⃣ Check local cache
    cached = get_cached_category(merchant)
    if cached:
        return cached

    # 2️⃣ LLM fallback (STRICT)
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        prompt = f"""
You are a financial transaction classifier.

Transaction description:
"{description}"

Choose EXACTLY ONE category from this list:
{ALLOWED_CATEGORIES}

Rules:
- Do NOT invent new categories
- Do NOT explain
- Return ONLY the category name
"""

        response = llm.invoke(prompt)
        category = response.content.strip()

        if category in ALLOWED_CATEGORIES:
            cache_category(merchant, category)
            return category

    except OpenAIError:
        pass

    return "Other"

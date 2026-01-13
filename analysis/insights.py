import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def build_prompt(metrics: dict) -> str:
    return f"""
You are a personal finance advisor.

Here is the user's financial summary:

Total Income: ₹{metrics['total_income']}
Total Expense: ₹{metrics['total_expense']}
Savings: ₹{metrics['savings']}

Category-wise spending:
{json.dumps(metrics.get('category_breakdown', {}), indent=2)}

Monthly expense:
{json.dumps(metrics.get('monthly_expense', {}), indent=2)}

Your task:
- Analyze the spending behavior
- Identify risks or overspending
- Suggest practical improvements

Return STRICT JSON in this format:
{{
  "summary": "short paragraph",
  "warnings": ["warning 1", "warning 2"],
  "recommendations": ["tip 1", "tip 2", "tip 3"]
}}

Rules:
- Do NOT include explanations
- Do NOT include markdown
- Output JSON only
"""


def call_ollama(prompt: str) -> dict:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()

    text = response.json().get("response", "").strip()
    return json.loads(text)


def local_fallback(metrics: dict) -> dict:
    warnings = []
    recommendations = []

    if metrics["total_expense"] > metrics["total_income"]:
        warnings.append("You are spending more than your income.")

    if metrics["savings"] < 0:
        warnings.append("Negative savings detected.")

    if metrics.get("category_breakdown"):
        top_category = max(metrics["category_breakdown"], key=metrics["category_breakdown"].get)
        recommendations.append(f"Consider reducing spending in '{top_category}' category.")

    if not recommendations:
        recommendations.append("Your spending appears balanced. Keep tracking regularly.")

    return {
        "summary": "This advice was generated locally using rule-based analysis.",
        "warnings": warnings,
        "recommendations": recommendations
    }


def generate_insights(metrics: dict) -> dict:
    prompt = build_prompt(metrics)

    try:
        return call_ollama(prompt)
    except Exception:
        # Safe local fallback (never crashes UI)
        return local_fallback(metrics)

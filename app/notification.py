from typing import Dict, Any


def build_push_message(analysis: Dict[str, Any]) -> str:
    parts = []

    oos = analysis.get("out_of_stock", [])
    if oos:
        items = ", ".join([f"{r['product_id']} ({r['variant']})" for r in oos])
        parts.append(f"You're running out of stock on {items}. Please replenish your stock.")

    if analysis.get("zero_purchases_2w"):
        parts.append("No purchases in the last 2 weeks — consider re-engaging customers or running a promotion.")

    suggestions = analysis.get("portfolio_suggestions", [])
    if suggestions:
        suggs = []
        for s in suggestions:
            suggs.append(f"{s['product_id']}: {', '.join(s.get('missing_variants', []))}")
        parts.append(f"Consider adding variants to your portfolio: {'; '.join(suggs)}.")

    if not parts:
        return "No action needed."

    # Join parts into a single concise prompt
    return " ".join(parts)

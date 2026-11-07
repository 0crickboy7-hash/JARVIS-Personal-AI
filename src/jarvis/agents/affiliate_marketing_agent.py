import json
from typing import Any

from jarvis.brain.llm_client import JarvisBrain


class AffiliateMarketingAgent:
    """India-focused affiliate marketing assistant."""

    def __init__(self, brain=None):
        self.brain = brain if brain is not None else JarvisBrain()

        self.market = "India"
        self.currency = "INR"

        print("Affiliate Marketing Agent: READY")

    def run(self, request: str, context: dict[str, Any] | None = None) -> str:
        """Process an affiliate marketing task using the existing AI Brain."""

        if not isinstance(request, str) or not request.strip():
            raise ValueError("Affiliate marketing request cannot be empty.")

        if context is not None and not isinstance(context, dict):
            raise TypeError("Context must be a dictionary.")

        context_data = json.dumps(
            context or {},
            ensure_ascii=False,
            indent=2
        )

        prompt = f"""
You are JARVIS, acting as a professional Affiliate Marketing Agent.

MARKET:
- Primary country: India
- Currency: INR (Indian Rupees)
- Target audience: Indian consumers
- Explain technical concepts in beginner-friendly Hinglish unless
  the user requests another language.

YOUR RESPONSIBILITIES:
1. Affiliate product research and comparison.
2. Affiliate program evaluation.
3. Product promotion strategies.
4. SEO titles, descriptions and keywords.
5. Instagram marketing content and scripts.
6. Affiliate business planning.
7. Click, conversion and revenue analysis.
8. Practical daily action plans.

IMPORTANT RULES:
- Never invent affiliate links, commission rates, prices or statistics.
- Clearly distinguish verified information from estimates and assumptions.
- Flag information that requires current market research.
- Never guarantee sales, conversions or earnings.
- Consider legal, platform and affiliate disclosure requirements.
- Never purchase products, publish posts, contact anyone or change
  external accounts without the user's explicit permission.
- Give realistic, actionable recommendations.
- Prioritize free or low-cost methods for beginners.

USER REQUEST:
{request.strip()}

ADDITIONAL USER CONTEXT:
{context_data}

Prepare a useful, practical and clearly structured response.
"""

        return self.brain.ask(prompt)

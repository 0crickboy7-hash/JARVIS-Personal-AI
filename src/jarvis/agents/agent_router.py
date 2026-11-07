from jarvis.agents.affiliate_marketing_agent import AffiliateMarketingAgent


class AgentRouter:
    """Routes affiliate marketing requests to the affiliate agent."""

    AFFILIATE_KEYWORDS = (
        "affiliate",
        "affliate",
        "affiliate marketing",
        "affliate marketing",
        "एफिलिएट",
        "एफिलिएट मार्केटिंग",
    )

    def __init__(self, brain):
        if brain is None:
            raise ValueError("AgentRouter requires an existing JarvisBrain.")

        self.affiliate_agent = AffiliateMarketingAgent(brain=brain)

    def is_affiliate_request(self, request):
        if not isinstance(request, str):
            return False

        normalized_request = request.casefold()

        return any(
            keyword in normalized_request
            for keyword in self.AFFILIATE_KEYWORDS
        )

    def handle(self, request, context=None):
        if not self.is_affiliate_request(request):
            return None

        return self.affiliate_agent.run(request, context=context)

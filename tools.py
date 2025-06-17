import os
from crewai.tools import BaseTool
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
from typing import Dict

# Define a custom CrewAI tool for currency conversion
class CurrencyConverterTool(BaseTool):
    name: str = "Currency Converter"
    description: str = "Converts USD to JPY for budgeting purposes."

    def _run(self, amount_usd: float) -> Dict[str, float]:
        # Assuming 1 USD = 150 JPY (rate for 2025, simplified)
        return {"amount_jpy": amount_usd * 150}

# Initialize tools
search_tool = WebsiteSearchTool()
scrape_tool = ScrapeWebsiteTool()
currency_tool = CurrencyConverterTool()
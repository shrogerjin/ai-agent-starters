"""Web scraper tool for AI agent."""
import aiohttp
from typing import Optional


class WebScraperTool:
    """Web scraping capability for agents."""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    async def scrape(self, url: str) -> str:
        """Scrape content from a URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Extracted text content
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        # Simple HTML to text conversion
                        import re
                        text = re.sub(r'<[^>]+>', ' ', text)
                        text = re.sub(r'\s+', ' ', text).strip()
                        return text[:5000]  # Limit to 5000 chars
                    return f"HTTP {resp.status}"
        except Exception as e:
            return f"Error: {str(e)}"

    async def extract_links(self, url: str) -> list:
        """Extract all links from a webpage."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    html = await resp.text()
                    import re
                    links = re.findall(r'href=["\'](.*?)["\']', html)
                    return [l for l in links if l.startswith('http')]
        except:
            return []

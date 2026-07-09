import urllib.parse
from bs4 import BeautifulSoup
import requests

def research_google(query: str) -> str:
    """
    Performs a lightweight Google Search scrape using requests and BeautifulSoup.
    Extracts the titles, snippet descriptions, and direct source links.
    """
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}&num=5"
    
    # Modern browser headers to avoid instant 429/403 blocks
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"[research_google] Failed to fetch search results. Status code: {response.status_code}"
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Target organic search card result blocks (Google structure uses 'div.g')
        search_results = soup.select("div.g")
        
        if not search_results:
            return f"[research_google] No organic results parsed for query: '{query}'"
            
        summary_lines = [f"### Google Search Results for: '{query}'\n"]
        
        for idx, result in enumerate(search_results, 1):
            title_node = result.select_one("h3")
            link_node = result.select_one("a")
            snippet_node = result.select_one("div[style*='-webkit-line-clamp'], div.VwiC3b")
            
            if title_node and link_node:
                title = title_node.get_text(strip=True)
                link = link_node.get("href", "")
                snippet = snippet_node.get_text(strip=True) if snippet_node else "No description available."
                
                # Clean up tracking metadata loops within internal redirection links if present
                if link.startswith("/url?q="):
                    link = urllib.parse.parse_qs(urllib.parse.urlparse(link).query).get("q", [link])[0]
                    
                summary_lines.append(f"{idx}. **{title}**\n   - Link: {link}\n   - Snippet: {snippet}\n")
                
        return "\n".join(summary_lines)
        
    except Exception as e:
        return f"[research_google] An error occurred during search: {str(e)}"


SKILLS = [
    {
        "name": "research_google",
        "description": "Searches Google for a given query and extracts the top organic titles, snippets, and links.",
        "trigger_phrases": ["search google", "google search", "research on google", "lookup google"],
        "func": research_google,
    },
]
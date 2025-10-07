import os
import requests

class WebSearchAgent:
    """Agent that searches the web and retrieves short snippets."""

    def __init__(self):
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        self.base_url = "https://serpapi.com/search"

    def search(self, query, num_results=3):  
                
        if not self.serpapi_key:
            return {"snippets": [{"source": "web", "text": " Missing SERPAPI_KEY environment variable."}]}

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.serpapi_key,
            "num": num_results
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            if response.status_code != 200:
                return {"snippets": [{"source": "web", "text": f"Error: {response.text}"}]}

            data = response.json()
            results = []
            for item in data.get("organic_results", [])[:num_results]:
                snippet = item.get("snippet") or item.get("title")
                link = item.get("link")
                if snippet:
                    results.append({
                        "source": "web",
                        "text": f"{snippet}\n({link})"
                    })

            if not results:
                results.append({"source": "web", "text": "No search results found."})

            return {"snippets": results}

        except Exception as e:
            return {"snippets": [{"source": "web", "text": f" Error during web search: {e}"}]}

import os
import httpx

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")
if not NEWS_API_KEY:
    raise EnvironmentError("Missing NEWSDATA_API_KEY environment variable.")

# Define allowed NewsData.io categories
ALLOWED_CATEGORIES = {"business", "technology", "health", "science", "sports", "world"}

async def fetch_sector_news(sector: str) -> list[str]:
    url = "https://newsdata.io/api/1/latest"
    query = f"{sector} sector India"

    params = {
        "apikey": NEWS_API_KEY,
        "q": query,
        "country": "in",
        "language": "en",
    }

    category = sector.lower()
    if category in ALLOWED_CATEGORIES:
        params["category"] = category

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            articles = data.get("results", [])
            if not articles:
                return [f"No news articles found for '{sector}' sector."]

            headlines = []
            for article in articles[:5]:
                title = article.get("title", "No Title").strip()
                desc = article.get("description", "").strip()
                headlines.append(f"{title} - {desc}" if desc else title)

            return headlines

    except httpx.HTTPStatusError as exc:
        return [f"News API error ({exc.response.status_code}): {exc.response.text}"]
    except Exception as e:
        return [f"Error fetching news: {str(e)}"]

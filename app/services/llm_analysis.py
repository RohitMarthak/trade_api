import os
import google.generativeai as genai
from fastapi.concurrency import run_in_threadpool

# Configure Gemini API key (free tier uses gemini-2.5-flash)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# Analyze news with Gemini
async def analyze_news_with_gemini(sector: str, news: list[str]) -> str:
    prompt = f"""
    You are a stock market analyst. Analyze the following news about the Indian {sector} sector:

    {chr(10).join(f"- {item}" for item in news)}

    Return a markdown-formatted report including:
    1. **Sector Summary**
    2. **Sentiment** (Bullish, Bearish, or Neutral)
    3. **Top Trade Ideas**
    4. **Key Risk Factors**
        """.strip()

    try:
        # Gemini's sync function must be wrapped for async context
        response = await run_in_threadpool(model.generate_content, prompt)
        return response.text
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

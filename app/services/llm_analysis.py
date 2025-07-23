import os
from datetime import datetime
import google.generativeai as genai
from fastapi.concurrency import run_in_threadpool

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Async Gemini news analyzer with structured Markdown response
async def analyze_news_with_gemini(sector: str, news: list[str]) -> str:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""
        You are a professional stock market analyst. Analyze the following news related to the Indian {sector} sector and generate a structured markdown report.

        ### Format the output using clean markdown:
        - Title with `#`: Market Analysis Report
        - Include sector and current date in bold
        - Use `##` for the following sections:
            - Summary
            - Sentiment
            - Top Trade Ideas
            - Key Risk Factors
        - Use bullet points where needed
        - Use horizontal rules (`---`) between major sections
        - Avoid any extra asterisks or markdown issues
        - Ensure the markdown renders correctly when saved as a `.md` file

        ### News for Analysis:
        {chr(10).join(f"- {item}" for item in news)}

        ### Structure to follow:

        ## Summary

        <Your sector overview goes here.>

        ## Sentiment

        <Bullish / Bearish / Neutral — backed by reasoning.>

        ## Top Trade Ideas

        - <Company 1>: <Rationale>
        - <Company 2>: <Rationale>

        ## Key Risk Factors

        - <Risk 1>
        - <Risk 2>

        ---

        Keep the report professional, well-structured, and easy to read in Markdown format.
            """.strip()

    try:
        # Run Gemini content generation in a thread-safe way
        response = await run_in_threadpool(model.generate_content, prompt)
        return response.text
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

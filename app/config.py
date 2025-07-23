# Configuration and env loading

import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
VALID_TOKENS = {"test-token-1234", os.getenv("API_TOKEN")}

ALLOWED_SECTORS = {
    "pharmaceuticals",
    "information technology",
    "agriculture",
    "banking",
    "automobile",
    "energy",
    "infrastructure",
    "fmcg",
    "telecommunications",
    "real estate",
    "metals",
    "finance",
    "technology",
    "healthcare"
}

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")




from fastapi import APIRouter, Request, HTTPException, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.utils.auth import validate_token
from app.services.news import fetch_sector_news
from app.services.llm_analysis import analyze_news_with_gemini
from app.utils.markdown_formatter import generate_markdown_report
from app.config import ALLOWED_SECTORS
from app.middleware.rate_limiter import limiter

router = APIRouter()

class AnalyzeRequest(BaseModel):
    sector: str

@router.post("/analyze")
@limiter.limit("2/minute")
async def analyze_sector(
    data: AnalyzeRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    token: str = Depends(validate_token)
):
    input_sector = data.sector.strip().lower()

    print(f"Received request to analyze sector: {input_sector}")
    
    if input_sector not in ALLOWED_SECTORS:
        supported = ", ".join(ALLOWED_SECTORS.values())
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported sector. Supported sectors: {supported}"
        )

    normalized_sector = normalized_sector = input_sector.title()

    try:
        news = await fetch_sector_news(normalized_sector)
        report = await analyze_news_with_gemini(normalized_sector, news)
        markdown = generate_markdown_report(normalized_sector, report)
        return Response(content=markdown, media_type="text/markdown")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

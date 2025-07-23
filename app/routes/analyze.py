from fastapi import APIRouter, Request, HTTPException, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.auth import validate_token
from app.services.news import fetch_sector_news
from app.services.llm_analysis import analyze_news_with_gemini
from app.utils.markdown_formatter import generate_markdown_report
from app.config import ALLOWED_SECTORS
from app.middleware.rate_limiter import limiter

router = APIRouter()

@router.get("/analyze/{sector}")
@limiter.limit("2/minute")
async def analyze_sector(
    sector: str,
    request: Request = None,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    token: str = Depends(validate_token)
):
    input_sector = sector.strip().lower()

    if input_sector not in ALLOWED_SECTORS:
        supported = ", ".join(sorted(ALLOWED_SECTORS))
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported sector. Supported sectors: {supported}"
        )

    try:
        news = await fetch_sector_news(input_sector)
        summary = await analyze_news_with_gemini(input_sector, news)
        markdown_report = generate_markdown_report(input_sector, summary)

        return Response(content=markdown_report, media_type="text/markdown")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

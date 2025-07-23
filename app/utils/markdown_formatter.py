from datetime import datetime

def generate_markdown_report(sector: str, summary: str) -> str:
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    markdown = f"""# Market Analysis Report
    **Sector:** {sector.capitalize()}  
    **Generated on:** {date_str}

    ---

    ## Summary & Insights
    {summary}
    """

    return markdown


from app.utils.logger import logger

def summarize_text(text, max_lines=3):
    logger.info("Summarizing...")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return " ".join(lines[:max_lines])

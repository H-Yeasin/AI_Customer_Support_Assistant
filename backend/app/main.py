import logging
from fastapi import FastAPI, HTTPException, status
from app.config import settings
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)


app = FastAPI(title="AI Customer Support Assistant")

# Create the SQLAlchemy engine using the URL from settings
engine = create_engine(settings.database_url)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
def db_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception:
        logger.exception("Database connection failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        )

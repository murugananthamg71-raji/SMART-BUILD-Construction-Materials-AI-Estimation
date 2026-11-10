from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.session import get_db
from app.core.config import settings

router = APIRouter(tags=["Health & Diagnostics"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@router.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        # Check connection
        result = db.execute(text("SELECT 1")).scalar()
        # Count tables
        from app.database.base import Base
        table_count = len(Base.metadata.tables)
        return {
            "status": "connected",
            "database": "online",
            "test_query": result,
            "registered_tables_count": table_count,
            "tables": list(Base.metadata.tables.keys())
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "offline",
            "error": str(e)
        }

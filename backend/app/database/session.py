import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

logger = logging.getLogger(__name__)

db_url = settings.DATABASE_URL
engine = None

def get_engine():
    global engine, db_url
    if engine is not None:
        return engine

    # Check if MySQL URL is provided
    if "mysql" in db_url.lower():
        try:
            temp_engine = create_engine(
                db_url,
                pool_pre_ping=True,
                pool_recycle=3600,
                pool_size=10,
                max_overflow=20,
                connect_args={"connect_timeout": 3}
            )
            # Test connectivity
            with temp_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Successfully connected to MySQL database.")
            engine = temp_engine
            return engine
        except Exception as e:
            if settings.USE_SQLITE_FALLBACK:
                logger.warning(
                    f"MySQL connection failed ({e}). Falling back to SQLite for local development: sqlite:///./smart_build.db"
                )
                db_url = "sqlite:///./smart_build.db"
                engine = create_engine(
                    db_url,
                    connect_args={"check_same_thread": False}
                )
                return engine
            else:
                raise e
    elif "sqlite" in db_url.lower():
        engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False}
        )
        return engine
    else:
        engine = create_engine(db_url, pool_pre_ping=True)
        return engine

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

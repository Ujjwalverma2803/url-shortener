from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# Add SSL args for Supabase
connect_args = {}
if "supabase" in settings.database_url:
    connect_args = {"sslmode": "require"}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
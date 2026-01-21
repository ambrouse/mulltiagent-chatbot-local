from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://bao:3568@postgres:5432/multiangent_db"


# echo=True để hiện log SQL lúc debug, lên production thì tắt đi
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)


# expire_on_commit=False là bắt buộc với AsyncSession
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False 
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            pass
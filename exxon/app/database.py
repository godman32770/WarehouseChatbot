from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL").replace('mysql://', 'mysql+aiomysql://')

engine = create_async_engine(MYSQL_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class Chat(Base):
    __tablename__ = "Chat"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(1024))
    sender = Column(String(16))
    createdAt = Column(DateTime(timezone=True), server_default=func.now())

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session 
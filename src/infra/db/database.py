from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Define onde o arquivo de DADOS (.db) será salvo/lido
DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Essa função é a que o main.py importa!
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
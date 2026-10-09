from fastapi import FastAPI
from sqlalchemy import text
from app.api.documents import router as documents_router
from app.db.session import engine
from app.api.chat import router as chat_router

app = FastAPI(title="AI Study Assistant")


@app.get("/")
def root():
    return {"message": "AI Study Assistant API is running"}

from app.api.users import router as users_router
app = FastAPI(title="AI Study Assistant")
app.include_router(users_router)
app.include_router(documents_router)
app.include_router(chat_router)

@app.get("/db-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database": result.scalar()}
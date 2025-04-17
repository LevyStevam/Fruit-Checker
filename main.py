import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from src.routes import auth
from src.database.database import engine, Base

load_dotenv('src/core/.env')

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API com Google Auth!"}

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
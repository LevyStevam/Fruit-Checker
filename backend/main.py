from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.routes import auth, stores
from src.database.database import Base, engine
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('src/core/.env')

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Adicionar SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "uma-chave-secreta-muito-segura"),
    same_site="lax",
    https_only=False  # Mudar para True em produção
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(auth.router)
app.include_router(stores.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
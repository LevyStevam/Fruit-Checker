from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.user import User
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo correto
load_dotenv('src/core/.env')

router = APIRouter()

# URI de redirecionamento fixo
REDIRECT_URI = "http://localhost:8000/auth/google"  # Removido o /api do caminho

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
        "redirect_uri": REDIRECT_URI
    }
)

@router.get("/login/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, REDIRECT_URI)

@router.get("/auth/google")
async def auth_google(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get("userinfo")
        if not user:
            raise HTTPException(status_code=400, detail="Não foi possível obter informações do usuário")
        
        email = user["email"]
        name = user["name"]

        # Verificar se o usuário já existe no banco
        db_user = db.query(User).filter(User.email == email).first()
        
        if not db_user:
            # Criar novo usuário
            db_user = User(email=email, name=name)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            action = "cadastrado"
        else:
            action = "logado"

        # Redirecionar de volta ao Streamlit com os dados do usuário
        return RedirectResponse(
            url=f"http://localhost:8501/?email={email}&name={name}"
        )
    
    except Exception as e:
        print(f"Erro detalhado: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Erro na autenticação: {str(e)}") 
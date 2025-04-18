from fastapi import APIRouter, Request, HTTPException, Depends, status, Response, Cookie
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.user import User
from src.core.security import create_access_token, verify_token
import os
from dotenv import load_dotenv
from datetime import timedelta
from typing import Optional

# Carregar variáveis de ambiente do arquivo correto
load_dotenv('src/core/.env')

router = APIRouter()

# URI de redirecionamento fixo (agora apontando para o frontend React)
FRONTEND_URL = "http://localhost:5173"
REDIRECT_URI = "http://localhost:8000/auth/google"

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
        print(f"Usuário autenticado - Email: {email}, Nome: {name}")

        # Verificar se o usuário já existe no banco
        db_user = db.query(User).filter(User.email == email).first()
        
        if not db_user:
            # Criar novo usuário
            db_user = User(email=email, name=name)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            print("Novo usuário criado no banco de dados")
        else:
            print("Usuário existente encontrado no banco de dados")

        # Criar token JWT
        access_token = create_access_token(
            data={"sub": email, "name": name},
            expires_delta=timedelta(minutes=30)
        )
        print("Token JWT criado")

        # Criar resposta com cookie e redirecionar para o frontend
        response = RedirectResponse(url=FRONTEND_URL)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=False,  # Permitir acesso via JavaScript
            secure=False,    # Permitir HTTP em desenvolvimento
            samesite="lax",
            max_age=1800,    # 30 minutos
            domain="localhost"
        )
        print("Cookie configurado e redirecionando para o frontend")
        
        return response
    
    except Exception as e:
        print(f"Erro na autenticação: {str(e)}")
        return RedirectResponse(url=f"{FRONTEND_URL}/login?error=auth_failed")

@router.get("/verify-token")
async def verify_session(request: Request):
    print("Verificando sessão")
    try:
        access_token = request.cookies.get("access_token")
        if not access_token:
            print("Nenhum token encontrado nos cookies")
            return JSONResponse({"authenticated": False})

        payload = verify_token(access_token)
        print(f"Token válido para usuário: {payload.get('name')}")
        return JSONResponse({
            "authenticated": True,
            "user": {
                "email": payload["sub"],
                "name": payload["name"]
            }
        })
    except Exception as e:
        print(f"Erro ao verificar sessão: {str(e)}")
        return JSONResponse({"authenticated": False})

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        domain="localhost",
        path="/",
        httponly=False,
        secure=False,
        samesite="lax"
    )
    return JSONResponse({"message": "Logout realizado com sucesso"}) 
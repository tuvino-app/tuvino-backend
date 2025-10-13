from fastapi import APIRouter, HTTPException, Depends
from src.utilities.supabase_client import supabase
from src.models.schemas.user import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user_data: UserCreate):
    try:
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
        })
        if response.user is None and response.session is None:
            raise HTTPException(status_code=400, detail="No se pudo registrar al usuario.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en el registro: {str(e)}")

    return {"message": "Usuario registrado."}


@router.post("/login")
async def login(user_data: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password,
        })
        if response.session is None:
            raise HTTPException(status_code=401, detail="Credenciales inválidas.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"access_token": response.session.access_token, "token_type": "bearer"}
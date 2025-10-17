from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from src.utilities.supabase_client import supabase
from src.models.schemas.user import UserCreate, UserLogin, LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user_data: UserCreate):
    try:
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "username": user_data.username
                }
            }
        })
        
        if response.user is None and response.session is None:
            raise HTTPException(status_code=400, detail="No se pudo registrar al usuario.")
        try:
            supabase.table("users").update({"name": user_data.username}).eq("uid", response.user.id).execute()
        except Exception as db_error:
            print(f"Error al actualizar username: {db_error}")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en el registro: {str(e)}")

    return {"message": "Usuario registrado exitosamente."}


@router.post("/login", response_model=LoginResponse)
async def login(user_data: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password,
        })
        if response.session is None:
            raise HTTPException(status_code=401, detail="Credenciales inválidas.")
            
        user_id = response.user.id
        user_data_response = supabase.table("users").select("onboarding_completed").eq("uid", user_id).single().execute()
        onboarding_completed = user_data_response.data.get("onboarding_completed", False)
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return LoginResponse(
        access_token=response.session.access_token,
        token_type="bearer",
        user_id=user_id,
        onboarding_completed=onboarding_completed
    )


def verify_token(token: str) -> dict:
    """Verifica el token JWT con Supabase y devuelve los datos del usuario o lanza una excepción."""
    try:
        user_response = supabase.auth.get_user(token)

        if user_response.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
            )
        return user_response.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"No se pudo validar el token: {e}",
        )

oauth2_scheme = HTTPBearer()
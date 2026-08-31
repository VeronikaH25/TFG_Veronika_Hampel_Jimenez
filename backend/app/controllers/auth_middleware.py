# app/controllers/auth_middleware.py
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "mi_clave_super_secreta_para_el_tfg_cambiala_luego"
ALGORITHM = "HS256"

# Esto le dice a FastAPI que use el estándar "Bearer Token" (y pone el candado en Swagger)
security = HTTPBearer()

def obtener_usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """El Segurata: Verifica el token y devuelve el email del usuario"""
    token = credentials.credentials
    try:
        # Intentamos desencriptar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Tu sesión ha caducado. Vuelve a hacer login.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token corrupto o falso.")
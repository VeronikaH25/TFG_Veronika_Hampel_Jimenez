from pydantic import BaseModel
from typing import Optional

class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str
    # Le decimos que son opcionales y por defecto valen None
    edad: Optional[int] = None
    peso: Optional[float] = None
    nivel: Optional[str] = None
    objetivo: Optional[str] = None
    dias_entreno: Optional[int] = None
    
class UsuarioLogin(BaseModel):
    email: str
    password: str
    

class UsuarioUpdate(BaseModel):
    peso: Optional[float] = None
    edad: Optional[int] = None
    objetivo: Optional[str] = None
    nivel: Optional[str] = None
    dias_entreno: Optional[int] = None
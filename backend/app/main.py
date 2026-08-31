# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos las dos rutas por separado
from app.routes import auth_routes, login_routes, perfil_routes, rutinas_routes

app = FastAPI(
    title="API TFG - Motor de Rutinas",
    description="Backend con Arquitectura Limpia para el TFG",
    version="1.0.0"
)

# ==========================================
# CONFIGURACIÓN CORS (Seguridad Frontend-Backend)
# ==========================================
origenes_permitidos = [
    "http://localhost:3000",   
    "http://localhost:5173",   
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos, # Lista segura 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def ruta_raiz():
    return {"mensaje": "¡Servidor FastAPI funcionando a la perfección! "}

# Enchufamos ambas rutas al servidor
app.include_router(auth_routes.router)
app.include_router(login_routes.router)
app.include_router(perfil_routes.router)
app.include_router(rutinas_routes.router, prefix="/api/rutinas", tags=["Rutinas"])
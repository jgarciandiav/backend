from fastapi import FastAPI
from database import engine, Base
from routers import (
    user_router,
    servicio_router,
    cliente_router,
    factura_router,
    facturaitems_router,
    configempresa_router,
    )
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Facturación")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(servicio_router.router, prefix="/servicios", tags=["Servicios"])
app.include_router(cliente_router.router, prefix="/clientes", tags=["Clientes"])
app.include_router(factura_router.router, prefix="/facturas", tags=["Facturas"])
app.include_router(facturaitems_router.router, prefix="/facturaitems", tags=["FacturaItems"])
app.include_router(configempresa_router.router, prefix="/configempresa", tags=["ConfigEmpresa"])
